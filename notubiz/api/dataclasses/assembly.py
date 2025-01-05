# from attrs import define, field
# import cattrs
# from typing import Optional, List
# from datetime import datetime

# from notubiz.api.dataclasses.planning import Planning

# @define
# class AssemblyMeeting:
#     id: int
#     order: int
#     plannings: list[Planning] 

# @define
# class Assembly:
#     # Auto-filled
#     permission_group: str
#     body: str
#     confidential: bool
#     announcement: bool
#     canceled: bool
#     inactive: bool
#     creation_date: datetime
#     last_modified: datetime
#     live: bool
#     plannings: list[Planning]
#     meetings: list[AssemblyMeeting]

#     # Manually filled
#     title: str = field(init=False)
#     location: str = field(init=False)
#     gremium_id: int = field(init=False)

#     @staticmethod
#     def from_json(json_object : any) -> 'Assembly':
#         c = cattrs.Converter()
#         c.register_structure_hook(datetime, lambda d, _: datetime.strptime(d, "%Y-%m-%d %H:%M:%S"))

#         assembly = c.structure(json_object, Assembly)



#         return assembly

from attrs import define
#from cattrs.strategies import include_subclasses
from cattrs import Converter

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

    #@classmethod
    # def from_parent(cls, parent : Event) -> 'Assembly':
    #     assembly = cls.__new__(parent)
    #     assembly.meetings = []
    #     return assembly
    
    # @staticmethod
    # def from_parent(event : Event) -> 'Assembly':
    #     return Assembly(*event.args())

    @staticmethod
    def from_json(json_object : any) -> 'Assembly':
        c = Converter()
        #include_subclasses(Event, c)

        event = Event.from_json(json_object["assembly"])

        assembly = c.structure(event, Assembly)
        assembly.meetings = [c.structure(item, AssemblyMeeting) for item in json_object["meetings"]]
