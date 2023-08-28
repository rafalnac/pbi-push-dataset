"""Module creates sample of weather measurements formatted as string.

Variables:
    event_to_sent: JSON formatted string with weather measurements.
"""

import json
import random
from datetime import datetime


start_date_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
cities = ("Warsaw", "London", "Munich", "Oslo", "Vienna")


data_weather = {
    "date": start_date_time,
    "City": random.choice(cities),
    "Temperature": random.randrange(-10, 30),
    "Humidity": random.randrange(40, 100),
    "Wind Speed": random.randrange(0, 100),
    "Precipitation": random.randrange(0, 1000),
    "Pressure": random.randrange(980, 1030),
    "UV Index": random.randrange(1, 6)
}

event_to_send = json.dumps(data_weather)