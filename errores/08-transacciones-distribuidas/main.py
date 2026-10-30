shard_a = {"ana": 100}
shard_b = {"beto": 0}

def debitar(cuenta, monto):
    if shard_a[cuenta] < monto:
        raise Exception("saldo insuficiente")
    shard_a[cuenta] -= monto

def acreditar(cuenta, monto, falla=False):
    if falla:
        raise Exception("shard B caído")
    shard_b[cuenta] += monto

# ❌ dos escrituras sueltas
try:
    debitar("ana", 30)
    acreditar("beto", 30, falla=True)
except Exception as e:
    print("❌", e, "| total en el sistema:", shard_a["ana"] + shard_b["beto"])  # 70: desaparecieron 30

# ✅ saga: cada paso tiene su compensación
shard_a["ana"] = 100

def saga(pasos):
    hechos = []
    for accion, compensacion in pasos:
        try:
            accion()
            hechos.append(compensacion)
        except Exception as e:
            print("  falló:", e, "-> compensando")
            for comp in reversed(hechos):
                comp()
            return False
    return True

ok = saga([
    (lambda: debitar("ana", 30), lambda: shard_a.__setitem__("ana", shard_a["ana"] + 30)),
    (lambda: acreditar("beto", 30, falla=True), lambda: None),
])
print("✅ saga ok:", ok, "| total en el sistema:", shard_a["ana"] + shard_b["beto"])  # 100
