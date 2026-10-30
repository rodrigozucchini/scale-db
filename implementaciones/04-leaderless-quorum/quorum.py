N, W, R = 3, 2, 2
nodos = [{"vivo": True, "datos": {}} for _ in range(N)]

def write(key, value, version):
    oks = 0
    for n in nodos:
        if n["vivo"]:
            n["datos"][key] = (version, value)
            oks += 1
    if oks < W:
        raise Exception(f"write fallido: {oks}/{W} confirmaciones")
    return oks

def read(key):
    respuestas = [n["datos"].get(key, (0, None)) for n in nodos if n["vivo"]][:R]
    if len(respuestas) < R:
        raise Exception("read fallido: no hay quorum")
    ultima = max(respuestas)  # gana la versión más alta
    # read repair: actualizo los nodos que estaban atrasados
    for n in nodos:
        if n["vivo"] and n["datos"].get(key, (0,)) < ultima:
            n["datos"][key] = ultima
    return ultima[1]

write("x", "v1", version=1)
nodos[2]["vivo"] = False            # se cae el nodo 3
write("x", "v2", version=2)         # igual llega a W=2
nodos[2]["vivo"] = True             # vuelve con el dato viejo (v1)
nodos[0]["vivo"] = False            # y se cae otro

print("read:", read("x"))           # v2: n2 tiene v2, n3 tiene v1 -> gana v2
print("n3 reparado:", nodos[2]["datos"]["x"])
nodos[1]["vivo"] = False
try:
    read("x")
except Exception as e:
    print(e)                        # solo 1 vivo < R=2
