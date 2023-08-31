import logging
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from typing import List

from data.config import MAN_GROUP
from keyboards.default.rekKeyboards import main_menu
from keyboards.inline.sos_inline_keyboards import user_yes_no, user_check_ikeys

from loader import dp, sdb, bot
from states.sos_states import Man_Woman_State, Man_State


async def first_check_man(call, user_id, text_id=None, any_id=None, m_id=False, unique=False):
    try:
        if call.data == 'user_yes':
            man_questions = await sdb.select_all_manuser(user_id=user_id)
            if len(man_questions) < 15:
                await bot.send_message(chat_id=MAN_GROUP,
                                       text='Yangi xat keldi!!! Ko"rish uchun /man_questions '
                                            'buyrug"ini yuboring')
                await call.message.answer('Xat yuborildi! Yana yuborasizmi?',
                                          reply_markup=user_check_ikeys)
                await Man_State.user_checkone.set()
            else:
                await call.message.answer(text='Kechirasiz 5tagacha xat yozolasiz!!!\n\n'
                                               'Admin Tasdiqlagach yana yozishingiz mumkin')

        elif call.data == 'user_no_again':
            if m_id:
                await sdb.delete_man_id(m_id=text_id)
            elif unique:
                await sdb.delete_man_unique(unique_id=any_id)
            await call.message.answer('<b><i>Xabaringizni qayta yuborishingiz mumin!</i></b>')
            await Man_Woman_State.man_one.set()
        await call.message.delete()
    except Exception as err:
        logging.error(err)


async def second_check_man(call, state):
    if call.data == 'user_check_yes':
        await call.message.answer('Xabaringizni kiriting:')
        await Man_Woman_State.man_one.set()
    elif call.data == 'user_check_no':
        await call.message.answer('Bosh menu', reply_markup=main_menu)
        await state.finish()
    await call.message.delete()


@dp.message_handler(text="Motivatsion Xat yuborish ✍️", state='*')
async def sos_func(msg: Message):
    javob = 'Motivatsion xatni yuboring'
    await msg.answer(javob, disable_web_page_preview=True)
    await Man_Woman_State.man_one.set()


@dp.message_handler(is_media_group=True, content_types=['video', 'photo', 'document', 'voice'],
                    state=Man_Woman_State.man_one)
async def mediagr(msg: Message, album: List[Message], state: FSMContext):
    await msg.answer('Илтимос, фақат керакли файлни ўзини юборинг! Бир нечта жамланган файлларни қабул қила олмаймиз!')
    await state.finish()


@dp.message_handler(state=Man_Woman_State.man_one, content_types=['audio', 'document', 'photo', 'text', 'video',
                                                                  'voice'])
