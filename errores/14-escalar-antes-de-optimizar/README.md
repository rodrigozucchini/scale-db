# Escalar antes de optimizar

"La base está lenta, hay que shardear." Y el problema era un índice que faltaba, un `SELECT *` sobre una tabla con un JSON de 2 MB, o un ORM haciendo 1000 queries por página.

Sharding agrega complejidad **para siempre** (joins, transacciones, rebalanceos, operación). Antes de eso, en orden:

1. `EXPLAIN ANALYZE` las queries más caras (`pg_stat_statements`).
2. **Índices** correctos (y borrar los que no se usan: cada índice cuesta en las escrituras).
3. Arreglar N+1 y `SELECT *`.
4. **Caché** para lecturas repetidas.
5. **Réplicas de lectura**.
6. **Particionado de tablas** nativo (Postgres `PARTITION BY RANGE`) y archivar datos viejos.
7. **Escalado vertical**.
8. Recién ahí: sharding.

**Ejemplo:** la query de abajo pasa de recorrer 1M de filas a leer unas pocas, solo con un índice.
