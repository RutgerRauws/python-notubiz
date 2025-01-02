from attrs import define

@define
class Configuration:
    organisation_id : int
    api_version : str = "1.10.8" # To keep the used API stable
    base_url : str = "https://api.notubiz.nl/"