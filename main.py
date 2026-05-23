import os
import telebot
import random
from flask import Flask, request

TOKEN = "8575847456:AAE0K2YUmc5Ri77kFwrl14IIMV999ewfpeU"
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

# --- وظيفة التحقق من المشرفين ---
def is_user_admin(message):
    try:
        admins = bot.get_chat_administrators(message.chat.id)
        for admin in admins:
            if admin.user.id == message.from_user.id:
                return True
        return False
    except:
        return False

# --- الأنظمة والبيانات ---
GREETING_PARTS_1 = ["يا هلا", "أهلاً", "مرحباً", "نورتنا", "يسعد هالمسا", "تحياتي", "يا مية هلا", "منور"]
GREETING_PARTS_2 = ["يا غالي", "يا بطل", "يا طيب", "يا مبدع", "يا صديقي", "يا ورد", "بطلنا", "يا عيوني"]

KIND_WELCOME = [
    "يا مرحباً بـ {name}، أشرقت الأنوار بوجودك معنا في عائلتنا الجميلة! 🌟",
    "أهلاً بـ {name}، وجودك بيننا يضفي جواً من البهجة والسرور. نورتنا! ✨",
    "بكل ود ومحبة، نرحب بـ {name} في جروبنا. نتمنى أن تقضي أسعد الأوقات معنا. 🌸"
]

FLIRT = ["عيونك أجمل من أي كلام.", "أنت شخص مميز جداً.", "وجودك يخلي اليوم أحلى.", "كلامك مثل العسل."]
JOKES = ["محشش سأل أخوه: إيش الفرق بين الأسبوع والصحراء؟ 😂", "بخيل طاح في البير قال أهم شيء ما تشربون الموية! 💸"] * 100
QUOTES = ["النجاح ليس النهاية. 🚀", "كن أنت التغيير. ✨", "العلم نور. 💡"] * 33
GAMES = ["حجر ورقة مقص 🪨", "رمي النرد 🎲", "تخمين الرقم 🔢"]

# --- الترحيب بالأعضاء الجدد ---
@bot.message_handler(content_types=['new_chat_members'])
def welcome_new(message):
    for new_user in message.new_chat_members:
        bot.reply_to(message, random.choice(KIND_WELCOME).replace("{name}", new_user.first_name))

# --- المعالج الرئيسي ---
@bot.message_handler(func=lambda m: True)
def handle_all(message):
    text = message.text.lower()
    
    # 1. أوامر الإدارة (مع حماية المشرفين)
    if message.reply_to_message and any(cmd in text for cmd in ["طرد", "كتم", "فك كتم", "حظر"]):
        if not is_user_admin(message):
            bot.reply_to(message, "⚠️ عذراً، هذه الأوامر للمشرفين فقط!")
            return
        
        target_id = message.reply_to_message.from_user.id
        chat_id = message.chat.id
        if "طرد" in text: bot.kick_chat_member(chat_id, target_id); bot.reply_to(message, "✅ تم الطرد.")
        elif "كتم" in text: bot.restrict_chat_member(chat_id, target_id, can_send_messages=False); bot.reply_to(message, "🔇 تم الكتم.")
        elif "فك كتم" in text: bot.restrict_chat_member(chat_id, target_id, can_send_messages=True); bot.reply_to(message, "✅ تم فك الكتم.")
        elif "حظر" in text: bot.ban_chat_member(chat_id, target_id); bot.reply_to(message, "🚫 تم الحظر.")
        return

    # 2. الأوامر العادية
    if text == "لارا":
        bot.reply_to(message, "👩‍💻 **أنا لارا!**\nاكتب: نكتة، اقتباس، لعبة، غزلني، أو سلام عليكم.\n⚙️ **إدارة:** (طرد، كتم، فك كتم، حظر) بالرد على الرسالة.")
    elif any(word in text for word in ["سلام عليكم", "شلونكم", "هلا", "مرحبا", "باي"]):
        bot.reply_to(message, f"{random.choice(GREETING_PARTS_1)} {random.choice(GREETING_PARTS_2)}!")
    elif "غزلني" in text: bot.reply_to(message, random.choice(FLIRT))
    elif "نكتة" in text: bot.reply_to(
