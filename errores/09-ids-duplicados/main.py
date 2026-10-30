import itertools
import threading
import time

# ❌ cada shard con su autoincremental
seq = {"shard-1": itertools.count(1), "shard-2": itertools.count(1)}
ids = [next(seq["shard-1"]), next(seq["shard-1"]), next(seq["shard-2"]), next(seq["shard-2"])]
print("❌ ids:", ids, "| duplicados:", len(ids) - len(set(ids)))

# ✅ Snowflake: 41 bits de timestamp | 10 bits de máquina | 12 bits de secuencia
EPOCH = 1_700_000_000_000

class Snowflake:
    def __init__(self, machine_id):
        self.machine_id = machine_id
        self.ultimo_ms = -1
        self.secuencia = 0
        self.lock = threading.Lock()

    def next_id(self):
        with self.lock:
            ms = int(time.time() * 1000)
            if ms == self.ultimo_ms:
                self.secuencia = (self.secuencia + 1) & 0xFFF
                if self.secuencia == 0:          # 4096 ids en este ms: esperar al siguiente
                    while ms <= self.ultimo_ms:
                        ms = int(time.time() * 1000)
            else:
                self.secuencia = 0
            self.ultimo_ms = ms
            return ((ms - EPOCH) << 22) | (self.machine_id << 12) | self.secuencia

gens = [Snowflake(1), Snowflake(2)]
ids = [g.next_id() for _ in range(50_000) for g in gens]
print("✅ snowflake: generados", len(ids), "| duplicados:", len(ids) - len(set(ids)))
print("   ejemplo:", ids[0], "-> máquina", (ids[0] >> 12) & 0x3FF)
