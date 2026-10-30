# Leaderless con quorum (estilo Dynamo)

No hay leader: el cliente escribe en varios nodos y lee de varios nodos. Con **N** réplicas, una escritura es exitosa si **W** nodos confirman, y una lectura consulta **R** nodos.

Si `R + W > N`, los nodos que leés y los que escribiste **se solapan**: al menos uno tiene el último valor.

**Ejemplo real:** Cassandra (`CONSISTENCY QUORUM`), DynamoDB, Riak.

```
N=3, W=2, R=2
write ─► [n1 ✓] [n2 ✓] [n3 ✗ caído]
read  ─► [n2 v2] [n3 v1]  → me quedo con la versión más nueva (v2)
```

- ✅ Sin failover: si un nodo cae, sigue funcionando. Ajustás consistencia vs latencia con R y W.
- ❌ Hay que reparar réplicas atrasadas (read repair, anti-entropy) y resolver conflictos.
