# Add the notubiz folder to the path
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import notubiz
import notubiz.api.event

configuration = notubiz.Configuration(organisation_id = 686) # Gemeente Eindhoven

api_client = notubiz.ApiClient(configuration)

event_client = notubiz.api.event.EventApi(api_client)

event = event_client.get(1229974)

print(event.title)
# for event. in meeting.agenda_items:
#     print("  {} - {}".format(agenda_item.start_date, agenda_item.title))
