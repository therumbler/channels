import logging
from fastapi import FastAPI

from hdhomerun import HDHomeRun
from lib.tvmedia import TVMedia

logger = logging.getLogger(__name__)

clients = set()


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
        return hdhr.get_lineup()

    @app.get("/streams/{channel_id}")
    async def start_stream(channel_id):
        return await hdhr.start_stream(channel_id)

  
    @app.delete("/streams/{channel_id}")
    async def stop_stream(channel_id):
        resp = await hdhr.stop_stream(channel_id)
        return "stopped"

    return app
