from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "user" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "user_id" BIGINT NOT NULL UNIQUE,
    "is_subscribed" INT   DEFAULT 0,
    "trader_id" VARCHAR(100),
    "is_paid" INT   DEFAULT 0,
    "lose_count" REAL NOT NULL  DEFAULT 0,
    "trade_type" VARCHAR(100),
    "trade_tools" VARCHAR(200),
    "trade_time" VARCHAR(100),
    "trade_choose_time" TIMESTAMP,
    "trade_start_time" TIMESTAMP,
    "trade_choose_tools" VARCHAR(100),
    "name" VARCHAR(50),
    "username" VARCHAR(32),
    "state" INT NOT NULL  DEFAULT 0,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
