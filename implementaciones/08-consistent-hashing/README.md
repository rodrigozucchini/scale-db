# Consistent hashing

Nodos y keys se ubican en un **anillo** de hash. Cada key va al primer nodo que encuentra yendo en sentido horario.

Al agregar un nodo, solo se mueven las keys del arco que ese nodo "roba" (~1/N), no todas.

**Nodos virtuales**: cada nodo físico aparece muchas veces en el anillo para que la distribución sea pareja (y para poder darle más peso a máquinas más grandes).

**Ejemplo real:** Cassandra, DynamoDB, Riak, balanceadores como Envoy (ring hash) y clientes de Memcached.

```
        nodo A
      ╱        ╲
 key1 ●          ● nodo B
     │            │
 nodo D ●      ● key2 ─► va a nodo C
      ╲        ╱
        nodo C
```
