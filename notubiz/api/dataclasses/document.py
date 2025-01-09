from attrs import define, field
from typing import Optional, List
from datetime import datetime

@define
class DocumentVersion:
    id: int
    file_name: str
    file_size: int
    mime_type: Optional[str] = field(default="") # Apparently some documents have no MIME type

@define
class Document:
    last_modified: datetime
    title: str
    version: int
    url: str
    versions: List[DocumentVersion]
    id: Optional[int] = field(default=None) # Apparently some documents have no ID