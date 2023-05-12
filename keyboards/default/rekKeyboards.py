from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

rekKey1 = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Rasm"),
            KeyboardButton(text="Video")
        ],
        [
            KeyboardButton(text='Text'),
            KeyboardButton(text='Back')
        ]
    ],
    resize_keyboard=True
)
back = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🔙️ Orqaga'),
        ]
    ],
    resize_keyboard=True
)


admin_key = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Mahsus Xabarni Yuborish 🗒'),
            KeyboardButton(text='Excel File'),
        ],
        [
            KeyboardButton(text='Barchaga Xabar Yuborish 🗒'),
            KeyboardButton(text='Bugungi balni kiriting'),
        ],
        [
            KeyboardButton(text='Kanal ➕'),
            KeyboardButton(text='Kanal ➖')
        ],
        [
            KeyboardButton(text="Kanallar 📈"),
            KeyboardButton(text="Statistika 📊")
        ],
        [
            KeyboardButton(text="Rasmni almashtirish 🖼"),
            KeyboardButton(text="Sovg'alar ro'yxatini kiritish 📄"),
        ],
        [
            KeyboardButton(text="Taklif miqdorini kiritish 🎁"),
            KeyboardButton(text="O'yin haqida matn 🎮")
        ],
        [
            KeyboardButton(text='Hisobni 0 ga tushirish'),
            KeyboardButton(text='Shartlarni qo"shish 🖼')
        ],
        [
            # KeyboardButton(text="Bugungi balni kiriting"),
            KeyboardButton(text="G'oliblar haqida ma'lumot")
        ],
        [
            KeyboardButton(text="🏘 Bosh menu")

        ]
    ],
    resize_keyboard=True
)
