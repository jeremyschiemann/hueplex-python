from typing import Optional, Dict, Any, List

import httpx
PATH_PREFIX = '/clip/v2'
HEADER_APP_KEY = 'hue-application-key'

hue_data: Dict[str, str] | None = None


async def is_user_authorized(http: httpx.AsyncClient, bridge_ip: str) -> bool:

    headers = {HEADER_APP_KEY: hue_data['username']} if hue_data else {}

    res = await http.get(f'https://{bridge_ip}{PATH_PREFIX}/resource/device', headers=headers)
    return res.is_success


async def get_all_resources(http: httpx.AsyncClient, bridge_ip) -> List[Dict[str, Any]] | None:

    if not hue_data:
        return None

    res = await http.get(
        f'https://{bridge_ip}{PATH_PREFIX}/resource',
        headers={HEADER_APP_KEY: hue_data['username']},
    )

    return res.json()['data'] if res.is_success else []


async def get_grouped_lights(http: httpx.AsyncClient, bridge_ip) -> List[Any]:

    res = await http.get(
        f'https://{bridge_ip}{PATH_PREFIX}/resource/grouped_light',
        headers={HEADER_APP_KEY: hue_data['username']}
    )

    return res.json()['data']


async def execute_commad(http: httpx.AsyncClient, bridge_ip, id: str, command):
    await http.put(
        f'https://{bridge_ip}{PATH_PREFIX}/resource/grouped_light/{id}',
        json=command,
        headers={'hue-application-key': hue_data['username']},
    )


async def create_api_key(http: httpx.AsyncClient, bridge_ip: str, app_name: str, hostname: str) -> Optional[Dict[str, str]]:
    res = await http.post(
        url=f'https://{bridge_ip}/api',
        json={
            'devicetype': f'{app_name}#{hostname}',
            'generateclientkey': True,
        },
    )
    if res.is_error:
        raise ValueError('Couldnt create api key')

    data = res.json()
    print(data)

    if 'error' in data[0]:
        return None

    global hue_data
    hue_data = data[0]['success']

    return data[0]['success']
