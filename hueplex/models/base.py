import datetime
from typing import Annotated

from pydantic import BaseModel, Field, FilePath, HttpUrl


class Account(BaseModel):
    id: int
    thumb: HttpUrl
    title: str


class Server(BaseModel):
    title: str
    uuid: str


class BaseEvent(BaseModel):
    event: str
    user: bool
    owner: bool
    account: Annotated[Account, Field(alias='Account')]
    server: Annotated[Server, Field(alias='Server')]


class BaseMetadata(BaseModel):
    library_section_type: Annotated[str, Field(alias='librarySectionType')]
    rating_key: Annotated[str, Field(alias='ratingKey')]
    key: str
    guid: str
    type: str
    title: str
    library_section_id: Annotated[int, Field(alias='librarySectionID')]
    summary: str
    index: int
    thumb: str
    art: str
    added_at: Annotated[datetime.datetime, Field(alias='addedAt')]
    updated_at: Annotated[datetime.datetime, Field(alias='updatedAt')]
