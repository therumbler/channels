import asyncio
import logging
import os
import subprocess
import time

import httpx

from .utilities import run_command

from lib.tvmedia import TVMedia
from lib.zap2it import Zap2It
logger = logging.getLogger(__name__)

TV_MEDIA_API_KEY = os.environ["TV_MEDIA_API_KEY"]
class HDHomeRun:
    def __init__(self, base_url=None):
        if not base_url:
            self.discover = self._discover()
            logger.info(self.discover)
            self.base_url = self.discover[0]["BaseURL"]
        else:
            self.base_url = base_url
        self.http_client = httpx.AsyncClient()
        self.lineup = self._fetch_lineup()
        self.streams = {}
        # self.tvmedia = TVMedia(TV_MEDIA_API_KEY)
        # self.tvmedia_lineup = self.tvmedia.lineup("CA", "ON", "12123")
        self.zap2it = Zap2It()


    def get_lineup(self):
        lineup = self.lineup
        zap2it_listing = self.zap2it.grid()
        for channel in lineup:
            zap2it_channel = list(filter(lambda c: c["channelNo"] == channel['GuideNumber'], zap2it_listing['channels']))
            channel['listing'] = zap2it_channel

        return lineup
        
    def _discover(self):
        url = "https://ipv4-api.hdhomerun.com/discover"
        return httpx.get(url).json()

    def _fetch_lineup(self):
        url = self.base_url + "/lineup.json"
        resp = httpx.get(url)
        return resp.json()

    def fetch_status(self):
        url = self.base_url + "/status.json"
        resp = httpx.get(url)
        return resp.json()

    def _get_channel(self, guide_number):
        channel = list(filter(lambda c: c["GuideNumber"] == guide_number, self.lineup))
        if not channel:
            return None
        # stations = self.tvmedia_lineup[0]["stations"]
        # tv_media_channels = list(filter(lambda s:s["number"] == guide_number.replace(".","-"), stations))
        # if tv_media_channels:
        #     tv_media_channel = tv_media_channels[0]
        #     logger.info("tv_media_channel %r", tv_media_channel)
        zap2it_listing = self.zap2it.grid()
        zap2it_channel = list(filter(lambda c: c["channelNo"] == guide_number, zap2it_listing['channels']))
        channel[0]['listing'] = zap2it_channel
        return channel[0]

    async def start_stream(self, guide_number):
        channel = self._get_channel(guide_number)
        if not channel:
            raise ValueError("no channel found for guide_number %s" % guide_number)
    
        stream_url = f"./live/{guide_number}/stream.m3u8"
        status = self.fetch_status()
        logger.info("status = %s", status)
        if guide_number in [s.get('VctNumber') for s in status]:
            logger.info('HDHomeRun status says stream already running')
            self.streams[guide_number]["clients"] += 1            
            return {"stream_url":stream_url, "title": channel["GuideName"], "listing": channel["listing"]}

        if self.streams.get(guide_number):
            logger.info('stream already running')
            self.streams[guide_number]["clients"] += 1
            logger.info("number of clients for channel %s is %s", guide_number, self.streams[guide_number]["clients"])
            return {"stream_url":stream_url, "title": channel["GuideName"], "listing": channel["listing"]}
        
        if len(self.streams.keys()) == 2:
            raise OverflowError("too many streams are running")
     
       
        url = channel["URL"] + "?transcode=mobile"

        cmd = ["./scripts/stream.sh", url, guide_number]
        # cmd = ["tail", "-f", "index.html"]
        task = asyncio.create_task(run_command(cmd))
        self.streams[guide_number] = {}
        self.streams[guide_number]["task"] = task
        self.streams[guide_number]["clients"] = 1
        logger.info("stream created")
        await asyncio.sleep(15)
        # await stream
        return {"stream_url":stream_url, "title": channel["GuideName"],"listing": channel["listing"]}

    async def stop_stream(self, channel_id):
        if channel_id not in self.streams:
            logger.error('%s not streaming', channel_id)
            return
        self.streams[channel_id]["clients"]  -= 1
        if self.streams[channel_id]["clients"] == 0:
            logger.info('stopping stream %r...', self.streams[channel_id])
            self.streams[channel_id]["task"].cancel()
            self.streams.pop(channel_id, None)
        
    def stop_streams(self):
        for s in self.streams:
            logger.error("cancelling stream...")
            s.cancel()
        self.streams.clear()


def check_tuner_status(session, host, tuner="tuner0"):
    url = f"{host}/tuners.html?page={tuner}"
    # url = f"http://10.0.1.2/tuners.html?page={tuner}"
    logger.debug('about to load %s', url)
    resp = session.get(url)
    rows = resp.html.find("table > tr")

    status = {}
    for row in rows:
        key = row.find("td")[0].text
        try:
            value = row.find("td")[1].text
        except IndexError:
            continue
        status[key] = value

    return status

