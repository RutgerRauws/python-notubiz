# Add the notubiz folder to the path
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import notubiz
import notubiz.api.meeting

configuration = notubiz.Configuration(organisation_id = 686) # Gemeente Eindhoven

api_client = notubiz.ApiClient(configuration)

meeting_client = notubiz.api.NotubizMeeting(api_client)

meeting = meeting_client.get(1147925)

print(meeting.title)
for agenda_item in meeting.agenda_items:
    print("  {} - {}".format(agenda_item.start_date, agenda_item.title))
