import itertools

class Nodo:
    def __init__(self, nombre):
        self.nombre = nombre
        self.datos = {}

leader = Nodo("leader")
followers = [Nodo("follower-1"), Nodo("follower-2")]
log = []  # log de replicación (WAL)

def write(key, value):
    leader.datos[key] = value
    log.append((key, value))

def replicar():
    # asincrónico: se aplica "más tarde"
    for f in followers:
        for key, value in log:
            f.datos[key] = value

turno = itertools.cycle(followers)

def read(key):
    f = next(turno)  # round robin entre réplicas
    return f.nombre, f.datos.get(key)

write("user:1", "Ana")
print(read("user:1"))  # ('follower-1', None) -> todavía no replicó (lag)
replicar()
print(read("user:1"))  # ('follower-2', 'Ana')
print(read("user:1"))  # ('follower-1', 'Ana')
