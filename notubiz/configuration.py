from attrs import define

@define
class Configuration:
    organisation_id : int
    base_url : str = "https://api.notubiz.nl/"