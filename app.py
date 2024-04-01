from aiogram.utils.executor import start_webhook
from data.config import WEBHOOK_PATH, WEBHOOK_URI
from loader import bot, dp
from utils.notify_admins import on_startup_notify, on_shutdown_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(_):
    # await set_webhook()
    await bot.set_webhook(WEBHOOK_URI)
    await set_default_commands(dp)
    await on_startup_notify(dp, user=None)
    


async def on_shutdown():
    await on_shutdown_notify(bot)


if __name__ == "__main__":

    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host='0.0.0.0',
        port=8080,
    )

