from typing import Dict

import ujson
from aiohttp import web


async def get_json(request: web.Request) -> Dict:
    text = await request.text()
    try:
        json = ujson.loads(text)
    except ValueError as e:
        raise web.HTTPClientError(reason="Can`t parse client payload") from e
    return json
