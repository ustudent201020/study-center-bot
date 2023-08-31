from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from handlers.sos_all.admin_functions import admin_answer_yes_text, admin_answer_yes_audio, admin_answer_yes_document, \
    admin_answer_yes_photo, admin_answer_yes_video, admin_answer_yes_voice
from handlers.sos_man.mb_bosh_oyna import user_id_dict, man_dict_one
from handlers.sos_man.mz_buttons import button_one
from handlers.sos_man.mz_functions import all_send_man, admin_check_delete
from keyboards.inline.sos_inline_keyboards import admin_yes_no, user_check_ikeys, answer_questions_two
from loader import dp, sdb
from states.sos_states import ManAdmin

mc_one = {}
man_state_dict = {}


@dp.message_handler(content_types=['text', 'photo', 'video', 'audio', 'voice', 'document'],
                    state=ManAdmin.admin_one)
async def admin_answer_one(msg: Message, state: FSMContext):
    if msg.content_type == 'text':
        mc_one['admin_answer_text'] = msg.text
    elif msg.content_type == 'photo':
        mc_one['photo_id'] = msg.photo[-1].file_id
        mc_one['photo_caption'] = msg.caption
    elif msg.content_type == 'video':
        mc_one['video_id'] = msg.video.file_id
        mc_one['video_caption'] = msg.caption
    elif msg.content_type == 'audio':
        mc_one['audio_id'] = msg.audio.file_id
        mc_one['audio_caption'] = msg.caption
    elif msg.content_type == 'voice':
        mc_one['voice_id'] = msg.voice.file_id
        mc_one['voice_caption'] = msg.caption
    elif msg.content_type == 'document':
        mc_one['document_id'] = msg.document.file_id
        mc_one['document_caption'] = msg.caption

    await msg.answer('Жавобингиз қабул қилинди! Саволни базада қолдирасизми ёки ўчирасизми?',
                     reply_markup=admin_yes_no)
    await ManAdmin.admin_two.set()


