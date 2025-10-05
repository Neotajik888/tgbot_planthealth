import telebot

token = '8339742095:AAHj9W0GXJ0M-AitfR1SEcViXN14W_5NlGo'

bot = telebot.TeleBot(token=token)

from telebot import types

@bot.message_handler(commands=['start'])
def message_received(message):
    print(message)
    bot.send_message(chat_id=message.from_user.id, text="привет, " + message.from_user.first_name)



bot.polling(none_stop=True, interval=0)