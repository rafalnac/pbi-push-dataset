"""Create Power BI Push Dataset."""

import json
import requests
from pathlib import Path
from os import environ as env
from typing import Dict, List, Any
from http import HTTPStatus


class Workspace:
    """Creates Power BI workspace object."""

    def __init__(self, workspace_id: str, headers: Dict[str, str]) -> None:
        """Instanciate an workspace object.

        Args:
            workspace_id: Power BI workspace ID
            headers: Headers used by Power BI Rest API:
                {"Content-Type": "application/json",
                "Authorization": "Bearer " + access_token}
        """
        self.workspace_id = workspace_id
        self.pbi_api_group_dataset = (
            f"https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/datasets"
        )
        self.headers = headers

    @staticmethod
    def load_file_to_json_object(path: str | Path) -> Any:
        """Read file and convert it to JSON object.

        Args:
            path: Path to file in JSON format.

        Returns:
            JSON object.
        """

        if not isinstance(path, Path) and not isinstance(path, str):
            raise TypeError("Path must be a string or Path")

        with open(path, "r") as file:
            json_object = json.load(file)
        return json_object

    @staticmethod
    def convert_event_to_push(event: str) -> Any:
        """Convert captured event to JSON object.

        Converted according to required schema:
        https://learn.microsoft.com/en-us/rest/api/power-bi
        /push-datasets/datasets-post-rows-in-group#example

        Args:
            event: JSON string.

        Returns:
            JSON object.
        """

        new_dict = {}
        new_dict["rows"] = [json.loads(event)]
        return json.dumps(new_dict)

    @staticmethod
    def get_name_of_dataset(dataset: Any) -> str:
        """Retrieve name of the dataset from tabular model.

        Args:
            dataset: Tabular model as JSON object.
        """

        return dataset.get("name")

    def get_id_of_dataset(self, dataset_name: str) -> str:
        """Retrieve id of the exising dataset in Power BI workspace.

        Args:
            dataset: Name of exising dataset in Power BI workspace.

        Retuns:
            Id of dataset with provided name.

        Raises:
            ValueError if dataset with provided name does not exists.
            TypeError if dataset_name is not a strig type
        """

        if not isinstance(dataset_name, str):
            raise TypeError(
                f"Argument dataset_name must be a string, {type(dataset_name)} provided."
            )
        if not self.is_dataset_in_workspace(dataset_name=dataset_name):
            raise ValueError(
                f"Provided dataset name: {dataset_name}, does not exist in workspace."
            )

        datasets_response = self._get_dataset_response()
        dataset_response_list_dict = [
            attr for attr in datasets_response.json().get("value")
        ]

        for dictionary in dataset_response_list_dict:
            for key, value in dictionary.items():
                if value == "RandomWeather":
                    dataset_id = dictionary.get("id")
        return dataset_id

    def _get_dataset_response(self):
        """Retunrs Response object with datasets from workspace"""

        datasets = requests.get(
            url=self.pbi_api_group_dataset,
            headers=self.headers,
        )
        return datasets

    def get_datasets(self) -> List:
        """Returs list of existing datasets within workspace."""

        # Response object with datasets converted to JSON
        response_object_json = self._get_dataset_response().json()

        # Retrieve list of datasets from workspace
        datasets_list = [attr.get("name") for attr in response_object_json.get("value")]
        return datasets_list

    def is_dataset_in_workspace(
        self, dataset: Any = None, dataset_name: str = None
    ) -> bool:
        """Check if provided push dataset exists in workspace.

        Check is based on the 'Name' attribute in dataset.
        If dataset_name attribute is provided, dataset is ommitted.

        Args:
            dataset: Tabular model as JSON object.
            dataset_name: Name of the dataset.

        Returns:
            True if dataset exist in workspace, otherwise False.
        """

        if dataset_name is not None:
            dataset_name_to_check = dataset_name
        else:
            dataset_name_to_check = self.get_name_of_dataset(dataset)

        names_existing_datasets = self.get_datasets()
        return dataset_name_to_check in names_existing_datasets

    def create_push_dataset(self, dataset: Any) -> HTTPStatus:
        """Create new power bi push dataset.

        Args:
            dataset: Tabular model of Power BI dataset as JSON object.
                Dataset can have only allowed attributes.
                More: https://learn.microsoft.com/en-us/rest/api/power-bi/push-datasets/datasets-post-dataset

        Returns:
            Status code from Response object.
        """

        response = requests.post(
            url=self.pbi_api_group_dataset,
            json=dataset,
            headers=self.headers,
        )
        return response.status_code

    def push_rows_to_dataset_table(
        self, dataset_name: str, table_name: str, rows: Any
    ) -> HTTPStatus:
        """Push rows to exsing power bi push dataset.

        Args:
            dataset_name: Name of the existing dataset in workspace.
            rows: Rows to add.

        Returns:
            Status code from Response object.
        """

        dataset_id = self.get_id_of_dataset(dataset_name=dataset_name)
        push_rows_pbi_api = (
            f"https://api.powerbi.com/v1.0/myorg/groups/{self.workspace_id}"
            f"/datasets/{dataset_id}/tables/{table_name}/rows"
        )

        response = requests.post(url=push_rows_pbi_api, data=rows, headers=self.headers)
        return response.status_code


if __name__ == "__main__":
    pass
