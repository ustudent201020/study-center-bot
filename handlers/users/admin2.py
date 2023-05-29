import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from data.config import ADMINS
from keyboards.default.all import menu
from keyboards.default.rekKeyboards import admin_key, darslar_key, main_menu
from keyboards.default.rekKeyboards import back
from loader import dp, db, bot
from states.rekStates import RekData, AllState, Lesson, ShowLessons
from utils.misc import subscription

admins = [935795577]


@dp.message_handler(text='Admin ➕')
async def add_channel(message: types.Message):
    global admins
    if message.from_user.id in admins:
        await message.answer('Id ni kiriting')
        await AllState.env.set()


@dp.message_handler(text='- Go School')
async def go_school(message: types.Message):
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
        buttons = await db.select_buttons()
        but = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, )
        but.add(*(KeyboardButton(text=str(button[1])) for button in buttons))
        but.add(KeyboardButton(text='🔝 Bosh menu'))

        await message.answer("Hozir <b>-Go School</b> bo'limidasiz",
                             reply_markup=but, disable_web_page_preview=True)
        await ShowLessons.show.set()
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


@dp.message_handler(state=ShowLessons.show)
async def show_lessons(message: types.Message, state: FSMContext):
    print('ishladi')
    global admins
    buttons = await db.select_buttons()
    all_buttons_list = []
    for button in buttons:
        all_buttons_list.append(button[1])

    if message.text in all_buttons_list:
        lessonss = await db.select_lesson_by_button_name(button_name=message.text)
        for i in lessonss:

            if message.from_user.id in admins:
                if i[2] == 'video':
                    await message.answer_video(
                        video=f"{i[3]}",
                        caption=f'{i[5]}\n\n'
                                f'🗑 o`chirish uchun mahsus code - {i[4]}'
                                f' (faqat adminlarga ko`rinadi)'
                    )
                elif i[2] == 'audio':
                    await message.answer_audio(
                        audio=f"{i[3]}",
                        caption=f'{i[5]}\n\n'
                                f'🗑 o`chirish uchun mahsus code - {i[4]}'
                                f' (faqat adminlarga ko`rinadi)'
                    )
                elif i[2] == 'photo':
                    await message.answer_photo(
                        photo=f"{i[3]}",
                        caption=f'{i[5]}\n\n'
                                f'🗑 o`chirish uchun mahsus code - {i[4]}'
                                f' (faqat adminlarga ko`rinadi)'
                    )
            else:
                if i[2] == 'video':
                    await message.answer_video(video=f"{i[3]}", caption=f'{i[5]}')
                elif i[2] == 'audio':
                    await message.answer_audio(audio=f"{i[3]}", caption=f'{i[5]}')
                elif i[2] == 'photo':
                    await message.answer_photo(photo=f"{i[3]}", caption=f'{i[5]}')

    elif message.text == '🔝 Bosh menu':
        await message.answer('Bosh Menu',reply_markup=main_menu)
        await state.finish()
    else:
        await message.answer("Ko'rsatilgan bo'limlardan birini tanlang ")


@dp.message_handler(state=AllState.env)
async def env_change(message: types.Message, state: FSMContext):
    global admins
    try:
        # key = 'ADMINS'
        input_value = int(message.text)
        # dotenvfile = dotenv.find_dotenv()
        # dotenv.load_dotenv(dotenvfile)
        # old = dotenv.get_key(dotenv_path=dotenvfile, key_to_get='ADMINS')
        # value = f"{old},{input_value}"
        # os.environ[key] = value
        # dotenv.set_key(
        #     dotenvfile,
        #     key,
        #     os.environ[key]
        # )
        admins.append(int(message.text))
        # new = dotenv.get_key(dotenv_path=dotenvfile, key_to_get='ADMINS')
        await message.answer(f"Qo'shildi\n\n"
                             f"Hozirgi adminlar-{admins}", reply_markup=darslar_key)
        await state.finish()
    except ValueError:
        await message.answer('Faqat son qabul qilinadi\n\n'
                             'Qaytadan kiriting')


