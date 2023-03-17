import telebot
from config import keys, Token
from extensions import ConververtionException, CriptiConverter

bot = telebot.TeleBot(Token)
@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Для того, чтобы начать работу введите сообщение в формате: \n <имя валюты, цену которой Вы хотите узнать> \
    <имя валюты, в которой надо узнать цену первой валюты> \
    <количество первой валюты> \n Доступные валюты: /values'

    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты'
    for key in keys.keys():
        text = '\n '.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:

        values = message.text.split(' ')

        if len(values) != 3:
            raise ConververtionException('Много параметров')

        quote, base, amount = values
        total_base = CriptiConverter.get_price(quote, base, amount)
    except ConververtionException as e:
        bot.reply_to(message, f'Ошибка пользователя \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду \n{e}')

    else:
        sum_val = int(amount)*total_base
        text = f'Цена {amount} {quote} в {base} - {sum_val}'
        bot.send_message(message.chat.id, text)

bot.polling()