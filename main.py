import pandas as pd
from datetime import datetime
import sqlite3
from enrich import enrich_bio

df = pd.read_csv("members_raw.csv")
conn = sqlite3.connect("volunteer_data.db")
cur = conn.cursor()

for _, row in df.iterrows():
    try:
        name = str(row["Name"]).strip().title()
        city = str(row.get("City", "Unknown")).title()
        created = datetime.utcnow().isoformat()

        cur.execute(
            "INSERT INTO members (name, city, created_at) VALUES (?, ?, ?)",
            (name, city, created)
        )
        member_id = cur.lastrowid

        skills, persona, confidence = enrich_bio(row["Bio_or_comment"])

        for skill in skills:
            cur.execute("INSERT OR IGNORE INTO skills (name) VALUES (?)", (skill,))
            cur.execute("SELECT id FROM skills WHERE name=?", (skill,))
            skill_id = cur.fetchone()[0]
            cur.execute(
                "INSERT INTO member_skills VALUES (?, ?)",
                (member_id, skill_id)
            )

        cur.execute(
            "INSERT INTO persona_scores VALUES (?, ?, ?, ?, ?)",
            (member_id, persona, confidence, "v1", created)
        )

        cur.execute(
            "INSERT INTO ingestion_meta VALUES (?, ?, ?)",
            (member_id, "SUCCESS", None)
        )

    except Exception as e:
        cur.execute(
            "INSERT INTO ingestion_meta VALUES (?, ?, ?)",
            (member_id if 'member_id' in locals() else None, "FAILED", str(e))
        )

conn.commit()
