import telebot, time
import config
from openai import OpenAI

token = config.token
bot = telebot.TeleBot(token=token)
client = OpenAI(api_key=config.GPT)

@bot.message_handler(commands=['start', 'help'])
def message_received(message):
    print(message)
    bot.send_message(chat_id=message.from_user.id, text="Привет, " + message.from_user.first_name + ', напиши свой вопрос')

@bot.message_handler(func=lambda message: True)
def AI_answer(message):

    print(message.text)

    try:
        completion = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[{"role": "user", "content": message.text}],
        )

        answer = completion.choices[0].message.content
        print(answer)
        bot.reply_to(message, answer)

    except Exception as e:
        bot.reply_to(message, f"Ошибка: {e}")

while True:
    try:
        bot.polling(none_stop=True, timeout=90)
    except Exception as e:
        print(e)
        time.sleep(5)
        continue