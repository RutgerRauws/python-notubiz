from notubiz import ApiClient
from notubiz.api.dataclasses import Meeting

class MeetingClient:
    api_client : ApiClient

    def __init__(self, api_client : ApiClient):
        self.api_client = api_client

    def get(self, meeting_id : int) -> Meeting:
        json_object = self.api_client.get("events/meetings/{}".format(meeting_id))
        return Meeting.from_json(json_object)
