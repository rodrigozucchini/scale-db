# Sharding por directorio (lookup)

Un servicio o tabla guarda explícitamente en qué shard está cada key (o cada tenant).

**Ejemplo real:** SaaS multi-tenant: `tenant_id → shard`. Los clientes grandes van a su propio shard; los chicos comparten. Vitess y Slack usan variantes de esto.

```
app ─► directorio: "tenant 42?" ─► "shard-3" ─► shard-3
```

- ✅ Flexibilidad total: podés mover un tenant puntual, aislar a un cliente enorme, balancear a mano.
- ❌ Un salto extra en cada request (se cachea) y el directorio pasa a ser crítico: si se cae, se cae todo.
