# Add the notubiz folder to the path
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime

import notubiz
import notubiz.api.event

configuration = notubiz.Configuration(organisation_id = 686) # Gemeente Eindhoven

api_client = notubiz.ApiClient(configuration)

event_client = notubiz.api.event.EventApi(api_client)

start_date = datetime(2019, 1, 1)
end_date = datetime(2020, 3, 31, 23, 59, 59)

events = event_client.get(start_date, end_date)

for event in events:
    print("{} - {} ({})".format(event.plannings[0].start_date, event.title, event.location))
