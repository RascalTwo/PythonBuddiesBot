import asyncio
import aiohttp

class GeneralScraper(object):
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.session = aiohttp.ClientSession()
        self.headers = {
            'content-type': 'application/json',
            'user-agent': 'python aiohttp web scraper'
        }

    @asyncio.coroutine
    def fetch_page(self, url, session=None, headers=None):
        if session is None:
            session = self.session
        if headers is None:
            headers = self.headers
        response = yield from aiohttp.request("GET", url, headers=headers)
        return (yield from response.read())

    @asyncio.coroutine
    def fetch_json(self, url, session=None, headers=None):
        if headers is None:
            headers = self.headers
        if session is None:
            session = self.session
        response = yield from aiohttp.request("GET", url, headers=headers)
        return (yield from response.json())