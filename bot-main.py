from functools import wraps
import pickle

from dataset import extra_data
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, CallbackQueryHandler
from private_data import TOKEN
from util import only_active, get_reply_data
import admin
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

REPLY = 1

users = None


@only_active
def c_start(bot, update):
    """ handler for /start command """

    update.message.reply_text('Welcome!\n'
                              'please use:\n'
                              '/question - to answer a question(the question will be requested separately)\n'
                              '/cancel - to stop the bot from waiting for question.')


@only_active
def c_question(bot, update):
    """ handler for /question command
        asks the user to write a question to be answered
        - this method is the one responsible to start the conversation."""

    update.message.reply_text('Please, write down your question.\n'
                              'Questions should be written in clear English.\n'
                              'If you don\'t want to write a question anymore '
                              'please write /cancel to save memory space.')

    # move to the reply state in the conversation
    return REPLY


def get_reply(question):
    respond = get_reply_data(question)


def answer_question(bot, update):
    """ answers the question """

    message = update.message
    logger.info("User %s asked %s.", message.from_user.first_name, message.text)
    reply = get_reply_data(message.text)
    # message.reply_text('the answer for\n%s\nIs:\n%s' % (message.text, reply))
    if reply['state'] == 2:
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton('Yes', callback_data=reply['extra'] + 0),
             InlineKeyboardButton('No', callback_data=reply['extra'] + 1)]
            # [InlineKeyboardButton('Yes', callback_data='qa,'),
            #  InlineKeyboardButton('No', callback_data=0)]
        ])

        message.reply_text(reply['message'], reply_markup=reply_markup)
    else:
        if reply['extra']:
            admin.send_to_admin(bot, '%s is Feeling depression' % (update.effective_user.full_name))
        message.reply_text(reply['message'])

    # end the conversation
    return ConversationHandler.END


def answer_question_2(bot, update):
    query = update.callback_query

    print(query.data)
    bot.edit_message_text(text=extra_data[int(query.data)],
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)


@only_active
def c_cancel(bot, update):
    """ handler for /cancel command
        stops the computer from waiting for a respond message. """
    print(users)
    logger.info("User %s canceled the conversation.", update.message.from_user.first_name)
    update.message.reply_text('OK, no question needed.')

    # end the conversation
    return ConversationHandler.END


def error_handler(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    with open('data.pkl', 'rb') as f:
        global users
        users = pickle.load(f)

    updater = Updater(TOKEN)  # TOKEN is not available in this code. (you need to put your own)

    dispatcher = updater.dispatcher

    # connect command 'start' to c_start function
    dispatcher.add_handler(CommandHandler('start', c_start))
    dispatcher.add_handler(MessageHandler(Filters.text, answer_question))
    dispatcher.add_handler(CallbackQueryHandler(answer_question_2))

    # conversation_handler = ConversationHandler(
    #     entry_points=[CommandHandler('question', c_question)],
    #
    #     states={
    #         REPLY: [MessageHandler(Filters.text, answer_question)]
    #     },
    #
    #     fallbacks=[CommandHandler('cancel', c_cancel)]
    # )
    #
    # dispatcher.add_handler(conversation_handler)

    admin.init(dispatcher)

    dispatcher.add_error_handler(error_handler)

    # start the bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
