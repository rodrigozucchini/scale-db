# Replication lag: no ves lo que acabás de escribir

Escribís en el leader y leés de una réplica asincrónica que todavía no recibió el cambio.

```
1. usuario guarda su nombre   ─► leader   (nombre = "Ana")
2. recarga la página          ─► réplica  (nombre = "viejo") 😱
```

**Variantes:**
- **Read-your-writes** roto: no ves tu propio cambio.
- **Monotonic reads** roto: refrescás dos veces, caés en réplicas distintas y el dato "vuelve atrás en el tiempo".

**Fix:** leer del leader durante unos segundos después de escribir (o siempre para los datos del propio usuario); guardar la posición del log (LSN) de tu última escritura y solo leer de réplicas que ya la alcanzaron; fijar cada usuario a una misma réplica (sticky).
