import telebot
import sqlite3

bot = telebot.TeleBot('')


@bot.message_handler(commands=['start'])
def start(message):
    data = sqlite3.connect('text.txt')
    cur = data.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users (id integer primary key, userid varchar(50))')
    data.commit()
    cur.close()
    data.close()


    userid = message.from_user.id

    data = sqlite3.connect('text.txt')
    cur = data.cursor()
    cur.execute("INSERT INTO users (userid) VALUES ('%s')" % (userid))
    cur.execute("DELETE FROM users WHERE rowid NOT IN(SELECT MIN(rowid) FROM users GROUP BY userid)")
    data.commit()
    cur.close()
    data.close()



@bot.channel_post_handler(content_types=['text'])
def channeltext(idtext):
    data = sqlite3.connect('text.txt')
    cur = data.cursor()
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()
    
    info = 0
    for el in users:
        info = el[1]
        bot.send_message(info, idtext.text)

    cur.close()
    data.close()


bot.infinity_polling(timeout=120, long_polling_timeout = 60)
