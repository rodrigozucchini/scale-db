import sqlite3
import time

db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE orders (id INTEGER PRIMARY KEY, user_id INTEGER, total REAL)")
db.executemany("INSERT INTO orders (user_id, total) VALUES (?, ?)",
               ((i % 50_000, i * 0.1) for i in range(1_000_000)))

QUERY = "SELECT SUM(total) FROM orders WHERE user_id = ?"

def medir():
    t0 = time.perf_counter()
    for uid in range(100):
        db.execute(QUERY, (uid,)).fetchone()
    return (time.perf_counter() - t0) * 1000

print("plan:", db.execute("EXPLAIN QUERY PLAN " + QUERY, (1,)).fetchone()[3])
print(f"❌ sin índice: {medir():.0f} ms para 100 queries")

db.execute("CREATE INDEX idx_orders_user ON orders(user_id)")
print("plan:", db.execute("EXPLAIN QUERY PLAN " + QUERY, (1,)).fetchone()[3])
print(f"✅ con índice: {medir():.0f} ms para 100 queries")