@dp.message_handler(text='add')
async def add_channel(message: types.Message):
    global admins
    await message.answer(f'{admins}')


@dp.message_handler(text='Admin ➖')
async def add_channel(message: types.Message):
    global admins
    if message.from_user.id in admins:
        await message.answer('Id ni kiriting')
        await AllState.env_remove.set()


@dp.message_handler(state=AllState.env_remove)
async def env_change(message: types.Message, state: FSMContext):
    try:
        test = int(message.text)
        global admins
        # key = 'ADMINS'
        # dotenvfile = dotenv.find_dotenv()
        # dotenv.load_dotenv(dotenvfile)
        # old = dotenv.get_key(dotenv_path=dotenvfile, key_to_get='ADMINS')
        if test in admins:
            # a = ''
            # if f",{message.text}" in old:
            #     a += old.replace(f",{message.text}", '')
            # os.environ[key] = a
            # dotenv.set_key(
            #     dotenvfile,
            #     key,
            #     os.environ[key]
            # )
            admins.remove(test)
            # new = dotenv.get_key(dotenv_path=dotenvfile, key_to_get='ADMINS')
            await message.answer(f'O"chirildi\n\n'
                                 f'Hozirgi adminlar {admins}', reply_markup=darslar_key)
            await state.finish()
        else:
            await message.answer('Bunday admin mavjud emas\n\n'
                                 'Faqat admin id sini qabul qilamiz', reply_markup=darslar_key)
    except Exception as err:
        await message.answer(f'{err}')
        await message.answer('Faqat son qabul qilinadi\n\n'
                             'Qaytadan kiriting')


@dp.message_handler(text='Barcha Adminlar')
async def add_channel(message: types.Message):
    # dotenvfile = dotenv.find_dotenv()
    #
    # old = dotenv.get_key(dotenv_path=dotenvfile, key_to_get='ADMINS')
    global admins
    await message.answer(f'Adminlar - {admins}', reply_markup=darslar_key)


@dp.message_handler(commands=['admin'])
async def admin(message: types.Message):
    global admins
    if message.from_user.id in admins:
        await message.answer(text='Admin panel',
                             reply_markup=admin_key)


@dp.message_handler(commands=['darslar'])
async def admin(message: types.Message):
    global admins
    if message.from_user.id in admins:
        await message.answer(text='Admin panel',
                             reply_markup=darslar_key)


@dp.message_handler(text='Kanal ➕')
async def add_channel(message: types.Message):
    await message.answer(text='Kanalni kiriting\n\n'
                              'Masalan : "@Chanel zayavkada bo`lsa chanel_id(-123123213),chanel_url"\n\n',
                         reply_markup=back)
    await RekData.add.set()


@dp.message_handler(state=RekData.add)
async def add_username(message: types.Message, state: FSMContext):
    text = message.text
    if text[0] == '@':
        text_split = text.split(',')

        await db.add_chanell(chanelll=f"{text_split[0]}",
                             channel_name=f"{text_split[1]}", url=f"{text_split[0][1:]}")
        await message.answer("Qo'shildi", reply_markup=admin_key)
        await state.finish()
    elif text == '🔙️ Orqaga':
        await message.answer('Admin panel', reply_markup=admin_key)
        await state.finish()
    elif text[0] == '-':
        split_chanel = message.text.split(',')
        chanel_lst = []
        url_lst = []
        channel_name_lst = []
        for i in split_chanel:
            lst = i.split('and')
            chanel_lst.append(lst[0])
            url_lst.append(lst[1])
            channel_name_lst.append(lst[2])
        chanel = f'{chanel_lst}'
        url = f'{url_lst}'
        channel_name = f'{url_lst}'
        ch_text = chanel.replace("'", '')
        ch_text2 = ch_text.replace(" ", '')
        u_text = url.replace("'", '')
        u_text2 = u_text.replace(" ", '')
        channel_name_text = channel_name.replace("'", '')
        channel_name_text2 = channel_name_text.replace(" ", '')

        await db.add_chanell(chanelll=ch_text2[1:-1], url=u_text2[1:-1], channel_name=channel_name_text2[1:-1])
        await message.answer("Qo'shildi", reply_markup=admin_key)
        await state.finish()

    else:
        await message.answer('Xato\n\n'
                             '@ belgi bilan yoki kanal id(-11001835334270andLink) sini link bilan birga kiriting kiriting')


