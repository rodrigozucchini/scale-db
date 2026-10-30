import hashlib
import random

N = 16

def shard_de(k):
    return int(hashlib.md5(str(k).encode()).hexdigest(), 16) % N

def latencia_shard():
    # 99% de las veces 5 ms, 1% de las veces 200 ms (GC, disco, vecino ruidoso)
    return 200 if random.random() < 0.01 else 5

shards = [{} for _ in range(N)]
indice_email = {}  # índice global: email -> user_id

for uid in range(10_000):
    email = f"u{uid}@mail.com"
    shards[shard_de(uid)][uid] = email
    indice_email[email] = uid

def por_email_scatter(email):
    lat = max(latencia_shard() for _ in range(N))  # espero a todos
    return next(uid for s in shards for uid, e in s.items() if e == email), lat

def por_email_indice(email):
    uid = indice_email[email]                       # 1 lookup
    return uid, latencia_shard() + latencia_shard() # índice + 1 shard

def lentos(fn, n=5000):
    return sum(fn("u42@mail.com")[1] >= 200 for _ in range(n)) / n

# cada shard es lento solo el 1% de las veces, pero preguntándole a 16...
print(f"❌ scatter-gather: {lentos(por_email_scatter):.0%} de requests lentos | {N} queries por request")
print(f"✅ índice global:  {lentos(por_email_indice):.0%} de requests lentos | 2 queries por request")
