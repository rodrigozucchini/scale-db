# Resharding online (sin downtime)

Pasar de N a M shards mientras el sistema sigue recibiendo tráfico. Receta clásica:

1. **Doble escritura**: escribir en el esquema viejo y en el nuevo.
2. **Backfill**: copiar los datos históricos al nuevo esquema.
3. **Verificar**: comparar viejo vs nuevo (conteos, checksums, lecturas sombra).
4. **Cortar lecturas** al nuevo.
5. **Cortar escrituras**: dejar de escribir en el viejo y borrarlo.

**Ejemplo real:** Vitess `MoveTables`/`Reshard`, la migración de Stripe a su DocDB, Figma partiendo Postgres.

- ✅ Sin downtime y con vuelta atrás en cada paso.
- ❌ Lento y delicado: hay que cuidar el orden entre backfill y escrituras nuevas para no pisar datos frescos con viejos.
