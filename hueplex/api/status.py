from typing import Dict

import fastapi
from starlette.templating import Jinja2Templates

router = fastapi.APIRouter()

is_active = False

@router.get(
    '/status',
    response_class=fastapi.responses.HTMLResponse,
)
async def get_status_page(request: fastapi.Request):
    global is_active
    templates: Jinja2Templates = request.state.templates
    return templates.TemplateResponse(
        request=request,
        name='status_page.html',
        context={
            'app_name': request.state.app_name,
            'is_active': is_active,
        },
    )


@router.put(
    '/status',
    response_model=Dict[str, bool],
)
def toggle_status():
    global is_active
    is_active = not is_active
    return {'status':  is_active}
