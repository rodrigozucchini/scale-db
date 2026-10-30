class Nodo:
    def __init__(self):
        self.stock = 10

a, b = Nodo(), Nodo()
particion = False

def comprar(nodo, otro, modo):
    if particion and modo == "CP":
        raise Exception("503: no puedo confirmar con el otro nodo")
    if nodo.stock <= 0:
        raise Exception("sin stock")
    nodo.stock -= 1
    if not particion:
        otro.stock = nodo.stock  # replicación

for modo in ["AP", "CP"]:
    a.stock = b.stock = 1
    particion = True  # se corta la red entre A y B
    vendidas = 0
    for nodo, otro in [(a, b), (b, a)]:  # dos clientes, uno en cada nodo
        try:
            comprar(nodo, otro, modo)
            vendidas += 1
        except Exception as e:
            print(f"  [{modo}] {e}")
    print(f"{modo}: vendí {vendidas} unidades teniendo 1 en stock")
    particion = False

# AP: siempre responde, pero vendió 2 (sobreventa)
# CP: no vendió nada mientras duró la partición, pero nunca vende de más
