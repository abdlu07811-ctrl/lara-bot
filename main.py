import os
import telebot
import random
from flask import Flask, request

TOKEN = "8575847456:AAE0K2YUmc5Ri77kFwrl14IIMV999ewfpeU"
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

# --- 100 عبارة ترحيبية ---
WELCOME_MSGS = [
    "يا هلا ومية هلا بـ {name}، نورت الكروب!", "نورتنا يا {name}، البيت بيتك.", "أهلاً بك يا {name}، وجودك زادنا نوراً.",
    "يا مرحب بـ {name}، نورت عائلتنا الجديدة.", "أهلاً وسهلاً يا {name}، سعيدون بوجودك معنا.", "يا هلا بـ {name}، نورت المكان بطلتك.",
    "مرحباً {name}، نتمنى لك وقتاً ممتعاً.", "نورت يا {name}، نورتنا بطلتك البهية.", "أهلاً {name}، البيت بيتك يا بطل.",
    "يا هلا بـ {name}، نورت الجروب.", "يا مرحباً يا {name}، نورتنا.", "أهلاً وسهلاً {name}، نورت الكروب يا غالي.",
    "يا هلا بـ {name}، نورت بوجودك.", "نورتنا يا {name}، يا هلا ومية هلا.", "أهلاً {name}، نورتنا يا طيب.",
    "يا هلا ومية مرحبا بـ {name}.", "نورت الجروب يا {name}، يا أهلاً بك.", "أهلاً بـ {name}، نورتنا يا بطل.",
    "يا مرحب يا {name}، نورت الكروب.", "يا هلا بـ {name}، نورتنا يا غالي.", "نورت يا {name}، يا هلا بك.",
    "أهلاً وسهلاً {name}، نورت المكان.", "يا هلا ومية هلا بـ {name}.", "نورتنا يا {name}، يا هلا ومية هلا.",
    "أهلاً بـ {name}، نورت الكروب.", "يا مرحب بـ {name}، نورت الجروب.", "نورت يا {name}، البيت بيتك.",
    "أهلاً {name}، نورتنا بطلتك.", "يا هلا بـ {name}، نورت الكروب يا بطل.", "أهلاً وسهلاً {name}، نورتنا.",
    "يا مرحب يا {name}، نورت الكروب.", "نورت يا {name}، يا هلا بك.", "أهلاً وسهلاً {name}، نورت المكان بطلتك.",
    "يا هلا بـ {name}، نورت الجروب.", "نورتنا يا {name}، يا هلا ومية هلا.", "أهلاً {name}، نورت الكروب.",
    "يا مرحب بـ {name}، نورتنا.", "نورت يا {name}، البيت بيتك.", "أهلاً وسهلاً {name}، نورتنا بطلتك.",
    "يا هلا بـ {name}، نورت الكروب يا بطل.", "أهلاً {name}، نورتنا.", "يا مرحب يا {name}، نورت الجروب.",
    "نورت يا {name}، يا هلا بك.", "أهلاً وسهلاً {name}، نورت المكان.", "يا هلا بـ {name}، نورت الجروب.",
    "نورتنا يا {name}، يا هلا ومية هلا.", "أهلاً {name}، نورت الكروب.", "يا مرحب بـ {name}، نورتنا.",
    "نورت يا {name}، البيت بيتك.", "أهلاً وسهلاً {name}، نورتنا بطلتك.", "يا هلا بـ {name}، نورت الكروب يا بطل.",
    "أهلاً {name}، نورتنا.", "يا مرحب يا {name}، نورت الجروب.", "نورت يا {name}، يا هلا بك.",
    "أهلاً وسهلاً {name}، نورت المكان.", "يا هلا بـ {name}، نورت الجروب.", "نورتنا يا {name}، يا هلا ومية هلا.",
    "أهلاً {name}، نورت الكروب.", "يا مرحب بـ {name}، نورتنا.", "نورت يا {name}، البيت بيتك.",
    "أهلاً وسهلاً {name}، نورتنا بطلتك.", "يا هلا بـ {name}، نورت الكروب يا بطل.", "أهلاً {name}، نورتنا.",
    "يا مرحب يا {name}، نورت الجروب.", "نورت يا {name}، يا هلا بك.", "أهلاً وسهلاً {name}، نورت المكان.",
    "يا هلا بـ {name}، نورت الجروب.", "نورتنا يا {name}، يا هلا ومية هلا.", "أهلاً {name}، نورت الكروب.",
    "يا مرحب بـ {name}، نورتنا.", "نورت يا {name}، البيت بيتك.", "أهلاً وسهلاً {name}، نورتنا بطلتك.",
    "يا هلا بـ {name}، نورت الكروب يا بطل.", "أهلاً {name}، نورتنا.", "يا مرحب يا {name}، نورت الجروب.",
    "نورت يا {name}، يا هلا بك.", "أهلاً وسهلاً {name}، نورت المكان.", "يا هلا بـ {name}، نورت الجروب.",
    "نورتنا يا {name}، يا هلا ومية هلا.", "أهلاً {name}، نورت الكروب.", "يا مرحب بـ {name}، نورتنا.",
    "نورت يا {name}، البيت بيتك.", "أهلاً وسهلاً {name}، نورتنا بطلتك.", "يا هلا بـ {name}، نورت الكروب يا بطل.",
    "أهلاً {name}، نورتنا.", "يا مرحب يا {name}، نورت الجروب.", "نورت يا {name}، يا هلا بك.",
    "أهلاً وسهلاً {name}، نورت المكان.", "يا هلا بـ {name}، نورت الجروب.", "نورتنا يا {name}، يا هلا ومية هلا.",
    "أهلاً {name}، نورت الكروب.", "يا مرحب بـ {name}، نورتنا.", "نورت يا {name}، البيت بيتك.",
    "أهلاً وسهلاً {name}، نورتنا بطلتك.", "يا هلا بـ {name}، نورت الكروب يا بطل."
]