@dp.message_handler(text='Kanal ➖')
async def add_channel(message: types.Message):
    await message.answer(text='Kanalni kiriting @ belgi bilan\n\n'
                              'Masalan : "Kanal zayavkada bo`lsa chanel_id(-123123213),chanel_url"\n\n',
                         reply_markup=back)
    await RekData.delete.set()


@dp.message_handler(state=RekData.delete)
async def del_username(message: types.Message, state: FSMContext):
    txt = message.text
    if txt[0] == '-':
        chanel = await db.get_chanel(channel=txt)
        if not chanel:
            await message.answer("Kanal topilmadi\n"
                                 "Qaytadan urinib ko'ring")

        else:
            await db.delete_channel(chanel=txt)
            await message.answer('Kanal o"chirildi', reply_markup=admin_key)
            await state.finish()

        # await message.answer("O'chirildi")
        # await state.finish()
    elif txt[0] == '@':
        chanel = await db.get_chanel(channel=f"{txt}")
        if not chanel:
            await message.answer("Kanal topilmadi\n"
                                 "Qaytadan urinib ko'ring")

        else:
            await db.delete_channel(chanel=txt)
            await message.answer('Kanal o"chirildi', reply_markup=admin_key)
            await state.finish()
    elif txt == '🔙️ Orqaga':
        await message.answer('Admin panel', reply_markup=admin_key)
        await state.finish()


activee = 0
blockk = 0


async def is_activeee():
    users = await db.select_all_users()
    global activee
    global blockk
    activate_test = 0
    blockk_test = 0
    # activee = 0
    # blockk = 0
    for user in users:

        user_id = user[6]
        try:
            await bot.send_chat_action(chat_id=user_id, action='typing')
            activate_test += 1
            await asyncio.sleep(0.034)

        except Exception as err:
            blockk_test += 1
            await asyncio.sleep(0.034)
    activee = activate_test
    blockk = blockk_test


@dp.message_handler(text='ttt')
async def is_activeee(a=None):
    users = await db.select_all_users()
    global activee
    global blockk
    activate_test = 0
    blockk_test = 0
    # activee = 0
    # blockk = 0
    for user in users:
        user_id = user[6]
        try:
            await bot.send_chat_action(chat_id=user_id, action='typing')
            activate_test += 1
            await asyncio.sleep(0.034)

        except Exception as err:
            blockk_test += 1
            await asyncio.sleep(0.034)
    activee = activate_test
    blockk = blockk_test


@dp.message_handler(text='Statistika 📊')
async def show_users(message: types.Message):
    a = await db.count_users()
    global activee
    global blockk

    await message.answer(f'<b>🔵 Jami obunachilar: {a} ta\n\n'
                         f'🟡 Active: {activee}\n'
                         f'⚫️ Block : {blockk}</b>')


@dp.message_handler(text='🏘 Bosh menu')
async def menuu(message: types.Message):
    await message.answer('Bosh menu', reply_markup=menu)


@dp.message_handler(text='Kanallar 📈')
async def channels(message: types.Message):
    channels = await db.select_chanel()
    text = ''
    for channel in channels:
        text += f"{channel['chanelll']}\n"
    try:
        await message.answer(f"{text}", reply_markup=admin_key)
    except:
        await message.answer(f"Kanallar mavjud emas")


@dp.message_handler(text='Hisobni 0 ga tushirish')
async def channels(message: types.Message):
    try:
        await db.update_users_all_score()
        await message.answer(f"Hisoblar 0 ga tushirildi", reply_markup=admin_key)
    except Exception as err:
        await message.answer(f"Muammo yuzaga keldi\n\n{err}")


