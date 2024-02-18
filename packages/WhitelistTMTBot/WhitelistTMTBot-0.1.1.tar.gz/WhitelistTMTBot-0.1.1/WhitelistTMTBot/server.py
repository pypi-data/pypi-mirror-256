import json
import logging

import aiohttp

logger = logging.getLogger(__name__)


class AsyncHTTPClient:
    def __init__(self):
        self.session = aiohttp.ClientSession()

    async def post(self, url, data, headers=None):
        headers = headers or {"Content-Type": "application/json"}
        try:
            async with self.session.post(
                url, data=json.dumps(data), headers=headers
            ) as response:
                return response
        except aiohttp.ClientError as e:
            logger.error(f"Aiohttp client error: {str(e)}")
            return None

    async def close(self):
        await self.session.close()
        logger.info("HTTP session closed.")
