from typing import Annotated

from pydantic import Field, BaseModel, IPvAnyAddress

from hueplex.models.base import BaseEvent, Metadata


class Player(BaseModel):
    local: bool
    public_address: Annotated[IPvAnyAddress, Field(alias='publicAddress')]
    title: str
    uuid: str


class MediaEvent(BaseEvent):
    player: Annotated[Player, Field(alias='Player')]
    metadata: Annotated[Metadata, Field(alias='Metadata')]
