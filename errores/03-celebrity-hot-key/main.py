import hashlib
import random
from collections import Counter

N = 8

def shard_de(key):
    return int(hashlib.md5(key.encode()).hexdigest(), 16) % N

# 90% de los likes van al post de la celebridad, 10% a posts normales
def trafico():
    for _ in range(100_000):
        yield "post:messi" if random.random() < 0.9 else f"post:{random.randint(1, 10_000)}"

# ❌ sin salting
carga = Counter(shard_de(k) for k in trafico())
print("❌ carga por shard:", [carga[i] for i in range(N)])

# ✅ salting: la hot key se parte en 64 sub-keys
HOT_KEYS = {"post:messi"}
SALT = 64

def key_real(key):
    return f"{key}#{random.randrange(SALT)}" if key in HOT_KEYS else key

carga = Counter(shard_de(key_real(k)) for k in trafico())
print("✅ carga por shard:", [carga[i] for i in range(N)])

# Leer el contador implica sumar las 64 sub-keys
contadores = Counter(key_real("post:messi") for _ in range(1000))
print("likes totales:", sum(contadores[f"post:messi#{i}"] for i in range(SALT)))