@dp.message_handler(text='Rasmni almashtirish 🖼', user_id=admins)
async def change_picture(message: types.Message):
    await message.answer('Rasmni kiriting', reply_markup=back)
    await RekData.picture.set()


@dp.message_handler(content_types=['photo', 'text', 'video'], state=RekData.picture)
async def change_picture_(message: types.Message, state: FSMContext):
    if message.photo:
        photo = message.photo[-1].file_id
        elements = await db.get_elements()
        if elements:
            await db.update_photo(photo=photo)
            await message.answer('Yangilandi', reply_markup=admin_key)
            await state.finish()

        else:
            await db.add_photo(photo=photo)
            await message.answer('Qo`shildi', reply_markup=admin_key)
            await state.finish()

    elif message.text == '🔙️ Orqaga':
        await message.answer('Bosh menu', reply_markup=menu)
        await state.finish()
    elif message.text == '/start':
        await message.answer('Bosh menu', reply_markup=menu)
        await state.finish()

    else:
        await message.answer('Faqat rasm qabul qilamiz')


@dp.message_handler(text="O'yin haqida matn 🎮", user_id=admins)
async def change_picture(message: types.Message):
    await message.answer('Textni kiriting', reply_markup=back)
    await RekData.text.set()


@dp.message_handler(state=RekData.text)
async def change_picture_(message: types.Message, state: FSMContext):
    if message.text:
        elements = await db.get_elements()
        if elements:
            await db.update_game_text(game_text=message.text)
            await message.answer('Yangilandi', reply_markup=admin_key)
            await state.finish()
        elif message.text == '/start':
            await message.answer('Bosh menu', reply_markup=menu)
            await state.finish()

        elif message.text == '🔙️ Orqaga':
            await message.answer('Bosh menu', reply_markup=menu)
            await state.finish()

        else:
            await db.add_text(game_text=message.text)
            await message.answer('Qo`shildi', reply_markup=admin_key)
            await state.finish()
    else:
        await message.answer('Faqat Text qabul qilamiz')


@dp.message_handler(text="Sovg'alar ro'yxatini kiritish 📄", user_id=admins)
async def change_picture(message: types.Message):
    await message.answer('Textni kiriting', reply_markup=back)
    await RekData.gift.set()


@dp.message_handler(state=RekData.gift)
async def change_picture_(message: types.Message, state: FSMContext):
    if message.text:
        elements = await db.get_elements()
        if elements:
            await db.update_gift(gift=message.text)
            await message.answer('Yangilandi', reply_markup=admin_key)
            await state.finish()
        elif message.text == '/start':
            await message.answer('Bosh menu', reply_markup=menu)
            await state.finish()

        else:
            await db.add_gift(gift=message.text)
            await message.answer('Qo`shildi', reply_markup=admin_key)
            await state.finish()

    elif message.text == '🔙️ Orqaga':
        await message.answer('Bosh menu', reply_markup=menu)
        await state.finish()
    else:
        await message.answer('Faqat Text qabul qilamiz')


@dp.message_handler(text="Taklif miqdorini kiritish 🎁", user_id=admins)
async def change_picture(message: types.Message):
    await message.answer('Faqat son kiriting', reply_markup=back)
    await RekData.score.set()


@dp.message_handler(state=RekData.score)
async def change_picture_(message: types.Message, state: FSMContext):
    try:
        text = int(message.text)

        if text:
            elements = await db.get_elements()
            if elements:
                await db.update_limit_score(limit_score=text)
                await message.answer('Yangilandi', reply_markup=admin_key)
                await state.finish()
            # else:
            # await db.add_text()
        elif message.text == '/start':
            await message.answer('Bosh menu', reply_markup=menu)
            await state.finish()

        elif message.text == '🔙️ Orqaga':
            await message.answer('Bosh menu', reply_markup=menu)
            await state.finish()
    except:
        if message.text == '/start':
            await message.answer('Bosh menu', reply_markup=menu)
            await state.finish()

        if message.text == '🔙️ Orqaga':
            await message.answer('Bosh menu', reply_markup=menu)
            await state.finish()
        else:
            await message.answer('Faqat Son qabul qilamiz')


