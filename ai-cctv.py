import telebot
import json
from openai import OpenAI
from telebot import types # Import module for inline buttons

TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN" # Replace with your actual token from BotFather
bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = OpenAI()

# Temporary storage to keep track of user property descriptions across callbacks
user_requests = {}

print("🤖 Updated Telegram Bot with inline buttons is running...")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "Hello! I am your AI Residential Security Assistant for Orlando. 🛡️🏠\n\n"
        "Send me a property description or a homeowner's security concern, and I will help you close the deal."
    )
    bot.reply_to(message, welcome_text)

# Intercept property descriptions
@bot.message_handler(func=lambda message: True)
def handle_object_description(message):
    chat_id = message.chat.id
    user_requests[chat_id] = message.text # Save message text to maintain context
    
    bot.reply_to(message, "⏳ One moment, analyzing property vulnerabilities...")
    
    try:
        # Step 1: Rapid risk analysis in English
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a residential security expert. Briefly list the main risks and vulnerabilities of the home based on the user's description in English. Be concise and professional."},
                {"role": "user", "content": message.text}
            ]
        )
        
        risks_analysis = response.choices[0].message.content
        
        # Create interactive inline keyboard
        markup = types.InlineKeyboardMarkup(row_width=1)
        
        btn_email = types.InlineKeyboardButton("📧 Generate Pitch Email", callback_data="get_email")
        btn_nextdoor = types.InlineKeyboardButton("💬 Nextdoor / Facebook Post", callback_data="get_nextdoor")
        btn_tech = types.InlineKeyboardButton("🛠️ Hardware Recommendations", callback_data="get_tech")
        
        markup.add(btn_email, btn_nextdoor, btn_tech)
        
        # Send risks overview accompanied by choice buttons
        bot.send_message(chat_id, f"🚨 *Vulnerability Analysis:*\n\n{risks_analysis}\n\n*What would you like to generate for this property?*", parse_mode="Markdown", reply_markup=markup)
        
    except Exception as e:
        bot.reply_to(message, f"Error: {e}")

# Handle inline button clicks
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    chat_id = call.message.chat.id
    
    # Verify session context exists
    if chat_id not in user_requests:
        bot.send_message(chat_id, "Sorry, your session has expired. Please send the property description again.")
        return

    original_text = user_requests[chat_id]
    
    # Acknowledge the callback immediately to stop the button loading animation
    bot.answer_callback_query(call.id, "AI is processing your request...")

    if call.data == "get_email":
        prompt = "Write a professional cold pitch email to the homeowner in English. Focus on the identified risks and offer a free security audit."
    elif call.data == "get_nextdoor":
        prompt = "Write a friendly, informal response for a US neighborhood platform like Nextdoor or Facebook in English. The tone must be helpful, neighborly, and expert, without an aggressive, direct sales pitch."
    elif call.data == "get_tech":
        prompt = "Create a structured hardware recommendation list in English. Specify types of cameras (dome, bullet), estimated quantities, and whether motion-activated floodlights or backyard sensors are recommended."

    # Request targeted content format from OpenAI based on selected button
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"You are an AI consultant specialized in CCTV systems. Based on the property details provided, execute this exact task: {prompt}"},
                {"role": "user", "content": original_text}
            ]
        )
        
        result_text = response.choices[0].message.content
        bot.send_message(chat_id, result_text, parse_mode="Markdown")
        
    except Exception as e:
        bot.send_message(chat_id, f"Generation failed: {e}")

bot.infinity_polling()
