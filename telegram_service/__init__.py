import os

import aiohttp
import requests

from telegram_service.process import load_questions, get_keyboard

token = os.environ.get("TELEGRAM_BOT_API_TOKEN")
assert token


class TG_WORK_QUEUE:

    token = token

    async def process(self, message):
        questions = await load_questions()
        if "callback_query" in message:
            ...
            """# User clicked on an inline keyboard button
            callback_data = message["callback_query"]["data"]
            chat_id = message["callback_query"]["message"]["chat"]["id"]
            print(f"User pressed button with data: {callback_data} in chat ID: {chat_id}")"""
        else:
            text_input = message["message"]["text"]
            chat_id = message["message"]["chat"]["id"]
            print(text_input)

        await self.send_particular_keyboard(message, chat_id)

    async def send_particular_keyboard(self, message, chat_id):
        buttons = [
            [
                {"text": "Button 1", "callback_data": "button1"},
                {"text": "Button 2", "callback_data": "button2"},
            ],
            [
                {"text": "Button 3", "callback_data": "button3"},
                {"text": "Button 4", "callback_data": "button4"},
            ],
        ]
        await self.send_reply_keyboard(chat_id=chat_id, text="vvv", buttons=buttons)

    async def send_reply_keyboard(self, chat_id, text, buttons):
        keyboard = {"keyboard": buttons, "one_time_keyboard": True}

        data = {"chat_id": chat_id, "text": text, "reply_markup": keyboard}

        response = requests.post(
            f"https://api.telegram.org/bot{self.token}/sendMessage", json=data
        )

        return response


class TG_PULL_QUEUE:

    token = token

    def __init__(self):
        self.offset = 0

    async def get_tg_updates(self, method_name="getUpdates"):
        """proceed not files"""
        url = f"https://api.telegram.org/bot{self.token}/{method_name}"
        params = {"offset": self.offset, "timeout": 30, "allowed_updates": []}

        response = requests.post(url, params)
        response_json = response.json()
        if response_json["ok"]:
            return response_json["result"]
        # async with aiohttp.ClientSession() as session:
        #     async with session.post(
        #         url, data=params, headers={"Content-Type": "application/json"}
        #     ) as resp:
        #         json_resp = await resp.json()
        #         print(json_resp)
        #         if json_resp["ok"]:
        #             messages = json_resp["result"]
        #             return messages

    async def get_new_messages(self):
        messages = await self.get_tg_updates()
        if messages:
            self.offset = messages[-1]["update_id"] + 1
        return messages