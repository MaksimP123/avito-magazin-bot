import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from telegram import Update, Bot
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
import json

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dispatcher = Dispatcher(bot=bot, update_queue=None, workers=1, use_context=True)

# Обработка команды /start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Бот запущен и работает!")

# 🔥 Обработка всех обычных сообщений
def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Ты сказал: {update.message.text}")

# Подключаем хендлеры
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

# Webhook обработчик
class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        print("📥 Пришёл POST от Telegram")

        try:
            update = Update.de_json(json.loads(post_data.decode("utf-8")), bot)
            dispatcher.process_update(update)
        except Exception as e:
            print(f"❌ Ошибка обработки: {e}")

        self.send_response(200)
        self.end_headers()

# Запуск сервера
def run(server_class=HTTPServer, handler_class=WebhookHandler):
    port = int(os.getenv("PORT", "8080"))
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"✅ Сервер запущен на порту {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
