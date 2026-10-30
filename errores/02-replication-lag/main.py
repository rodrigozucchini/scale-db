import time

leader = {"datos": {}, "lsn": 0}
replica = {"datos": {}, "lsn": 0}
log = []

def write(key, value):
    leader["lsn"] += 1
    leader["datos"][key] = value
    log.append((leader["lsn"], key, value))
    return leader["lsn"]

def replicar_hasta(lsn):
    for n, k, v in log:
        if replica["lsn"] < n <= lsn:
            replica["datos"][k] = v
            replica["lsn"] = n

write("nombre", "viejo")
replicar_hasta(1)

# ❌ leer siempre de la réplica
mi_lsn = write("nombre", "Ana")
print("❌ réplica:", replica["datos"]["nombre"])  # viejo

# ✅ read-your-writes: si la réplica no llegó a mi LSN, leo del leader
def read(key, min_lsn=0):
    if replica["lsn"] >= min_lsn:
        return "réplica", replica["datos"][key]
    return "leader", leader["datos"][key]

print("✅", read("nombre", min_lsn=mi_lsn))  # ('leader', 'Ana')
replicar_hasta(mi_lsn)
print("✅", read("nombre", min_lsn=mi_lsn))  # ('réplica', 'Ana')
