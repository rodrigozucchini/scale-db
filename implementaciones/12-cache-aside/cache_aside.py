import time

db = {"user:1": "Ana"}
db_reads = 0
cache = {}  # key -> (valor, expira)

def db_get(key):
    global db_reads
    db_reads += 1
    return db.get(key)

def get(key, ttl=60):
    if key in cache and cache[key][1] > time.time():
        return cache[key][0]
    valor = db_get(key)
    cache[key] = (valor, time.time() + ttl)
    return valor

def update(key, valor):
    db[key] = valor
    cache.pop(key, None)  # invalidar, no actualizar (evita carreras)

for _ in range(1000):
    get("user:1")
print("lecturas a la DB:", db_reads)  # 1

update("user:1", "Ana María")
print(get("user:1"), "| lecturas a la DB:", db_reads)  # 2
