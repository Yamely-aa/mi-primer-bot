import os
from flask import Flask, request
import telebot

TOKEN = os.getenv("TOKEN")
URL_APP = os.getenv("URL_APP")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Telegram enviará los mensajes aquí
@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "ok", 200


@app.route("/")
def index():
    return "Bot activo", 200


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hola! Soy tu bot 🤖")


@bot.message_handler(func=lambda message: True)
def echo(message):
    bot.send_message(message.chat.id, "Escribiste: " + message.text)


# Registrar webhook al iniciar
bot.remove_webhook()
bot.set_webhook(url=URL_APP + "/" + TOKEN)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))