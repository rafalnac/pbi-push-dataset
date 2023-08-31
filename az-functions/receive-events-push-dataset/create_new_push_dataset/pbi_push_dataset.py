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
    def get_name_of_dataset(dataset: Any) -> str:
        """Retrieve name of the dataset from tabular model.

        Args:
            dataset: Tabular model as JSON object.
        """

        return dataset.get("name")

    @staticmethod
    def get_id_of_dataset(dataset: Any) -> str:
        """Retrieve id of the dataset from tabular model.

        Args:
            dataset: Tabular model as JSON object.
        """

        return dataset.get("id")

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

    def is_dataset_in_workspace(self, dataset: Any) -> bool:
        """Check if provided push dataset exists in workspace.

        Check is based on the 'Name' attribute in dataset.

        Args:
            dataset: Tabular model as JSON object.

        Returns:
            True if dataset exist in workspace, otherwise False.
        """

        names_existing_datasets = self.get_datasets()
        name_new_dataset_to_upload = self.get_name_of_dataset(dataset)
        return name_new_dataset_to_upload in names_existing_datasets

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


if __name__ == "__main__":
    pass
