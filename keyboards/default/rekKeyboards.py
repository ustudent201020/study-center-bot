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

main_section = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🔝 Bosh menu'),
        ]
    ],
    resize_keyboard=True
)

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='- Tanlov'),
        ],
        [
            KeyboardButton(text="- Go School")
        ]
    ], resize_keyboard=True
)

save = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Video Yuklash'),
            KeyboardButton(text='Rasm Yuklash'),
            KeyboardButton(text='Audio Yuklash'),
        ],
        [
            KeyboardButton(text='🔙️ Orqaga')
        ]
    ], resize_keyboard=True
)
darslar_key = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Add File'),
            KeyboardButton(text='Remove File')
        ],
        [
            KeyboardButton(text='Barcha Adminlar'),
            KeyboardButton(text='Admin ➕'),
            KeyboardButton(text='Admin ➖')
        ],
        [
            KeyboardButton(text='Tugma ➕'),
            KeyboardButton(text='Tugma ➖')
        ],
        [
            KeyboardButton(text="🏘 Bosh menu")

        ],
    ],
    resize_keyboard=True
)
admin_key = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Barchaga Xabar Yuborish 🗒'),
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
