import telebot
import requests
from telebot import apihelper
from telebot import types

apihelper.proxy=None
bot=telebot.TeleBot('8616748425:AAFCiG0g6NRoYnUz6_nJaoMOUkQzvQAGc4E')

user_weather_state={}
bot.remove_webhook()
Weather_API_Key='49db1855b34c70e7a77fd4e12e60f601'
@bot.message_handler(commands=['start'])
def main(message):
  bot.send_message(message.chat.id,'Привет я zalupka bot')
    
@bot.message_handler(commands=['menu'])
def menu( message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Что может этот бот?')
    btn2 = types.KeyboardButton('Обращение к юзеру')
    btn3 = types.KeyboardButton('Кто тебя создал?')
    btn4=types.KeyboardButton('Погода')
    markup.add(btn1,btn2,btn3,btn4)
    bot.send_message(message.chat.id,'Смотри че могу', reply_markup=markup)
@bot.message_handler(commands=['weather'])
def weather_command(message):
    user_weather_state[message.chat.id]=True
    bot.reply_to(message,'Напиши название города ')
@bot.message_handler(func=lambda message:message.text=='Погода')
def weather_button(message):
    weather_command(message)

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    chat_id=message.chat.id
    text=message.text
    if user_weather_state.get(chat_id):
        user_weather_state[chat_id]=False
        show_weather(message,text)
        return

    if text=='Что может этот бот?':
        bot.reply_to(message,'Zalupka bot просто лабороторная крыса, пока хз че он сможет')
    elif text=='Обращение к юзеру':
        bot.reply_to(message,f'привет,{message.from_user.first_name}!')
    elif text=='Кто тебя создал?':
        bot.reply_to(message,'Меня создал великий Никита_Хоумлендер67')
    else:
        pass
def show_weather(message,city):
    try:
        url=f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={Weather_API_Key}&units=metric&lang=ru'
        response=requests.get(url)
        data=response.json()
        if data.get('cod')!=200:
            bot.reply_to(message,f'Город {city} отсутсвует, напиши настоящий город.\nЧтобы найти город напиши /weather или нажми на кнопку Погода')
            return
        temp=data['main']['temp']
        feels_like=data['main']['feels_like']
        humidity=data['main']['humidity']
        wind_speed=data['wind']['speed']
        description=data['weather'][0]['description']
        answer=f'{city.capitalize()}\n'
        answer+=f'Температура {temp}°C. Ощущается как {feels_like}°C\n'
        answer += f'Влажность {humidity}%\n'
        answer += f'{description.capitalize()}'

        bot.reply_to(message, answer, parse_mode='Markdown')
        bot.reply_to(message,'для нового города нажми на комнаду /weather еще раз')
    except Exception as e:
        bot.reply_to(message,f' Ошибка: не удалось получить погоду.\n{e}')


bot.polling(none_stop=True)
