import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Programs table
cursor.execute("""
CREATE TABLE IF NOT EXISTS programs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    status TEXT NOT NULL
)
""")

# Applicants table
cursor.execute("""
CREATE TABLE IF NOT EXISTS applicants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    program_id INTEGER,
    status TEXT NOT NULL,
    FOREIGN KEY (program_id) REFERENCES programs (id)
)
""")

# Insert default programs
cursor.execute("INSERT INTO programs (name, status) VALUES ('AI Intern', 'Active')")
cursor.execute("INSERT INTO programs (name, status) VALUES ('Data Science', 'Active')")

conn.commit()
conn.close()

print("Database initialized successfully")