# Queries cross-shard (scatter-gather)

Shardeaste `users` por `user_id`. Ahora llega `SELECT * FROM users WHERE email = ?`: el router no sabe en qué shard está, así que pregunta a **todos** y junta las respuestas.

```
query ─┬─► shard 1 (5 ms)
       ├─► shard 2 (6 ms)
       ├─► shard 3 (300 ms, está con GC) ◄── latencia total = la del más lento
       └─► shard 4 (5 ms)
```

Problemas: la latencia la define el shard más lento (**tail latency**), la carga se multiplica por N, y con más shards empeora. Lo mismo pasa con JOINs entre tablas shardeadas por keys distintas y con agregaciones globales.

**Fix:**
- Que las queries frecuentes incluyan la shard key.
- **Índice secundario global**: una tabla `email → user_id` (shardeada por email).
- Denormalizar / co-localizar datos que se consultan juntos en el mismo shard (`orders` shardeado por `user_id`, igual que `users`).
- Para analítica, un data warehouse aparte, no scatter-gather sobre producción.
