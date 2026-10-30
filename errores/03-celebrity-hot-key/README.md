# Celebrity problem / hot key

El sharding reparte las **keys** parejo, pero no el **tráfico**. Si una key es muchísimo más popular que el resto (el post de una celebridad, el producto del Hot Sale, el partido de la final), todo ese tráfico cae en **un solo shard**.

```
shard 0: ▁▁  shard 1: ▁▁  shard 2: ████████████ (post de Messi)  shard 3: ▁▁
```

Agregar shards **no ayuda**: la key sigue estando en uno solo.

**Fix:**
- **Salting / key splitting**: partir la key caliente en N sub-keys (`post:123#0` … `post:123#63`) en shards distintos. Escribís en una al azar, leés todas y sumás (ideal para contadores).
- **Caché** (y caché local en la app) para las lecturas de hot keys.
- Detectar hot keys en tiempo real y tratarlas aparte (cuentas verificadas, eventos).
