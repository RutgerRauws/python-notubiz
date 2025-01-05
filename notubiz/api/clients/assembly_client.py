from notubiz import ApiClient
from notubiz.api.dataclasses.assembly import Assembly

class AssemblyClient:
    api_client : ApiClient
    
    def __init__(self, api_client : ApiClient):
        self.api_client = api_client

    def get(self, assembly_event_id) -> Assembly:
        json_assembly = self.api_client.get("events/assemblies/{}".format(assembly_event_id))
        return Assembly.from_json(json_assembly)