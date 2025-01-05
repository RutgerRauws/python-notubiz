# Add the notubiz folder to the path
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from notubiz import ApiClient, Configuration
from notubiz.api.clients import AssemblyClient, MeetingClient

configuration = Configuration(organisation_id = 686) # Gemeente Eindhoven

api_client = ApiClient(configuration)

assembly_client = AssemblyClient(api_client)
meeting_client = MeetingClient(api_client)

assembly = assembly_client.get(1253866)

for assembly_meeting in assembly.meetings:
    meeting = meeting_client.get(assembly_meeting.id)

    print("{} - {} ({})".format(assembly_meeting.plannings[0].start_date, meeting.title, meeting.location))
