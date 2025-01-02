# Add the notubiz folder to the path
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from notubiz import ApiClient, Configuration
from notubiz.api.clients import SpeakersClient

configuration = Configuration(organisation_id = 686) # Gemeente Eindhoven

api_client = ApiClient(configuration)

speakers = SpeakersClient(api_client).get()

speaker = speakers.find_by_person_id(194366) 

print(speaker.full_name())