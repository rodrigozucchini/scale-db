import bisect

# límite superior (exclusivo) de cada shard
limites = [1000, 2000, float("inf")]
shards = [{} for _ in limites]

def shard_de(user_id):
    return bisect.bisect_right(limites, user_id)

def write(user_id, data):
    shards[shard_de(user_id)][user_id] = data

def range_query(desde, hasta):
    tocados = range(shard_de(desde), shard_de(hasta) + 1)
    print(f"  range {desde}-{hasta} toca shards {list(tocados)}")
    return [v for i in tocados for k, v in shards[i].items() if desde <= k <= hasta]

for uid in [5, 999, 1000, 1500, 2500]:
    write(uid, f"user {uid}")
    print(uid, "-> shard", shard_de(uid))

print(range_query(1, 900))      # un solo shard
print(range_query(900, 1600))   # dos shards
