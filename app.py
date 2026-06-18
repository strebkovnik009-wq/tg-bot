import os
from flask import Flask
import threading
import tg

app = Flask(__name__)

@app.route('/')
def home():
    return "Бот работает!", 200

if __name__ == '__main__':
    # Берем порт из переменной Render или используем 8080
    port = int(os.environ.get('PORT', 8080))
    
    # Запускаем бота в фоне
    bot_thread = threading.Thread(target=tg.bot.polling, kwargs={'non_stop': True}, daemon=True)
    bot_thread.start()
    
    # Запускаем Flask на нужном порту
    app.run(host='0.0.0.0', port=port)
