# `hash % N` y el resharding

Con `shard = hash(key) % N`, al cambiar N cambia el resultado para casi todas las keys. Pasar de 4 a 5 shards mueve ~80% de los datos (y en una caché, es un miss masivo de golpe).

```
hash = 13:   13 % 4 = 1   →   13 % 5 = 3   (se mueve)
```

**Fix:**
- **Consistent hashing**: agregar un nodo mueve solo ~1/N (ver `implementaciones/08-consistent-hashing`).
- **Particiones lógicas fijas**: definir muchas particiones desde el día uno (Redis Cluster usa 16384 slots) y mover particiones enteras entre nodos.
- Si igual usás `% N`, crecer duplicando (4 → 8): cada key se queda o se mueve a un único shard nuevo (50%).
