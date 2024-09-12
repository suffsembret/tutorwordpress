import telebot
from telebot import types
from Token import TELEGRAM_TOKEN
from acs import gantissid
from acs import gantipw

print("Bot Jalan...")
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Dictionary untuk menyimpan state pengguna
sufyan_state = {}

# Menangani perintah /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(types.KeyboardButton("Ubah SSID nama WiFi"))
    markup.add(types.KeyboardButton("Ubah Password WiFi"))
    markup.add(types.KeyboardButton("Ubah Pw dan SSID"))
    markup.add(types.KeyboardButton("Cek status perangkat"))
    markup.add(types.KeyboardButton("Complain"))
    bot.reply_to(message, "Selamat datang di Bot sufsembret! Silakan pilih menu:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ["Ubah SSID nama WiFi", "Ubah Password WiFi", "Ubah Pw dan SSID",  "Cek status perangkat", "Complain" ])
def start(message):
    chat_id = message.chat.id
    print(message.text)
    
    if message.text == "Ubah SSID nama WiFi":
        step_key = "sn_ssid"
    elif message.text == "Ubah Password WiFi":
        step_key = "sn_pw"
    elif message.text == "Ubah Pw dan SSID":
        step_key = "sn_pw_ssid"
    
    sufyan_state[chat_id] = {"step" : step_key}
    print(sufyan_state)
    bot.reply_to(message, "Masukkan serial number")

@bot.message_handler(func=lambda message: sufyan_state.get(message.chat.id, {}).get("step") == "sn_ssid")
def serial_number(message):
    chat_id = message.chat.id
    sn = message.text.strip()
    
    sufyan_state[chat_id] = {"step" : "isi_ssid", "sn": sn}
    print(sufyan_state)
    bot.reply_to(message, "Masukkan SSID baru")
    
@bot.message_handler(func=lambda message: sufyan_state.get(message.chat.id, {}).get("step") == "isi_ssid")
def isi_ssidoke(message):
    chat_id = message.chat.id
    ssid = message.text.strip()
    
    data = sufyan_state[chat_id]
    
    result = gantissid(data, ssid)
    
    print(result)
  
    bot.reply_to(message, f"SSID berhasil diubah menjadi {ssid}")
    sufyan_state.pop(chat_id)  # Reset state setelah selesai

@bot.message_handler(func=lambda message: sufyan_state.get(message.chat.id, {}).get("step") == "sn_pw")
def serial_number(message):
    chat_id = message.chat.id
    sn = message.text.strip()
    
    sufyan_state[chat_id] = {"step" : "isi_pw", "sn": sn}
    print(sufyan_state)
    bot.reply_to(message, "Masukkan password baru")
    
@bot.message_handler(func=lambda message: sufyan_state.get(message.chat.id, {}).get("step") == "isi_pw")
def isi_pwoke(message):
    chat_id = message.chat.id
    pw = message.text.strip()
    
    if len(pw) < 8:
        bot.reply_to(message, "Password minimal 8 karakter, mohon masukkan ulang password")
    else:
        print(pw)
        bot.reply_to(message, f"Password berhasil diubah menjadi {pw}")
        sufyan_state.pop(chat_id)  # Reset state setelah selesai

# Penanganan "Ubah Pw dan SSID"
@bot.message_handler(func=lambda message: sufyan_state.get(message.chat.id, {}).get("step") == "sn_pw_ssid")
def serial_number_pw_ssid(message):
    chat_id = message.chat.id
    sn = message.text.strip()
    
    sufyan_state[chat_id] = {"step": "isi_ssid_pw", "sn": sn}
    print(sufyan_state)
    bot.reply_to(message, "Masukkan SSID baru")

#ubh pw
@bot.message_handler(func=lambda message: sufyan_state.get(message.chat.id, {}).get("step") == "isi_ssid_pw")
def isi_ssid_pw(message):
    chat_id = message.chat.id
    ssid = message.text.strip()
    
    sufyan_state[chat_id]["ssid"] = ssid
    sufyan_state[chat_id]["step"] = "isi_pw_ssid"
    print(sufyan_state)
    bot.reply_to(message, "Masukkan password baru")

@bot.message_handler(func=lambda message: sufyan_state.get(message.chat.id, {}).get("step") == "isi_pw_ssid")
def isi_pw_ssid(message):
    chat_id = message.chat.id
    pw = message.text.strip()
    
    if len(pw) < 8:
        bot.reply_to(message, "Password minimal 8 karakter, mohon masukkan ulang password")
    else:
        ssid = sufyan_state[chat_id]["ssid"]
        print(f"SSID: {ssid}, Password: {pw}")
        bot.reply_to(message, f"SSID berhasil diubah menjadi {ssid} dan password berhasil diubah menjadi {pw}")
        sufyan_state.pop(chat_id)  # Reset state setelah selesai

bot.polling(none_stop=True)
