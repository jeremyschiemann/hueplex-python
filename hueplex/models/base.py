from pathlib import Path
from typing import Annotated

import pydantic
from pydantic import BaseModel, Field, HttpUrl, ConfigDict


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


class Metadata(BaseModel):
    model_config = ConfigDict(
        extra=pydantic.Extra.allow,
    )

    library_section_type: Annotated[str, Field(alias='librarySectionType')]
    type: str
    thumb: Path
    art: Path
