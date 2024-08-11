import os
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
import gspread
from loguru import logger
import pytz

from utils import language

load_dotenv(override=True)


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    DB_URL: SecretStr
    ADMINS_ID: List
    SHEET_ID: SecretStr
    LANG: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


class Google_sheet:
    def __init__(self) -> None:
        self.scope = ["https://www.googleapis.com/auth/spreadsheets"]
        self.creds = Credentials.from_service_account_file(
            "creds.json", scopes=self.scope
        )
        self.client = gspread.authorize(self.creds)

        self.sheet_id = config.SHEET_ID.get_secret_value()
        self.workbook = self.client.open_by_key(self.sheet_id)

        self.sheet = self.workbook.sheet1
        self.moscow_timezone = pytz.timezone("Europe/Moscow")

    def create_user(
        self,
        start_date,
        start_time,
        user_id,
        bot_is_active,
        username="",
    ):
        data = [
            start_date,
            start_time,
            user_id,
            username,
            bot_is_active,
        ]
        self.sheet.append_row(data, table_range="A1")

    def update_manual_trading(self, user_id, number):
        try:
            self.sheet.update_cell(self.sheet.find(str(user_id)).row, 8, number)
        except Exception as e:
            logger.error(f"update error {e}")

    def update_auto_trading(self, user_id, number):
        try:
            self.sheet.update_cell(self.sheet.find(str(user_id)).row, 9, number)
        except Exception as e:
            logger.error(f"update error {e}")

    def update_top_up(self, user_id, number):
        try:
            self.sheet.update_cell(self.sheet.find(str(user_id)).row, 10, number)
        except Exception as e:
            logger.error(f"update error {e}")

    def update_indecator_count(self, user_id, number):
        try:
            self.sheet.update_cell(self.sheet.find(str(user_id)).row, 11, number)
        except Exception as e:
            logger.error(f"update error {e}")

    def update_win_count(self, user_id, number):
        try:
            self.sheet.update_cell(self.sheet.find(str(user_id)).row, 12, number)
        except Exception as e:
            logger.error(f"update error {e}")

    def update_lose_win_count(self, user_id, number):
        try:
            self.sheet.update_cell(self.sheet.find(str(user_id)).row, 13, number)
        except Exception as e:
            logger.error(f"update error {e}")

    def update_win_amount(self, user_id, number):
        try:
            self.sheet.update_cell(self.sheet.find(str(user_id)).row, 14, number)
        except Exception as e:
            logger.error(f"update error {e}")


config = Settings()
google_sheet = Google_sheet()
tiime_options = language.tiime_options[config.LANG]
os.environ["TZ"] = "Europe/Moscow"
TRADER_TOOLS = language.TRADER_TOOLS[config.LANG]

times_list = [5, 15, 30, 60, 60*5, 60*10, 60*15]
time_splitter =  { key:value for key, value in zip(language.tiime_options[config.LANG], times_list)}
indicator_form = language.indicator_form[config.LANG]
lose_text = language.lose_text[config.LANG]
