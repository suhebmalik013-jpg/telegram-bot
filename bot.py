import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = os.getenv("8663151182:AAE6oSnIN2c-j2RVGe8qnEvmVKzHfJkeoZk")

CHANNEL_LINKS = [
    ("JOIN 1", "https://t.me/+nM-Kyv4FeiE0YmVl"),
    ("JOIN 2", "https://t.me/+zqgNaxVz5Qg0Yjhl"),
    ("JOIN 3", "https://t.me/+Jm83zxnKTMdiODhl"),
]

SUPPORT_URL = "https://t.me/+JAKpdwaI9dI0ZmY9"
BANNER_PATH = "banner.jpg"

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")


def build_keyboard():
    kb = InlineKeyboardMarkup(row_width=2)
    for label, link in CHANNEL_LINKS:
        kb.add(InlineKeyboardButton(label, url=link))
    kb.add(
        InlineKeyboardButton("✅ VERIFY", callback_data="verify"),
        InlineKeyboardButton("🎧 SUPPORT", url=SUPPORT_URL),
    )
    return kb


def send_welcome(chat_id, name):
    caption = (
        f"👋 <b>Hey {name}, Welcome To IGFreeFollowers!</b>\n\n"
        f"🎁 <b>Join 3 required channels and get 10K free followers</b>\n\n"
        f"📌 <b>Must join all channels to unlock bot</b>\n"
        f"✅ After joining, click on <b>VERIFY</b>"
    )

    try:
        if os.path.exists(BANNER_PATH):
            with open(BANNER_PATH, "rb") as photo:
                bot.send_photo(chat_id, photo, caption=caption, reply_markup=build_keyboard(), timeout=20)
        else:
            bot.send_message(chat_id, caption, reply_markup=build_keyboard(), timeout=20)
    except Exception:
        bot.send_message(chat_id, caption, reply_markup=build_keyboard(), timeout=20)


@bot.message_handler(commands=["start"])
def start(msg):
    name = msg.from_user.first_name or "User"
    send_welcome(msg.chat.id, name)


@bot.callback_query_handler(func=lambda call: call.data == "verify")
def verify(call):
    bot.answer_callback_query(call.id, "Verification done!")
    bot.send_message(
        call.message.chat.id,
        "✅ <b>Verification Successful!</b>\n\nBot unlock ho gaya.",
        timeout=20
    )


@bot.message_handler(func=lambda message: True)
def fallback(message):
    bot.send_message(
        message.chat.id,
        "Bot use karne ke liye /start bhejo.",
        reply_markup=build_keyboard(),
        timeout=20
    )


if __name__ == "__main__":
    print("Bot running...")
    bot.infinity_polling(skip_pending=True, timeout=20, long_polling_timeout=20)
