from attrs import define, field
from typing import Optional, List
from datetime import datetime

@define
class DocumentVersion:
    id: int
    type: str # Known possible values: file, link
    url: Optional[str]       = field(default=None)
    file_name: Optional[str] = field(default=None)
    file_size: Optional[int] = field(default=None)
    mime_type: Optional[str] = field(default=None) # Some documents have no MIME type

@define
class Document:
    last_modified: datetime
    title: str
    version: int
    url: str
    versions: List[DocumentVersion]
    id: Optional[int] = field(default=None) # Apparently some documents have no ID