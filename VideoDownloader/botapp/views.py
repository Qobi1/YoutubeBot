from django.shortcuts import render
from telegram.ext import CallbackContext
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from .models import *
from pytube import YouTube, Stream
import os

# Create your views here.


def start(update: Update, context: CallbackContext):
    user = update.effective_user
    log = User.objects.filter(user_id=user.id).first()
    if log is None:
        log = User()
        log.user_id = user.id
    update.message.reply_text(f"""🇦🇺 - Good Day! Send me Youtube link to download video\n
🇷🇺 - Здраствуйте, пришлите мне ссылку на Youtube для скачивания видео\n
🇺🇿 - Assalomu alaykum, Youtube silkani tashlang videoni skachat qlish uchun""")

    log.log = {'state': 0}
    log.save()


def received_message(update: Update, context: CallbackContext):
    msg = update.message.text
    user = update.effective_user
    log = User.objects.filter(user_id=user.id).first()
    state = log.log
    if state['state'] == 1:
        msg = msg.split(' ')
        print(msg)
        itag = 0
        type = ''
        if msg[0] == '180':
            print(">>>", msg[0])
            itag = 17
            type = '3gpp'
        elif msg[0] == '360':
            itag = 18
            type = 'mp4'
        elif msg[0] == '720':
            itag = 22
            type = 'mp4'
        elif msg[0] == 'Audio':
            itag = 251
            type = 'webm'
        update.message.reply_text("""🇦🇺 - Please wait..\n🇷🇺 - Пожалуйста, подождите..\n🇺🇿 - Iltimos kuting..""")
        yt = YouTube(state['link'])
        filename = yt.title
        yt = yt.streams.get_by_itag(itag)
        yt.download(output_path='video')
        context.bot.send_video(video=open(f'video/{filename}.{type}', 'rb'), chat_id=user.id, timeout=1000)
        # os.remove(f'video/{filename}.{type}')
    log.log = state
    log.save()


def received_link(update: Update, context: CallbackContext):
    user = update.effective_user
    link = update.message.text
    log = User.objects.filter(user_id=user.id).first()
    state = log.log
    if 0 <= state['state'] <= 1:
        state['link'] = link
        state['state'] = 1
        update.message.reply_text("🇦🇺 - Choose the format\n🇷🇺 - Выберите формат\n🇺🇿 - Formatni tanlang",
                                  reply_markup=btns(type='format'))
    log.log = state
    log.save()


def btns(type=None):
    btn = []
    if type == 'format':
        btn = [
            [KeyboardButton('180'), KeyboardButton('360')],
            [KeyboardButton('720')],
            [KeyboardButton('Audio')]
        ]

    return ReplyKeyboardMarkup(btn, resize_keyboard=True, one_time_keyboard=True)
