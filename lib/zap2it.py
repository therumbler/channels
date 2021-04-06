import logging
import time

import httpx

logger = logging.getLogger(__name__)


class Zap2It():
    def __init__(self):
        self.base_url = "https://tvlistings.zap2it.com/api"
        

    def _call(self, endpoint, **params):
       
        url = f"{self.base_url}/{endpoint}"
        logger.debug("fetching %s, %s", url, params)
        resp = httpx.get(url, params=params)
        if resp.status_code >= 400:
            logger.error('response error %d: %s', resp.status_code, resp.text)
        logger.info('response from %s', resp.url)
        return resp.json()

    def grid(self):
      
        endpoint = "grid"
        #device=-&postalCode=M6J3S8&isOverride=true&time=1617732000&pref=16%2C128&userId=-&aid=gapzap&languagecode=en"

        params = {
            "lineupId":"CAN-lineupId-DEFAULT",
            "timespan": 3,
            "headendId": "lineupId",
            "country": "CAN", 
            "postalCode":"M6J3S8",
            "timezone": "",
            "isOverride":"true",
            "device":"-",
            # "time":"1617732000"
            "time": int(time.time()),

        }
        return self._call(endpoint, **params)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    zap2it = Zap2It()
    grid = zap2it.grid()
    # print(grid)