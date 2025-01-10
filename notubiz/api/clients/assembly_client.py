from notubiz import ApiClient
from notubiz.api.dataclasses.assembly import Assembly

from notubiz.api._converter import get_converter

class AssemblyClient:
    api_client : ApiClient
    
    def __init__(self, api_client : ApiClient):
        self.api_client = api_client

    def get(self, assembly_event_id : int) -> Assembly:
        json_object = self.api_client.get("events/assemblies/{}".format(assembly_event_id))
        
        json_assembly = json_object["assembly"]

        return get_converter().structure(json_assembly, Assembly)