# Sharding por hash

Se hashea la shard key y se usa el resultado para elegir el shard: `shard = hash(key) % N`.

**Ejemplo real:** Redis Cluster (16384 slots con CRC16), DynamoDB, Cassandra (con token ring), Citus.

```
hash("user:1") % 4 = 2  ─► shard 2
hash("user:2") % 4 = 0  ─► shard 0
```

- ✅ Distribución pareja aunque las keys sean secuenciales. Sin hot spots por orden.
- ❌ Las range queries tienen que ir a **todos** los shards. Y cambiar N mueve casi todas las keys (ver `errores/06-resharding-modulo`).

Truco habitual: usar **muchas particiones lógicas** fijas (ej. 1024) y asignarlas a pocos nodos. Al crecer movés particiones enteras, no keys sueltas.
