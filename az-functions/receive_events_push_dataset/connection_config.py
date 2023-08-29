"""Module contains connection configurations.

Authentication to required azure services is based on DefaultAzureCredential.

DefaultAzureCredential:
https://learn.microsoft.com/en-us/python/api/azure-identity/azure.identity.defaultazurecredential?view=azure-python
"""

from os import environ as env

from azure.identity import DefaultAzureCredential
from azure.storage.blob import ContainerClient


# Initialize the Credentials
default_credentials = DefaultAzureCredential()

# Get container URL string
blob_container_conn_string = env.get("PBI_PUSH_DATASET_CONTAINER")

# Create container client
container_pbi_push_dataset_raw_data = ContainerClient.from_container_url(
    container_url=f"{blob_container_conn_string}/raw-data",
    credential=default_credentials,
)