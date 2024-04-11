from queue import Full
import telebot
from telebot import types
import tesseractocr
from CREDENTIALS import BOT_KEY
import os
import sqlite3

res_text: any
source_image: any #костыли, но можно обернуть в класс, и хранить их уже локально непосредственно там

bot = telebot.TeleBot(token=BOT_KEY)

conn = sqlite3.connect('db/newdb', check_same_thread=False) #поделючение к бдшке
cursor = conn.cursor()

def db_table_val(user_id: int, mark: int, source_image, res_text: str):
	cursor.execute('INSERT INTO logs (user_id, mark, source_image, res_text) VALUES (?, ?, ?, ?)', (user_id, mark, source_image, res_text)) #функция записи данных в таблицу
	conn.commit()

def convert_to_binary_data(filename):
    # Преобразование данных в двоичный формат
    with open(filename, 'wb') as file:
        blob_data = file.read()
    return blob_data

@bot.message_handler(commands=["start"])
def start(m, res=False):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Хочу загрузить изображение")
    markup.add(item1)
    bot.send_message(m.chat.id, 'Начнем?', reply_markup=markup)

@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.text.strip() == 'Хочу загрузить изображение':
        bot.send_message(message.chat.id, 'Жду ваше изображение')
    if (message.text.strip() == '1' or
        message.text.strip() == '2' or
        message.text.strip() == '3' or
        message.text.strip() == '4' or
        message.text.strip() == '5'):
        user_id = message.from_user.id ## Ид юзера в message.from_user.id получать в момент выставления оценки ЗАПИСАТЬ В БД
        mark = message.text ## это оценочка

        bot.send_message(message.chat.id, 'Спасибо за оценку')
        db_table_val(user_id = user_id, mark = mark, source_image = source_image, res_text = res_text)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Хочу загрузить изображение")
        markup.add(item1)
        bot.send_message(message.chat.id, 'Хотите загрузить изображение?', reply_markup=markup)



@bot.message_handler(content_types=["photo"])
def photo(message):
    file_id = message.photo[-1].file_id
    chat_id = message.chat.id
    ocr_file_Tesseract(bot, file_id, chat_id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    mark1 = types.KeyboardButton("1")
    mark2 = types.KeyboardButton("2")
    mark3 = types.KeyboardButton("3")
    mark4 = types.KeyboardButton("4")
    mark5 = types.KeyboardButton("5")
    markup.add(mark1, mark2, mark3, mark4, mark5)
    bot.send_message(message.chat.id, 'Оцените качество:', reply_markup=markup)


def ocr_file_Tesseract(bot, file_id, chat_id):
    filepath = os.path.expanduser('~') + '/' + file_id + '.jpg'
    bot.send_message(chat_id, "Пожалуйста подождите...")
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(filepath, 'wb') as new_file:
        new_file.write(downloaded_file)
    global source_image
    source_image = downloaded_file## Изображние сохранилось по пути filepath ЗАГРУЗИТЬ В БД

    ocr_text = tesseractocr.read_image_Tesseract(filepath)  
    global res_text
    res_text = str(ocr_text)## Выходной текст в ocr_text ЗАГРУЗИТЬ В БД

    bot.send_message(chat_id=chat_id, text='Вот ваш текст:\n\n' + str(ocr_text))
    os.remove(filepath)


bot.polling(none_stop=True, interval=0)




