"""Get access token."""

from msal import ConfidentialClientApplication
from connection_config import (
    AUTHORITY_URL,
    POWER_BI_REST_API_CLIENT_ID,
    POWER_BI_REST_API_CLIENT_SECRET,
    PBI_SCOPE_URL,
)

# create application using generated secrets
app = ConfidentialClientApplication(
    client_id=POWER_BI_REST_API_CLIENT_ID,
    client_credential=POWER_BI_REST_API_CLIENT_SECRET,
    authority=AUTHORITY_URL,
)

# aquire access token
token = app.acquire_token_for_client(scopes=[PBI_SCOPE_URL])
access_token = token.get("access_token")

# create headers for PBI API request
PBI_REQUESTS_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + access_token,
}

if __name__ == "__main__":
    pass
