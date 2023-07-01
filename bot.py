import telebot
import sqlite3

bot = telebot.TeleBot('%your token/ваш токен%');

# Creating a database and table for subscribers (создание базы данных и таблицы для подписчиков).
conn = sqlite3.connect('news_bot.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS subscribers (
                    id INTEGER PRIMARY KEY,
                    chat_id INTEGER UNIQUE,
                    username TEXT
                )''')

# Create a news table (создание таблицы для новостей).
cursor.execute('''CREATE TABLE IF NOT EXISTS news (
                    id INTEGER PRIMARY KEY,
                    category TEXT,
                    message TEXT
                )''')

conn.commit()

# Registering the /start command to add subscribers to the database (регистрация команды /start, чтобы добавить подписчиков в базу данных).
@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id
    username = message.chat.username

    # Adding a Subscriber to the Database (добавление подписчика в базу данных).
    conn = sqlite3.connect('news_bot.db')
    cursor = conn.cursor()

    cursor.execute("INSERT OR IGNORE INTO subscribers (chat_id, username) VALUES (?, ?)", (chat_id, username))
    conn.commit()

    bot.reply_to(message, "Вы были успешно подписаны на новости.")

# Registering a message handler to receive messages with selected categories from users (регистрация обработчика сообщений, чтобы получать сообщения с выбранными рубриками от пользователей).
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    category = message.text

    # Filtering news by selected category (отфильтровывание новостей по выбранной рубрике).
    conn = sqlite3.connect('news_bot.db')
    cursor = conn.cursor()

    cursor.execute("SELECT message FROM news WHERE category=?", (category,))
    news = cursor.fetchall()

    for news_item in news:
        bot.send_message(chat_id, news_item[0])

    conn.close()

# Creating a keyboard with rubrics to offer a choice to the user (создание клавиатуры с рубриками для предложения выбора пользователю).
keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2)
keyboard.add(*['Рубрика 1', 'Рубрика 2', 'Рубрика 3'])

@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id
    username = message.chat.username

    # Adding a Subscriber to the Database (добавление подписчика в базу данных).
    conn = sqlite3.connect('news_bot.db')
    cursor = conn.cursor()

    cursor.execute("INSERT OR IGNORE INTO subscribers (chat_id, username) VALUES (?, ?)", (chat_id, username))
    conn.commit()

    bot.reply_to(message, "Вы были успешно подписаны на новости.", reply_markup=keyboard)

# Bot launch (запуск бота).
bot.polling()
