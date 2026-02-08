import time
import io
import base64
from PIL import Image
import telebot
from telebot import types
from openai import OpenAI
import config

token = config.token
bot = telebot.TeleBot(token=token)
client = OpenAI(api_key=config.GPT)

user_photos = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "👋 Привет! Я бот для лечения растений.\n\n"
        "📸 Что я умею:\n"
        "• Оценивать состояние растения по фото\n"
        "• Предлагать рекомендации по уходу за растением\n"
        "• Отслеживать состояние растения с помощью датчиков\n\n"
        "📎 Как использовать:\n"
        "1. Отправь мне фото - я расскажу что с растением\n"
        "2. Отправь фото с подписью - я отвечу на твой вопрос\n"
        "3. Сначала отправь фото, потом задай вопрос текстом\n\n"
        "🔍 Используй /help для подробной инструкции"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode='Markdown')

@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = (
        "🆘 Помощь по использованию бота:\n\n"
        "📤 Отправка фото:\n"
        "• Прикрепи фото как документ или сжатое изображение\n"
        "• Добавь вопрос в подпись к фото\n"
        "• Или задай вопрос отдельным сообщением после фото\n\n"
        "❓ Примеры вопросов:\n"
        "• Что с моим растением?\n"
        "• Что следует сделать?\n"
        "• Как избежать повторения?\n"
        "⚙️ Другие команды:\n"
        "/start - Начало работы\n"
        "/help - Эта справка\n"
        "/clear - Очистить историю фото\n\n"
        "⚠️ Ограничения:\n"
        "• Размер фото до 20 МБ\n"
        "• Поддерживаемые форматы: JPG, PNG, JPEG, GIF\n"
        "• Для анализа используется gpt-4.1-mini"
    )
    bot.send_message(message.chat.id, help_text, parse_mode='Markdown')

@bot.message_handler(commands=['clear'])
def clear_history(message):
    user_id = message.from_user.id
    if user_id in user_photos:
        del user_photos[user_id]
        bot.send_message(message.chat.id, "✅ История ваших фото очищена.")
    else:
        bot.send_message(message.chat.id, "📭 У вас нет сохранённых фото в истории.")


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        user_id = message.from_user.id
        user_photos[user_id] = {
            'photo_bytes': downloaded_file,
            'message_id': message.message_id
        }
        question = message.caption or "Что с моим растением?."
        response = analyze_image_with_gpt(downloaded_file, question)
        bot.reply_to(message, response)
    except Exception as e:
        print(f"Ошибка при обработке фото: {e}")
        bot.reply_to(message, "❌ Произошла ошибка при анализе фото. Пожалуйста, попробуйте ещё раз.")

@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_text(message):
    try:
        user_id = message.from_user.id
        if user_id not in user_photos:
            if '?' in message.text or any(
                    word in message.text.lower() for word in ['почему', 'зачем', 'что', 'как', 'сколько']):
                bot.send_message(
                    message.chat.id,
                    "📸 Сначала отправьте мне фотографию, затем задайте вопрос по ней."
                )
            else:
                handle_regular_text(message)
            return
        bot.send_chat_action(message.chat.id, 'typing')
        photo_data = user_photos[user_id]
        photo_bytes = photo_data['photo_bytes']
        response = analyze_image_with_gpt(photo_bytes, message.text)
        bot.reply_to(message, response)
    except Exception as e:
        print(f"Ошибка при обработке текста: {e}")
        bot.send_message(message.chat.id, "❌ Произошла ошибка. Попробуйте отправить фото заново.")

def handle_regular_text(message):
    text = message.text.lower()
    if 'привет' in text or 'здравствуй' in text:
        bot.reply_to(message, "Привет! 👋 Отправь мне фото для анализа.")
    elif 'спасибо' in text:
        bot.reply_to(message, "Пожалуйста! 😊 Если есть ещё фото - отправляй!")
    else:
        bot.reply_to(message, "Отправь мне фотографию, и я её проанализирую! 📷")

def analyze_image_with_gpt(image_bytes, question):
    try:
        image = Image.open(io.BytesIO(image_bytes))
        if image.mode != 'RGB':
            image = image.convert('RGB')
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG", quality=85)
        buffered.seek(0)
        img_base64 = base64.b64encode(buffered.read()).decode('utf-8')
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Ты помощник, который анализирует изображения растений. "
                        "Отвечай подробно и информативно на русском языке. "
                        "Тебе надо определить болезнь растения по фото. "
                        "Предоставь рекомендации по уходу в соответствии с болезнью."
                        "Будь точным и объективным в рекомендациях."
                    )
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": question},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{img_base64}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=1500,
            temperature=0.7
        )

        return response.choices[0].message.content

    except Exception as e:
        print(f"Ошибка при анализе изображения: {e}")
        return "Не удалось проанализировать изображение. Пожалуйста, убедитесь что:\n• Фото чёткое и хорошо освещено\n• Размер файла не превышает 20 МБ\n• Формат поддерживается (JPG, PNG, JPEG, GIF)"

def process_large_photos(image_bytes, max_size=(1024, 1024)):
    try:
        image = Image.open(io.BytesIO(image_bytes))
        if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
                image.thumbnail(max_size, Image.Resampling.LANCZOS)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG", quality=85, optimize=True)
        return buffered.getvalue()
    except Exception as e:
        print(f"Ошибка при обработке фото: {e}")
        return image_bytes

@bot.message_handler(content_types=['document'])
def handle_document(message):
    try:
        mime_type = message.document.mime_type
        if mime_type and mime_type.startswith('image/'):
            bot.send_chat_action(message.chat.id, 'typing')
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            user_id = message.from_user.id
            user_photos[user_id] = {
                'photo_bytes': downloaded_file,
                'message_id': message.message_id
            }
            question = message.caption or "Что изображено на этой фотографии? Опиши подробно на русском языке."
            response = analyze_image_with_gpt(downloaded_file, question)
            bot.reply_to(message, response)
        else:
            bot.reply_to(message,"📄 Пожалуйста, отправьте изображение (JPG, PNG, JPEG, GIF), а не документ другого типа.")
    except Exception as e:
        print(f"Ошибка при обработке документа: {e}")
        bot.reply_to(message,"❌ Не удалось обработать файл. Убедитесь, что это изображение и его размер не превышает 20 МБ.")

while True:
    try:
        bot.polling(none_stop=True, timeout=90)
    except Exception as e:
        print(e)
        time.sleep(5)
        continue