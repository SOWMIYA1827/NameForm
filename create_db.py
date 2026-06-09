
import sqlite3

conn = sqlite3.connect("feedback.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    rno TEXT,
    dept TEXT,
    year TEXT,
    domain TEXT,
    experience TEXT,
    skills TEXT,
    specific TEXT
)
""")

conn.commit()
conn.close()

print("Feedback table created successfully!")
