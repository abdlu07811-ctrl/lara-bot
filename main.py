import os
import telebot
import random
from flask import Flask, request

TOKEN = "8575847456:AAE0K2YUmc5Ri77kFwrl14IIMV999ewfpeU"
ADMIN_ID = 8369014219
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

# --- القوائم الضخمة ---
REPLIES = ["وعليكم السلام!", "يا هلا بيك، نورتنا!", "يسعد هالطله!", "يا مية هلا!", "منور الدنيا كلها!", "أهلاً وسهلاً بك!", "يا مرحباً يا صديقي!", "أسعدتني بوجودك!", "نورت الجروب!", "تحياتي لك!", "يا هلا والله!", "أهلاً بك يا بطل!", "نورتنا يا غالي!", "أهلاً يا طيب!", "يا مية أهلاً!", "مرحباً بك!", "كيف حالك اليوم؟", "يا أهلاً بالطلة الحلوة!", "منور الكروب!", "يا هلا ومية هلا!", "أهلاً وسهلاً يا صديق لارا!", "يا هلا بيك يا مبدع!", "يا مرحب فيك!", "يا أهلاً بالطيب!", "نورت بوجودك!", "يا هلا يا غالي!", "يا أهلاً ومرحباً!", "يا هلا والله بالكل!", "نورتنا يا مبدع!", "يسعد هالمسا!", "أهلاً بك مجدداً!", "نورت بطلتك!", "يا أهلاً وسهلاً!", "يا هلا ومرحباً!", "يا هلا بالطيبين!", "يا هلا يا أصدقائي!", "يا أهلاً بالجميع!", "يا هلا ومية مرحبا!", "نورتوني جميعاً!", "يا هلا يا بطل!", "أهلاً وسهلاً بالجميع!", "يا هلا ومية هلا بالجميع!", "يا أهلاً وسهلاً بكم!", "يا هلا والله بالكل!", "يا هلا بوجودكم!", "أهلاً بالجميع!", "يا هلا بالكل!", "يا هلا ومية هلا بالجميع!", "نورتوني يا أبطال!", "أهلاً وسهلاً بالجميع!"]
JOKES = ["محشش سأل أخوه: إيش الفرق بين الأسبوع والصحراء؟ قال: الأسبوع فيه أحد، والصحراء ما فيها أحد! 😂", "بخيل طاح في البير، قال: أهم شيء ما تشربون من الموية! 💸", "غبي راح للدكتور، قال: كل ما ألمس جسمي يعورني. قال: سلامتك، أصبعك مكسور! 🤕", "مره واحد اشترى خبز، لقى الخبز خلص، قال: خلاص عطني خبز! 🍞"]
QUOTES = ["النجاح ليس النهاية، والفشل ليس قاتلاً.. الشجاعة للاستمرار هي ما يهم. 🚀", "كن أنت التغيير الذي تريد أن تراه في العالم. ✨", "الحياة تجربة شجاعة أو لا شيء. 💪"]
BAD_WORDS = ["سكس", "اباحي", "خناقة", "لعنة", "وسخ", "قذر", "لعين"]

@bot.message_handler(content_types=['new_chat_members'])
def welcome_new(message):
    for new_user in message.new_chat_members:
        bot.reply_to(message, f"يا هلا وغلا يا {new_user.first_name}، نورت الكروب يا غالي!")

@bot.message_handler(func=lambda m: True)
def handle_all(message):
    text = message.text.lower()
    chat_id = message.chat.id
    
    # 1. فلتر +18
    if any(word in text for word in BAD_WORDS):
        try: bot.delete_message(chat_id, message.message_id); return
        except: pass

    # 2. نداء لارا والاوامر
    if text == "لارا": bot.reply_to(message, random.choice(["نعم يا بطل؟", "معك لارا، كيف أساعدك؟", "لارا هنا!"]))
    elif "اوامر لارا" in text:
        bot.reply_to(message, "📜 **قائمة أوامر لارا:**\n- نكتة، اقتباس، لعبة، نرد\n- (بالرد على الرسالة): طرد، كتم، فك كتم، حظر")
    elif any(word in text for word in ["سلام", "نورت", "هلا", "مرحبا", "هاي"]): bot.reply_to(message, random.choice(REPLIES))
    elif "نكتة" in text: bot.reply_to(message, random.choice(JOKES))
    elif "اقتباس" in text: bot.reply_to(message, random.choice(QUOTES))
    elif "لعبة" in text: bot.reply_to(message, f"لعبة مقترحة: {random.choice(['حجر ورقة مقص 🪨', 'رمي النرد 🎲', 'تحدي المعلومات'])}")
    
    # 3. الإدارة
    elif message.reply_to_message:
        target_id = message.reply_to_message.from_user.id
        if "طرد" in text: bot.kick_chat_member(chat_id, target_id); bot.reply_to(message, "✅ تم الطرد.")
        elif "كتم" in text: bot.restrict_chat_member(chat_id, target_id, can_send_messages=False); bot.reply_to(message, "🔇 تم الكتم.")
        elif "فك كتم" in text: bot.restrict_chat_member(chat_id, target_id, can_send_messages=True, can_send_media_messages=True); bot.reply_to(message, "✅ تم فك الكتم.")
        elif "حظر" in text: bot.ban_chat_member(chat_id, target_id); bot.reply_to(message, "🚫 تم الحظر.")

# Webhook
@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode('utf-8'))])
    return "!", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

