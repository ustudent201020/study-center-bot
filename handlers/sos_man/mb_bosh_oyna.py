import logging

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, AdminFilter
from aiogram.types import CallbackQuery, Message

from data.config import MAN_GROUP
from handlers.sos_all.admin_functions import admin_answer_func
from handlers.sos_man.mz_buttons import button_one
from handlers.sos_man.mz_functions import all_send_man, admin_check_delete, bot_answer_content_type
from keyboards.inline.sos_inline_keyboards import answer_questions_two
from loader import sdb, dp
from states.sos_states import ManAdmin

user_id_dict = {}
add_bot_answer = {}
man_dict_one = {}
man_bot_dict = {}


class CommandMan(Command):

    def __init__(self):
        super().__init__(['man_questions'])


@dp.message_handler(AdminFilter(), commands=['man_questions'], state='*')
async def questions_command_func(msg: Message):
    if msg.chat.id == int(MAN_GROUP):
        try:
            all_users_db = await sdb.select_all_man()
            if len(all_users_db) == 0:
                await msg.answer('Базада саволлар мавжуд эмас!')
            else:
                await msg.answer('❓ Саволлар бўлими', reply_markup=await button_one())
            await msg.delete()
            await ManAdmin.SOS_one.set()
        except Exception as err:
            logging.info(err)


@dp.callback_query_handler(state=ManAdmin.SOS_one)
async def group_ans_two(call: CallbackQuery):
    user_id = int(call.data)
    audio_db = await sdb.select_man_audio(user_id=user_id, turi='audio')
    document_db = await sdb.select_man_document(user_id=user_id, turi='document')
    photo_db = await sdb.select_man_photo(user_id=user_id, turi='photo')
    text_db = await sdb.select_man_text(user_id=user_id, turi='text')
    video_db = await sdb.select_man_video(user_id=user_id, turi='video')
    voice_db = await sdb.select_man_voice(user_id=user_id, turi='voice')
    user_id_dict['user_id'] = user_id

    try:
        await all_send_man(call=call, markup=await answer_questions_two(), audio_db=audio_db, document_db=document_db,
                           photo_db=photo_db, text_db=text_db, video_db=video_db, voice_db=voice_db)
    except Exception as err:
        logging.info(err)
    await ManAdmin.SOS_two.set()


@dp.callback_query_handler(state=ManAdmin.SOS_two)
async def group_ans_three(call: CallbackQuery, state: FSMContext):
    bot_db = await sdb.select_bot_answer(gender='man')
    user_id = user_id_dict['user_id']
    audio_db = await sdb.select_man_audio(user_id=user_id, turi='audio')
    document_db = await sdb.select_man_document(user_id=user_id, turi='document')
    photo_db = await sdb.select_man_photo(user_id=user_id, turi='photo')
    text_db = await sdb.select_man_text(user_id=user_id, turi='text')
    video_db = await sdb.select_man_video(user_id=user_id, turi='video')
    voice_db = await sdb.select_man_voice(user_id=user_id, turi='voice')
    try:
        if call.data == 'bot_answer':
            if len(bot_db) == 0:
                await call.message.answer('Жавоб киритилмаган! Бот жавобини киритинг.\n\nУшбу жавоб <b>ℹ Бот '
                                          'жавоби</b> тугмасини босганингизда фойдаланувчига боради')
                await ManAdmin.bot_addone.set()
            else:
                bot_answer = f'\n\n<b>ℹ Бот жавоби:\n\n{bot_db[0][1]}</b>'
                await bot_answer_content_type(call=call, bot_answer=bot_answer, bot_dict=man_bot_dict)
                await ManAdmin.bot_one.set()
        elif call.data == 'admin_answer':
            await admin_answer_func(call=call, gender_state=man_dict_one)
            await ManAdmin.admin_one.set()
        elif call.data == 'delete_answer':
            if call.message.content_type == 'audio':
                await admin_check_delete(answer=call.message.audio.file_unique_id,
                                         type_db=audio_db, boshqa=True)
            elif call.message.content_type == 'document':
                await admin_check_delete(answer=call.message.document.file_unique_id,
                                         type_db=document_db, boshqa=True)
            elif call.message.content_type == 'photo':
                await admin_check_delete(answer=call.message.photo[-1].file_unique_id,
                                         type_db=photo_db, boshqa=True)
            elif call.message.content_type == 'text':
                await admin_check_delete(answer=call.message.text, type_db=text_db,
                                         text=True)
            elif call.message.content_type == 'video':
                await admin_check_delete(answer=call.message.video.file_unique_id,
                                         type_db=video_db, boshqa=True)
            elif call.message.content_type == 'voice':
                await admin_check_delete(answer=call.message.voice.file_unique_id,
                                         type_db=voice_db, boshqa=True)
            await call.answer(text='Савол базадан ўчирилди!', show_alert=True)

            await call.message.delete()
            all_users_db = await sdb.select_all_man()
            user_questions = await sdb.select_all_manuser(user_id=user_id)
            if len(user_questions) == 0:
                if len(all_users_db) == 0:
                    await call.message.answer('Базада саволлар мавжуд эмас!')
                    await state.finish()
                else:
                    await call.message.answer('❓ Саволлар бўлими', reply_markup=await button_one())
                    await ManAdmin.SOS_one.set()
        elif call.data == 'back_answer_true':
            await call.message.answer('❓ Саволлар бўлими', reply_markup=await button_one())
            await ManAdmin.SOS_one.set()
        elif call.data == 'back_answer_false':
            all_users_db = await sdb.select_all_man()
            if len(all_users_db) == 0:
                await call.message.answer('Базада саволлар мавжуд эмас!')
                await state.finish()
            else:
                await call.message.answer('❓ Саволлар бўлими', reply_markup=await button_one())
                await ManAdmin.SOS_one.set()
    except Exception as err:
        logging.info(err)