JOKES = ["محشش سأل أخوه: إيش الفرق بين الأسبوع والصحراء؟ قال: الأسبوع فيه أحد، والصحراء ما فيها أحد! 😂", "بخيل طاح في البير، قال: أهم شيء ما تشربون من الموية! 💸", "غبي راح للدكتور، قال: كل ما ألمس جسمي يعورني. قال: سلامتك، أصبعك مكسور! 🤕", "مرة واحد راح يشتري خبز، لقى الخبز خلص، قال: خلاص عطني خبز! 🍞"] * 25
QUOTES = ["النجاح ليس النهاية، والفشل ليس قاتلاً.. الشجاعة للاستمرار هي ما يهم. 🚀", "كن أنت التغيير الذي تريد أن تراه في العالم. ✨", "الحياة تجربة شجاعة أو لا شيء. 💪", "القراءة هي غذاء الروح والعقل. 📚"] * 25
BAD_WORDS = ["سكس", "اباحي", "خناقة", "لعنة", "وسخ", "قذر", "لعين"]

@bot.message_handler(content_types=['new_chat_members'])
def welcome_new(message):
    for new_user in message.new_chat_members:
        bot.reply_to(message, random.choice(WELCOME_MSGS).replace("{name}", new_user.first_name))

@bot.message_handler(func=lambda m: True)
def handle_all(message):
    text = message.text.lower()
    chat_id = message.chat.id
    
    if any(word in text for word in BAD_WORDS):
        try: bot.delete_message(chat_id, message.message_id); return
        except: pass

    if "لارا" in text and "اوامر" in text:
        bot.reply_to(message, "📜 **أوامر لارا:**\n- نكتة، اقتباس، لعبة، نرد\n- (رد على الرسالة): طرد، كتم، فك كتم، حظر")
    elif text == "لارا": bot.reply_to(message, "نعم يا دراكون، لارا في خدمتك! 👩‍💻")
    elif "نكتة" in text: bot.reply_to(message, random.choice(JOKES))
    elif "اقتباس" in text: bot.reply_to(message, random.choice(QUOTES))
    elif "لعبة" in text: bot.reply_to(message, f"🎲 جرب حظك: {random.choice(['حجر ورقة مقص', 'رمي النرد', 'تخمين رقم'])}")
    
    elif message.reply_to_message:
        target_id = message.reply_to_message.from_user.id
        if "طرد" in text: bot.kick_chat_member(chat_id, target_id); bot.reply_to(message, "✅ تم الطرد.")
        elif "كتم" in text: bot.restrict_chat_member(chat_id, target_id, can_send_messages=False); bot.reply_to(message, "🔇 تم الكتم.")
        elif "فك كتم" in text: bot.restrict_chat_member(chat_id, target_id, can_send_messages=True); bot.reply_to(message, "✅ تم فك الكتم.")
        elif "حظر" in text: bot.ban_chat_member(chat_id, target_id); bot.reply_to(message, "🚫 تم الحظر.")

@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode('utf-8'))])
    return "!", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
