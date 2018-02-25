import datetime

from telegram.ext import Updater, CommandHandler

from game import Game
from reminders import Reminders
from filters import MessageHandlers
from config import TOKEN, CHAT_ID
from utils import message_chat


class UtregBot(object):

    def __init__(self, chat_id=None, team=None):
        self.chat_id = chat_id
        self.team = team

        self.game = None

        self.updater = Updater(TOKEN)
        self.dp = self.updater.dispatcher

        # Jobs handler
        self.jobs = self.updater.job_queue
        self.jobs.run_daily(self.get_game, datetime.time(hour=9, minute=0))
        self.jobs.run_repeating(self.check_score, interval=30)

        # Other handlers
        self.dp.add_handler(CommandHandler('remind', self.reminder, pass_args=True))
        self.dp.add_handler(CommandHandler('uuu', self.uuu))
        self.dp.add_handler(CommandHandler('opdedom', self.opdedom))

        # Filters and filter handlers
        self.filters = MessageHandlers(self.dp)
        self.dp.add_handler(CommandHandler('remove', self.filters.remove, pass_args=True))
        self.dp.add_handler(CommandHandler('filter', self.filters.new_filter, pass_args=True))
        self.dp.add_handler(CommandHandler('houjebek', self.filters.disable_proactive_messages))
        self.dp.add_handler(CommandHandler('wakkerworden', self.filters.enable_proactive_messages))
        self.filters.load_filters()

        self.reminders = Reminders(self.jobs)

        self.updater.start_polling()

        self.updater.idle()

    def reminder(self, bot, update, args):
        self.reminders.new_reminder(bot, update, args)

    def get_game(self, bot, update):
        self.game = Game(team=self.team)
        if self.game.check_game_today():
            self.game.get_stats()
            message = self.game.notify_game_today()
            bot.send_message(chat_id=self.chat_id, text=message)

    def check_score(self, bot, update):
        if self.game and self.game.time:
            current_time = datetime.datetime.now()
            if self.game.time < current_time < self.game.time + datetime.timedelta(hours=3):
                message = self.game.get_score()
                if message:
                    bot.send_message(chat_id=self.chat_id, text=message)

    @staticmethod
    def uuu(bot, update):
        message = 'UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU'
        message_chat(bot, update, message)

    @staticmethod
    def opdedom(bot, update):
        message = """
        .
        🎼🎵🎶
        Als ik boven op de dom sta
        kjik ik even naar benee
        dan zie ik het ouwe graggie
        het Vreeburg en Wijk C
        Ja dan sprink me hartjie ope
        ik ben trots wat daggie wat
        er is geen mooier plekkie
        as Utereg me stad
        as Utereg me stad
        🎶🎵🎼
        
        """
        message_chat(bot, update, message)

if __name__ == '__main__':
    UtregBot(chat_id=CHAT_ID)
