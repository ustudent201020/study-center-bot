from aiogram.dispatcher.filters.state import StatesGroup, State


class AllState(StatesGroup):
    env = State()
    env_remove = State()


class RekData(StatesGroup):
    choice = State()
    special = State()
    picture = State()
    score = State()
    text = State()
    shart = State()
    gift = State()
    add = State()
    delete = State()
    kbsh = State()
    winners = State()


class Number(StatesGroup):
    number = State()
    add_user = State()


class DelUser(StatesGroup):
    user = State()
    fix = State()


class Lesson(StatesGroup):
    choice_section = State()
    choice_button = State()
    choice_video_section = State()
    choice_photo_section = State()
    choice_audio_section = State()
    add_audio = State()
    add_audio_text = State()
    add_video = State()
    add_video_text = State()
    add_image = State()
    add_image_text = State()
    dell = State()
    but_add = State()
    but_del = State()
