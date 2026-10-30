# Sharding geográfico

Los datos viven en la región del usuario.

**Ejemplo real:** datos de usuarios europeos que por GDPR no pueden salir de la UE; CockroachDB/Spanner con `REGIONAL BY ROW`.

```
usuario AR ─► app LATAM ─► shard São Paulo
usuario DE ─► app EU    ─► shard Frankfurt
```

- ✅ Latencia baja (los datos están cerca) y cumplimiento legal.
- ❌ ¿Qué pasa cuando un usuario se muda, o cuando un usuario de EU le escribe a uno de LATAM? Las queries globales son cross-region y lentas.
