# Add the notubiz folder to the path
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import notubiz
import notubiz.api.speakers

configuration = notubiz.Configuration(organisation_id = 686) # Gemeente Eindhoven

api_client = notubiz.ApiClient(configuration)

speakers = notubiz.api.NotubizSpeakers(api_client).get()

speaker = speakers.find_by_person_id(194366) 

print(speaker.full_name())