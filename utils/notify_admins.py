import asyncio
import logging

from aiogram import Bot, Dispatcher
from data.config import ADMINS

async def on_startup_notify(dp: Dispatcher, user:str):
    
    for admin in ADMINS:
        try:
            if user != 'None':
                text = ""
                user = user[7:-1].split(' ')
                datetime = user[-1]
                for i in user[:-1]:
                    text += i.strip()
                    text += "\n"
                text += datetime
                await dp.bot.send_message(admin, f"{text}\n\nUshbu user barcha jarayonni yakunladi", parse_mode=None)
            else:
                await dp.bot.send_message(admin, "Bot ishga tushdi")

        except Exception as err:
            logging.exception(err)
            
async def send_delayed_video(dp: Dispatcher, user_id):
    await asyncio.sleep(5)  # 10 daqiqa kutish (10 minut * 60 soniya)
    video_file_path = 'AAMCAgADGQEAAgP5ZfimxFKTw5q7ek-fubWwoy1gwF8AAlwoAAJl_ShL34RAUB0OT4YBAAdtAAM0BA'
    # await dp.bot.send_video(user_id, video=video_file_path)
