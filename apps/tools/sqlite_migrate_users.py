# apps/tools/sqlite_migrate_users.py
import os, sqlite3

# DB yo‘lini aniqlang: DATABASE_URL='sqlite:///unihero.db' bo'lsa:
DB_FILE = os.getenv("SQLITE_PATH") or "unihero.db"
if not os.path.exists(DB_FILE):
    # Loyihada topishga urinib ko'ramiz
    candidates = []
    for root, _, files in os.walk("."):
        for f in files:
            if f.endswith(".db"):
                candidates.append(os.path.join(root, f))
    if not candidates:
        raise SystemExit("*.db topilmadi. SQLITE_PATH env o'rnating yoki DB faylni ko'rsating.")
    DB_FILE = candidates[0]

print("Using DB:", DB_FILE)
conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()

cur.execute("PRAGMA table_info(users)")
cols = {r[1] for r in cur.fetchall()}
to_add = []

def add_if_missing(name, ddl):
    if name not in cols:
        print(f" - adding column: {name}")
        cur.execute(ddl)

add_if_missing("telegram_id", "ALTER TABLE users ADD COLUMN telegram_id INTEGER")
add_if_missing("full_name",   "ALTER TABLE users ADD COLUMN full_name TEXT")
add_if_missing("phone",       "ALTER TABLE users ADD COLUMN phone TEXT")
add_if_missing("username",    "ALTER TABLE users ADD COLUMN username TEXT")
add_if_missing("student_id",  "ALTER TABLE users ADD COLUMN student_id TEXT")
add_if_missing("status",      "ALTER TABLE users ADD COLUMN status TEXT DEFAULT 'pending'")
add_if_missing("lang",        "ALTER TABLE users ADD COLUMN lang TEXT")
add_if_missing("created_at",  "ALTER TABLE users ADD COLUMN created_at DATETIME")

conn.commit()
conn.close()
print("Done.")
