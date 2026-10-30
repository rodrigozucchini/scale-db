# Sharding por rango

Cada shard tiene un rango continuo de la shard key.

**Ejemplo real:** HBase, Bigtable, MongoDB con range sharding, CockroachDB (divide los rangos automáticamente cuando crecen).

```
user_id    1 – 1000  ─► shard A
user_id 1001 – 2000  ─► shard B
user_id 2001 – ∞     ─► shard C
```

- ✅ Las consultas por rango (`BETWEEN`, "pedidos de octubre") tocan uno o pocos shards.
- ❌ Hot spots: si la key es secuencial (IDs autoincrementales, fechas), todas las escrituras nuevas van al último shard. Ver `errores/05-shard-key-mala`.
