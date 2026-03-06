import os
from flask import Flask, request
import telebot

TOKEN = os.getenv("TOKEN")
URL_APP = os.getenv("URL_APP")

bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=URL_APP + "/" + TOKEN)
    return "Bot funcionando", 200


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hola! Soy tu primer bot en Python 🤖")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Escribiste: " + message.text)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))