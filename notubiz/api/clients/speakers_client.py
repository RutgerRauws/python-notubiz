from notubiz.api_client import ApiClient
from notubiz.api.dataclasses import Speakers
from notubiz.api._converter import get_converter

class SpeakersClient:
    api_client : ApiClient

    def __init__(self, api_client : ApiClient):
        self.api_client = api_client

    def get(self) -> Speakers:
        json_object = self.api_client.get("speakers")
        return get_converter().structure(json_object, Speakers)