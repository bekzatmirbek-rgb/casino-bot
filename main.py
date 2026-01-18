import telebot
import random
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

balance = {}
last_bet = {}

def get_balance(user_id):
    return balance.get(user_id, 1000)

def set_balance(user_id, amount):
    balance[user_id] = amount

@bot.message_handler(commands=['start'])
def start(msg):
    uid = msg.from_user.id
    if uid not in balance:
        set_balance(uid, 1000)
    bot.send_message(msg.chat.id,
        "🎰 Казино бот\n"
        "Баланс: 1000\n\n"
        "/roulette сумма\n"
        "/slot сумма\n"
        "/bandit сумма\n"
        "/repeat\n"
        "/double\n"
        "/balance"
    )

@bot.message_handler(commands=['balance'])
def bal(msg):
    uid = msg.from_user.id
    bot.send_message(msg.chat.id, f"💰 Баланс: {get_balance(uid)}")

# 🎯 РУЛЕТКА
@bot.message_handler(commands=['roulette'])
def roulette(msg):
    uid = msg.from_user.id
    try:
        bet = int(msg.text.split()[1])
    except:
        bot.send_message(msg.chat.id, "❌ /roulette 100")
        return

    bal = get_balance(uid)
    if bet > bal or bet <= 0:
        bot.send_message(msg.chat.id, "❌ Баланс жетпейт")
        return

    last_bet[uid] = bet
    win = random.choice([True, False])

    if win:
        set_balance(uid, bal + bet)
        bot.send_message(msg.chat.id, f"✅ Уттуң +{bet}")
    else:
        set_balance(uid, bal - bet)
        bot.send_message(msg.chat.id, f"❌ Утулдуң -{bet}")

# 🎰 SLOT
@bot.message_handler(commands=['slot'])
def slot(msg):
    uid = msg.from_user.id
    try:
        bet = int(msg.text.split()[1])
    except:
        bot.send_message(msg.chat.id, "❌ /slot 100")
        return

    bal = get_balance(uid)
    if bet > bal or bet <= 0:
        bot.send_message(msg.chat.id, "❌ Баланс жетпейт")
        return

    last_bet[uid] = bet
    spin = random.randint(1, 10)

    if spin >= 8:
        win = bet * 2
        set_balance(uid, bal + win)
        bot.send_message(msg.chat.id, f"🎰 Джекпот +{win}")
    else:
        set_balance(uid, bal - bet)
        bot.send_message(msg.chat.id, f"😢 Утулдуң -{bet}")

# 🏴‍☠️ BANDIT
@bot.message_handler(commands=['bandit'])
def bandit(msg):
    uid = msg.from_user.id
    try:
        bet = int(msg.text.split()[1])
    except:
        bot.send_message(msg.chat.id, "❌ /bandit 100")
        return

    bal = get_balance(uid)
    if bet > bal or bet <= 0:
        bot.send_message(msg.chat.id, "❌ Баланс жетпейт")
        return

    last_bet[uid] = bet
    chance = random.randint(1, 100)

    if chance > 60:
        win = bet * 3
        set_balance(uid, bal + win)
        bot.send_message(msg.chat.id, f"💣 Bandit утту +{win}")
    else:
        set_balance(uid, bal - bet)
        bot.send_message(msg.chat.id, f"💀 Bandit утулду -{bet}")

# 🔁 REPEAT
@bot.message_handler(commands=['repeat'])
def repeat(msg):
    uid = msg.from_user.id
    if uid not in last_bet:
        bot.send_message(msg.chat.id, "❌ Акыркы ставка жок")
        return
    bot.send_message(msg.chat.id, f"🔁 Акыркы ставка: {last_bet[uid]}")

# ✖️ DOUBLE
@bot.message_handler(commands=['double'])
def double(msg):
    uid = msg.from_user.id
    if uid not in last_bet:
        bot.send_message(msg.chat.id, "❌ Акыркы ставка жок")
        return
    last_bet[uid] *= 2
    bot.send_message(msg.chat.id, f"✖️ Удвоить: {last_bet[uid]}")

bot.infinity_polling()
      
