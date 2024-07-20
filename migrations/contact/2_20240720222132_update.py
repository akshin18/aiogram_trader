from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" ADD "auto_trade_choose_count" INT   DEFAULT 0;
        ALTER TABLE "user" DROP COLUMN "auto_trade_time";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" ADD "auto_trade_time" VARCHAR(100);
        ALTER TABLE "user" DROP COLUMN "auto_trade_choose_count";"""
