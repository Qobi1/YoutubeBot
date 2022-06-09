from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from django.core.management import BaseCommand


from botapp.views import *


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        updater = Updater('5028779716:AAEWI_822MoMa8GKg2wADRNKkTBvI0eujA4')
        updater.dispatcher.add_handler(CommandHandler('start', start))
        # updater.dispatcher.add_handler(MessageHandler(Filters.entity('url'), received_link))
        updater.dispatcher.add_handler(MessageHandler(Filters.text, received_message))

        updater.start_polling()
        updater.idle()
