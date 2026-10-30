# CQRS / modelos de lectura denormalizados

Separar el modelo de **escritura** (normalizado, transaccional) del de **lectura** (denormalizado, precalculado, optimizado para la consulta). Se sincronizan por eventos o CDC (change data capture).

**Ejemplo real:** escribir en Postgres y leer búsquedas desde Elasticsearch; Debezium leyendo el WAL y alimentando otras bases; vistas materializadas.

```
comando ─► [ DB escritura ] ─► eventos/CDC ─► [ DB lectura (denormalizada) ] ◄─ queries
```

- ✅ Cada lado se escala por separado. Las lecturas pesadas no compiten con las escrituras. Sin JOINs al leer.
- ❌ Consistencia eventual entre los dos modelos y más piezas que operar.
