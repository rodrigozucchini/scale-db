REGIONES = {"AR": "sa-east", "BR": "sa-east", "DE": "eu-central", "ES": "eu-central", "US": "us-east"}
LATENCIA_MS = {("sa-east", "sa-east"): 5, ("sa-east", "eu-central"): 200, ("sa-east", "us-east"): 120,
               ("eu-central", "eu-central"): 5, ("eu-central", "us-east"): 90, ("us-east", "us-east"): 5}
shards = {r: {} for r in set(REGIONES.values())}

def lat(a, b):
    return LATENCIA_MS.get((a, b)) or LATENCIA_MS[(b, a)]

def crear_usuario(uid, pais):
    shards[REGIONES[pais]][uid] = {"pais": pais}

def leer(uid, region_cliente):
    for region, datos in shards.items():
        if uid in datos:
            return region, lat(region_cliente, region)

crear_usuario("ana", "AR")
crear_usuario("hans", "DE")

print("ana desde sa-east:", leer("ana", "sa-east"))    # local, 5 ms
print("hans desde sa-east:", leer("hans", "sa-east"))  # cross-region, 200 ms
