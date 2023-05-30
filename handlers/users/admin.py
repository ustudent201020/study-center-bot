import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import exceptions

from data.config import ADMINS
from keyboards.default.all import menu
from keyboards.default.rekKeyboards import rekKey1, back, admin_key
from loader import dp, db, bot
from states.rekStates import RekData


@dp.message_handler(text='Barchaga Xabar Yuborish 🗒')
async def bot_start(msg: types.Message, state: FSMContext):
    await msg.answer("<b>Xabarni yuboring</b>", reply_markup=back)
    await RekData.choice.set()


@dp.message_handler(content_types=['video', 'audio', 'voice', 'photo', 'document', 'text'], user_id=ADMINS,
                    state=RekData.choice)
async def contumum(msg: types.Message, state: FSMContext):
    if msg.text == '🔙️ Orqaga':
        await msg.answer('Bekor qilindi', reply_markup=admin_key)
        await state.finish()

    elif msg.video or msg.audio or msg.voice or msg.document or msg.photo or msg.text:
        if msg.text == 'Barchaga Xabar Yuborish 🗒':
            await msg.answer('Adashdingiz Shekilli\n\n'
                             'To`g`ri ma`lumot kirting')
        else:
            await state.finish()

            users = await db.select_all_users()
            count_baza = await db.count_users()
            count_err = 0
            count = 0
            await msg.answer('Xabar yuborish boshlandi\n\n'
                             'Iltimos barchaga habar yuborilguncha kuting')

            for user in users:
                user_id = user[6]
                try:
                    await msg.send_copy(chat_id=user_id)
                    count += 1
                    await asyncio.sleep(0.05)

                except Exception as err:
                    count_err += 1
                    await asyncio.sleep(0.05)

            await msg.answer(f"Yuborilganlar: <b>{count}</b> tа."
                             f"\n\nYuborilmagan: <b>{count_err}</b> tа."
                             f"\n\Bazada jami: <b>{count_baza}</b> tа"
                             f" foydalanuvchi mavjud.", reply_markup=admin_key
                             )

@dp.message_handler(text='Mahsus Xabarni Yuborish 🗒', user_id=ADMINS)
async def bot_start(msg: types.Message, state: FSMContext):
    await msg.answer("<b>Xabarni yuboring</b>", reply_markup=back)
    await RekData.special.set()


@dp.message_handler(content_types=['video', 'audio', 'voice', 'photo', 'document', 'text'], user_id=ADMINS,
                    state=RekData.special)
async def contumum(msg: types.Message, state: FSMContext):
    elements = await db.get_elements()

    winner_ball = 0
    for i in elements:
        winner_ball += int(i["winners"])

    if msg.text == '🔙️ Orqaga':
        await msg.answer('Bekor qilindi', reply_markup=admin_key)
        await state.finish()

    elif msg.video or msg.audio or msg.voice or msg.document or msg.photo or msg.text:
        if msg.text == 'Mahsus Xabarni Yuborish 🗒':
            await msg.answer('Adashdingiz Shekilli\n\n'
                             'To`g`ri ma`lumot kirting')
        else:
            await state.finish()

            users = await db.select_all_users()
            count_baza = await db.count_users()
            count_err = 0
            count = 0
            for user in users:
                if user[4] <= winner_ball:
                    continue
                else:
                    try:
                        await msg.send_copy(chat_id=user[6])
                        count += 1
                        await asyncio.sleep(0.05)

                    except Exception as err:
                        count_err += 1
                        await asyncio.sleep(0.05)

            await msg.answer(f"Ҳабар юборилганлар: <b>{count}</b> та.", reply_markup=admin_key
                             )


@dp.message_handler(state='*')
async def back_all(message: types.Message, state: FSMContext):
    if message.text == 'Back':
        await message.answer(text='Bosh menu', reply_markup=menu)
        await state.finish()

