from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from keyboards.default.all import menu
from keyboards.default.rekKeyboards import main_menu
from loader import dp, db, bot
from states.rekStates import ShowLessons
from utils.misc import subscription


@dp.message_handler(text='🔝 Bosh menu')
async def main_menuu(message: types.Message):
    status = True
    all = await db.select_chanel()
    chanels = []
    url = []
    channel_names = []
    for i in all:
        chanels.append(i['chanelll'])
        url.append(i['url'])
        channel_names.append(i['channel_name'])

    for channel in chanels:
        status *= await subscription.check(user_id=message.from_user.id,
                                           channel=f'{channel}')
    if status:
        await message.answer("<b>Bosh menu</b>",
                             reply_markup=main_menu, disable_web_page_preview=True)
    else:
        button = types.InlineKeyboardMarkup(row_width=1, )
        counter = 0
        for i in url:
            button.add(types.InlineKeyboardButton(f"{channel_names[counter]}", url=f'https://t.me/{i}'))
            counter += 1
        button.add(types.InlineKeyboardButton(text="A’zo bo’ldim", callback_data="check_subs"))

        await message.answer(
            '✅Tanlovda ishtirok etish uchun quyidagi kanallarga a’zo bo’ling.\nKeyin <b>“A’zo bo’ldim”</b>'
            ' tugmasini bosing.',
            reply_markup=button,
            disable_web_page_preview=True)


@dp.message_handler(text='Konkurs 🎉')
async def konkurs(message: types.Message):
    status = True
    all = await db.select_chanel()
    chanels = []
    url = []
    channel_names = []
    for i in all:
        chanels.append(i['chanelll'])
        url.append(i['url'])
        channel_names.append(i['channel_name'])

    for channel in chanels:
        status *= await subscription.check(user_id=message.from_user.id,
                                           channel=f'{channel}')
    if status:
        await message.answer("<b>Quyidagi menudan kerakli bo`limni tanlang 👇</b>",
                             reply_markup=menu, disable_web_page_preview=True)
    else:
        button = types.InlineKeyboardMarkup(row_width=1, )
        counter = 0
        for i in url:
            button.add(types.InlineKeyboardButton(f"{channel_names[counter]}", url=f'https://t.me/{i}'))
            counter += 1
        button.add(types.InlineKeyboardButton(text="A’zo bo’ldim", callback_data="check_subs"))

        await message.answer(
            '✅Tanlovda ishtirok etish uchun quyidagi kanallarga a’zo bo’ling.\nKeyin <b>“A’zo bo’ldim”</b>'
            ' tugmasini bosing.',
            reply_markup=button,
            disable_web_page_preview=True)

