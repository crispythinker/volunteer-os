import sqlite3

conn = sqlite3.connect("volunteer_data.db")
cur = conn.cursor()

cur.execute("""
SELECT m.name, p.confidence
FROM members m
JOIN persona_scores p ON m.id = p.member_id
WHERE p.persona = 'Mentor Material'
ORDER BY p.confidence DESC, p.created_at DESC
LIMIT 5
""")

for row in cur.fetchall():
    print(row)

conn.close()
