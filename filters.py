from csv import reader, writer
import os.path
from re import split

from telegram.ext import BaseFilter, MessageHandler

from utils import message_chat


class CustomTextFilter(BaseFilter):
    def __init__(self, filter_text):
        self.filter_text = filter_text

    def filter(self, message):
        return self.filter_text.lower() in message.text.lower()


class FilterCallback(object):
    def __init__(self, reply, get_active):
        self.reply = reply
        self.get_active = get_active

    def callback(self, bot, update):
        if self.get_active():
            message_chat(bot, update, self.reply)


class MessageHandlers(object):
    def __init__(self, dp, filter_file=None):
        self.dp = dp
        self.filter_file = filter_file or 'filters.csv'
        self.active = True

        if os.path.isfile(self.filter_file):
            self._load_filters()

    def disable_proactive_messages(self, bot, update):
        self.active = False
        message_chat(bot, update, 'Oke, ik zeg al niks meer')

    def enable_proactive_messages(self, bot, update):
        self.active = True
        message_chat(bot, update, 'Mogge!')

    def new_filter(self, bot, update, args):
        error_text = 'Voeg als volgt een filter toe: /filter filter text "reply"'
        if not args:
            return message_chat(bot, update, error_text)

        split_args = split(r'"|“', ' '.join(args))
        if not len(split_args) in [2, 3]:
            return message_chat(bot, update, error_text)

        filter_text = split_args[0].strip()
        reply = split_args[1].strip()

        self._add_filter(filter_text, reply)
        self._save_filter(filter_text, reply)
        message_chat(bot, update, 'Filter voor "{}" met als reactie "{}" toegevoegd'.format(filter_text, reply))

    def _load_filters(self):
        with open(self.filter_file) as f:
            for loaded_filter in reader(f):
                self._add_filter(loaded_filter[0], loaded_filter[1])

    def _save_filter(self, filter_text, reply):
        with open(self.filter_file, 'a+') as f:
            csv_writer = writer(f)
            csv_writer.writerow([filter_text, reply])

    def _add_filter(self, filter_text, reply):
        custom_filter = CustomTextFilter(filter_text)
        callback_reply = FilterCallback(reply, self._get_active)
        self.dp.add_handler(MessageHandler(custom_filter, callback_reply.callback))

    def _get_active(self):
        return self.active


