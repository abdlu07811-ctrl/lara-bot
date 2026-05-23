import os
import telebot
import random
from flask import Flask, request

TOKEN = "8575847456:AAE0K2YUmc5Ri77kFwrl14IIMV999ewfpeU"
ADMIN_ID = 8369014219
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

# مكتبة غنية بالمحتوى
JOKES = ["محشش سأل أخوه: إيش الفرق بين الأسبوع والصحراء؟ قال: الأسبوع فيه أحد، والصحراء ما فيها أحد! 😂", "بخيل طاح في البير، قال: أهم شيء ما تشربون من الموية! 💸", "غبي راح للدكتور، قال: كل ما ألمس جسمي يعورني. قال: سلامتك، أصبعك مكسور! 🤕", "مره واحد اشترى خبز، لقى الخبز خلص، قال: خلاص عطني خبز! 🍞", "محشش يسأل محشش: كم الساعة؟ قال: ما أدري. قال: غريبة، أنا عندي الثنتين! 😂"]
QUOTES = ["النجاح ليس النهاية، والفشل ليس قاتلاً.. الشجاعة للاستمرار هي ما يهم. 🚀", "كن أنت التغيير الذي تريد أن تراه في العالم. ✨", "الحياة تجربة شجاعة أو لا شيء. 💪", "القراءة هي غذاء الروح والعقل. 📚", "الابتسامة هي مفتاح القلوب. 😊"]

@bot.message_handler(func=lambda m: True)
def handle_all(message):
    text = message.text.lower()
    chat_id = message.chat.id
    
    # الردود التلقائية
    if "لارا" in text: 
        bot.reply_to(message, "أهلاً يا صديقي، لارا في خدمتك! ماذا نلعب أو نكتشف اليوم؟ 👩‍💻")
    elif "نكتة" in text: 
        bot.reply_to(message, random.choice(JOKES))
    elif "اقتباس" in text: 
        bot.reply_to(message, random.choice(QUOTES))
    
    # الألعاب
    elif "لعبة" in text:
        choice = random.choice(['🪨', '📄', '✂️'])
        bot.reply_to(message, f"لعبة حجر ورقة مقص: أنا اخترت {choice}")
    elif "نرد" in text:
        bot.reply_to(message, f"🎲 رميت النرد وظهر لك الرقم: {random.randint(1, 6)}")
    
    # الأوامر الإدارية (رد على العضو + كلمة الأمر)
    elif message.reply_to_message:
        target_id = message.reply_to_message.from_user.id
        if "طرد" in text:
            try:
                bot.kick_chat_member(chat_id, target_id)
                bot.reply_to(message, "✅ تم الطرد بنجاح.")
            except: bot.reply_to(message, "❌ تأكد أنني مشرف في المجموعة!")
        elif "كتم" in text:
            try:
                bot.restrict_chat_member(chat_id, target_id, can_send_messages=False)
                bot.reply_to(message, "🔇 تم كتم العضو.")
            except: bot.reply_to(message, "❌ تأكد أنني مشرف في المجموعة!")

# نظام الويب هوك للربط
@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode('utf-8'))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=f'https://web-production-f90f6.up.railway.app/{TOKEN}')
    return "تم التحديث بنجاح!", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
