import os
import telebot
import random
from flask import Flask, request

TOKEN = "8575847456:AAE0K2YUmc5Ri77kFwrl14IIMV999ewfpeU"
ADMIN_ID = 8369014219
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

# --- الردود التلقائية لاسم "لارا" ---
LARA_GREETINGS = [
    "معك لارا يا دراكون، كيف أقدر أساعدك؟ 👩‍💻",
    "نعم يا بطل؟ لارا في خدمتك! ✨",
    "لارا هنا، هل تحتاج مساعدة في شيء؟ 🌟",
    "أنا بسمعك، ماذا تريد يا دراكون؟ 🌈"
]

# --- الردود للتحيات (50 رد) ---
REPLIES = ["وعليكم السلام يا غالي!", "يا هلا بيك، نورتنا!", "يسعد هالطله!", "يا مية هلا!", "منور الدنيا كلها!", "أهلاً وسهلاً بك!", "يا مرحباً يا صديقي!", "أسعدتني بوجودك!", "نورت الجروب!", "تحياتي لك!", "يا هلا والله!", "أهلاً بك يا بطل!", "نورتنا يا غالي!", "أهلاً يا طيب!", "يا مية أهلاً!", "مرحباً بك!", "كيف حالك اليوم؟", "يا أهلاً بالطلة الحلوة!", "منور الكروب!", "يا هلا ومية هلا!", "أهلاً وسهلاً يا صديق لارا!", "يا هلا بيك يا مبدع!", "يا مرحب فيك!", "يا أهلاً بالطيب!", "نورت بوجودك!", "يا هلا يا غالي!", "يا أهلاً ومرحباً!", "يا هلا والله بالكل!", "نورتنا يا مبدع!", "يسعد هالمسا!", "أهلاً بك مجدداً!", "نورت بطلتك!", "يا أهلاً وسهلاً!", "يا هلا ومرحباً!", "يا هلا بالطيبين!", "يا هلا يا أصدقائي!", "يا أهلاً بالجميع!", "يا هلا ومية مرحبا!", "نورتوني جميعاً!", "يا هلا يا بطل!", "أهلاً وسهلاً بالجميع!", "يا هلا ومية هلا بالجميع!", "يا أهلاً وسهلاً بكم!", "يا هلا والله بالكل!", "يا هلا بوجودكم!", "أهلاً بالجميع!", "يا هلا بالكل!", "يا هلا ومية هلا بالجميع!", "نورتوني يا أبطال!", "أهلاً وسهلاً بالجميع!"]

@bot.message_handler(func=lambda m: True)
def handle_all(message):
    text = message.text.lower()
    
    # 1. نداء باسم لارا
    if text == "لارا":
        bot.reply_to(message, random.choice(LARA_GREETINGS))
    
    # 2. أمر "اوامر لارا"
    elif "اوامر لارا" in text:
        bot.reply_to(message, "📜 **قائمة أوامر لارا:**\n\n1️⃣ **الأوامر الترفيهية:**\n- نكتة / اقتباس / لعبة / نرد\n\n2️⃣ **أوامر الإدارة (رد على رسالة):**\n- طرد / كتم / حظر")
        
    # 3. التحيات
    elif any(word in text for word in ["سلام", "نورت", "هلا", "مرحبا", "هاي"]):
        bot.reply_to(message, random.choice(REPLIES))
        
    # 4. باقي الأوامر (نكتة، اقتباس، إلخ)
    elif "نكتة" in text: bot.reply_to(message, "نكتة: محشش سأل محشش: كم الساعة؟ قال: ما أدري. قال: غريبة، أنا عندي الثنتين! 😂")
    elif "اقتباس" in text: bot.reply_to(message, "النجاح ليس النهاية، والفشل ليس قاتلاً.. الشجاعة للاستمرار هي ما يهم. 🚀")
    
    # 5. الإدارة
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
