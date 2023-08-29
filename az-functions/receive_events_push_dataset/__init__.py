"""Get events from Event Hub, sink them to blob container and sent to PBI push dataset."""

import logging
from typing import List
from datetime import datetime

import azure.functions as func

from .connection_config import container_pbi_push_dataset_raw_data


def main(events: List[func.EventHubEvent]):
    for event in events:
        # Get event body
        event_body = event.get_body().decode("utf-8")
        logging.info(f"Python EventHub trigger processed an event: \n {event_body}")

        # Sent event body to container in json format
        container_pbi_push_dataset_raw_data.upload_blob(
            name=f"export_{datetime.utcnow()}.json",
            data=event_body,
            blob_type="BlockBlob",
        )
