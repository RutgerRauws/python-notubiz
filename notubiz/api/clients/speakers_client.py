from notubiz.api_client import ApiClient
from notubiz.api.dataclasses import Speakers

class SpeakersClient:
    api_client : ApiClient

    def __init__(self, api_client : ApiClient):
        self.api_client = api_client

    def get(self) -> Speakers:
        json_object = self.api_client.get("speakers")
        return Speakers.from_json(json_object)