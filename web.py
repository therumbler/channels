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


    async def process_message(message):
        """process a websocket message"""
        if 'channel' in message:
            return await hdhr.start_stream(message['channel'])
        logger.error('process_message can\'t process %r', message)
   
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
        channel = None
        while True:
            try:
                data = await ws.receive_json()
                resp = await process_message(data)
                if resp:
                    channel = data['channel']
                    await ws.send_json(resp)

            except WebSocketDisconnect as ex:
                logger.info('WebSocketDisconnect exception')
                break
            except RuntimeError as ex:
                logger.info('Websocket disconnected')
                break
        if channel:
            await hdhr.stop_stream(channel)
        logger.info('websocket disconnected')

    return app

