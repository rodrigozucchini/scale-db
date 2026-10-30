# Last-write-wins con relojes desincronizados

En multi-leader o leaderless, la resolución más simple de conflictos es "gana el timestamp más alto" (LWW). Pero los relojes de distintas máquinas **no están sincronizados** (NTP tiene errores de ms a segundos), así que "el último" según el reloj puede no ser el último de verdad. Resultado: se pierden escrituras **sin ningún error**.

```
nodo A (reloj adelantado 5s):  t=1005  precio = 100
nodo B (reloj bien):           t=1002  precio = 120   ◄── llegó después, pero pierde
```

**Fix:**
- **Version vectors / vector clocks**: detectan que dos escrituras son concurrentes en vez de elegir una a ciegas; la app (o el usuario) resuelve.
- **CRDTs**: estructuras que siempre se pueden mezclar sin perder nada (contadores, sets, textos colaborativos).
- Relojes con incertidumbre acotada (Spanner TrueTime) o **hybrid logical clocks** (CockroachDB).
- Evitar multi-leader para datos donde un conflicto importa.
