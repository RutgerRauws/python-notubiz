# Python client for NotuBiz
This is an unofficial python client for NotuBiz. [NotuBiz](https://www.notubiz.nl/) is a Dutch council information system. 
I am not affiliated with NotuBiz in any way.

## Requirements 
The package has been tested with Python 3.9, 3.10, and 3.11.
First, create a new virtual environment, source into it, and install the dependencies.

```
python -m venv .venv
source .venv/bin/activate
pip install -r ./requirements.in
```

## Usage
Import the `ApiClient` and `Configuration` and provide the configuration with an organisation ID.
This ID can be found [here](https://api.notubiz.nl/organisations).

```python
from notubiz import ApiClient, Configuration

configuration = Configuration(organisation_id = 686) # Gemeente Eindhoven

api_client = ApiClient(configuration)
```

Now that you have configured the API client, we can pass the API client to the various clients that are provided.
Below, you can find an example for the `MeetingClient`. 
We retrieve a meeting with ID `1147925` and iterate over all agenda items in that meeting to print them.

```python
from notubiz.api.clients.meeting_client import MeetingClient
meeting_client = MeetingClient(api_client)

meeting = meeting_client.get(1147925)

print(meeting.title)
for agenda_item in meeting.agenda_items:
    print("  {} - {}".format(agenda_item.start_date, agenda_item.title))

    for sub_agenda_item in agenda_item.agenda_items:
        print("                      - {}".format(sub_agenda_item.title))
```

Next to the `MeetingClient`, we also have `EventsClient` and `SpeakersClient`.
Examples for these clients can be found in the examples folder.