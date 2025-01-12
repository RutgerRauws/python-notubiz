from attrs import define

from datetime import datetime
from typing import Optional

@define
class Planning:
    # Auto-filled
    start_date : datetime
    end_date : Optional[datetime]