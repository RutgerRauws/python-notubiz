from attrs import define

from notubiz.api.dataclasses.event import Event
from notubiz.api.dataclasses.planning import Planning

@define
class AssemblyMeeting:
    id: int
    order: int
    plannings: list[Planning] 

@define
class Assembly(Event):
    meetings: list[AssemblyMeeting]