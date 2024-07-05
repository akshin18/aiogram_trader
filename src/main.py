import asyncio
import logging

from tortoise import Tortoise

from handlers.admin import router as admin_router
from handlers.client import router as client_router
from config_reader import config
from app import bot, dp
from utils.func import check_forgotten


async def on_startup() -> None:
    await Tortoise.init(
        db_url=config.DB_URL.get_secret_value(),
        modules={"models": ["db.models"]},
        timezone="Europe/Moscow",
    )
    await Tortoise.generate_schemas()
    asyncio.create_task(check_forgotten())


async def on_shutdown() -> None:
    await Tortoise.close_connections()


async def main():
    dp.include_routers(admin_router, client_router)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
