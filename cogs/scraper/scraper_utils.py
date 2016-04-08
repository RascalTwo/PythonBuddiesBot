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

    async def fetch_page(self, url, session=None, headers=None):
        if session is None:
            session = self.session
        if headers is None:
            headers = self.headers
        with aiohttp.Timeout(10):
            async with session.get(url, headers=headers) as response:
                assert response.status == 200
                return await response.read()

    async def fetch_json(self, url, session=None, headers=None):
        if headers is None:
            headers = self.headers
        if session is None:
            session = self.session
        with aiohttp.Timeout(10):
            async with session.get(url, headers=headers) as resp:
                return await resp.json()
