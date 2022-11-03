from aiogram import Dispatcher
from .is_admin import IsAdmin
from .is_user import IsUser

def setup(dp: Dispatcher):
    db.filters_factory.bind(IsAdmin, event_handlers = [db.message_handlers])
    db.filters_factory.bind(IsUser, event_handlers = [db.message_handlers])