@dp.callback_query_handler(state=ManAdmin.admin_two)
async def admin_answer_fcheck(call: CallbackQuery, state: FSMContext):
    user_id = user_id_dict['user_id']
    all_questions = await sdb.select_all_man()
    audio_db = await sdb.select_man_audio(user_id=user_id, turi='audio')
    document_db = await sdb.select_man_document(user_id=user_id, turi='document')
    photo_db = await sdb.select_man_photo(user_id=user_id, turi='photo')
    text_db = await sdb.select_man_text(user_id=user_id, turi='text')
    video_db = await sdb.select_man_video(user_id=user_id, turi='video')
    voice_db = await sdb.select_man_voice(user_id=user_id, turi='voice')

    if call.data == 'admin_yes':
        for n in mc_one.keys():
            if n == 'admin_answer_text':
                await admin_answer_yes_text(user_id=user_id, admin_javobi=mc_one[n],
                                            user_savoli=man_dict_one)
                await all_send_man(call=call, markup=await answer_questions_two(), audio_db=audio_db,
                                   document_db=document_db, photo_db=photo_db, text_db=text_db, video_db=video_db,
                                   voice_db=voice_db)
            elif n == 'audio_id':
                await admin_answer_yes_audio(user_id=user_id, admin_javobi=mc_one, user_savoli=man_dict_one)
                await all_send_man(call=call, markup=await answer_questions_two(), audio_db=audio_db,
                                   document_db=document_db, photo_db=photo_db, text_db=text_db, video_db=video_db,
                                   voice_db=voice_db)
            elif n == 'document_id':
                await admin_answer_yes_document(user_id=user_id, admin_javobi=mc_one,
                                                user_savoli=man_dict_one)
                await all_send_man(call=call, markup=await answer_questions_two(), audio_db=audio_db,
                                   document_db=document_db, photo_db=photo_db, text_db=text_db, video_db=video_db,
                                   voice_db=voice_db)
            elif n == 'photo_id':
                await admin_answer_yes_photo(user_id=user_id, admin_javobi=mc_one, user_savoli=man_dict_one)
                await all_send_man(call=call, markup=await answer_questions_two(), audio_db=audio_db,
                                   document_db=document_db, photo_db=photo_db, text_db=text_db, video_db=video_db,
                                   voice_db=voice_db)
            elif n == 'video_id':
                await admin_answer_yes_video(user_id=user_id, admin_javobi=mc_one, user_savoli=man_dict_one)
                await all_send_man(call=call, markup=await answer_questions_two(), audio_db=audio_db,
                                   document_db=document_db, photo_db=photo_db, text_db=text_db, video_db=video_db,
                                   voice_db=voice_db)
            elif n == 'voice_id':
                await admin_answer_yes_voice(user_id=user_id, admin_javobi=mc_one, user_savoli=man_dict_one)
                await all_send_man(call=call, markup=await answer_questions_two(), audio_db=audio_db,
                                   document_db=document_db, photo_db=photo_db, text_db=text_db, video_db=video_db,
                                   voice_db=voice_db)
        mc_one.clear()
        man_dict_one.clear()
        await ManAdmin.SOS_two.set()

    elif call.data == 'admin_check_delete':
        for n in man_dict_one.keys():
            if n == 'audio_admin_unique':
                for i in mc_one.keys():
                    if i == 'audio_id':
                        await admin_answer_yes_audio(user_id=user_id, admin_javobi=mc_one,
                                                     user_savoli=man_dict_one)
                    elif i == 'document_id':
                        await admin_answer_yes_document(user_id=user_id, admin_javobi=mc_one,
                                                        user_savoli=man_dict_one)
                    elif i == 'photo_id':
                        await admin_answer_yes_photo(user_id=user_id, admin_javobi=mc_one,
                                                     user_savoli=man_dict_one)
                    elif i == 'admin_answer_text':
                        await admin_answer_yes_text(user_id=user_id, admin_javobi=mc_one[i],
                                                    user_savoli=man_dict_one)
                    elif i == 'video_id':
                        await admin_answer_yes_video(user_id=user_id, admin_javobi=mc_one,
                                                     user_savoli=man_dict_one)
                    elif i == 'voice_id':
                        await admin_answer_yes_voice(user_id=user_id, admin_javobi=mc_one,
                                                     user_savoli=man_dict_one)
                await admin_check_delete(answer=man_dict_one['audio_admin_unique'], type_db=audio_db, boshqa=True)

            elif n == 'document_admin_unique':
                for i in mc_one.keys():
                    if i == 'audio_id':
                        await admin_answer_yes_audio(user_id=user_id, admin_javobi=mc_one,
                                                     user_savoli=man_dict_one)
                    elif i == 'document_id':
                        await admin_answer_yes_document(user_id=user_id, admin_javobi=mc_one,
                                                        user_savoli=man_dict_one)
                    elif i == 'photo_id':
                        await admin_answer_yes_photo(user_id=user_id, admin_javobi=mc_one,
                                                     user_savoli=man_dict_one)
                    elif i == 'admin_answer_text':
                        await admin_answer_yes_text(user_id=user_id, admin_javobi=mc_one[i],
                                                    user_savoli=man_dict_one)
                    elif i == 'video_id':
                        await admin_answer_yes_video(user_id=user_id, admin_javobi=mc_one,
                                                     user_savoli=man_dict_one)
                    elif i == 'voice_id':
                        await admin_answer_yes_voice(user_id=user_id, admin_javobi=mc_one,
                                                     user_savoli=man_dict_one)
                await admin_check_delete(answer=man_dict_one['document_admin_unique'], type_db=document_db,
                                         boshqa=True)

            elif n == 'photo_admin_unique':
                for i in mc_one.keys():
                    if i == 'audio_id':
                        await admin_answer_yes_audio(user_id=user_id, admin_javobi=mc_one,
                                                     user_savoli=man_dict_one)
                    elif i == 'document_id':
                        await admin_answer_yes_document(user_id=user_id, admin_javobi=mc_one,
                                                        user_savoli=man_dict_one)
                    elif i == 'photo_id':
                        await admin_answer_yes_photo(user_id=user_id, admin_javobi=mc_one,
                                                     user_savoli=man_dict_one)
                    elif i == 'admin_answer_text':
                        await admin_answer_yes_text(user_id=user_id, admin_javobi=mc_one[i],
                                                    user_savoli=man_dict_one)
                    elif i == 'video_id':
                        await admin_answer_yes_video(user_id=user_id, admin_javobi=mc_one,
                                                     user_savoli=man_dict_one)
                    elif i == 'voice_id':
                        await admin_answer_yes_voice(user_id=user_id, admin_javobi=mc_one,
                                                     user_savoli=man_dict_one)
                await admin_check_delete(answer=man_dict_one['photo_admin_unique'], type_db=document_db, boshqa=True)

            elif n == 'text_adm_ans':
                for i in mc_one.keys():
                    if i == 'audio_id':
                        await admin_answer_yes_audio(user_id=user_id, admin_javobi=mc_one,
                                                     user_savoli=man_dict_one)
                    elif i == 'document_id':
                        await admin_answer_yes_document(user_id=user_id, admin_javobi=mc_one,
                                                        user_savoli=man_dict_one)
                    elif i == 'photo_id':
                        await admin_answer_yes_photo(user_id=user_id, admin_javobi=mc_one,
                                                     user_savoli=man_dict_one)
                    elif i == 'admin_answer_text':
                        await admin_answer_yes_text(user_id=user_id, admin_javobi=mc_one[i],
                                                    user_savoli=man_dict_one)
                    elif i == 'video_id':
                        await admin_answer_yes_video(user_id=user_id, admin_javobi=mc_one,
                                                     user_savoli=man_dict_one)
                    elif i == 'voice_id':
                        await admin_answer_yes_voice(user_id=user_id, admin_javobi=mc_one,
                                                     user_savoli=man_dict_one)
                await admin_check_delete(answer=man_dict_one['text_adm_ans'], type_db=text_db, text=True)

            elif n == 'video_admin_unique':
                for i in mc_one.keys():
                    if i == 'audio_id':
                        await admin_answer_yes_audio(user_id=user_id, admin_javobi=mc_one,
                                                     user_savoli=man_dict_one)
                    elif i == 'document_id':
                        await admin_answer_yes_document(user_id=user_id, admin_javobi=mc_one,
                                                        user_savoli=man_dict_one)
                    elif i == 'photo_id':
                        await admin_answer_yes_photo(user_id=user_id, admin_javobi=mc_one,
                                                     user_savoli=man_dict_one)
                    elif i == 'admin_answer_text':
                        await admin_answer_yes_text(user_id=user_id, admin_javobi=mc_one[i],
                                                    user_savoli=man_dict_one)
                    elif i == 'video_id':
                        await admin_answer_yes_video(user_id=user_id, admin_javobi=mc_one,
                                                     user_savoli=man_dict_one)
                    elif i == 'voice_id':
                        await admin_answer_yes_voice(user_id=user_id, admin_javobi=mc_one,
                                                     user_savoli=man_dict_one)
                await admin_check_delete(answer=man_dict_one['video_admin_unique'], type_db=video_db, boshqa=True)

            elif n == 'voice_admin_unique':
                for i in mc_one.keys():
                    if i == 'audio_id':
                        await admin_answer_yes_audio(user_id=user_id, admin_javobi=mc_one,
                                                     user_savoli=man_dict_one)
                    elif i == 'document_id':
                        await admin_answer_yes_document(user_id=user_id, admin_javobi=mc_one,
                                                        user_savoli=man_dict_one)
                    elif i == 'photo_id':
                        await admin_answer_yes_photo(user_id=user_id, admin_javobi=mc_one,
                                                     user_savoli=man_dict_one)
                    elif i == 'admin_answer_text':
                        await admin_answer_yes_text(user_id=user_id, admin_javobi=mc_one[i],
                                                    user_savoli=man_dict_one)
                    elif i == 'video_id':
                        await admin_answer_yes_video(user_id=user_id, admin_javobi=mc_one,
                                                     user_savoli=man_dict_one)
                    elif i == 'voice_id':
                        await admin_answer_yes_voice(user_id=user_id, admin_javobi=mc_one,
                                                     user_savoli=man_dict_one)
                await admin_check_delete(answer=man_dict_one['voice_admin_unique'], type_db=voice_db, boshqa=True)

        if len(all_questions) == 1:
            await call.message.answer('Базада саволлар мавжуд эмас!')
            await state.finish()
        else:
            user_questions = await sdb.select_all_manuser(user_id=user_id)
            if len(user_questions) > 0:
                await call.message.answer('Фойдаланувчи саволлари бўлимига қайтасизми?',
                                          reply_markup=user_check_ikeys)
                await ManAdmin.admin_delone.set()
            else:
                await call.message.answer('❓ Саволлар бўлими', reply_markup=await button_one())
                await ManAdmin.SOS_one.set()
        man_state_dict.clear()
        mc_one.clear()
        man_dict_one.clear()

    elif call.data == 'admin_no_again':
        await all_send_man(call=call, markup=await answer_questions_two(), audio_db=audio_db, document_db=document_db,
                           photo_db=photo_db, text_db=text_db, video_db=video_db, voice_db=voice_db)
        await ManAdmin.SOS_two.set()


@dp.callback_query_handler(state=ManAdmin.admin_delone)
async def admin_check_delete_one(call: CallbackQuery):
    user_id = user_id_dict['user_id']
    audio_db = await sdb.select_man_audio(user_id=user_id, turi='audio')
    document_db = await sdb.select_man_document(user_id=user_id, turi='document')
    photo_db = await sdb.select_man_photo(user_id=user_id, turi='photo')
    text_db = await sdb.select_man_text(user_id=user_id, turi='text')
    video_db = await sdb.select_man_video(user_id=user_id, turi='video')
    voice_db = await sdb.select_man_voice(user_id=user_id, turi='voice')

    if call.data == 'user_check_yes':
        await all_send_man(call=call, markup=await answer_questions_two(), audio_db=audio_db, document_db=document_db,
                           photo_db=photo_db, text_db=text_db, video_db=video_db, voice_db=voice_db)
        await ManAdmin.SOS_two.set()
    elif call.data == 'user_check_no':
        await call.message.answer('❓ Саволлар бўлими', reply_markup=await button_one())
        await ManAdmin.SOS_one.set()
