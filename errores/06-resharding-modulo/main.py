import hashlib

def h(k):
    return int(hashlib.md5(k.encode()).hexdigest(), 16)

keys = [f"user:{i}" for i in range(100_000)]

def movidas(antes, despues):
    return sum(antes(k) != despues(k) for k in keys) / len(keys)

print(f"❌ % 4 -> % 5:  {movidas(lambda k: h(k) % 4, lambda k: h(k) % 5):.0%}")
print(f"   % 4 -> % 8:  {movidas(lambda k: h(k) % 4, lambda k: h(k) % 8):.0%}")

# ✅ 1024 slots fijos; al sumar un nodo se le reasignan algunos slots
SLOTS = 1024
asignacion_4 = {s: s % 4 for s in range(SLOTS)}
asignacion_5 = dict(asignacion_4)
for s in range(0, SLOTS, 5):  # el nodo nuevo se lleva 1/5 de los slots
    asignacion_5[s] = 4
print(f"✅ slots fijos: {movidas(lambda k: asignacion_4[h(k) % SLOTS], lambda k: asignacion_5[h(k) % SLOTS]):.0%}")