async def man_bir(msg: Message, state: FSMContext):
    fullname = msg.from_user.full_name
    user_id = int(msg.from_user.id)
    await state.update_data({'user_id': user_id})
    m_one = '<b><i>Xabaringiz qabul qilindi! Tasdiqlaysizmi jo"natilsinmi?</i></b>'
    try:
        if msg.content_type == 'audio':
            await msg.answer_audio(audio=msg.audio.file_id, caption=msg.caption)
            await sdb.add_man_audio(fullname=fullname, user_id=user_id, audio_id=msg.audio.file_id,
                                    unique_id=msg.audio.file_unique_id, caption=msg.caption, turi='audio')
            user_audio = await sdb.select_man_audio(user_id=user_id, turi='audio')
            for n in user_audio:
                if n[1] == msg.audio.file_unique_id:
                    await state.update_data({'audio_unique': n[1]})
            await Man_State.man_audio.set()
            await msg.answer(m_one, reply_markup=user_yes_no)

        elif msg.content_type == 'document':
            await msg.answer_document(document=msg.document.file_id, caption=msg.caption)
            await sdb.add_man_document(fullname=fullname, user_id=user_id, document_id=msg.document.file_id,
                                       unique_id=msg.document.file_unique_id, caption=msg.caption, turi='document')
            user_document = await sdb.select_man_document(user_id=user_id, turi='document')
            for n in user_document:
                if n[1] == msg.document.file_unique_id:
                    await state.update_data({'document_unique': n[1]})
            await Man_State.man_document.set()
            await msg.answer(m_one, reply_markup=user_yes_no)

        elif msg.content_type == 'photo':
            await msg.answer_photo(photo=msg.photo[-1].file_id, caption=msg.caption)
            await sdb.add_man_photo(fullname=fullname, user_id=user_id, photo_id=msg.photo[-1].file_id,
                                    unique_id=msg.photo[-1].file_unique_id, caption=msg.caption, turi='photo')
            user_photo = await sdb.select_man_photo(user_id=user_id, turi='photo')
            for n in user_photo:
                if n[1] == msg.photo[-1].file_unique_id:
                    await state.update_data({'photo_unique': n[1]})
            await Man_State.man_photo.set()
            await msg.answer(m_one, reply_markup=user_yes_no)

        elif msg.content_type == 'text':
            await msg.answer(msg.text)
            await sdb.add_man_text(fullname=fullname, user_id=msg.from_user.id, text=msg.text, turi='text')
            user_text = await sdb.select_man_text(user_id=user_id, turi='text')
            for n in user_text:
                if n[1] == msg.text:
                    await state.update_data({'question_id': n[0]})
            await Man_State.man_text.set()
            await msg.answer(m_one, reply_markup=user_yes_no)

        elif msg.content_type == 'video':
            await msg.answer_video(video=msg.video.file_id, caption=msg.caption)
            await sdb.add_man_video(fullname=fullname, user_id=user_id, video_id=msg.video.file_id,
                                    unique_id=msg.video.file_unique_id, caption=msg.caption, turi='video')
            user_video = await sdb.select_man_video(user_id=user_id, turi='video')
            for n in user_video:
                if n[1] == msg.video.file_unique_id:
                    await state.update_data({'video_unique': n[1]})
            await Man_State.man_video.set()
            await msg.answer(m_one, reply_markup=user_yes_no)

        elif msg.content_type == 'voice':
            await msg.answer_voice(voice=msg.voice.file_id, caption=msg.caption)
            await sdb.add_man_voice(fullname=fullname, user_id=user_id, voice_id=msg.voice.file_id,
                                    unique_id=msg.voice.file_unique_id, caption=msg.caption, turi='voice')
            user_voice = await sdb.select_man_voice(user_id=user_id, turi='voice')
            for n in user_voice:
                if n[1] == msg.voice.file_unique_id:
                    await state.update_data({'voice_unique': n[1]})
            await Man_State.man_voice.set()
            await msg.answer(m_one, reply_markup=user_yes_no)
        elif msg.content_type:
            await msg.answer('Фақат аудио/видео/матн/расм/овозли ва ҳужжат шаклидаги саволлар қабул қилинади!!!')
        await msg.delete()
    except Exception as err:
        logging.error(err)
        await msg.answer('Бир марта ботга старт буйруғини киритиб хабарингизни қайта киритинг')


@dp.callback_query_handler(state=Man_State.man_audio)
async def stateaudio_func(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    unique = data['audio_unique']
    await first_check_man(call=call, user_id=data['user_id'], any_id=unique, unique=True)


@dp.callback_query_handler(state=Man_State.man_document)
async def statedocumentid_func(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    unique = data['document_unique']
    await first_check_man(call=call, user_id=data['user_id'], any_id=unique, unique=True)


@dp.callback_query_handler(state=Man_State.man_photo)
async def statephotoid_func(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    unique = data['photo_unique']
    await first_check_man(call=call, user_id=data['user_id'], any_id=unique, unique=True)


@dp.callback_query_handler(state=Man_State.man_text)
async def statesos2_func(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text = data['question_id']
    await first_check_man(call=call, user_id=data['user_id'], text_id=int(text), m_id=True)


@dp.callback_query_handler(state=Man_State.man_video)
async def statevideoid_func(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    unique = data['video_unique']
    await first_check_man(call=call, user_id=data['user_id'], any_id=unique, unique=True)


@dp.callback_query_handler(state=Man_State.man_voice)
async def statevoiceid_func(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    unique = data['voice_unique']
    await first_check_man(call=call, user_id=data['user_id'], any_id=unique, unique=True)


@dp.callback_query_handler(state=Man_State.user_checkone)
async def check_ikeys_func(call: CallbackQuery, state: FSMContext):
    await second_check_man(call=call, state=state)
