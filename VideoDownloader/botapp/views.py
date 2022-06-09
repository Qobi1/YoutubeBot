from django.shortcuts import render
from telegram.ext import CallbackContext
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from .models import *
from pytube import YouTube

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
    print('>>>>>>>>>>>>>>>>>', msg)
    if state['state'] == 0:
        yt = YouTube(msg)
        filename = yt.title
        print(filename)
        s = yt.streams.get_by_itag(17)
        s.download(output_path='video')
        update.message.reply_text("""🇦🇺 - Please wait..\n🇷🇺 - Пожалуйста, подождите..\n🇺🇿 - Iltimos kuting..""")
        context.bot.send_video(video=open(f'video/{filename}.3gpp', 'rb'), chat_id=user.id, timeout=1000)
    log.log = state
    log.save()


# def received_link(update: Update, context: CallbackContext):
#     user = update.effective_user
#     msg = update.message.text
#     log = User.objects.filter(user_id=user.id).first()
#     state = log.log
#     if state['state'] == 0:
#         yt = YouTube(msg)
#         filename = yt.title
#         print(filename)
#         s = yt.streams.get_by_itag(17)
#         s.download(output_path='video')
#         update.message.reply_text("""🇦🇺 - Please wait..\n🇷🇺 - Пожалуйста, подождите..\n🇺🇿 - Iltimos kuting..""")
#         context.bot.send_video(video=open(f'video/{filename}.3gpp', 'rb'), chat_id=user.id, timeout=1000)


def btns(type=None):
    btn = []
    if type == 'format':
        btn = [
            [KeyboardButton('180'), KeyboardButton('360')],
            [KeyboardButton('720')],
            [KeyboardButton('Audio')]
        ]

    else:
        pass
    return ReplyKeyboardMarkup(btn, resize_keyboard=True, one_time_keyboard=True)
