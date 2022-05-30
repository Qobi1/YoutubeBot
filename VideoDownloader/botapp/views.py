from django.shortcuts import render
from telegram.ext import CallbackContext
from telegram import Update
from .models import *

# Create your views here.


def start(update: Update, context: CallbackContext):
    user = update.effective_user
    log = User.objects.filter(user_id=user.id).first()
    if log is None:
        log = User()
        log.user_id = user.id
        log.log = {'state': 0}
        log.save()
    update.message.reply_text(f"""🇦🇺 """)




def language():
    dictionary = {
        'uzb': {

        },
        'rus': {

        },
        'en': {

        }
    }