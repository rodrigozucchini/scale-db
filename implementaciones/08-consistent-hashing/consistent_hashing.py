import bisect
import hashlib

def h(s):
    return int(hashlib.md5(s.encode()).hexdigest(), 16)

class Anillo:
    def __init__(self, nodos, vnodes=100):
        self.vnodes = vnodes
        self.anillo = []  # lista ordenada de (hash, nodo)
        for n in nodos:
            self.agregar(n)

    def agregar(self, nodo):
        for i in range(self.vnodes):
            bisect.insort(self.anillo, (h(f"{nodo}#{i}"), nodo))

    def nodo_de(self, key):
        i = bisect.bisect(self.anillo, (h(key),)) % len(self.anillo)
        return self.anillo[i][1]

keys = [f"user:{i}" for i in range(100_000)]

anillo = Anillo(["db-a", "db-b", "db-c", "db-d"])
antes = {k: anillo.nodo_de(k) for k in keys}

anillo.agregar("db-e")
despues = {k: anillo.nodo_de(k) for k in keys}

movidas = sum(antes[k] != despues[k] for k in keys)
print(f"consistent hashing: se movieron {movidas / len(keys):.0%} de las keys")  # ~20%

modulo_movidas = sum(h(k) % 4 != h(k) % 5 for k in keys)
print(f"hash % N:           se movieron {modulo_movidas / len(keys):.0%} de las keys")  # ~80%
