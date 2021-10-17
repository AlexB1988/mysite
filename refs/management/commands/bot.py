from django.core.management.base import BaseCommand
from telegram import Bot,Update,InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import Updater,CommandHandler,MessageHandler,Filters,CallbackContext,CallbackQueryHandler
from telegram.utils.request import Request
from .config import *
from refs.models import *

temp_dict={}

def dynamic_buttns(text,user_id):
    object_list = Reflist.objects.filter(title__icontains=text)
    temp_dict[user_id]={user_id:user_id,'text':text}
    keyboard = [
        [InlineKeyboardButton(object_list[m].title, callback_data=str(object_list[m].title))] for m in range(len(object_list))
    ]
    return keyboard

def log_errors(f):
    def inner(*args,**kwargs):
        try:
            return f(*args,**kwargs)
        except Exception as e:
            error_message=f'Произошла ошиибка: {e}'
            print(error_message)
            raise e
    return inner

@log_errors
def do_start(update:Update,context:CallbackContext):
    chat_id=update.message.chat_id
    text=update.message.text

    reply_text='Привет, напишиите нам название вашей ' \
               'темы,\nили её часть\nЕсли бот не отвечает' \
               ' на ваше сообщение, то подходящая тема не найдена'
    update.message.reply_text(
        text=reply_text,
    )

@log_errors
def do_search(update:Update,context:CallbackContext):
    chat_id=update.message.chat_id
    text=update.message.text
    user_id=update.effective_user.id
    keyboard=dynamic_buttns(text,user_id)
    update.message.reply_text(
        text='Всё, что есть...',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

@log_errors
def keyboard_callback_handler(update:Update,context:CallbackContext):
    query=update.callback_query
    data=query.data

    user_id = update.effective_user.id
    text=temp_dict[user_id]['text']
    object_list=Reflist.objects.filter(title__icontains=text)
    object_length=len(object_list)
    temp_list=[]
    index_count=0

    for n in range(object_length):
        temp_list.append(object_list[n].title)

    for m in range(len(temp_list)-1):
        if data != temp_list[m]:
            index_count=index_count+1
        elif data == temp_list[m]:
            break
    print(index_count)
    if data in temp_list:
        query.message.reply_document(
        filename= object_list[index_count].title,
        document=object_list[index_count].file,

        )

class Command(BaseCommand):
    help = 'Телеграм-бот'

    def handle(self, *args, **options):
        request= Request(
            connect_timeout=0.5,
            read_timeout=1,
        )
        bot=Bot(
            request=request,
            token=TOKEN,
        )
        print(bot.get_me())

        updater=Updater(
            bot=bot,
            use_context=True,
        )
        start_handler=CommandHandler('start',do_start)
        message_handler=MessageHandler(Filters.text,do_search)
        buttons_handler=CallbackQueryHandler(callback=keyboard_callback_handler,pass_chat_data=True)

        updater.dispatcher.add_handler(start_handler)
        updater.dispatcher.add_handler(message_handler)
        updater.dispatcher.add_handler(buttons_handler)


        updater.start_polling()
        updater.idle()