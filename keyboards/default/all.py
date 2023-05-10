from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🎁 Tanlovda ishtirok etish'),
        ],
        [
            KeyboardButton(text='🎁 Sovg`alar'),
            KeyboardButton(text='👤 Ballarim'),
        ],
        [
            KeyboardButton(text='📊 Рейтинг'),
            KeyboardButton(text='💡 Shartlar'),
        ],
        # [
        #     KeyboardButton(text='📈 Статистика')
        # ]
    ],
    resize_keyboard=True
)

number = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='📲 Raqamni yuborish', request_contact=True),
        ],
    ],
    resize_keyboard=True
)
