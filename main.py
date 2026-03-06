import os
from flask import Flask, request
import telebot

TOKEN = os.getenv("TOKEN")
URL_APP = os.getenv("URL_APP")

bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

# Telegram enviará aquí los mensajes
@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "ok", 200


# Ruta principal para configurar webhook
@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=URL_APP + "/" + TOKEN)
    return "Bot funcionando", 200


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hola! Soy tu bot 🤖")


@bot.message_handler(func=lambda message: True)
def echo(message):
    bot.send_message(message.chat.id, "Escribiste: " + message.text)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))