class Leader:
    def __init__(self, nombre):
        self.nombre = nombre
        self.datos = {}      # key -> (valor, timestamp, origen)
        self.pendientes = []

    def write(self, key, value, ts):
        self.datos[key] = (value, ts, self.nombre)
        self.pendientes.append((key, value, ts, self.nombre))

    def recibir(self, key, value, ts, origen):
        actual = self.datos.get(key)
        # resolución de conflictos: last-write-wins (gana el timestamp mayor)
        if actual is None or (ts, origen) > (actual[1], actual[2]):
            self.datos[key] = (value, ts, origen)
        else:
            print(f"  [{self.nombre}] conflicto en {key}: descarto '{value}' de {origen}")

def sync(a, b):
    for op in a.pendientes:
        b.recibir(*op)
    for op in b.pendientes:
        a.recibir(*op)
    a.pendientes.clear(); b.pendientes.clear()

eu, us = Leader("EU"), Leader("US")
eu.write("doc:1:titulo", "Hola", ts=100)
us.write("doc:1:titulo", "Hello", ts=101)  # escritura concurrente en otro DC

sync(eu, us)
print("EU:", eu.datos["doc:1:titulo"][0])  # Hello
print("US:", us.datos["doc:1:titulo"][0])  # Hello -> convergen, pero "Hola" se perdió
