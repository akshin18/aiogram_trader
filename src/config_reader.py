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
print(config.FTM)
print(config.FOR_PAY)
google_sheet = Google_sheet()
os.environ["TZ"] = "Europe/Moscow"
TRADER_TOOLS = {
    "Blitz": {
        "tools": [
            "USD/BRL (OTC)",
            "EUR/USD (OTC)",
            "US 100 (OTC)",
            "EUR/JPY (OTC)",
            "AUD/CAD (OTC)",
            "BTC/USD (OTC)",
            "EUR/GBP (OTC)",
            "US 30 (OTC)",
            "PEN/USD (OTC)",
            "USD/MXN (OTC)",
            "USOUSD (OTC)",
            "XAUUSD (OTC)",
            "Tesla (OTC)",
            "Apple (OTC)",
            "Amazon (OTC)",
            "Google (OTC)",
            "CARDANO (OTC)",
            "XAGUSD (OTC)",
            "US 500 (OTC)",
            "DOGECOIN (OTC)",
            "Meta (OTC)",
            "SOL/USD (OTC)",
            "UKOUSD (OTC)",
            "TRON/USD (OTC)",
        ],
        "time":[
            "5 секунд",
            "15 секунд",
            "30 секунд",
            "1 минута",
            "5 минуты",
            "10 минуты",
            "15 минуты",
        ]
    },
    "Binary": {
        "tools": [
            "AUD/JPY",
            "EUR/JPY",
            "EUR/USD",
            "AUD/CAD",
            "AUD/USD",
            "AMAZON",
            "MCDON",
            "COKE",
            "CITI",
            "INTEL",
            "BAIDU",
            "TESLA",
            "JPM",
            "GOOGLE",
            "MORSTAN",
            "MSFT",
            "Meta",
            "ALIBABA",
            "GS",
            "NIKE",
            "APPLE",
            "GBP/USD",
            "CAD/CHF",
            "USD/CHF",
            "EUR/JPY (OTC)",
            "EUR/GBP (OTC)",
            "AUD/CAD (OTC)",
            "NZD/USD (OTC)",
            "EUR/USD (OTC)",
            "GBP/USD (OTC)",
            "USD/CHF (OTC)",
            "EUR/GBP",
            "USD/JPY",
            "GBP/JPY",
            "USD/CAD",
            "USD/JPY (OTC)",
            "GBP/JPY (OTC)",
            "NZD/USD (OTC)",
            "EUR/USD (OTC)",
            "GBP/USD (OTC)",
            "USD/CHF (OTC)",
            "FUR/GBP",
            "USD/JPY",
            "GBP/JPY",
            "USD/CAD",
            "USD/JPY (OTC)",
            "GBP/JPY (OTC)",
        ],
        "time":[
            "1 вариант",
            "2 вариант",
            "3 вариант",
        ],
        "image": "https://i.ibb.co/Cb5nFY5/Mind-Maps-May-22-Screenshot.png",
    },
    "Digital": {
        "tools": [
            "EUR/USD",
            "EUR/JPY",
            "GBP/USD",
            "GBP/JPY",
            "AUD/USD",
            "USD/CAD",
            "AUD/CAD",
            "US 100",
            "US 500",
            "US 30",
            "GBP/USD (OTC)",
            "NZD/USD (OTC)",
            "USD/CHF (OTC)",
            "AUD/JPY",
            "USD/CHF",
        ],
        "time":[
            "1 вариант",
            "2 вариант",
            "3 вариант",
        ],
         "image": "https://i.ibb.co/8xy3nPq/Mind-Maps-May-22-Screenshot-1.png",
    },
    "Forex": {
        "tools": [
            "EUR/USD",
            "USD/JPY",
            "AUD/USD",
            "EUR/JPY",
            "GBP/USD",
            "AUD/JPY",
            "GBP/JPY",
            "AUD/CAD",
            "USD/CAD",
            "EUR/GBP",
            "USD/JPY×1000",
            "EUR/AUD",
            "CHF/JPY",
            "EUR/NZD",
            "AUD/CHF",
            "AUD/NZD",
            "EUR/JPYx1000",
            "EUR/CAD",
            "CAD/CHF",
            "GBP/CAD",
            "NZD/CAD",
            "CAD/JPY",
            "EUR/CHF",
            "USD/ZAR",
            "GBP/USDx1000",
            "USD/CHFx1000",
            "NZD/CHE",
            "GBP/AUD",
            "NZD/JPY",
            "NOK/JPY",
            "EUR/ZAR",
            "CHF/NOK",
            "GBP/CHF",
            "EUR/NOK",
        ],
        "time":[]
    },
    "Crypto": {
        "tools": [
            "Bitcoin",
            "Pepe ×20",
            "EOS",
            "OmiseGo",
            "Bitcoin ×100",
            "Dash",
            "Bitcoin ×1000",
            "Ethereum",
            "Ethereum Classic",
            "Ripple",
            "ZCash",
            "Litecoin",
            "Qtum",
            "TRON",
        ],
        "time":[]
    },
}

time_splitter = {
    "5 секунд": 5,
    "15 секунд": 15,
    "30 секунд": 30,
    "1 минута": 60,
    "5 минуты": 60*5,
    "10 минуты": 60*10,
    "15 минуты": 60*15,
}

indicator_form = """💱Валютная пара:(%s)\n⏳Время эксперации:(%s)\n\n\n✅ Бот рекомендует открывать торги на %s \nВремя на использование сигнала 15 секунд"""
lose_text = """Бот рекомендует вам сделать паузу 5 минут, вы проигрывайте из за разницы в тайм фрейме вашего устройства и бота!\nЧерез 5 минут вам нужно выбрать новую трейдинговую пару обновить страницу Экснова и подтвердить обновление и выбор новой пары для трейдинга !"""