from aiogram import Dispatcher

from loader import dp
from .throttling import ThrottlingMiddleware
from .ban_user import BigBrother
from . import check_subscription
if __name__ == "middlewares":
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(check_subscription.BigBrother())
    dp.middleware.setup(BigBrother())
