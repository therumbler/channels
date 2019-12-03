import asyncio
import logging
import subprocess
import time
from .utilities import run_command
from requests_html import HTMLSession


logger = logging.getLogger(__name__)


class HDHomeRun:
    def __init__(self, base_url):
        self.base_url = base_url
        self.lineup = self._get_lineup()
        self.streams = set()

    def _get_lineup(self):
        session = HTMLSession()
        url = self.base_url + "lineup.json"
        resp = session.get(url)
        return resp.json()

    def _get_channel(self, guide_number):
        channel = list(filter(lambda c: c["GuideNumber"] == guide_number, self.lineup))
        if not channel:
            return None
        return channel[0]

    def start_stream(self, guide_number):
        logger.info("start_stream...")
        if len(self.streams) == 2:
            raise OverflowError("too many streams are running")

        channel = self._get_channel(guide_number)
        if not channel:
            raise ValueError("no channel found for guide_number %s" % guide_number)
        url = channel["URL"] + "?transcode=mobile"

        cmd = ["./bin/stream.sh", url]
        # cmd = ["tail", "-f", "index.html"]
        stream = asyncio.create_task(run_command(cmd))
        self.streams.add(stream)
        logger.info("stream created")
        # await stream

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

