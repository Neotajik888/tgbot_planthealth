import telebot, time
import config
import openai


token = config.token

bot = telebot.TeleBot(token=token)

from telebot import types


@bot.message_handler(commands=['start', 'help'])
def message_received(message):
    print(message)
    bot.send_message(chat_id=message.from_user.id, text="привет, " + message.from_user.first_name)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🇷🇺 Русский")
    btn2 = types.KeyboardButton('🇬🇧 English')

    markup.add(btn1, btn2)
    bot.send_message(message.from_user.id, "🇷🇺 Выберите язык / 🇬🇧 Choose your language", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def func(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    if message.text == "🇷🇺 Русский":
        bot.send_message(message.chat.id, text="Напишите свой вопрос")


    elif message.text == "🇬🇧 English":
        bot.send_message(message.chat.id, text="Write your question")


from openai import OpenAI
client = OpenAI(api_key=config.GPT)


response = client.responses.create(
  model="gpt-5-mini",
  input=''
)

print(response.output_text)

while True:
    try:
        bot.polling(none_stop=True, timeout=90)
    except Exception as e:
        print(e)
        time.sleep(5)
        continue