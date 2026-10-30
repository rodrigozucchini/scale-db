# Escalado vertical (scale up)

Misma base, máquina más grande: más CPU, más RAM (para que los índices y los datos calientes entren en memoria), discos más rápidos.

**Ejemplo real:** pasar una RDS de `db.r6g.large` (16 GB) a `db.r6g.8xlarge` (256 GB).

```
[ 4 vCPU / 16 GB ] ──► [ 32 vCPU / 256 GB ]
```

- ✅ Cero cambios en el código. Siempre es lo primero.
- ❌ Tiene techo, el precio crece más rápido que la capacidad y sigue siendo un único punto de falla.

El ejemplo muestra que no escala lineal: duplicar CPUs no duplica el throughput (locks, disco, contención).
