import hashlib
from collections import Counter

N = 4

def h(key):
    # no usar hash() de Python: cambia entre ejecuciones
    return int(hashlib.md5(key.encode()).hexdigest(), 16)

def shard_de(key):
    return h(key) % N

# IDs secuenciales igual se reparten parejo
reparto = Counter(shard_de(f"user:{i}") for i in range(100_000))
for shard, cant in sorted(reparto.items()):
    print(f"shard {shard}: {cant} keys")

# Particiones lógicas fijas -> nodos físicos
PARTICIONES = 1024
nodo_de_particion = {p: f"db-{p % 3}" for p in range(PARTICIONES)}  # 3 nodos hoy

def nodo_de(key):
    return nodo_de_particion[h(key) % PARTICIONES]

print("user:42 ->", nodo_de("user:42"))
