from notubiz.api.dataclasses import Event, event_hook
from notubiz.api.dataclasses import Meeting, meeting_hook
from notubiz.api.dataclasses import AgendaItem, agenda_item_hook
#from notubiz.api.dataclasses import Speakers, speakers_nook

Hooks = {
    Event: event_hook,
    Meeting: meeting_hook,
    AgendaItem: agenda_item_hook
}