import logging

from aiohttp import web, ClientSession

logger = logging.getLogger(__name__)

clients = set()


async def lineup_handler(req):
    async with ClientSession() as session:
        async with session.get("http://192.168.1.15/lineup.json") as resp:
            lineup = await resp.json()
            return web.json_response(lineup)


async def websocket_handler(req):
    logger.error("in websocket_handler")
    ws = web.WebSocketResponse()
    # if not ws:
    #     logger.error("cant create websocket")
    #     return
    await ws.prepare(req)
    await ws.send_json({"hi": "there"})
    async for msg in ws:
        if msg.data == "close":
            await ws.close()
    logger.error("websocket disconnocected")


async def index_handler(req):
    return web.HTTPFound("index.html")


def make_app():
    app = web.Application()
    app.add_routes(
        [
            web.get("/", index_handler),
            web.get("/ws", websocket_handler),
            web.get("/lineup.json", lineup_handler),
        ]
    )
    app.router.add_static("/", "static")
    return app


if __name__ == "__main__":
    app = make_app()
    web.run_app(app, port=9090)
