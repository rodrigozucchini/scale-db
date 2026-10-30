# Shard key mala

La shard key decide todo, y cambiarla después es carísimo. Las malas más comunes:

- **Monotónica** (ID autoincremental, `created_at`) con sharding por rango: todas las escrituras nuevas van al **último** shard. Los demás miran.
- **Baja cardinalidad** (`pais`, `status`, `plan`): solo hay unos pocos valores posibles, así que nunca vas a poder tener más shards que valores, y uno ("AR", "activo") se lleva casi todo.
- **No coincide con el patrón de acceso**: shardeás por `order_id` pero siempre consultás "pedidos del usuario X" → todas las queries van a todos los shards.

```
❌ rango por created_at:   shard 1: ▁  shard 2: ▁  shard 3: ████ (hoy)
✅ hash(user_id):          shard 1: ██ shard 2: ██ shard 3: ██
```

**Fix:** alta cardinalidad + distribución pareja + que las queries frecuentes la incluyan. Normalmente `tenant_id` / `user_id` (hasheado).
