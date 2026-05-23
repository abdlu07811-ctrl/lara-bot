import os
import telebot
import random
from flask import Flask, request

# الإعدادات
TOKEN = "8575847456:AAE0K2YUmc5Ri77kFwrl14IIMV999ewfpeU"
ADMIN_ID = 8369014219
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

# قوائم المحتوى المنفصلة
JOKES_LIST = [
    "نكتة: مرة محشش سأل محشش: كم الساعة؟ قال: ما أدري. قال: غريبة، أنا عندي الثنتين! 😂",
    "نكتة: بخيل طاح في البير، طلع أهله قالوا له: إيش صار؟ قال: ما يهم، أهم شيء ما تشربون من الموية! 💸",
    "نكتة: غبي راح للدكتور، قال له: يا دكتور كل ما ألمس جسمي يعورني. قال: سلامتك، أصبعك مكسور! 🤕",
    "نكتة: ليه القطار مهم؟ لأنه تحته خطين! 🚂",
    "نكتة: محشش يسأل أخوه: إيش الفرق بين الأسبوع والصحراء؟ قال: الأسبوع فيه أحد، والصحراء ما فيها أحد! 🌵"
]

QUOTES_LIST = [
    "اقتباس: النجاح ليس النهاية، والفشل ليس قاتلاً.. الشجاعة للاستمرار هي ما يهم. 🚀",
    "اقتباس: كن أنت التغيير الذي تريد أن تراه في العالم. ✨",
    "اقتباس: الحياة تجربة شجاعة أو لا شيء. 💪",
    "اقتباس: القوة ليست في عدم السقوط، بل في النهوض بعد كل سقوط. 🦁",
    "اقتباس: القراءة هي غذاء الروح والعقل. 📚"
]

REPLIES_LIST = [
    "لارا هنا، اطلب ما تشاء يا بطل! 👩‍💻",
    "أنا دائماً في خدمتك، كيف أقدر أسعدك اليوم؟ 🌟",
    "لارا تتمنى لك يوماً مليئاً بالإنجازات! 🌈",
    "أنت اليوم في أفضل حالاتك، استمر! 🔥",
    "لارا هي رفيقتك في كل الأوقات. 🤝"
]

# الأوامر الإدارية
@bot.message_handler(commands=['kick', 'mute', 'ban'])
def admin_commands(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "🚫 عذراً، هذه الأوامر للمشرف فقط!")
        return
    if not message.reply_to_message:
        bot.reply_to(message, "⚠️ يرجى الرد على رسالة العضو!")
        return
    chat_id, user_id = message.chat.id, message.reply_to_message.from_user.id
    if '/kick' in message.text: 
        bot.kick_chat_member(chat_id, user_id)
        bot.reply_to(message, "✅ تم الطرد.")
    elif '/mute' in message.text: 
        bot.restrict_chat_member(chat_id, user_id, can_send_messages=False)
        bot.reply_to(message, "🔇 تم الكتم.")
    elif '/ban' in message.text: 
        bot.ban_chat_member(chat_id, user_id)
        bot.reply_to(message, "🚫 تم الحظر.")

# الردود التلقائية الذكية
@bot.message_handler(func=lambda message: True)
def auto_responses(message):
    text = message.text.lower()
    if "لارا" in text: 
        bot.reply_to(message, random.choice(REPLIES_LIST))
    elif "نكتة" in text: 
        bot.reply_to(message, random.choice(JOKES_LIST))
    elif "اقتباس" in text: 
        bot.reply_to(message, random.choice(QUOTES_LIST))

# نظام الويب (Webhooks)
@server.route('/' + TOKEN
bot.set_webhook(url='https://web-production-f90f6.up.railway.app/8575847456:AAE0K2YUmc5Ri77kFwrl14IIMV999ewfpeU')
