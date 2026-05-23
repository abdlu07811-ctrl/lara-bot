import os
import telebot
import random
from flask import Flask, request

# الإعدادات
TOKEN = "8575847456:AAE0K2YUmc5Ri77kFwrl14IIMV999ewfpeU"
ADMIN_ID = 8369014219
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

# --- قوائم المحتوى ---
JOKES_LIST = ["نكتة: محشش سأل محشش: كم الساعة؟ قال: ما أدري. قال: غريبة، أنا عندي الثنتين! 😂", "نكتة: بخيل طاح في البير، قال: أهم شيء ما تشربون من الموية! 💸"]
QUOTES_LIST = ["اقتباس: النجاح ليس النهاية، والفشل ليس قاتلاً.. الشجاعة للاستمرار هي ما يهم. 🚀", "اقتباس: كن أنت التغيير الذي تريد أن تراه في العالم. ✨"]

# --- الألعاب المضافة حديثاً ---
@bot.message_handler(commands=['game'])
def play_game(message):
    choices = ['حجر 🪨', 'ورقة 📄', 'مقص ✂️']
    bot.reply_to(message, f"أنا اخترت: {random.choice(choices)}.. حاول الفوز علي! 😎")

@bot.message_handler(commands=['dice'])
def roll_dice(message):
    # رمي النرد
    result = random.randint(1, 6)
    bot.reply_to(message, f"🎲 رميت النرد وظهر لك الرقم: {result}")

@bot.message_handler(commands=['guess'])
def guess_number(message):
    # لعبة تخمين رقم
    secret = random.randint(1, 10)
    bot.reply_to(message, f"فكرت في رقم بين 1 و 10.. هل يمكنك تخمينه؟ (اكتب الرقم في رسالة أخرى)")
    # يمكن تطوير هذا لاحقاً ليكون تفاعلياً أكثر

# --- الأوامر الإدارية ---
@bot.message_handler(commands=['kick', 'mute', 'ban'])
def admin_commands(message):
    if message.from_user.id != ADMIN_ID: return bot.reply_to(message, "🚫 للأدمن فقط!")
    if not message.reply_to_message: return bot.reply_to(message, "⚠️ يرجى الرد على رسالة العضو!")
    
    chat_id, user_id = message.chat.id, message.reply_to_message.from_user.id
    try:
        if '/kick' in message.text: bot.kick_chat_member(chat_id, user_id); bot.reply_to(message, "✅ تم الطرد.")
        elif '/mute' in message.text: bot.restrict_chat_member(chat_id, user_id, can_send_messages=False); bot.reply_to(message, "🔇 تم الكتم.")
        elif '/ban' in message.text: bot.ban_chat_member(chat_id, user_id); bot.reply_to(message, "🚫 تم الحظر.")
    except Exception as e: bot.reply_to(message, f"❌ تأكد أنني مشرف في المجموعة! ({e})")

# --- الردود التلقائية ---
@bot.message_handler(func=lambda message: True)
def auto_responses(message):
    text = message.text.lower()
    if "لارا" in text: bot.reply_to(message, "لارا هنا، اطلب ما تشاء يا بطل! 👩‍💻")
    elif "نكتة" in text: bot.reply_to(message, random.choice(JOKES_LIST))
    elif "اقتباس" in text: bot.reply_to(message, random.choice(QUOTES_LIST))

# --- نظام الويب ---
@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode('utf-8'))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=f'https://web-production-f90f6.up.railway.app/{TOKEN}')
    return "تم ضبط الويب بنجاح!", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
