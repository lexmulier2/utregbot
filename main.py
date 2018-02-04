from telegram.ext import Updater, CommandHandler

TOKEN = '520822004:AAFKK9EozBuM-GUHuxhxSV9v5FdLFq-D35E'


def next_game(bot, update):
    update.message.reply_text('Hi!')


def uuu(bot, update):
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text='UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU')


def main():

    game = current_game()
    # updater = Updater(TOKEN)
    # dp = updater.dispatcher
    # dp.add_handler(CommandHandler('nextgame', next_game))
    # dp.add_handler(CommandHandler('uuu', uuu))
    #
    # updater.start_polling()
    #
    # updater.idle()
    #

