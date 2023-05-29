from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from data.config import ADMINS
from keyboards.default.all import menu
from keyboards.default.rekKeyboards import admin_key, darslar_key, save
from keyboards.default.rekKeyboards import back
from loader import dp, db, bot
from states.rekStates import Lesson


@dp.message_handler(text='Remove File')
async def add_channel(message: types.Message):
    # buttons = await db.select_buttons()
    # but = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, )
    # but.add(*(KeyboardButton(text=str(button[1])) for button in buttons))
    # but.add(KeyboardButton(text='🔙️ Orqaga'))
    await message.answer(
        text="Barcha ma'lumotlar o'chadi\n\nBarchasiga rozimisiz\n\nHa bo'lsa file_unique_id ni kiriting",
        reply_markup=back
    )
    await Lesson.but_del.set()


@dp.message_handler(state=Lesson.but_del)
async def del_button(message: types.Message, state: FSMContext):
    txt = message.text
    lessons = await db.select_lessons()
    unique_id = []
    for lesson in lessons:
        unique_id.append(lesson[3])
    if txt == '🔙️ Orqaga':
        await message.answer('Admin panel', reply_markup=darslar_key)
        await state.finish()
    elif message.text in unique_id:
        await db.delete_lesson(file_unique_id=message.text)
        await message.answer("O'chirildi", reply_markup=darslar_key)
        await state.finish()
    else:
        await message.answer('Xato\n\nBunday id yo`q\n\nChiqish uchun orqaga tugmasini bosing')


@dp.message_handler(text='Add File')
async def add_channel(message: types.Message):
    buttons = await db.select_buttons()
    but = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, )
    but.add(*(KeyboardButton(text=str(button[1])) for button in buttons))
    but.add(KeyboardButton(text='🔙️ Orqaga'))

    await message.answer(
        text="Qaysi bo'limga qo'shamiz",
        reply_markup=but
    )
    await Lesson.choice_button.set()


@dp.message_handler(state=Lesson.choice_button)
async def choice(message: types.Message, state: FSMContext):
    buttons = await db.select_buttons()
    all_buttons_list = []
    for button in buttons:
        all_buttons_list.append(button[1])

    if message.text in all_buttons_list:
        await state.update_data(
            {
                "button_name": message.text,
            }
        )

        await message.answer(text="Kerakli bo'limni tanlang",
                             reply_markup=save)
        await Lesson.choice_section.set()
    else:
        await message.answer('Xato\n\n'
                             'Tugmalardan birni tanlashingiz shart')


@dp.message_handler(state=Lesson.choice_section)
async def add_username(message: types.Message, state: FSMContext):
    text = message.text
    if text == '🔙️ Orqaga':
        await message.answer('Admin panel', reply_markup=darslar_key)
        await state.finish()
    elif text == 'Video Yuklash':
        await message.answer('Faqat Video Yuboring', reply_markup=types.ReplyKeyboardRemove())
        await Lesson.add_video.set()
    elif text == 'Audio Yuklash':
        await message.answer('Faqat Audio Yuboring', reply_markup=types.ReplyKeyboardRemove())
        await Lesson.add_audio.set()
    elif text == 'Rasm Yuklash':
        await message.answer('Faqat Rasm Yuboring', reply_markup=types.ReplyKeyboardRemove())
        await Lesson.add_image.set()


@dp.message_handler(state=Lesson.add_video, content_types=['video', 'audio', 'voice', 'photo', 'document', 'text'])
async def add_lesson(message: types.Message, state: FSMContext):
    if message.video:

        await state.update_data(
            {
                "file_id": message.video.file_id,
                "file_unique_id": message.video.file_unique_id
            }
        )
        await message.answer("Qo'shimcha Text kiriting")
        await Lesson.add_video_text.set()
    else:
        await message.answer('🚫 Xato\n\n'
                             'Bu video emas')


@dp.message_handler(state=Lesson.add_video_text)
async def add_lesson(message: types.Message, state: FSMContext):
    data = await state.get_data()

    file = data.get('file_id')
    button_name = data.get('button_name')
    file_unique_id = data.get('file_unique_id')
    if message.text:
        await message.answer("Qo'shildi")
        await bot.send_video(
            chat_id=message.from_user.id,
            video=file,
            caption=f'{message.text}\n\n'
                    f'🗑 o`chirish uchun mahsus code - {file_unique_id}'
                    f' (faqat adminlarga ko`rinadi)')
        await db.add_lesson(button_name=f'{button_name}', file_id=file,
                            file_unique_id=file_unique_id,type='video',description=message.text)
        await state.finish()
    else:
        await message.answer('🚫 Xato\n\n'
                             'Bu text emas')


@dp.message_handler(state=Lesson.add_audio, content_types=['video', 'audio', 'voice', 'photo', 'document', 'text'])
async def add_lesson(message: types.Message, state: FSMContext):
    if message.audio:
        await state.update_data(
            {
                "file_id": message.audio.file_id,
                "file_unique_id": message.audio.file_unique_id
            }
        )

        await message.answer("Qo'shimcha Text kiriting")
        await Lesson.add_audio_text.set()

    else:
        await message.answer('🚫 Xato\n\n'
                             'Bu audio emas')


@dp.message_handler(state=Lesson.add_audio_text)
async def add_lesson(message: types.Message, state: FSMContext):
    data = await state.get_data()

    file = data.get('file_id')
    file_unique_id = data.get('file_unique_id')
    button_name = data.get('button_name')
    if message.text != "Shart emas":
        await message.answer("Qo'shildi")
        await bot.send_audio(
            chat_id=message.from_user.id,
            audio=file,
            caption=f'{message.text}\n\n'
                    f'🗑 o`chirish uchun mahsus code - {file_unique_id}'
                    f' (faqat adminlarga ko`rinadi)')
        await db.add_lesson(button_name=f'{button_name}', file_id=file,
                            file_unique_id=file_unique_id,type='audio',description=message.text)

        await state.finish()
    else:
        await message.answer('🚫 Xato\n\n'
                             'Bu text emas')


@dp.message_handler(state=Lesson.add_image, content_types=['video', 'audio', 'voice', 'photo', 'document', 'text'])
async def add_image(message: types.Message, state: FSMContext):
    if message.photo:
        await state.update_data(
            {
                "file_id": message.photo[-1].file_id,
                "file_unique_id": message.photo[-1].file_unique_id
            }
        )

        await message.answer("Qo'shimcha Text kiriting")
        await Lesson.add_image_text.set()
    else:
        await message.answer('🚫 Xato\n\n'
                             'Bu rasm emas')


@dp.message_handler(state=Lesson.add_image_text)
async def add_lesson(message: types.Message, state: FSMContext):
    data = await state.get_data()

    file = data.get('file_id')
    button_name = data.get('button_name')
    file_unique_id = data.get('file_unique_id')
    if message.text:
        await bot.send_photo(
            chat_id=message.from_user.id,
            photo=file,
            caption=f'{message.text}\n\n'
                    f'🗑 o`chirish uchun mahsus code - {file_unique_id}'
                    f' (faqat adminlarga ko`rinadi)')
        await db.add_lesson(button_name=f'{button_name}', file_id=file,
                            file_unique_id=file_unique_id,type='photo',description=message.text)

        await state.finish()
    else:
        await message.answer('🚫 Xato\n\n'
                             'Bu text emas')
