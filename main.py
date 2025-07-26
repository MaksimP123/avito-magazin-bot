import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from telegram import Update, Bot
from telegram.ext import Dispatcher, CommandHandler
import json

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dispatcher = Dispatcher(bot=bot, update_queue=None, workers=0, use_context=True)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Бот запущен и работает!")

dispatcher.add_handler(CommandHandler("start", start))

class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        update = Update.de_json(json.loads(post_data.decode("utf-8")), bot)
        dispatcher.process_update(update)
        self.send_response(200)
        self.end_headers()

def run(server_class=HTTPServer, handler_class=WebhookHandler):
    port = int(os.getenv("PORT", "8080"))
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Запуск сервера на порту {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
