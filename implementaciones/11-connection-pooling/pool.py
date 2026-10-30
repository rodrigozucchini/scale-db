import queue
import threading
import time

MAX_CONNECTIONS = 100  # max_connections de Postgres
abiertas = 0
pico = 0
rechazadas = 0
creadas = 0
lock = threading.Lock()

def conectar():
    global abiertas, pico, rechazadas, creadas
    with lock:
        if abiertas >= MAX_CONNECTIONS:
            rechazadas += 1
            raise Exception("FATAL: too many connections")
        abiertas += 1
        creadas += 1
        pico = max(pico, abiertas)
    time.sleep(0.05)  # handshake + TLS + auth + fork del proceso
    return object()

def cerrar():
    global abiertas
    with lock:
        abiertas -= 1

def query():
    time.sleep(0.01)

class Pool:
    def __init__(self, tamaño):
        self.libres = queue.Queue()
        for _ in range(tamaño):
            self.libres.put(conectar())

    def ejecutar(self):
        conn = self.libres.get()  # espera si no hay libres
        try:
            query()
        finally:
            self.libres.put(conn)

def sin_pool():
    try:
        conectar()
    except Exception:
        return
    query()
    cerrar()

def correr(fn, n=500):
    hilos = [threading.Thread(target=fn) for _ in range(n)]
    for h in hilos: h.start()
    for h in hilos: h.join()

correr(sin_pool)
print(f"sin pool: {creadas} conexiones creadas, pico {pico}, {rechazadas} requests rechazados")

abiertas = pico = rechazadas = creadas = 0
pool = Pool(20)
correr(pool.ejecutar)
print(f"con pool: {creadas} conexiones creadas, pico {pico}, {rechazadas} requests rechazados")
