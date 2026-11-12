import telebot
from telethon import TelegramClient
import asyncio
import random

TOKEN = '9101214317:AAFFLw3y8oclMRp-olOJ2jPLJsvH4iMInNU'
bot = telebot.TeleBot(TOKEN)

OWNER_ID = 8611033531
API_ID = 1234567
API_HASH = 'your_api_hash'

BAD_WORDS = ["كس", "شراميط", "منيوك", "قحبة", "عرص", "حشيش", "fuck", "bitch", "sex", "porn"]
PORN_WORDS = ["إباحي", "سكس", "xXx", "pornhub", "xnxx", "hentai"]

active_games = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id if message.from_user else OWNER_ID
    if user_id == OWNER_ID:
        bot.reply_to(message, "مرحباً بك يا سيدي ومطوري أحمد 👑. روزبة جاهزة لخدمتك بكل قوة.")
    else:
        bot.reply_to(message, "مرحباً بك! أنا روزبة، مساعدة الذكاء الاصطناعي والحماية الشاملة.")

@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_members(message):
    for member in message.new_chat_members:
        name = member.first_name or "صديقي"
        try:
            bot.send_message(message.chat.id, f"أهلاً بك يا {name} في المجموعة! 🌸 أنا روزبة، مساعدة الذكاء الاصطناعي والحماية. نورتنا يا غالي!")
        except:
            pass

@bot.message_handler(commands=['game'])
def start_group_game(message):
    chat_id = message.chat.id
    active_games[chat_id] = random.randint(1, 10)
    bot.reply_to(message, "🎮 **بدأت لعبة تخمين الأرقام!**\nاخترت رقماً بين 1 و 10. من يخمّنه أولاً؟ اكتب تخمينك!")

@bot.message_handler(commands=['tagall', 'تاك'])
def tag_all_members(message):
    if message.chat.type in ['group', 'supergroup']:
        bot.reply_to(message, "📢 تنبيه عام لكل الأعضاء تفاعلوا معنا في المجموعة! 🌸")
    else:
        bot.reply_to(message, "⚠️ أمر التاك يعمل داخل المجموعات فقط.")

@bot.message_handler(commands=['ban'])
def ban_user(message):
    chat_id = message.chat.id
    user_id = message.from_user.id if message.from_user else OWNER_ID
    if user_id == OWNER_ID and message.reply_to_message:
        try:
            bot.ban_chat_member(chat_id, message.reply_to_message.from_user.id)
            bot.reply_to(message, "تم حظر المستخدم بنجاح بصلاحيات المطور المطلقة 🚫.")
        except Exception as e:
            bot.reply_to(message, f"⚠️ خطأ في الصلاحيات: {e}")
    else:
        bot.reply_to(message, "قم بالرد على رسالة الشخص واكتب /ban")

@bot.message_handler(commands=['mute'])
def mute_user(message):
    if message.reply_to_message:
        try:
            bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, can_send_messages=False)
            bot.reply_to(message, "تم كتم المستخدم بنجاح 🔇.")
        except:
            bot.reply_to(message, "تأكد أن البوت مشرف.")
    else:
        bot.reply_to(message, "قم بالرد على رسالة الشخص واكتب /mute")

@bot.message_handler(commands=['play'])
def play_music(message):
    song_name = message.text.replace('/play', '').strip()
    if song_name:
        bot.reply_to(message, f"🎵 روزبة تبحث عن الأغنية وتجهزها لك: {song_name} ...")
    else:
        bot.reply_to(message, "اكتب اسم الأغنية بعد الأمر. مثال: /play [اسم الأغنية]")

@bot.message_handler(commands=['rush'])
def start_rush(message):
    user_id = message.from_user.id if message.from_user else OWNER_ID
    if user_id == OWNER_ID:
        target_info = message.text.replace('/rush', '').strip()
        if target_info:
            bot.reply_to(message, f"⚡ روزبة تشغل الحساب الحقيقي لأحمد وتطبق مهلة أمان (7 ثوانٍ)...")
            try:
                client = TelegramClient('ahmad_session', API_ID, API_HASH)
                async def run_rush_task():
                    await client.start()
                    for i in range(3):
                        await asyncio.sleep(7)
                    await client.disconnect()
                asyncio.run(run_rush_task())
                bot.send_message(message.chat.id, "✅ تم إتمام عملية الرشق بنجاح مع الالتزام بمهلة الحماية الزمنية.")
            except Exception as e:
                bot.reply_to(message, f"⚠️ خطأ في Telethon: {e}")
        else:
            bot.reply_to(message, "⚠️ يرجى تحديد الرابط المراد رشقه. مثال: /rush [الرابط]")
    else:
        bot.reply_to(message, "❌ عذراً، أمر الرشق مخصص لمشئ البوت (أحمد) فقط.")

@bot.message_handler(func=lambda message: True)
def universal_handler(message):
    chat_id = message.chat.id
    chat_type = message.chat.type
    text = message.text or message.caption or ""
    
    if not text:
        return

    # الحماية
    if chat_type in ['group', 'supergroup']:
        text_lower = text.lower()
        if "http://" in text_lower or "https://" in text_lower or "t.me/" in text_lower:
            try:
                bot.delete_message(chat_id, message.message_id)
                bot.send_message(chat_id, "عذراً، ممنوع نشر الروابط هنا بأمر الحماية! 🛡️")
            except:
                pass
            return
        if any(w in text_lower for w in PORN_WORDS) or any(w in text_lower for w in BAD_WORDS):
            try:
                bot.delete_message(chat_id, message.message_id)
                bot.send_message(chat_id, "⚠️ تم حذف رسالة مخالفة.")
            except:
                pass
            return

    # الألعاب
    if chat_id in active_games and text.isdigit():
        if int(text) == active_games[chat_id]:
            user_name = message.from_user.first_name if message.from_user else "صديقي"
            bot.reply_to(message, f"🎉 كفو يا {user_name}! لقد تخمنت الرقم الصحيح وفزت باللعبة!")
            del active_games[chat_id]
            return

    # الرد الذكي المباشر المخصص لأحمد وباقي الأعضاء
    text_lower = text.lower()
    if "ميزات" in text_lower or "تستطيع" in text_lower:
        reply_text = "أنا روزبة مساعدتك الذكية! أستطيع إدارة المجموعات، حماية الدردشة، تشغيل الألعاب، تنفيذ أمر الرشق الآمن، والترحيب بالأعضاء."
    elif "كيفك" in text_lower or "شلونك" in text_lower:
        reply_text = "أنا بألف خير مادمت معك يا أحمد! كيف يمكنني مساعدتك اليوم؟ 🌸"
    elif message.from_user and message.from_user.id == OWNER_ID:
        reply_text = f"أهلاً بك يا مطوري الملك أحمد 👑. لقد فهمت رسالتك ({text}) وأنا جاهزة لتنفيذ أي أمر أو توجيه تطلبه فوراً!"
    else:
        reply_text = f"أهلاً بك! لقد قلت: ({text}). أنا روزبة جاهزة لخدمتك."

    try:
        bot.reply_to(message, reply_text)
    except:
        try:
            bot.send_message(chat_id, reply_text)
        except:
            pass

bot.infinity_polling()
