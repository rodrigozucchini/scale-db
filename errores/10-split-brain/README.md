# Split brain

El leader queda aislado por un problema de red (pero sigue vivo). El resto del cluster cree que murió y promueve a otro. Ahora hay **dos leaders** aceptando escrituras y los datos divergen. Cuando la red vuelve, no hay forma limpia de unirlos.

```
[ leader viejo ] ─╳─ [ follower → nuevo leader ]
   ▲ clientes A          ▲ clientes B
   escriben acá          escriben acá
```

**Fix:**
- **Quorum / consenso** (Raft, Paxos): solo puede ser leader quien tenga el voto de la mayoría. Con 3 nodos, el aislado (1 de 3) no tiene mayoría y deja de aceptar escrituras. Por eso los clusters son de 3 o 5 nodos, nunca 2.
- **Fencing tokens**: cada leader recibe un número de época creciente; el storage rechaza escrituras con un token viejo.
- **STONITH** ("shoot the other node in the head"): apagar al leader viejo antes de promover al nuevo.
- Herramientas: Patroni + etcd (Postgres), Orchestrator (MySQL), los managed services lo hacen por vos.
