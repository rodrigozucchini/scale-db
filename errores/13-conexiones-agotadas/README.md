# Agotar las conexiones

La base tiene CPU y RAM de sobra, pero empieza a tirar `FATAL: sorry, too many clients already`. Pasa al escalar la **app** horizontalmente sin pensar en la DB:

```
200 pods × pool de 20 = 4000 conexiones   vs   max_connections = 500
+ lambdas/serverless que abren una conexión por invocación
+ conexiones que quedan "idle in transaction" por un bug
```

En Postgres cada conexión es un proceso (~5–10 MB) y subir `max_connections` a 5000 hace que todo vaya más lento (context switches, contención de locks).

**Fix:**
- Pooler externo (**PgBouncer**, RDS Proxy) en modo transaction: miles de clientes, decenas de conexiones reales.
- Pools chicos por instancia: `tamaño_pool × instancias < max_connections` (dejando margen para admin y réplicas).
- Timeouts: `idle_in_transaction_session_timeout`, `statement_timeout`.
- Monitorear `pg_stat_activity`.

Ver `implementaciones/11-connection-pooling/pool.py`.
