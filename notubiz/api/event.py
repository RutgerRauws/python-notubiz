from attrs import define
import cattrs
from cattrs import transform_error
from cattrs.gen import make_dict_structure_fn, override

from datetime import datetime

from notubiz.api.meeting import Meeting, meeting_structure_hook
from notubiz.api.agenda_item import AgendaItem, agenda_item_structure_hook
from notubiz import ApiClient

@define
class Event:
    title : str
    description : str
    location : str
    chairman : str
    clerk : str
    secretary : str

    # TODO: media
    # TODO: speakers 

    agenda : list[AgendaItem]

    # meeting_id : int
    # type : str
    # start_date : datetime
    # end_date : datetime

    # meetings : list[Meeting]

    @staticmethod
    def from_json(json_object : any) -> 'Event':
        c = cattrs.Converter()
        c.register_structure_hook(Meeting, meeting_structure_hook)
        # c.register_structure_hook(AgendaItem, agenda_item_structure_hook)
        st_hook = make_dict_structure_fn(
            AgendaItem, c, agenda=override(struct_hook=lambda v, _: agenda_item_structure_hook(v["agendaitem"])))
        c.register_structure_hook(AgendaItem, st_hook)

        try:
            meeting = c.structure(json_object["event"][0], Event)
        except Exception as exc:
            print("\n".join(transform_error(exc)))
            quit()

        return meeting

class EventApi:
    api_client : ApiClient

    
    def __init__(self, api_client : ApiClient):
        self.api_client = api_client

    def get(self, event_id : int) -> Event:
        json_object = self.api_client.get("events/{}".format(event_id))
        return Event.from_json(json_object)
    