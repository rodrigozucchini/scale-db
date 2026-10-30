# Dos nodos; el reloj de A está 5 segundos adelantado
reloj = {"A": lambda t: t + 5, "B": lambda t: t}

# ❌ LWW con timestamps de reloj
datos = {}
def lww_write(nodo, t_real, valor):
    ts = reloj[nodo](t_real)
    if "precio" not in datos or ts > datos["precio"][0]:
        datos["precio"] = (ts, valor)

lww_write("A", t_real=1000, valor=100)
lww_write("B", t_real=1002, valor=120)  # escrita DESPUÉS en el tiempo real
print("❌ LWW: precio =", datos["precio"][1], "(la escritura de B se perdió en silencio)")

# ✅ Version vectors: detectan concurrencia en vez de adivinar
def concurrentes(v1, v2):
    return not all(v1.get(k, 0) <= v2.get(k, 0) for k in v1 | v2) and \
           not all(v2.get(k, 0) <= v1.get(k, 0) for k in v1 | v2)

base = {"A": 1, "B": 1}
escritura_a = (dict(base, A=2), 100)   # A modificó sin ver lo de B
escritura_b = (dict(base, B=2), 120)   # B modificó sin ver lo de A
if concurrentes(escritura_a[0], escritura_b[0]):
    print("✅ conflicto detectado, guardo ambas versiones:", [escritura_a[1], escritura_b[1]])

# ✅ CRDT G-Counter: cada nodo suma en su propio casillero, el merge es el máximo
contador_a, contador_b = {"A": 3}, {"B": 5}
merge = {k: max(contador_a.get(k, 0), contador_b.get(k, 0)) for k in contador_a | contador_b}
print("✅ G-Counter: visitas =", sum(merge.values()), "(no se pierde ninguna)")
