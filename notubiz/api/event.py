
from attrs import define, field
import cattrs
from cattrs import transform_error

from typing import Optional

from datetime import datetime
from notubiz.api._helpers import parse_date, get_title, get_location

from notubiz import ApiClient

@define
class Planning:
    # Auto-filled
    start_date : datetime
    end_date : Optional[datetime]

@define
class Event:
    # Auto-filled
    id: int
    type: str
    permission_group: str
    body: str
    confidential: bool
    announcement: bool
    canceled: bool
    inactive: bool
    creation_date: datetime
    last_modified: datetime
    live: bool
    archive_state: str
    archive_state_last_modified: Optional[datetime]
    allow_subscriptions: bool
    plannings: list[Planning]

    # Manually filled
    title: str = field(init=False)
    location: str = field(init=False)
    gremium_id: int = field(init=False)

    @staticmethod
    def from_json(json_object : any) -> 'Event':
        c = cattrs.Converter()

        c.register_structure_hook(datetime, lambda date_string, _: parse_date(date_string))

        try:
            meeting = c.structure(json_object, Event)
        except Exception as exc:
            print("\n".join(transform_error(exc)))
            quit()

        attributes = json_object.get("attributes", [])
        meeting.title = get_title(attributes)
        meeting.location = get_location(attributes)
        meeting.gremium_id = json_object["gremium"]["id"]

        return meeting

class EventApi:
    api_client : ApiClient
    
    def __init__(self, api_client : ApiClient):
        self.api_client = api_client


    def get(self, date_from: datetime, date_to: datetime, gremia: list[int] = None) -> list[Event]:

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
        return [Event.from_json(json_event) for json_event in json_events]