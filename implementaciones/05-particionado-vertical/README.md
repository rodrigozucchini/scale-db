# Particionado vertical / federación

Partir por **tablas o columnas**: cada dominio en su propia base. Usuarios en una DB, pedidos en otra, analytics en otra.

**Ejemplo real:** lo que pasa naturalmente con microservicios (una DB por servicio). También sacar columnas pesadas (`avatar_blob`, `descripcion_larga`) a otra tabla.

```
antes:   [ DB: users, orders, payments, analytics ]
después: [ DB users ]  [ DB orders ]  [ DB payments ]  [ DB analytics ]
```

- ✅ Cada base es más chica, se escala y se tunea por separado. Fácil de entender.
- ❌ No hay JOINs ni transacciones entre bases. Una tabla puede seguir creciendo demasiado (ahí toca sharding).
