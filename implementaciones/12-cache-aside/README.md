# Cache-aside delante de la DB

La app consulta la caché; si no está (miss), va a la DB y guarda el resultado. Al escribir, actualiza la DB e **invalida** la key.

**Ejemplo real:** Redis o Memcached delante de Postgres/MySQL. Facebook con Memcached (TAO).

```
read:  app ─► cache (HIT) ✓
       app ─► cache (MISS) ─► DB ─► guardo en cache
write: app ─► DB ─► borro de cache
```

- ✅ Saca la mayoría de las lecturas de la DB. Es lo que más rinde antes de pensar en réplicas o sharding.
- ❌ Invalidación (datos viejos), stampede cuando vence una key caliente.
