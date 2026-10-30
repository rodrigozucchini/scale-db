# Ley de Amdahl: la parte serial (locks, WAL, disco) limita cuánto ganás con más CPUs
PARTE_SERIAL = 0.10   # 10% del trabajo no se paraleliza
TPS_1_CPU = 1000
PRECIO_POR_CPU = 50   # el precio por CPU sube en máquinas grandes

for cpus in [1, 2, 4, 8, 16, 32, 64, 128]:
    speedup = 1 / (PARTE_SERIAL + (1 - PARTE_SERIAL) / cpus)
    precio = cpus * PRECIO_POR_CPU * (1 + cpus / 64)
    print(f"{cpus:>3} CPUs: {TPS_1_CPU * speedup:>6.0f} TPS  ${precio:>7.0f}/mes  (${precio / speedup:.0f} por unidad)")

# Con 128 CPUs no llegás ni a 10x: el techo es 1 / PARTE_SERIAL
