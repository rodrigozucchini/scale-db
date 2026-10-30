import sqlite3

# una conexión por dominio
users_db = sqlite3.connect(":memory:")
orders_db = sqlite3.connect(":memory:")

users_db.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, nombre TEXT)")
orders_db.execute("CREATE TABLE orders (id INTEGER PRIMARY KEY, user_id INTEGER, total REAL)")

users_db.executemany("INSERT INTO users VALUES (?, ?)", [(1, "Ana"), (2, "Beto")])
orders_db.executemany("INSERT INTO orders VALUES (?, ?, ?)", [(1, 1, 50), (2, 1, 30), (3, 2, 99)])

# Ya no podés hacer: SELECT ... FROM users JOIN orders ...
# El "join" se hace en la aplicación:
ordenes = orders_db.execute("SELECT user_id, SUM(total) FROM orders GROUP BY user_id").fetchall()
ids = [u for u, _ in ordenes]
nombres = dict(users_db.execute(
    f"SELECT id, nombre FROM users WHERE id IN ({','.join('?' * len(ids))})", ids))

for user_id, total in ordenes:
    print(nombres[user_id], total)
