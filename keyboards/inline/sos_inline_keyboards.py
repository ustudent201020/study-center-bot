from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import db


async def answer_questions_button(gender):
    user = await db.select_question_id(gender=gender)
    markup = InlineKeyboardMarkup(row_width=3)
    for n in user:
        markup.insert(InlineKeyboardButton(text=f"{n[1]}", callback_data=f"{n[0]}"))
    return markup


async def answer_questions_two(back_button=False):
    markup = InlineKeyboardMarkup(row_width=2)

    markup.insert(InlineKeyboardButton(text='👤 Админ жавоби', callback_data='admin_answer'))
    markup.insert(InlineKeyboardButton(text='❎ Ўчириш!', callback_data='delete_answer'))

    if not back_button:
        markup.insert(InlineKeyboardButton(text='◀ Ортга', callback_data='back_answer_false'))
    else:
        markup.insert(InlineKeyboardButton(text='◀ Ортга', callback_data='back_answer_true'))
    return markup


bot_answer_keyboard = InlineKeyboardMarkup(row_width=2)
bot_answer_keyboard.insert(InlineKeyboardButton(text='♻ Бот жавобини ўзгартириш', callback_data='edit_bot_answer'))
bot_answer_keyboard.add(InlineKeyboardButton(text='◀ Ортга', callback_data='back_bot_answer'))
bot_answer_keyboard.insert(InlineKeyboardButton(text='📤 Юбориш', callback_data='send_answer'))

check_bot_answer = InlineKeyboardMarkup(row_width=2)
check_bot_answer.insert(InlineKeyboardButton(text='💾 Сақлаш', callback_data='check_bot'))
check_bot_answer.insert(InlineKeyboardButton(text='♻ Қайта киритиш', callback_data='again_bot'))
check_bot_answer.add(InlineKeyboardButton(text='◀ Ортга', callback_data='back_check'))

admin_yes_no = InlineKeyboardMarkup(row_width=2)
admin_yes_no.insert(InlineKeyboardButton(text='✅  Қолдириш', callback_data='admin_yes'))
admin_yes_no.insert(InlineKeyboardButton(text='❎  Ўчириш', callback_data='admin_check_delete'))
admin_yes_no.insert(InlineKeyboardButton(text='◀ Ортга', callback_data='admin_no_again'))

user_yes_no = InlineKeyboardMarkup(row_width=2)
user_yes_no.insert(InlineKeyboardButton(text='✅  Тасдиқлаш', callback_data='user_yes'))
user_yes_no.insert(InlineKeyboardButton(text='♻  Қайта киритиш', callback_data='user_no_again'))

user_check_ikeys = InlineKeyboardMarkup(row_width=2)
user_check_ikeys.insert(InlineKeyboardButton(text='✅  Ҳа', callback_data='user_check_yes'))
user_check_ikeys.insert(InlineKeyboardButton(text='♻  Йўқ', callback_data='user_check_no'))
