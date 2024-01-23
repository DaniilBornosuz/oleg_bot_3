import sqlite3

def sql_start():

  global conn, cur
  conn = sqlite3.connect('bot.db')
  cur = conn.cursor()
  if conn:
    print('Подключение в базе данных...')
    print('База данных подключена')
  else:
    print('Не удалось подключится к базе данных')

  cur.execute(
    """CREATE TABLE IF NOT EXISTS user(
    user_id INTEGER NOT NULL,
    username VARCHAR PRIMARY KEY NOT NULL,
    chat_id INTEGER NOT NULL,
    phone_number VARCHAR NOT NULL,
    state VARCHAR NOT NULL
    );
    """)

  conn.commit()
