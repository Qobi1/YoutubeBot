from django.shortcuts import render
from telegram.ext import CallbackContext
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
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
    update.message.reply_text(f"""🇦🇺 - Choose the language\n🇷🇺 - Выбирай язык\n🇺🇿 - Tilni tanlang""", reply_markup=btns(type='language'))


def btns(type=None):
    if type == 'language':
        btn = [
            [KeyboardButton('🇦🇺Eng'), KeyboardButton('🇷🇺Rus')],
            [KeyboardButton('🇺🇿Uzb')]
               ]
    else:
        pass


def language():
    dictionary = {
        'uzb': {

        },
        'rus': {

        },
        'en': {

        }
    }