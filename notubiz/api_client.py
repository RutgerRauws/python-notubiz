from attrs import define
from notubiz.configuration import Configuration

import requests
import json

@define
class ApiClient:
    configuration : Configuration

    def get_base_payload(self) -> dict:
        return {'format': 'json', 'organisation': self.configuration.organisation_id}
    
    def get(self, relative_path : str, extra_payload : dict = None) -> any:
        request_url = self.configuration.base_url + relative_path

        # Merge payloads
        payload = self.get_base_payload()
        if extra_payload is not None: payload = payload | extra_payload

        response = requests.get(request_url, params=payload)        
        json_object = json.loads(response.text)

        return json_object