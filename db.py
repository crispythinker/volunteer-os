import sqlite3

conn = sqlite3.connect("volunteer_data.db")
cur = conn.cursor()

cur.executescript("""
CREATE TABLE IF NOT EXISTS members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    city TEXT,
    created_at TEXT
);

CREATE TABLE IF NOT EXISTS skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS member_skills (
    member_id INTEGER,
    skill_id INTEGER
);

CREATE TABLE IF NOT EXISTS persona_scores (
    member_id INTEGER,
    persona TEXT,
    confidence REAL,
    model_version TEXT,
    created_at TEXT
);

CREATE TABLE IF NOT EXISTS ingestion_meta (
    member_id INTEGER,
    status TEXT,
    error TEXT
);
""")

conn.commit()
