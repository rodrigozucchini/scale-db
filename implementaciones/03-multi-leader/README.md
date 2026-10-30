# Replicación multi-leader

Varios nodos aceptan escrituras (típicamente uno por datacenter) y se replican entre ellos.

**Ejemplo real:** MySQL Group Replication en multi-primary, CouchDB, apps offline-first (cada celular es un "leader").

```
usuarios EU ──► [ leader EU ] ◄──replicación──► [ leader US ] ◄── usuarios US
```

- ✅ Escrituras locales con baja latencia; un datacenter caído no frena al otro.
- ❌ **Conflictos**: dos leaders modifican lo mismo a la vez. Hay que resolverlos (last-write-wins, merge, CRDTs).
