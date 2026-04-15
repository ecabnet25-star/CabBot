def delete_scheduled_post_by_index(post_id):
	conn = sqlite3.connect(DB_PATH)
	c = conn.cursor()
	c.execute('DELETE FROM scheduled_posts WHERE id=?', (post_id,))
	conn.commit()
	conn.close()
def get_scheduled_posts():
	conn = sqlite3.connect(DB_PATH)
	c = conn.cursor()
	c.execute('SELECT * FROM scheduled_posts ORDER BY scheduled_time DESC')
	posts = c.fetchall()
	conn.close()
	return posts

import sqlite3
import os
DB_PATH = os.path.join(os.path.dirname(__file__), 'botdata.db')

def init_db():
	conn = sqlite3.connect(DB_PATH)
	c = conn.cursor()
	c.execute('''CREATE TABLE IF NOT EXISTS scheduled_posts (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		text TEXT,
		platforms TEXT,
		scheduled_time TEXT
	)''')
	conn.commit()
	conn.close()

def save_scheduled_post(text, platforms, dt):
	conn = sqlite3.connect(DB_PATH)
	c = conn.cursor()
	c.execute('INSERT INTO scheduled_posts (text, platforms, scheduled_time) VALUES (?, ?, ?)',
			  (text, ','.join(platforms), dt.isoformat()))
	conn.commit()
	conn.close()

init_db()
