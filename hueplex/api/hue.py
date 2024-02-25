
import fastapi
import httpx
from starlette.templating import Jinja2Templates

from hueplex import hue_api

router = fastapi.APIRouter()


@router.get(
    '/hue',
    response_class=fastapi.responses.HTMLResponse,
)
async def hue_landing_page(request: fastapi.Request):
    templates: Jinja2Templates = request.state.templates

    #TODO: handle no bridge found

    return templates.TemplateResponse(
        request=request,
        name='hue/hue_base.html',
        context={},
    )

@router.get(
    '/hue/auth_status',
    response_class=fastapi.responses.HTMLResponse,
)
async def hue_auth_status(request: fastapi.Request):
    http: httpx.AsyncClient = request.state.http_client
    bridge_ip: str | None = request.state.bridge_ip
    templates: Jinja2Templates = request.state.templates

    if await hue_api.is_user_authorized(http, bridge_ip):
        return fastapi.Response(
            status_code=fastapi.status.HTTP_204_NO_CONTENT,
            headers={'HX-Redirect': request.url_for('get_status_page').path}
        )


    return templates.TemplateResponse(
        request=request,
        name='hue/no_auth.html',
        context={
            'is_authenticated': await hue_api.is_user_authorized(http, bridge_ip)
        },
    )


@router.post(
    '/hue/auth',
    status_code=204,
)
async def hue_do_auth(request: fastapi.Request):
    http: httpx.AsyncClient = request.state.http_client
    hostname: str = request.state.hostname
    app_name: str = request.state.app_name
    bridge_ip: str | None = request.state.bridge_ip
    res = await hue_api.create_api_key(http, bridge_ip, app_name, hostname)
    return fastapi.Response(
        status_code=fastapi.status.HTTP_204_NO_CONTENT,
        headers={'HX-Redirect': request.url_for('root').path},
    )
