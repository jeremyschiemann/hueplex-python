import datetime
from typing import Annotated, List

from pydantic import Field, FilePath, BaseModel, HttpUrl

from hueplex.models.base import BaseEvent, BaseMetadata


class Genre(BaseModel):
    id: str
    filter: str
    tag: str


class Country(BaseModel):
    id: str
    filter: str
    tag: str


class Guid(BaseModel):
    id: str


class Rating(BaseModel):
    image: str
    value: float
    type: str


class Role(BaseModel):
    id: str
    filter: str
    tag: str
    tag_key: Annotated[str, Field(alias='tagKey')]
    role: str
    thumb: HttpUrl


class Location(BaseModel):
    path: FilePath


class LibraryMetadata(BaseMetadata):
    slug: str
    studio: str
    library_selection_title: Annotated[str, Field(alias='librarySectionTitle')]
    library_selection_key: Annotated[str, Field(alias='librarySectionKey')]
    original_title: Annotated[str, Field(alias='originalTitle')]
    content_rating: Annotated[str, Field(alias='contentRating')]
    audience_rating: Annotated[float, Field(alias='audienceRating')]
    year: int
    theme: FilePath
    duration: int
    originally_available_at: Annotated[datetime.date, Field(alias='originallyAvailableAt')]
    leaf_count: Annotated[int, Field(alias='leafCount')]
    viewed_leaf_count: Annotated[int, Field(alias='viewedLeafCount')]
    child_count: Annotated[int, Field(alias='childCount')]
    audience_rating_image: Annotated[str, Field(alias='audienceRatingImage')]
    genre: Annotated[List[Genre], Field(alias='Genre')]
    country: Annotated[List[Country], Field(alias='Country')]
    guids: Annotated[List[Guid], Field(alias='Guid')]
    ratings: Annotated[List[Rating], Field(alias='Rating')]
    roles: Annotated[List[Role], Field(alias='Role')]
    location: Annotated[Location, Field(alias='Location')]


class LibraryEvent(BaseEvent):
    metadata: Annotated[LibraryMetadata, Field(alias='Metadata')]
