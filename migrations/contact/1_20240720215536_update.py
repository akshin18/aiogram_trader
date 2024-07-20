from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" ADD "auto_trade_count" INT   DEFAULT 0;
        ALTER TABLE "user" ADD "auto_trade_time" VARCHAR(100);
        ALTER TABLE "user" ADD "trade_mode" INT   DEFAULT 0;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" DROP COLUMN "auto_trade_count";
        ALTER TABLE "user" DROP COLUMN "auto_trade_time";
        ALTER TABLE "user" DROP COLUMN "trade_mode";"""
