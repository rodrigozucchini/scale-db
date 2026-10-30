# Perder datos en un failover asincrónico

Con replicación **asincrónica**, el leader confirma la escritura al cliente **antes** de que llegue a las réplicas. Si el leader muere en ese momento y se promueve una réplica, esas escrituras confirmadas **no existen** en el nuevo leader.

```
t0  cliente ─► leader: INSERT pedido 1001   ✓ "OK"
t1  leader 💀 (el pedido 1001 nunca llegó a la réplica)
t2  réplica promovida a leader — no tiene el pedido 1001
t3  nuevo INSERT reusa el id 1001 para OTRO pedido 😱
```

Lo peor no es perder el dato, sino que sistemas externos (Redis, emails, el pago en Stripe) ya lo vieron. Caso real: GitHub 2012, un failover de MySQL reusó IDs y mostró datos privados a otros usuarios.

**Fix:**
- **Replicación semi-sincrónica**: al menos una réplica confirma antes de responder al cliente (Postgres `synchronous_standby_names`, MySQL semi-sync).
- Conocer y medir tu **RPO** (cuántos datos aceptás perder) y tu **RTO** (cuánto tardás en recuperarte).
- IDs que no dependan de la secuencia de la DB (ver `09-ids-duplicados`).
- No hacer failover automático "a ciegas": promover la réplica más adelantada.
