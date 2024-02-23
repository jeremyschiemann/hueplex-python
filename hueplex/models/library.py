
from typing import Annotated

from pydantic import Field

from hueplex.models.base import BaseEvent, Metadata


class LibraryEvent(BaseEvent):
    metadata: Annotated[Metadata, Field(alias='Metadata')]
