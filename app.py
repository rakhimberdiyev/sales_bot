from aiogram import types
from aiohttp import web
from fastapi import Request, FastAPI, HTTPException
from fastapi.responses import JSONResponse

from aiogram.dispatcher.webhook import SendMessage
from aiogram.utils.executor import start_webhook

from data.config import WEBHOOK_PATH, WEBHOOK_URI, BOT_TOKEN
from loader import bot, dp, db

import handlers
from utils.misc import logging
from utils.notify_admins import on_startup_notify, on_shutdown_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(_):
    # await set_webhook()
    await bot.set_webhook(WEBHOOK_URI)
    await set_default_commands(dp)
    await on_startup_notify(dp, user=None)
    
    await db.create()
    await db.drop_users()
    await db.create_table_users()
    
    await db.add_default_user()


async def on_shutdown():
    await on_shutdown_notify(bot)


if __name__ == "__main__":

    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host='127.0.0.1',
        port=8080,
    )


# from aiogram import executor

# from loader import dp, db
# import middlewares, filters, handlers
# from utils.notify_admins import on_startup_notify
# from utils.set_bot_commands import set_default_commands


# async def on_startup(dispatcher):
#     await db.create()
#     await db.drop_users()
#     await db.create_table_users()
#     print("Bot ishga tushdi")
    
#     # Birlamchi komandalar (/star va /help)
#     await set_default_commands(dispatcher)

#     # Bot ishga tushgani haqida adminga xabar berish
#     await on_startup_notify(dispatcher, user="None")

#     await db.add_default_user()

# if __name__ == '__main__':
#     executor.start_polling(dp, on_startup=on_startup)
