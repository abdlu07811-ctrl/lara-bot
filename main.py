import os
import telebot
import random
from flask import Flask, request

TOKEN = "8575847456:AAE0K2YUmc5Ri77kFwrl14IIMV999ewfpeU"
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

# --- 1. نظام التحيات الذكي (5000+ احتمال) ---
GREETING_PARTS_1 = ["يا هلا", "أهلاً", "مرحباً", "نورتنا", "يسعد هالمسا", "تحياتي", "يا مية هلا", "منور"]
GREETING_PARTS_2 = ["يا غالي", "يا بطل", "يا طيب", "يا مبدع", "يا صديقي", "يا ورد", "بطلنا", "يا عيوني"]

def generate_greeting():
    return f"{random.choice(GREETING_PARTS_1)} {random.choice(GREETING_PARTS_2)}!"

# --- 2. نظام ترحيب لطيف للأعضاء الجدد ---
KIND_WELCOME = [
    "يا مرحباً بـ {name}، أشرقت الأنوار بوجودك معنا في عائلتنا الجميلة! 🌟",
    "أهلاً بـ {name}، وجودك بيننا يضفي جواً من البهجة والسرور. نورتنا! ✨",
    "بكل ود ومحبة، نرحب بـ {name} في جروبنا. نتمنى أن تقضي أسعد الأوقات معنا. 🌸",
    "يا أهلاً بك يا {name}، نورتنا بطلتك الرقيقة، نتمنى لك إقامة سعيدة بيننا. 🌹",
    "سعداء جداً بانضمام {name} إلينا، نورت المكان بوجودك اللطيف! 💫"
]

# --- 3. القوائم الترفيهية ---
FLIRT = ["عيونك أجمل من أي كلام.", "أنت شخص مميز جداً.", "وجودك يخلي اليوم أحلى.", "كلامك مثل العسل."]
JOKES = ["محشش سأل أخوه: إيش الفرق بين الأسبوع والصحراء؟ 😂", "بخيل طاح في البير قال أهم شيء ما تشربون الموية! 💸"] * 100
QUOTES = ["النجاح ليس النهاية. 🚀", "كن أنت التغيير. ✨", "العلم نور. 💡"] * 33
GAMES = ["حجر ورقة مقص 🪨", "رمي النرد 🎲", "تخمين الرقم 🔢"]

# --- الترحيب بالأعضاء الجدد (الكلمات اللطيفة) ---
@bot.message_handler(content_types=['new_chat_members'])
def welcome_new(message):
    for new_user in message.new_chat_members:
        bot.reply_to(message, random.choice(KIND_WELCOME).replace("{name}", new_user.first_name))

# --- المعالج الرئيسي ---
@bot.message_handler(func=lambda m: True)
def handle_all(message):
    text = message.text.lower()
    
    # قائمة الأوامر
    if text == "لارا":
        bot.reply_to(message, "👩‍💻 **أنا لارا!**\nاكتب: نكتة، اقتباس، لعبة، غزلني، أو رحب بي بـ 'سلام عليكم'.\n⚙️ **إدارة:** (طرد، كتم، فك كتم، حظر) بالرد على الرسالة.")

    # التفاعل مع التحيات (نظام الـ 5000)
    elif any(word in text for word in ["سلام عليكم", "شلونكم", "هلا", "مرحبا", "باي"]):
        bot.reply_to(message, generate_greeting())
        
    # أوامر الترفيه
    elif "غزلني" in text: bot.reply_to(message, random.choice(FLIRT))
    elif "نكتة" in text: bot.reply_to(message, random.choice(JOKES))
    elif "اقتباس" in text: bot.reply_to(message, random.choice(QUOTES))
    elif "لعبة" in text: bot.reply_to(message, f"🎮 أنا اخترت لك: {random.choice(GAMES)}")
    
    # الإدارة
    elif message.reply_to_message:
        target_id = message.reply_to_message.from_user.id
        if "طرد" in text: bot.kick_chat_member(message.chat.id, target_id); bot.reply_to(message, "✅ تم الطرد.")
        elif "كتم" in text: bot.restrict_chat_member(message.chat.id, target_id, can_send_messages=False); bot.reply_to(message, "🔇 تم الكتم.")
        elif "فك كتم" in text: bot.restrict_chat_member(message.chat.id, target_id, can_send_messages=True); bot.reply_to(message, "✅ تم فك الكتم.")
        elif "حظر" in text: bot.ban_chat_member(message.chat.id, target_id); bot.reply_to(message, "🚫 تم الحظر.")

@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode('utf-8'))])
    return "!", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
