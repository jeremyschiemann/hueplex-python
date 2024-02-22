import datetime

from pydantic import BaseModel, Field, HttpUrl, IPvAnyAddress

from typing import Annotated


class Account(BaseModel):
    id: int
    thumb: HttpUrl
    title: str


class Server(BaseModel):
    title: str
    uuid: str


class Player(BaseModel):
    local: bool
    public_address: Annotated[IPvAnyAddress, Field(alias='publicAddress')]
    title: str
    uuid: str


class Metadata(BaseModel):
    library_selection_type: Annotated[str, Field(alias='librarySectionType')]
    rating_key: Annotated[str, Field(alias='ratingKey')]
    key: str
    parent_rating_key: Annotated[str, Field(alias='parentRatingKey')]
    grandparent_rating_key: Annotated[str, Field(alias='grandparentRatingKey')]
    guid: str
    library_selection_id: Annotated[int, Field(alias='librarySectionID')]
    type: str
    title: str
    grandparent_key: Annotated[str, Field(alias='grandparentKey')]
    parent_key: Annotated[str, Field(alias='parentKey')]
    grandparent_title: Annotated[str, Field(alias='grandparentTitle')]
    parent_title: Annotated[str, Field(alias='parentTitle')]
    summary: str
    index: int
    parent_index: Annotated[int, Field(alias='parentIndex')]
    rating_count: Annotated[int, Field(alias='ratingCount')]
    thumb: str
    art: str
    parent_thumb: Annotated[str, Field(alias='parentThumb')]
    grandparent_thumb: Annotated[str, Field(alias='grandparentThumb')]
    grandparent_art: Annotated[str, Field(alias='grandparentArt')]
    added_at: Annotated[datetime.datetime, Field(alias='addedAt')]
    updated_at: Annotated[datetime.datetime, Field(alias='updatedAt')]


class Payload(BaseModel):
    event: str
    user: bool
    owner: bool
    account: Annotated[Account, Field(alias='Account')]
    server: Annotated[Server, Field(alias='Server')]
    player: Annotated[Player, Field(alias='Player')]
    metadata: Annotated[Metadata, Field(alias='Metadata')]