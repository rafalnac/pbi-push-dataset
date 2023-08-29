"""Send event to Event Hub.

The purpose of the module is to simulate event sending to Event Hub.

Paswordless authentication and authorization configured according to:
https://learn.microsoft.com/en-us/azure/event-hubs/
event-hubs-python-get-started-send?tabs=passwordless%2Croles-azure-portal
#authenticate-the-app-to-azure

Functions:
    run: Asynchronous function to send messages to Event Hub.
"""

import asyncio
import sys
from os import environ as env

from azure.eventhub import EventData
from azure.eventhub.aio import EventHubProducerClient
from azure.identity.aio import DefaultAzureCredential

EVENT_HUB_FULLY_QUALIFIED_NAMESPACE = env.get("EVENTHUB_NAMESPACE")
EVENT_HUB_NAME = env.get("EVENTHUB_NAME")

credential = DefaultAzureCredential()

async def run(event: str | bytes) -> None:
    """Create a producer client to send messages to the event hub

    Method from MS doc: https://learn.microsoft.com/en-us/azure/event-hubs/
    event-hubs-python-get-started-send?tabs=passwordless%2Croles-azure-portal#send-events

    Args:
        event: Event to send to Event Hub.
    """

    producer = EventHubProducerClient(
        fully_qualified_namespace=EVENT_HUB_FULLY_QUALIFIED_NAMESPACE,
        eventhub_name=EVENT_HUB_NAME,
        credential=credential,
    )
    async with producer:
        # Create a batch.
        event_data_batch = await producer.create_batch()

        # Add events to the batch.
        event_data_batch.add(EventData(event))

        # Send the batch of events to the event hub.
        await producer.send_batch(event_data_batch)

        # Close credential when no longer needed.
        await credential.close()

# Workaround to issue https://github.com/encode/httpx/issues/914
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

if __name__ == "main":
    asyncio.run(run("Event"))
