import hashlib

def h(k):
    return int(hashlib.md5(k.encode()).hexdigest(), 16)

viejo = [{} for _ in range(2)]
nuevo = [{} for _ in range(4)]
fase = "viejo"  # viejo -> doble_escritura -> leer_nuevo -> nuevo

def write(k, v):
    if fase in ("viejo", "doble_escritura", "leer_nuevo"):
        viejo[h(k) % 2][k] = v
    if fase in ("doble_escritura", "leer_nuevo", "nuevo"):
        nuevo[h(k) % 4][k] = v

def read(k):
    tabla, n = (viejo, 2) if fase in ("viejo", "doble_escritura") else (nuevo, 4)
    return tabla[h(k) % n].get(k)

def backfill():
    for shard in viejo:
        for k, v in list(shard.items()):
            nuevo[h(k) % 4].setdefault(k, v)  # setdefault: no pisar escrituras más nuevas

for i in range(1000):
    write(f"k{i}", i)

fase = "doble_escritura"
write("k5", "actualizado durante la migración")
backfill()

faltan = sum(read(f"k{i}") != nuevo[h(f"k{i}") % 4].get(f"k{i}") for i in range(1000))
print("diferencias viejo vs nuevo:", faltan)  # 0

fase = "leer_nuevo"
print("k5 ->", read("k5"))
fase = "nuevo"
write("k6", "solo en el nuevo")
print("k6 ->", read("k6"), "| keys por shard:", [len(s) for s in nuevo])
