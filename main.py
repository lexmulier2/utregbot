import datetime

from telegram.ext import Updater, CommandHandler

from game import Game

TOKEN = '520822004:AAFKK9EozBuM-GUHuxhxSV9v5FdLFq-D35E'


class UtregBot(object):
    def __init__(self, chat_id=None):
        self.chat_id = chat_id or '-16383268'
        self.game = None

        self.updater = Updater(TOKEN)
        self.dp = self.updater.dispatcher

        # Jobs handler
        self.jobs = self.updater.job_queue
        self.jobs.run_daily(self.get_game, datetime.time(hour=15, minute=28))
        self.jobs.run_repeating(self.check_score, interval=60)

        self.dp.add_handler(CommandHandler('uuu', self.uuu))

        self.updater.start_polling()

        self.updater.idle()

    def get_game(self, bot, update):
        self.game = Game()
        if self.game.check_game_today():
            self.game.get_stats()
            message = self.game.notify_game_today()
            bot.send_message(chat_id=self.chat_id, text=message)

    def check_score(self, bot, update):
        current_time = datetime.datetime.now()
        if self.game < current_time < self.game.timedelta(hours=3):
            if self.game.get_score():
                message = self.game.score_message()
                print(message)
                #bot.send_message(chat_id=self.chat_id, text=message)

    @staticmethod
    def uuu(bot, update):
        chat_id = update.message.chat_id
        bot.send_message(chat_id=chat_id, text='UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU')


if __name__ == '__main__':
    UtregBot()
