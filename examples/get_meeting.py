# Add the notubiz folder to the path
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from notubiz import ApiClient, Configuration
from notubiz.api.clients.meeting_client import MeetingClient

configuration = Configuration(organisation_id = 686) # Gemeente Eindhoven

api_client = ApiClient(configuration)

meeting_client = MeetingClient(api_client)

meeting = meeting_client.get(1147925)

print(meeting.title)
for agenda_item in meeting.agenda_items:
    print("  {} - {}".format(agenda_item.start_date, agenda_item.title))

    for sub_agenda_item in agenda_item.agenda_items:
        print("                      - {}".format(sub_agenda_item.title))
