"""Get events from Event Hub, sink them to blob container and sent to PBI push dataset."""

import logging
from datetime import datetime
from pathlib import Path
from typing import List

import azure.functions as func
from .create_new_push_dataset.pbi_push_dataset import Workspace
from .create_new_push_dataset.get_pbi_access_token import PBI_REQUESTS_HEADERS
from .create_new_push_dataset.connection_config import (
    PUSH_DATASET_PBI_WORKSPACE_ID,
    container_pbi_push_dataset_raw_data,
)


def main(events: List[func.EventHubEvent]):
    # Create PBI Push Dataset
    # Create instance of workspace object
    workspace = Workspace(
        workspace_id=PUSH_DATASET_PBI_WORKSPACE_ID, headers=PBI_REQUESTS_HEADERS
    )
    dataset_path = (
        Path(__file__).parent / "create_new_push_dataset/push_dataset_schema.json"
    )

    # Load tabular model as JSON file and convert in to JSON object.
    dataset = Workspace.load_file_to_json_object(dataset_path)

    # Create PBI push dataset in PBI workspace if not exists.
    if not workspace.is_dataset_in_workspace(dataset):
        workspace.create_push_dataset(dataset)

    for event in events:
        # Get event body
        event_body = event.get_body().decode("utf-8")
        logging.info(f"Python EventHub trigger processed an event: \n {event_body}")

        # Send event body to container in json format
        container_pbi_push_dataset_raw_data.upload_blob(
            name=f"export_{datetime.utcnow()}.json",
            data=event_body,
            blob_type="BlockBlob",
        )

        # Create event ready to be sent to PBI Push Dataset
        event_to_send = workspace.convert_event_to_push(event_body)
        logging.info(event_to_send)
        with open("sample.txt", "w") as file:
            file.write(event_to_send)

        # Send event to Power BI Push Dataset
        status_code = workspace.push_rows_to_dataset_table(
            dataset_name="RandomWeather",
            table_name="Table",
            rows=event_to_send
        )
        logging.info(f"Status code: {status_code}")
