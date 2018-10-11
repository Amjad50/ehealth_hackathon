from functools import wraps

from telegram.ext import CommandHandler, CallbackQueryHandler, MessageHandler, Filters, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from util import only_active, change_state

ADMIN_IDS = [28737678]

USER_NAME, USER_ID = range(2)


def restricted(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        chat_id = update.effective_chat.id

        if chat_id not in ADMIN_IDS:
            # update.message.reply_text('You have no permission to run this command')
            return

        return func(bot, update)

    return wrapped


def label_to_inlinekKeyboardBtn(labels):
    return [InlineKeyboardButton(label, callback_data=label) for label in labels]


@restricted
def c_admin_setting(bot, update):
    chat_id = update.effective_chat.id
    message_id = update.message.message_id
    print(chat_id, message_id)

    reply_markup = InlineKeyboardMarkup([
        label_to_inlinekKeyboardBtn(['ON', 'OFF'])
    ])

    update.message.reply_text('Please choose:', reply_markup=reply_markup)


@restricted
def callback_handler(bot, update):
    query = update.callback_query

    if query.data == 'ON':
        change_state(True)
    else:
        change_state(False)

    bot.edit_message_text(text="Done".format(query.data),
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)


def init(dispatcher):
    # admin commands
    dispatcher.add_handler(CommandHandler('setting', c_admin_setting))
    dispatcher.add_handler(CallbackQueryHandler(callback_handler))


def send_to_admin(bot, msg):
    bot.send_message(ADMIN_IDS[0], msg)