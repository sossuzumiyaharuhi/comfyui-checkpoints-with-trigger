from aiohttp import web
import server
from .checkpoint_trigger import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS, TRIGGER_MAP

WEB_DIRECTORY = "js"

@server.PromptServer.instance.routes.get("/checkpoint_trigger_map")
async def get_trigger_map(request):
    return web.json_response(TRIGGER_MAP)

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']