import os
import telebot
import random
from flask import Flask, request

TOKEN = "8575847456:AAE0K2YUmc5Ri77kFwrl14IIMV999ewfpeU"
ADMIN_ID = 8369014219
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

# --- 50 رد ترحيبي وتفاعلي ---
REPLIES = [
    "وعليكم السلام يا غالي!", "يا هلا بيك، نورتنا!", "يسعد هالطله!", "يا مية هلا!", "منور الدنيا كلها!",
    "أهلاً وسهلاً بك!", "يا مرحباً يا صديقي!", "أسعدتني بوجودك!", "نورت الجروب!", "تحياتي لك!",
    "يا هلا والله!", "أهلاً بك يا بطل!", "نورتنا يا غالي!", "أهلاً يا طيب!", "يا مية أهلاً!",
    "مرحباً بك!", "كيف حالك اليوم؟", "يا أهلاً بالطلة الحلوة!", "منور الكروب!", "يا هلا ومية هلا!",
    "أهلاً وسهلاً يا صديق لارا!", "يا هلا بيك يا مبدع!", "يا مرحب فيك!", "يا أهلاً بالطيب!", "نورت بوجودك!",
    "يا هلا يا غالي!", "يا أهلاً ومرحباً!", "يا هلا والله بالجميع!", "نورتنا يا مبدع!", "يسعد هالمسا!",
    "أهلاً بك مجدداً!", "نورت بطلتك!", "يا أهلاً وسهلاً!", "يا هلا ومرحباً!", "يا هلا بالطيبين!",
    "يا هلا يا أصدقائي!", "يا أهلاً بالجميع!", "يا هلا ومية مرحبا!", "نورتوني جميعاً!", "يا هلا يا بطل!",
    "أهلاً وسهلاً بالجميع!", "يا هلا ومية هلا بالكل!", "يا أهلاً وسهلاً بكم!", "يا هلا والله بالكل!", "يا هلا بوجودكم!",
    "أهلاً بالجميع!", "يا هلا بالكل!", "يا هلا ومية هلا بالجميع!", "نورتوني يا أبطال!", "أهلاً وسهلاً بالجميع!"
]

# --- المكتبة (النكت والاقتباسات والألعاب) ---
JOKES = ["محشش سأل أخوه: إيش الفرق بين الأسبوع والصحراء؟ قال: الأسبوع فيه أحد، والصحراء ما فيها أحد! 😂", "بخيل طاح في البير، قال: أهم شيء ما تشربون من الموية! 💸", "غبي راح للدكتور، قال: كل ما ألمس جسمي يعورني. قال: سلامتك، أصبعك مكسور! 🤕", "مره واحد اشترى خبز، لقى الخبز خلص، قال: خلاص عطني خبز! 🍞"]
QUOTES = ["النجاح ليس النهاية، والفشل ليس قاتلاً.. الشجاعة للاستمرار هي ما يهم. 🚀", "كن أنت التغيير الذي تريد أن تراه في العالم. ✨", "الحياة تجربة شجاعة أو لا شيء. 💪"]
GAMES = ["لعبة التخمين", "حجر ورقة مقص 🪨📄✂️", "رمي النرد 🎲", "تحدي الألغاز"]

BAD_WORDS = ["سكس", "اباحي", "خناقة", "لعنة", "وسخ", "قذر", "لعين"]

@bot.message_handler(func=lambda m: True)
def handle_all(message):
    text = message.text.lower()
    
    # 1. فلتر +18
    if any(word in text for word in BAD_WORDS):
        try: bot.delete_message(message.chat.id, message.message_id); return
        except: pass

    # 2. الردود والترحيب
    if any(word in text for word in ["سلام", "نورت", "هلا", "مرحبا", "هاي"]):
        bot.reply_to(message, random.choice(REPLIES))
    elif "لارا" in text and "الأوامر" in text:
        bot.reply_to(message, "📜 **قائمة أوامر لارا:**\n- نكتة، اقتباس، لعبة، نرد\n- طرد، كتم، حظر (بالرد على الرسالة)")
    elif "نكتة" in text: bot.reply_to(message, random.choice(JOKES))
    elif "اقتباس" in text: bot.reply_to(message, random.choice(QUOTES))
    elif "لعبة" in text: bot.reply_to(message, f"لعبة مقترحة: {random.choice(GAMES)}")
    
    # 3. إدارة
    elif message.reply_to_message:
        target_id = message.reply_to_message.from_user.id
        if "طرد" in text: bot.kick_chat_member(message.chat.id, target_id); bot.reply_to(message, "✅ تم الطرد.")
        elif "كتم" in text: bot.restrict_chat_member(message.chat.id, target_id, can_send_messages=False); bot.reply_to(message, "🔇 تم الكتم.")
        elif "حظر" in text: bot.ban_chat_member(message.chat.id, target_id); bot.reply_to(message, "🚫 تم الحظر.")

# Webhook
@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode('utf-8'))])
    return "!", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
