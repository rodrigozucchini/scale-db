directorio = {}           # tenant_id -> shard
shards = {"shard-1": {}, "shard-2": {}, "shard-dedicado": {}}
cache_directorio = {}     # cache local en la app para no consultar siempre

def shard_de(tenant):
    if tenant not in cache_directorio:
        cache_directorio[tenant] = directorio.setdefault(tenant, "shard-1" if len(directorio) % 2 == 0 else "shard-2")
    return cache_directorio[tenant]

def mover(tenant, destino):
    origen = shard_de(tenant)
    shards[destino][tenant] = shards[origen].pop(tenant)  # copiar datos
    directorio[tenant] = destino                          # actualizar el directorio
    cache_directorio.pop(tenant, None)                    # invalidar caches

for t in ["acme", "globex", "mega-corp"]:
    shards[shard_de(t)][t] = f"datos de {t}"

print({t: shard_de(t) for t in ["acme", "globex", "mega-corp"]})

# mega-corp creció muchísimo: lo aislamos en su propio shard
mover("mega-corp", "shard-dedicado")
print({t: shard_de(t) for t in ["acme", "globex", "mega-corp"]})
