from aiogram.dispatcher.filters.state import StatesGroup, State


class NewPost(StatesGroup):
    EnterMessage = State()
    Confirm = State()


class CancelPost(StatesGroup):
    EnterMessage = State()
    Confirm = State()


class MentionId(StatesGroup):
    EnterMessage = State()
    Confirm = State()