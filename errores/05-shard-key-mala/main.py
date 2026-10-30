import bisect
import hashlib
import random
from collections import Counter

# 4 shards por rango de id: [0-250k) [250k-500k) [500k-750k) [750k-∞)
limites = [250_000, 500_000, 750_000, float("inf")]

def por_rango(id_):
    return bisect.bisect_right(limites, id_)

def por_hash(user_id):
    return int(hashlib.md5(str(user_id).encode()).hexdigest(), 16) % 4

# Ya hay 800k pedidos; llegan 10k nuevos con ids autoincrementales
nuevos = range(800_000, 810_000)

print("❌ rango por order_id:", Counter(por_rango(i) for i in nuevos))
print("❌ por país:          ", Counter(random.choices(["AR", "AR", "AR", "AR", "UY", "CL"], k=10_000)))
print("✅ hash(user_id):     ", Counter(por_hash(random.randint(1, 1_000_000)) for _ in nuevos))
