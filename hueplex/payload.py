import typing

from fastapi import Form
from pydantic import Tag, Discriminator, RootModel, Json

from typing import Annotated, Any, Dict, Union

from hueplex.models.admin import AdminEvent
from hueplex.models.library import LibraryEvent
from hueplex.models.media import MediaEvent


Events = Union[
    Annotated[MediaEvent, Tag('media')],
    Annotated[AdminEvent, Tag('admin')],
    Annotated[LibraryEvent, Tag('library')],
    Annotated[Dict[str, Any], Tag('')]
]

def get_discriminator_value(v: Dict[str, Any]) -> str | None:
    tags = [event_type.__metadata__[0].tag for event_type in typing.get_args(Events) if event_type.__metadata__[0].tag]
    event = v.get('event', '').split('.')[0]

    return event if event in tags else ''

def model_from_form(payload: Json = Form(...)) -> Events:
    return RootModel[
        Annotated[Events, Discriminator(get_discriminator_value)]
    ](**payload).root
