from datetime import datetime

import aiohttp
from aiogram import Bot
from settings import settings


class TelegramRawClient:
    def __init__(self, token: str, base_url: str = "https://api.telegram.org"):
        self.token = token
        self.base_url = base_url.rstrip("/")
        self.session = None

    async def ensure_session(self):
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session

    async def prepare_url(self, method: str):
        result_url = f"{self.base_url}/bot{self.token}/"
        if method is not None:
            result_url += method
        return result_url

    async def post(self, method: str, **payload):
        url = self.prepare_url(method)
        session = await self.ensure_session()
        try:
            async with session.post(url, json=payload) as resp:
                return await resp.json()
        except Exception as e:
            print(f"Error calling Telegram API: {e}")
            return {"ok": False, "error": str(e)}

    def create_err_message(self, err):
        return f"{datetime.now()} :: {err.__class__} :: {err}"

    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()


class CompanyBot(Bot):
    def __init__(self, token: str, telegram_client=None, **kwargs):
        super().__init__(token=token, **kwargs)
        self.raw_client = telegram_client or TelegramRawClient(token=token)

    async def raw_call(self, method: str, **payload):
        return await self.raw_client.post(method, **payload)

    async def close(self):
        await super().close()
        await self.raw_client.close()


telegram_client = TelegramRawClient(token=settings.bot_token)
