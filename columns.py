from database import engine
from sqlalchemy import text

with engine.begin() as conn:
    conn.execute(text("""CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT ,
                    email TEXT
                    )"""))
with engine.begin() as conn:
    conn.execute(text("""CREATE TABLE IF NOT EXISTS tasks(
                    id INTEGER  PRIMARY KEY AUTOINCREMENT,
                    title TEXT ,
                    description TEXT,
                    status TEXT DEFAULT "todo",
                    owner_id INTEGER ,
                    FOREIGN KEY (owner_id) REFERENCES users(id))"""))
