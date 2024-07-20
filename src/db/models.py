from tortoise import fields
from tortoise.models import Model
import pytz
import datetime


class User(Model):
    id = fields.BigIntField(pk=True)
    user_id = fields.BigIntField(null=False, unique=True)
    is_subscribed = fields.BooleanField(default=False, null=True)
    trader_id = fields.CharField(max_length=100, null=True)
    is_paid = fields.BooleanField(default=False, null=True)
    lose_count = fields.FloatField(default=0, null=False)
    trade_type = fields.CharField(max_length=100, null=True)
    trade_tools = fields.CharField(max_length=200, null=True)
    trade_time = fields.CharField(max_length=100, null=True)
    trade_choose_time = fields.DatetimeField(null=True)
    trade_start_time = fields.DatetimeField(null=True)
    trade_choose_tools = fields.CharField(max_length=100, null=True)
    trade_mode = fields.IntField(null=True, default=0)
    auto_trade_count = fields.IntField(null=True, default=0)
    auto_trade_choose_count = fields.IntField(null=True, default=0)

    
    name = fields.CharField(max_length=50, null=True)
    username = fields.CharField(max_length=32, null=True)
    state = fields.IntField(null=False, default=0)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)