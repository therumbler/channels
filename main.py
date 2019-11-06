import asyncio
import logging
import subprocess
import time

from hdhomerun import HDHomeRun, check_tuner_status
from hdhomerun.utilities import setup_logging
from requests_html import HTMLSession

logger = logging.getLogger(__name__)


async def main_async():
    setup_logging(level=logging.DEBUG)
    hdhomerun = HDHomeRun("http://192.168.1.15/")
    try:
        hdhomerun.start_stream("9.1")
    except KeyboardInterrupt:
        logger.error("KeyboardInterrupt!!!")
        hdhomerun.stop_streams()
        raise
    await asyncio.sleep(30)
    hdhomerun.stop_streams()

    for task in asyncio.all_tasks():
        logger.info("cancelling a task")
        task.cancel()
    logger.error("FINISHED")


def main():
    # hdhomerun = HDHomeRun("http://192.168.1.15/")
    # channel = hdhomerun._get_channel("2.41")
    # print(channel)

    # return

    session = HTMLSession()
    virtual_channel = None
    signal_quality = None
    while True:
        status = check_tuner_status(session)
        if virtual_channel != status["Virtual Channel"]:
            virtual_channel = status["Virtual Channel"]
            subprocess.call(["say", "channel", status["Virtual Channel"]])
        if signal_quality != status["Signal Quality"]:
            signal_quality = status["Signal Quality"]
            subprocess.call(["say", status["Signal Quality"]])

        time.sleep(2)


if __name__ == "__main__":
    main()
    # asyncio.run(main_async())
