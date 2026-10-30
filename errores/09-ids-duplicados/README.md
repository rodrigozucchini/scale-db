# IDs autoincrementales con varios shards

Cada shard tiene su propio `SERIAL` / `AUTO_INCREMENT` que arranca en 1. Dos usuarios distintos en shards distintos tienen `id = 1`. Cualquier cosa que asuma IDs globalmente únicos (URLs, caché, eventos, merges) se rompe.

**Fix:**
- **UUID**: únicos sin coordinación. Preferir **UUIDv7** (ordenado por tiempo): los v4 aleatorios fragmentan los índices B-tree.
- **Snowflake ID** (Twitter): 64 bits = timestamp + id de máquina + secuencia. Ordenables, compactos, sin coordinación.
- **Rangos / offsets por shard**: `auto_increment_increment = N`, `offset = shard` (shard 1: 1, 4, 7…; shard 2: 2, 5, 8…). Simple pero rígido al agregar shards.
- Un servicio central de IDs (ticket server, como Flickr): simple, pero es un punto de falla.
