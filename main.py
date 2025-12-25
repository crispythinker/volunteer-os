import pandas as pd
from datetime import datetime, timezone
import sqlite3
import db
from enrich import enrich_bio

df = pd.read_csv("members_raw.csv")

NAME_COL = "member_name"
BIO_COL = "bio_or_comment"

conn = sqlite3.connect("volunteer_data.db")
cur = conn.cursor()

for _, row in df.iterrows():
    member_id = None
    try:
        name = str(row[NAME_COL]).strip().title()
        city = "Unknown"
        created_at = datetime.now(timezone.utc).isoformat()

        cur.execute(
            "INSERT INTO members (name, city, created_at) VALUES (?, ?, ?)",
            (name, city, created_at)
        )
        member_id = cur.lastrowid

        skills, persona, confidence, model_v, out_hash = enrich_bio(row[BIO_COL])

        for skill in skills:
            cur.execute("INSERT OR IGNORE INTO skills (name) VALUES (?)", (skill,))
            cur.execute("SELECT id FROM skills WHERE name=?", (skill,))
            skill_id = cur.fetchone()[0]
            cur.execute(
                "INSERT INTO member_skills VALUES (?, ?)",
                (member_id, skill_id)
            )

        cur.execute(
            """
            INSERT INTO persona_scores
            (member_id, persona, confidence, model_version, prompt_version, output_hash, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (member_id, persona, confidence, "model-v1", model_v, out_hash, created_at)
        )

        cur.execute(
            "INSERT INTO ingestion_meta VALUES (?, ?, ?)",
            (member_id, "SUCCESS", None)
        )

    except Exception as e:
        cur.execute(
            "INSERT INTO ingestion_meta VALUES (?, ?, ?)",
            (member_id, "FAILED", str(e))
        )

conn.commit()
conn.close()

print("Pipeline completed successfully.")
