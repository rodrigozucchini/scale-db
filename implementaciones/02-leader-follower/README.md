# Replicación leader–follower

Todas las escrituras van al **leader**. Los **followers** reciben una copia (el log de cambios) y atienden lecturas.

**Ejemplo real:** Postgres streaming replication, RDS read replicas, MySQL replicas.

```
escrituras ──► [ leader ] ──log──► [ follower 1 ] ◄── lecturas
                          └──log──► [ follower 2 ] ◄── lecturas
```

- ✅ Escala lecturas linealmente (agregás réplicas). Las réplicas sirven de respaldo para failover.
- ❌ No escala escrituras. Con replicación asincrónica hay **lag**: las réplicas pueden estar atrasadas.
