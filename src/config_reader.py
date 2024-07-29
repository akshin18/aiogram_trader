import os
from typing import List, Union
from datetime import datetime

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from dotenv import load_dotenv
from aiogram.types import Message
from google.oauth2.service_account import Credentials
import gspread
from gspread.cell import Cell
from loguru import logger
import pytz


load_dotenv(override=True)


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    DB_URL: SecretStr
    ADMINS_ID: List
    SHEET_ID: SecretStr
    FTM: str
    FOR_PAY: str

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
tiime_options = [
            "5 секунд",
            "15 секунд",
            "30 секунд",
            "1 минута",
            "5 минуты",
            "10 минуты",
            "15 минуты",
        ]
print(config.FTM)
print(config.FOR_PAY)
google_sheet = Google_sheet()
os.environ["TZ"] = "Europe/Moscow"
TRADER_TOOLS = {
    "Валюты": {
        "tools": [
            "AED/CNY OTC",
            "AUD/CAD OTC",
            "AUD/NZD OTC",
            "AUD/USD OTC",
            "CAD/CHF OTC",
            "CAD/JPY OTC",
            "EUR/CHF OTC",
            "EUR/GBP OTC",
            "EUR/TRY OTC",
            "GBP/AUD OTС",
            "GBP/JPY OTC",
            "JOD/CNY OTC",
            "LBP/USD OTC",
            "MAD/USD OTC",
            "SAR/CNY OTC",
            "USD/BRL OTC",
            "USD/CNH OTC",
            "USD/COP OTC",
            "USD/DZD OTC",
            "USD/INR OTC",
            "USD/JPY OTC",
            "USD/MXN OTC",
            "USD/MYR OTC",
            "USD/PKR OT",
            "USD/RUB OTC",
            "USD/SGD OTC",
            "USD/THB OTC",
            "CHF/NOK OTC",
            "EUR/HUF OTC",
            "EUR/JPY OTC",
            "TND/USD OTC",
            "YER/USD OTС",
            "USD/VND OTC",
            "GBP/USD OTC",
            "USD/CAD OTC",
            "QAR/CNY OTC",
            "EUR/NZD OTC",
            "USD/IDR OTC",
            "BHD/CNY OTC",
            "EUR/RUB OTC",
            "USD/BDT OTC",
            "USD/EGP OTC",
            "NZD/USD OTC",
            "EUR/USD OTC",
            "USD/CLP OTC",
            "AUD/JPY OTC",
            "USD/ARS OTC",
            "USD/PHP OTC",
            "OMR/CNY OTС",
            "CHF/JPY OTC",
            "NZD/JPY OTC",
            "AUD/CHF OTC",
            "USD/CHF OTC",
        ],
        "time": tiime_options,
    },
    "Криптовалюты": {
        "tools": [
            "Cardano OTС",
            "Avalanche OTC",
            "Bitcoin ETF OTC",
            "Chainlink OTC",
            "Polygon OTC",
            "Toncoin OTC",
            "TRON OTC",
            "Ethereum OTC",
            "Bitcoin OTC",
            "Ripple OTC",
            "Litecoin OTC",
            "BNB OTC",
            "Solana OTC",
            "Polkadot OTC",
            "Dogecoin OTC",
        ],
        "time": tiime_options,
        "image": "",
    },
    "Сырьевые товары": {
        "tools": [
            "Brent Oil OTC",
            "WTI Crude Oil OTC",
            "Silver OTC",
            "Gold OTC",
            "Natural Gas OTC",
            "Palladium spot OTC",
            "Platinum spot OTC",
        ],
        "time": tiime_options,
        "image": "",
    },
    "Акции": {
        "tools": [
            "Apple OTC",
            "American Express OTC",
            "Intel OTC",
            "Pfizer Inc OTC",
            "Citigroup Inc OTC",
            "TWITTER OTC",
            "McDonald's OTC",
            "VISA OTC",
            "Microsoft OTC",
            "Alibaba OTC",
            "Johnson & Johnson OTС",
            "Cisco OTC",
            "Boeing Company OTC",
            "Amazon OTC",
            "FedEx OTC",
            "Tesla OTC",
            "ExxonMobil OTC",
            "Netflix OTC",
            "FACEBOOK INC OTC",
        ],
        "time": tiime_options,
    },
    "Индексы": {
        "tools": [
            "AUS 200 OTC",
            "100GBP OTC",
            "D30EUR OTC",
            "DJI30 OTC",
            "E35EUR OTC",
            "E50EUR OTC",
            "F40EUR OTC",
            "JPN225 OTC",
            "US100 OTC",
            "SP500 OTC",
        ],
        "time": tiime_options,
    },
}

time_splitter = {
    "5 секунд": 5,
    "15 секунд": 15,
    "30 секунд": 30,
    "1 минута": 60,
    "5 минуты": 60 * 5,
    "10 минуты": 60 * 10,
    "15 минуты": 60 * 15,
}

indicator_form = """💱Валютная пара:(%s)\n⏳Время эксперации:(%s)\n\n\n✅ Бот рекомендует открывать торги на %s \nВремя на использование сигнала 15 секунд"""
lose_text = """Бот рекомендует вам сделать паузу 5 минут, вы проигрывайте из за разницы в тайм фрейме вашего устройства и бота!\nЧерез 5 минут вам нужно выбрать новую трейдинговую пару обновить страницу и подтвердить обновление и выбор новой пары для трейдинга !"""
