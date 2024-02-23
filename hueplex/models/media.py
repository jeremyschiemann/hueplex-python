from typing import Annotated

from pydantic import Field, BaseModel, IPvAnyAddress

from hueplex.models.base import BaseEvent, BaseMetadata



class Player(BaseModel):
    local: bool
    public_address: Annotated[IPvAnyAddress, Field(alias='publicAddress')]
    title: str
    uuid: str


class MediaMetadata(BaseMetadata):
    parent_rating_key: Annotated[str, Field(alias='parentRatingKey')]
    grandparent_rating_key: Annotated[str, Field(alias='grandparentRatingKey')]
    grandparent_key: Annotated[str, Field(alias='grandparentKey')]
    parent_key: Annotated[str, Field(alias='parentKey')]
    grandparent_title: Annotated[str, Field(alias='grandparentTitle')]
    parent_title: Annotated[str, Field(alias='parentTitle')]
    parent_index: Annotated[int, Field(alias='parentIndex')]
    rating_count: Annotated[int | None, Field(alias='ratingCount')] = None
    parent_thumb: Annotated[str, Field(alias='parentThumb')]
    grandparent_thumb: Annotated[str, Field(alias='grandparentThumb')]
    grandparent_art: Annotated[str, Field(alias='grandparentArt')]


class MediaEvent(BaseEvent):
    player: Annotated[Player, Field(alias='Player')]
    metadata: Annotated[MediaMetadata, Field(alias='Metadata')]
