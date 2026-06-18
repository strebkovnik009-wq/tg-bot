from flask import Flask
import threading
import tg

app = Flask(__name__)

@app.route('/')
def home():
    return "Бот работает!", 200

@app.route('/health')
def health():
    return "OK", 200

if __name__ == '__main__':

    bot_thread = threading.Thread(target=tg.bot.polling, kwargs={'non_stop': True}, daemon=True)
    bot_thread.start()

    app.run(host='0.0.0.0', port=8080)
