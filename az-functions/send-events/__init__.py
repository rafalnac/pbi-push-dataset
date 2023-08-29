import asyncio
import logging

import azure.functions as func

from .send import run
from .event import event_to_send


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    asyncio.run(run(event=event_to_send))
    logging.info(f"Sent event: {event_to_send}")

    return func.HttpResponse.status_code(200)
