import logging
from hdhomerun import HDHomeRun
# from aiohttp import web, ClientSession
from fastapi import FastAPI


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

def make_app():
    app = FastAPI(
        title="HDHomeRun Web",
        description="Benji's custom HDHomeRun web app")
    hdhr = HDHomeRun()
   
    @app.get("/")
    async def index():
        return 'hi'
    
    @app.get("/lineup")
    async def get_lineup():
        return hdhr.lineup

    @app.get("/streams/{channel_id}")
    async def start_stream(channel_id):
        return await hdhr.start_stream(channel_id)

  
    @app.delete("/streams/{channel_id}")
    async def stop_stream(channel_id):
        resp = await hdhr.stop_stream(channel_id)
        return "stopped"

    return app
if __name__ == "__main__":
    app = make_app()
    web.run_app(app, port=9090)
