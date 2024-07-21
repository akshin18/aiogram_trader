from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" ADD "win_count" INT   DEFAULT 0;
        ALTER TABLE "user" ADD "manual_click_count" INT   DEFAULT 0;
        ALTER TABLE "user" ADD "signals_count" INT   DEFAULT 0;
        ALTER TABLE "user" ADD "auto_click_count" INT   DEFAULT 0;
        ALTER TABLE "user" ADD "top_up_date" VARCHAR(100);
        ALTER TABLE "user" ADD "last_lose_count" INT   DEFAULT 0;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" DROP COLUMN "win_count";
        ALTER TABLE "user" DROP COLUMN "manual_click_count";
        ALTER TABLE "user" DROP COLUMN "signals_count";
        ALTER TABLE "user" DROP COLUMN "auto_click_count";
        ALTER TABLE "user" DROP COLUMN "top_up_date";
        ALTER TABLE "user" DROP COLUMN "last_lose_count";"""
