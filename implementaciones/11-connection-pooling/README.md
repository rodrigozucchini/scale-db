# Connection pooling

Abrir una conexión a la DB es caro (handshake, TLS, auth, y en Postgres **un proceso por conexión**). Un pool mantiene pocas conexiones abiertas y las reusa.

**Ejemplo real:** PgBouncer, RDS Proxy, ProxySQL, HikariCP en Java, el pool de SQLAlchemy.

```
500 clientes ─► [ PgBouncer ] ─► 20 conexiones reales ─► Postgres
```

- ✅ La DB atiende miles de clientes con pocas conexiones. Menos RAM, menos context switches.
- ❌ En modo *transaction pooling* no podés usar features de sesión (`SET`, prepared statements, `LISTEN`) sin cuidado.
