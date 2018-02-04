import datetime

from telegram.ext import Updater, CommandHandler, MessageHandler

from game import Game
from reminders import Reminders
import filters
from config import TOKEN, CHAT_ID


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
        self.dp.add_handler(CommandHandler('houjebek', self.disable_proactive_messages))
        self.dp.add_handler(CommandHandler('wakkerworden', self.enable_proactive_messages))
        self.dp.add_handler(CommandHandler('remind', self.reminder, pass_args=True))
        self.dp.add_handler(CommandHandler('uuu', self.uuu))
        self.dp.add_handler(CommandHandler('opdedom', self.opdedom))
        self.flip_message_handlers()

        self.reminders = Reminders(self.jobs, self.message_chat)

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
        if self.game:
            current_time = datetime.datetime.now()
            if self.game.time < current_time < self.game.time + datetime.timedelta(hours=3):
                message = self.game.get_score()
                if message:
                    bot.send_message(chat_id=self.chat_id, text=message)

    def disable_proactive_messages(self, bot, update):
        self.flip_message_handlers(False)
        self.message_chat(bot, update, 'Oke Oke, Trekvlek. Ik zeg al niks meer en luister alleen naar commando\'s')

    def enable_proactive_messages(self, bot, update):
        self.flip_message_handlers(True)
        self.message_chat(bot, update, 'Mogge!')

    def flip_message_handlers(self, enable=True):
        handler = self.dp.add_handler if enable else self.dp.remove_handler
        for handle in self.get_message_handlers():
            handler(handle)

    def get_message_handlers(self):
        return [MessageHandler(filters.filter_steen, self.message_handler_steen),
                MessageHandler(filters.filter_beter_als, self.message_handler_beter_als)]

    def message_handler_steen(self, bot, update):
        self.message_chat(bot, update, 'Fok Steen!')

    def message_handler_beter_als(self, bot, update):
        self.message_chat(bot, update, 'Nee.... Beter he!')

    def uuu(self, bot, update):
        message = 'UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU'
        self.message_chat(bot, update, message)

    def opdedom(self, bot, update):
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
        self.message_chat(bot, update, message)

    @staticmethod
    def message_chat(bot, update, message, chat_id=None):
        chat_id = chat_id or update.message.chat_id
        bot.send_message(chat_id=chat_id, text=message)

if __name__ == '__main__':
    UtregBot(chat_id=CHAT_ID)