@dp.message_handler(text='Shartlarni qo"shish 🖼', user_id=admins)
async def shartlar(message: types.Message):
    await message.answer('Shartlarni kiriting', reply_markup=back)
    await RekData.kbsh.set()


@dp.message_handler(state=RekData.kbsh)
async def shartlarr(message: types.Message, state: FSMContext):
    if message.text:
        elements = await db.get_elements()
        if message.text == '/start':
            await message.answer('Bosh menu', reply_markup=menu)
            await state.finish()

        if elements:
            await db.update_shartlar(shartlar=message.text)
            await message.answer('Yangilandi', reply_markup=admin_key)
            await state.finish()

        else:
            await db.add_shartlar(shartlar=message.text)
            await message.answer('Qo`shildi', reply_markup=admin_key)
            await state.finish()

    elif message.text == '🔙️ Orqaga':
        await message.answer('Bosh menu', reply_markup=menu)
        await state.finish()
    else:
        await message.answer('Faqat text qabul qilamiz')


@dp.message_handler(text="Bugungi balni kiriting")
async def change_picture(message: types.Message):
    await message.answer('Faqat son kiriting', reply_markup=back)
    await RekData.winners.set()


@dp.message_handler(state=RekData.winners)
async def change_picture_(message: types.Message, state: FSMContext):
    try:
        text = int(message.text) + 2
        if message.text == '/start':
            await message.answer('Bosh menu', reply_markup=menu)
            await state.finish()

        if text:
            elements = await db.get_elements()
            if elements:
                await db.winners(winners=text)
                await message.answer('Yangilandi', reply_markup=admin_key)
                await state.finish()

        elif message.text == '🔙️ Orqaga':
            await message.answer('Bosh menu', reply_markup=menu)
            await state.finish()
    except Exception as err:

        if message.text == '🔙️ Orqaga':
            await message.answer('Bosh menu', reply_markup=menu)
            await state.finish()
        elif message.text == '/start':
            await message.answer('Bosh menu', reply_markup=menu)
            await state.finish()

        else:
            await message.answer('Faqat Son qabul qilamiz')


@dp.message_handler(text='Tugma ➕')
async def add_channel(message: types.Message):
    await message.answer(text='Textni kiriting\n\n',
                         reply_markup=back)
    await Lesson.but_add.set()


@dp.message_handler(state=Lesson.but_add)
async def add_username(message: types.Message, state: FSMContext):
    text = message.text
    if text == '🔙️ Orqaga':
        await message.answer('Admin panel', reply_markup=darslar_key)
        await state.finish()
    else:
        await db.add_button(button_name=message.text)
        await message.answer("Qo'shildi", reply_markup=darslar_key)
        await state.finish()


@dp.message_handler(text='Tugma ➖')
async def add_channel(message: types.Message):
    buttons = await db.select_buttons()
    but = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, )
    but.add(*(KeyboardButton(text=str(button[1])) for button in buttons))
    but.add(KeyboardButton(text='🔙️ Orqaga'))
    await message.answer(
        text="Tugmani tanlang\n\n"
             "Tugmaga biriktirilgan barcha ma'lumotlar ham o'chadi\n\nBarchasiga rozimisiz",
        reply_markup=but
    )
    await Lesson.but_del.set()


@dp.message_handler(state=Lesson.but_del)
async def del_button(message: types.Message, state: FSMContext):
    txt = message.text
    buttons = await db.select_buttons()
    all_buttons_list = []
    for button in buttons:
        all_buttons_list.append(button[1])
    if txt == '🔙️ Orqaga':
        await message.answer('Admin panel', reply_markup=darslar_key)
        await state.finish()
    elif message.text in all_buttons_list:
        await db.delete_button_name(button_name=message.text)
        await db.delete_lesson(lesson=message.text)
        await message.answer("O'chirildi", reply_markup=darslar_key)
        await state.finish()
    else:
        await message.answer('Xato\n\nTugmalardan birini tanlang yoki orqaga tugmasini bosing')
