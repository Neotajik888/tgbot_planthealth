import telebot
import os

from openai import OpenAI

token = '8339742095:AAHj9W0GXJ0M-AitfR1SEcViXN14W_5NlGo'

bot = telebot.TeleBot(token=token)

from telebot import types

@bot.message_handler(commands=['start'])
def message_received(message):
    print(message)
    bot.send_message(chat_id=message.from_user.id, text="привет, " + message.from_user.first_name)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🇷🇺 Русский")
    btn2 = types.KeyboardButton('🇬🇧 English')
    markup.add(btn1, btn2)
    bot.send_message(message.from_user.id, "🇷🇺 Выберите язык / 🇬🇧 Choose your language", reply_markup=markup)



client = OpenAI(api_key='sk-fb8ad433e167445f86efe794900fecc1', base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
    ],
    stream=False
)

print(response.choices[0].message.content)

bot.polling(none_stop=True, interval=0)