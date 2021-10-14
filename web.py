import logging
import os
from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect

from hdhomerun import HDHomeRun
from lib.tvmedia import TVMedia

logger = logging.getLogger(__name__)

clients = set()

def make_app():
    app = FastAPI(
        title="HDHomeRun Web",
        description="Benji's custom HDHomeRun web app")
    hdhr = HDHomeRun(base_url=os.getenv('HDHOMERUN_BASE_URL'))
   
    @app.get("/")
    async def index():
        return 'hi'
    
    @app.get("/lineup")
    async def get_lineup():
        return hdhr.get_lineup()

    @app.get("/streams/{channel_id}")
    async def start_stream(channel_id):
        return await hdhr.start_stream(channel_id)

  
    @app.delete("/streams/{channel_id}")
    async def stop_stream(channel_id):
        resp = await hdhr.stop_stream(channel_id)
        return "stopped"

    @app.websocket("/ws/")
    async def websocket_endpoint(ws: WebSocket):
        logger.info('websocket_endpoint')
        await ws.accept()
        while True:
            try:
                data = await ws.receive_text()
                await ws.send_text(f"Message text was: {data}")
            except WebSocketDisconnect as ex:
                logger.info('WebSocketDisconnect exception')
                break
            except RuntimeError as ex:
                logger.info('Websocket disconnected')
                break
        logger.info('websocket disconnected')

    return app

