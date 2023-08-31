from aiogram.dispatcher.filters.state import StatesGroup, State


class WomanAdmin(StatesGroup):
    SOS_one = State()
    SOS_two = State()
    SOS_three = State()
    bot_addone = State()
    bot_editone = State()
    bot_one = State()
    bot_two = State()
    admin_one = State()
    admin_two = State()
    admin_delone = State()


# _____________ HAMMASI BOR _____________ #
class Man_State(StatesGroup):
    man_audio = State()
    man_document = State()
    man_photo = State()
    man_text = State()
    man_video = State()
    man_voice = State()
    user_checkone = State()


class ManAdmin(StatesGroup):
    SOS_one = State()
    SOS_two = State()
    SOS_three = State()
    bot_addone = State()
    bot_editone = State()
    bot_one = State()
    bot_two = State()
    admin_one = State()
    admin_two = State()
    admin_delone = State()


class Woman_State(StatesGroup):
    woman_audio = State()
    woman_document = State()
    woman_photo = State()
    woman_text = State()
    woman_video = State()
    woman_voice = State()
    user_checkone = State()


class Man_Woman_State(StatesGroup):
    man_woman = State()
    man_one = State()
    woman_one = State()
    woman_two = State()


class AddAdmin(StatesGroup):
    one = State()
    two = State()
    three = State()
