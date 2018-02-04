import datetime
import csv
from os import path

import dateparser


class Reminders(object):

    def __init__(self, jobs, message_chat):
        self.jobs = jobs
        self.message_chat = message_chat

        self.reminder_file = 'reminders.csv'

        if path.isfile(self.reminder_file):
            self.load_reminders()

    def new_reminder(self, bot, update, args):
        split = ' '.join(args).split('/')
        reminder_time = dateparser.parse(split[0])
        if reminder_time:
            context = {'message': split[1], 'chat_id': update.message.chat_id}
            self.jobs.run_once(self.reminder_message, reminder_time, context=context)
            self.reminder_to_file(reminder_time, context)
            message = 'Aight. Reminder op: {}'.format(reminder_time.strftime("%Y-%m-%d %H:%M:%S"))
            self.message_chat(bot, update, message)
        else:
            message = 'Sorry maat dat heb ik niet begrepen. Tijden moeten in het Engels: /remind tijd / bericht'
            self.message_chat(bot, update, message)

    def reminder_message(self, bot, job):
        message = 'Reminder: ' + job.context['message']
        self.message_chat(bot, None, message, chat_id=job.context['chat_id'])

    def reminder_to_file(self, reminder_time, context):
        with open(self.reminder_file, 'a+') as f:
            writer = csv.writer(f)
            writer.writerow([str(reminder_time), context['message'], context['chat_id']])

    def load_reminders(self):
        current_date = datetime.datetime.now()
        with open(self.reminder_file, 'r') as f:
            reader = csv.reader(f)
            for reminder in reader:
                reminder_time = dateparser.parse(reminder[0])
                if reminder_time > current_date:
                    context = {'message': reminder[1], 'chat_id': reminder[2]}
                    self.jobs.run_once(self.reminder_message, reminder_time, context=context)
