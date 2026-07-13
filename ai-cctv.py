import telebot
import json
from openai import OpenAI
from telebot import types # Импортируем модуль для создания кнопок

TELEGRAM_TOKEN = "Твой токен от BotFather" # Твой токен от BotFather
bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = OpenAI()

# Будем временно хранить последний запрос пользователя, чтобы кнопки знали контекст
user_requests = {}

print("🤖 Обновленный Telegram-бот с кнопками успешно запущен...")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "Привет! Я твой ИИ-Ассистент по безопасности жилых домов в Орландо. 🛡️🏠\n\n"
        "Отправь мне описание дома или проблему жильца, и я помогу тебе закрыть сделку."
    )
    bot.reply_to(message, welcome_text)

# Перехватываем описание объекта
@bot.message_handler(func=lambda message: True)
def handle_object_description(message):
    chat_id = message.chat.id
    user_requests[chat_id] = message.text # Сохраняем текст запроса
    
    bot.reply_to(message, "⏳ Секунду, анализирую уязвимости объекта...")
    
    try:
        # Первым шагом ИИ делает только быстрый анализ рисков на русском
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Ты — эксперт по безопасности Residential объектов. Кратко перечисли главные риски и уязвимости дома на основе описания пользователя на русском языке. Будь лаконичен."},
                {"role": "user", "content": message.text}
            ]
        )
        
        risks_analysis = response.choices[0].message.content
        
        # Создаем интерактивную клавиатуру под сообщением
        markup = types.InlineKeyboardMarkup(row_width=1)
        
        btn_email = types.InlineKeyboardButton("📧 Сгенерировать Pitch Email", callback_data="get_email")
        btn_nextdoor = types.InlineKeyboardButton("💬 Текст для соседского чата (Nextdoor)", callback_data="get_nextdoor")
        btn_tech = types.InlineKeyboardButton("🛠️ Рекомендация по камерам", callback_data="get_tech")
        
        markup.add(btn_email, btn_nextdoor, btn_tech)
        
        # Отправляем риски вместе с кнопками
        bot.send_message(chat_id, f"🚨 *Анализ уязвимостей:*\n\n{risks_analysis}\n\n*Что нужно сгенерировать для этого объекта?*", parse_mode="Markdown", reply_markup=markup)
        
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {e}")

# Обработчик нажатия на кнопки (Callback)
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    chat_id = call.message.chat.id
    
    # Проверяем, есть ли у нас сохраненный текст объекта для этого чата
    if chat_id not in user_requests:
        bot.send_message(chat_id, "Извини, сессия устарела. Отправь описание объекта заново.")
        return

    original_text = user_requests[chat_id]
    
    # Уведомляем Telegram, что нажатие обработано (чтобы кнопка не «зависала»)
    bot.answer_callback_query(call.id, "ИИ создает контент...")

    if call.data == "get_email":
        prompt = "Напиши профессиональное холодное письмо (Pitch Email) владельцу дома строго на английском языке. Предложи аудит безопасности."
    elif call.data == "get_nextdoor":
        prompt = "Напиши дружелюбный, неформальный ответ для американской соседской соцсети Nextdoor / Facebook на английском языке. Тон должен быть помогающим, соседским, экспертным, без прямой агрессивной продажи."
    elif call.data == "get_tech":
        prompt = "Составь список рекомендаций по оборудованию на русском языке (какие камеры лучше поставить: купольные, цилиндрические, сколько штук примерно, нужны ли датчики движения или прожекторы на бэкъярд)."

    # Запрашиваем у OpenAI нужный формат по кнопке
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"Ты — ИИ-консультант по системам видеонаблюдения. Основываясь на описании объекта, выполни задачу: {prompt}"},
                {"role": "user", "content": original_text}
            ]
        )
        
        result_text = response.choices[0].message.content
        bot.send_message(chat_id, result_text, parse_mode="Markdown" if call.data != "get_tech" else None)
        
    except Exception as e:
        bot.send_message(chat_id, f"Ошибка при генерации: {e}")

bot.infinity_polling()