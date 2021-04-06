from hashlib import sha256
import os
import json
from urllib.parse import urlencode

import httpx


import logging
logger = logging.getLogger(__name__)

CACHE_DIR = os.getenv("CACHE_DIR", "/cache")

def _check_cache(key):
    try:
        with open(f"{CACHE_DIR}/{key}.json") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.debug("cache miss")

def _save_cache(key, data):
    logger.debug("saving cache key %s...", key)
    with open(f"{CACHE_DIR}/{key}.json", "w") as f:
        f.write(json.dumps(data))

def _create_cache_key(*args, **kwargs):
    raw_string = ""
    for arg in args:
        if type(arg) == str:
            raw_string += arg
        else:
            raw_string += arg.base_url
    
    raw_string += "?" + urlencode(kwargs)
    logger.debug('raw_string %s', raw_string)
    cache_key = sha256(raw_string.encode()).hexdigest()
    logger.debug("cache_key %s", cache_key)
    return cache_key

def cacheable():
    def inner(func):
        def wrapper(*args, **kwargs):
            logger.info('args %r', args)
            cache_key = _create_cache_key(*args, **kwargs)
            cached = _check_cache(cache_key)
            if cached:
                logger.debug("cache hit!")
                return cached
            resp = func(*args, **kwargs)
            _save_cache(cache_key, resp)
            return resp

        return wrapper
    return inner

class TVMedia():
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.tvmedia.ca/tv/v4"
        logger.info('hi')

    @cacheable()
    def _call(self, endpoint, **params):
        if "api_key" not in params:
            params["api_key"] = self.api_key
        url = f"{self.base_url}/{endpoint}"
        logger.debug("fetching %s, %s", url, params)
        resp = httpx.get(url, params=params)
        return resp.json()

    def lineup(self, country_id, region_id, area_id):
        endpoint = f"lineups/browse/{country_id}/{region_id}/{area_id}"
        return self._call(endpoint, lineupType="OTA", detail="full")

def main():
    import os
    logging.basicConfig(level=logging.DEBUG)
    api_key = os.environ["TV_MEDIA_API_KEY"]
    tvmedia = TVMedia(api_key)
    lineup = tvmedia.lineup("CA", "ON", "12123")
if __name__ == "__main__":
    main()