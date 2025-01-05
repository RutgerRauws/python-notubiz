# Add the notubiz folder to the path
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime

from notubiz import ApiClient, Configuration
from notubiz.api.clients import EventsClient

configuration = Configuration(organisation_id = 686) # Gemeente Eindhoven

api_client = ApiClient(configuration)

event_client = EventsClient(api_client)

start_date = datetime(2025, 1, 5)
end_date = datetime(2025, 1, 7, 23, 59, 59)

events = event_client.get(start_date, end_date)

for event in events:
    print("{} - {} ({})".format(event.plannings[0].start_date, event.title, event.location))
