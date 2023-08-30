"""Module contains connection configurations.

DefaultAzureCredential:
https://learn.microsoft.com/en-us/python/api/azure-identity/azure.identity.defaultazurecredential?view=azure-python
"""

from os import environ as env

from azure.identity import DefaultAzureCredential
from azure.storage.blob import ContainerClient


# Constans to be imported by others modules
TENANT_ID = env.get("AZURE_TENANT_ID")
AUTHORITY_URL = f"https://login.microsoftonline.com/{TENANT_ID}"
PBI_SCOPE_URL = "https://analysis.windows.net/powerbi/api/.default"

# Service Principal data
POWER_BI_REST_API_CLIENT_ID = env.get("AZURE_CLIENT_ID")
POWER_BI_REST_API_CLIENT_SECRET = env.get("AZURE_CLIENT_SECRET")

# Constants used for POWER BI REST API
PUSH_DATASET_PBI_WORKSPACE_ID = env.get("PUSH_DATASET_PBI_WORKSPACE_ID")
PUSH_DATSET_ID = env.get("PUSH_DATSET_ID")


# Initialize the default Azure Credentials
default_credentials = DefaultAzureCredential()

# Get container URL string
blob_container_conn_string = env.get("PBI_PUSH_DATASET_CONTAINER")

# Create container client
container_pbi_push_dataset_raw_data = ContainerClient.from_container_url(
    container_url=f"{blob_container_conn_string}/raw-data",
    credential=default_credentials,
)
