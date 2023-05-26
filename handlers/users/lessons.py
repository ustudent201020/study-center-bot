from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from keyboards.default.all import menu
from keyboards.default.rekKeyboards import admin_key
from keyboards.default.rekKeyboards import back
from loader import dp, db, bot
from states.rekStates import Lesson


@dp.message_handler(text='Video Yuklash')
async def lesson(message: types.Message):
    await message.answer('Faqat Video Yuboring')
    await Lesson.add_video.set()


@dp.message_handler(state=Lesson.add_video, content_types=['video', 'audio', 'voice', 'photo', 'document', 'text'])
async def add_lesson(message: types.Message, state: FSMContext):
    if message.video:

        await state.update_data(
            {
                "file_id": message.video.file_id,
                "file_unique_id": message.video.file_unique_id
            }
        )
        await message.answer("Qo'shimcha Text kiritasizmi")
        await Lesson.add_video_text.set()
    else:
        await message.answer('🚫 Xato\n\n'
                             'Bu video emas')


@dp.message_handler(state=Lesson.add_video_text)
async def add_lesson(message: types.Message, state: FSMContext):
    data = await state.get_data()

    file = data.get('file_id')
    file_unique_id = data.get('file_unique_id')
    if message.text != "Shart emas":
        await bot.send_video(chat_id=message.from_user.id, video=file, caption=f'{message.text}')
        await message.answer(f"Biror muammo bo'lsa o'chirish uchun mahsus code - {file_unique_id}")

    elif message.text == "Shart emas":
        await message.answer('-')
    else:
        await message.answer('🚫 Xato\n\n'
                             'Bu text emas')


@dp.message_handler(text='Audio Yuklash')
async def lesson(message: types.Message):
    await message.answer('Faqat Audio Yuboring')
    await Lesson.add_audio.set()


@dp.message_handler(state=Lesson.add_audio, content_types=['video', 'audio', 'voice', 'photo', 'document', 'text'])
async def add_lesson(message: types.Message, state: FSMContext):
    if message.audio:
        print(message.audio)
        await state.update_data(
            {
                "file_id": message.audio.file_id,
                "file_unique_id": message.audio.file_unique_id
            }
        )

        await message.answer("Qo'shimcha Text kiritasizmi")
        await Lesson.add_audio_text.set()

    else:
        await message.answer('🚫 Xato\n\n'
                             'Bu audio emas')


@dp.message_handler(state=Lesson.add_audio_text)
async def add_lesson(message: types.Message, state: FSMContext):
    data = await state.get_data()

    file = data.get('file_id')
    file_unique_id = data.get('file_unique_id')
    if message.text != "Shart emas":
        await message.answer_audio(audio=file, caption=f'{message.text}')
        await message.answer(f"Biror muammo bo'lsa o'chirish uchun mahsus code - {file_unique_id}")

    elif message.text == "Shart emas":
        await message.answer('-')
    else:
        await message.answer('🚫 Xato\n\n'
                             'Bu text emas')


@dp.message_handler(text='Rasm Yuklash')
async def lesson(message: types.Message):
    await message.answer('Faqat Rasm Yuboring')
    await Lesson.add_image.set()


@dp.message_handler(state=Lesson.add_image, content_types=['video', 'audio', 'voice', 'photo', 'document', 'text'])
async def add_image(message: types.Message, state: FSMContext):
    if message.photo:
        print(message.photo)
        await state.update_data(
            {
                "file_id": message.photo[-1].file_id,
                "file_unique_id": message.photo[-1].file_unique_id
            }
        )

        await message.answer("Qo'shimcha Text kiritasizmi")
        await Lesson.add_image_text.set()
    else:
        await message.answer('🚫 Xato\n\n'
                             'Bu rasm emas')


@dp.message_handler(state=Lesson.add_image_text)
async def add_lesson(message: types.Message, state: FSMContext):
    data = await state.get_data()

    file = data.get('file_id')
    file_unique_id = data.get('file_unique_id')
    if message.text != "Shart emas":
        await message.answer_photo(photo=file, caption=f'{message.text}')
        await message.answer(f"Biror muammo bo'lsa o'chirish uchun mahsus code - {file_unique_id}")
    elif message.text == "Shart emas":
        await message.answer('-')
    else:
        await message.answer('🚫 Xato\n\n'
                             'Bu text emas')
