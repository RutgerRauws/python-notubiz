from notubiz import ApiClient
from notubiz.api.dataclasses import Event
from datetime import datetime

from notubiz.api._converter import get_converter

class EventsClient:
    api_client : ApiClient
    
    def __init__(self, api_client : ApiClient):
        self.api_client = api_client


    def get(self, date_from: datetime, date_to: datetime, gremia: list[int] = None) -> list[Event]:
        converter = get_converter()

        json_events : list[dict] = []
        has_more_pages = True
        page = 1 # Notubiz uses 1-based paging

        # We loop over the pages until no more pages are left
        while has_more_pages:

            additional_payload = {
                'date_from': date_from.strftime("%Y-%m-%d %H:%M:%S"),
                'date_to': date_to.strftime("%Y-%m-%d %H:%M:%S"),
                # For some reason this endpoint requires 'organisation_id' instead of 'organisation"
                'organisation_id': self.api_client.configuration.organisation_id,
                'gremia': gremia,
                'page': page
            }

            json_events_page = self.api_client.get("events/", additional_payload)
            json_events.extend(json_events_page["events"])

            has_more_pages = json_events_page["pagination"]["has_more_pages"]
            page += 1
        
        # Now run the deserialization based on the merged events
        return [converter.structure(json_event, Event) for json_event in json_events]