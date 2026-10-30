import sqlite3

LATENCIA_RED_MS = 2
db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE autores (id INTEGER PRIMARY KEY, nombre TEXT)")
db.execute("CREATE TABLE posts (id INTEGER PRIMARY KEY, autor_id INTEGER, titulo TEXT)")
db.executemany("INSERT INTO autores VALUES (?, ?)", [(i, f"autor {i}") for i in range(100)])
db.executemany("INSERT INTO posts VALUES (?, ?, ?)", [(i, i % 100, f"post {i}") for i in range(100)])

queries = 0
def q(sql, params=()):
    global queries
    queries += 1
    return db.execute(sql, params).fetchall()

# ❌ N+1
posts = q("SELECT id, autor_id, titulo FROM posts")
for _, autor_id, _ in posts:
    q("SELECT nombre FROM autores WHERE id = ?", (autor_id,))
print(f"❌ N+1:  {queries} queries ≈ {queries * LATENCIA_RED_MS} ms de red")

# ✅ un solo viaje
queries = 0
q("SELECT p.titulo, a.nombre FROM posts p JOIN autores a ON a.id = p.autor_id")
print(f"✅ JOIN: {queries} query  ≈ {queries * LATENCIA_RED_MS} ms de red")
