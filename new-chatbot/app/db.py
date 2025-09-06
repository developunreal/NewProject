import sqlite3

def save_chat(prompt, response):
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS chats (prompt TEXT, response TEXT)")
    cursor.execute("INSERT INTO chats (prompt, response) VALUES (?, ?)", (prompt, response))
    conn.commit()
    conn.close()

