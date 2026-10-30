# Escalado de bases de datos

Cuando una sola base de datos ya no da abasto (demasiadas lecturas, demasiadas escrituras, demasiados datos o demasiadas conexiones), hay dos caminos:

```
Vertical (scale up):    [ DB chica ] ──► [ DB GIGANTE ]        más CPU, RAM, disco
Horizontal (scale out): [ DB ] ──► [ DB ] [ DB ] [ DB ] [ DB ] más máquinas
```

- **Vertical**: misma base, máquina más grande. Simple, cero cambios en el código, pero tiene techo (físico y de precio) y sigue siendo un único punto de falla.
- **Horizontal**: repartir el trabajo entre varias máquinas. Escala "infinito", pero trae todos los problemas de los sistemas distribuidos: consistencia, particiones de red, rebalanceo, joins entre máquinas, etc.

La regla práctica: **exprimí lo vertical primero** (índices, queries, caché, pool de conexiones, máquina más grande) y escalá horizontal cuando de verdad no quede otra. Una sola Postgres bien tuneada aguanta muchísimo más de lo que la gente cree.

## Qué estás escalando

No todos los problemas de escala son iguales, y cada uno se resuelve distinto:

| Cuello de botella | Síntoma | Solución típica |
|---|---|---|
| **Lecturas** | CPU alta por SELECTs, latencia de lectura | Índices, caché, **réplicas de lectura** |
| **Escrituras** | Locks, WAL saturado, disco al 100% | **Sharding**, batching, colas |
| **Tamaño de datos** | Disco lleno, índices que no entran en RAM | **Sharding**, particionado, archivado |
| **Conexiones** | `too many connections` | **Connection pooling** (PgBouncer, ProxySQL) |
| **Geografía** | Usuarios lejos = latencia alta | Réplicas regionales, sharding geográfico |

## Conceptos clave

| Concepto | Qué es |
|---|---|
| **Réplica** | Copia completa de los datos en otra máquina. Sirve para leer y para tener respaldo. |
| **Leader / Follower** | El leader (primary/master) recibe las escrituras; los followers (replicas/slaves) las copian. |
| **Replication lag** | Cuánto atrasado está un follower respecto del leader. |
| **Partición / Shard** | Un pedazo de los datos. Cada shard tiene un subconjunto de las filas. |
| **Shard key** | La columna que decide en qué shard va cada fila (ej. `user_id`). La decisión más importante de todas. |
| **Particionado vertical** | Partir por **columnas o tablas** (usuarios en una DB, pagos en otra). |
| **Particionado horizontal** | Partir por **filas** (usuarios 1–1M en un shard, 1M–2M en otro). Eso es sharding. |
| **Rebalanceo / Resharding** | Mover datos entre shards cuando agregás o sacás máquinas. |
| **Quorum** | Cantidad mínima de nodos que tienen que responder para que una operación cuente. |
| **Failover** | Promover un follower a leader cuando el leader se cae. |
| **Hot spot / Hot key** | Un shard o una key que recibe muchísimo más tráfico que el resto. |

## Teorema CAP (y PACELC)

En un sistema distribuido, cuando hay una **partición de red** (P) —y siempre va a haber— tenés que elegir:

- **C (Consistencia)**: todos ven el mismo dato; si no puedo garantizarlo, devuelvo error.
- **A (Disponibilidad)**: siempre respondo, aunque sea con un dato viejo.

```
            Partición de red entre nodo A y nodo B
  CP:  "no sé si tengo el último dato → error"       (ZooKeeper, etcd, HBase, Spanner)
  AP:  "te doy lo que tengo, quizás viejo"           (Cassandra, DynamoDB, Riak, CouchDB)
```

No es "elegí 2 de 3": **P no es opcional**. La elección real es C o A *durante* una partición.

**PACELC** completa la idea: si hay **P**artición elegís **A** o **C**; **E**n cambio (else), cuando todo anda bien, elegís entre **L**atencia o **C**onsistencia. Replicar sincrónico = consistente pero lento; asincrónico = rápido pero con lag.

### Niveles de consistencia (de más fuerte a más débil)

- **Linealizable / fuerte**: como si hubiera una sola copia.
- **Read-your-writes**: al menos vos ves lo que escribiste.
- **Monotonic reads**: nunca ves un dato "volver atrás en el tiempo".
- **Eventual**: en algún momento todas las réplicas convergen.

## Tipos de implementación

### 1. Escalado vertical
Más CPU, RAM, disco NVMe, IOPS. Lo primero que hay que hacer. Techo: la máquina más grande que te venda tu cloud, y el precio crece más que lineal.

### 2. Replicación

**Leader–follower (single-leader)**: un nodo escribe, N nodos leen. Escala lecturas, no escrituras. Lo más común (Postgres streaming replication, MySQL replicas, RDS read replicas).
- Sincrónica: no perdés datos, pero cada escritura espera a la réplica.
- Asincrónica: rápida, pero hay lag y si el leader muere podés perder las últimas escrituras.

**Multi-leader**: varios nodos aceptan escrituras (típico: un leader por datacenter). Escrituras locales rápidas, pero aparecen **conflictos** que hay que resolver (last-write-wins, CRDTs, merge a mano).

**Leaderless (estilo Dynamo)**: cualquier nodo acepta escrituras; se usa **quorum**: con N réplicas, escribís en W y leés de R. Si `R + W > N`, al menos un nodo de los que leés tiene el último dato. (Cassandra, DynamoDB, Riak.)

### 3. Particionado vertical / federación
Separar por dominio: tabla `users` en una DB, `orders` en otra, `analytics` en otra. Fácil de hacer, pero perdés los JOINs y las transacciones entre dominios. Es lo que pasa naturalmente con microservicios.

### 4. Sharding (particionado horizontal)

| Estrategia | Cómo decide el shard | ✅ | ❌ |
|---|---|---|---|
| **Por rango** | `user_id` 1–1M → shard A, 1M–2M → shard B | Range queries eficientes | Hot spots con keys secuenciales |
| **Por hash** | `hash(user_id) % N` | Distribución pareja | Range queries van a todos los shards; cambiar N mueve casi todo |
| **Consistent hashing** | Anillo de hash, cada nodo agarra un arco | Agregar un nodo mueve solo ~1/N | Más complejo; necesita nodos virtuales para balancear |
| **Por directorio** | Tabla de lookup `key → shard` | Total flexibilidad, mover keys individuales | El directorio es un punto de falla y un salto extra |
| **Geográfico** | `region = 'EU'` → shard Europa | Latencia baja, cumplimiento legal (GDPR) | Usuarios que viajan / datos cross-region |

### 5. Connection pooling
Postgres crea un proceso por conexión: 5000 conexiones de 500 pods la matan aunque las queries sean livianas. Un pooler (PgBouncer, RDS Proxy, ProxySQL) multiplexa miles de clientes en pocas conexiones reales.

### 6. Caché delante de la DB
Cache-aside con Redis/Memcached: la app mira la caché, si no está va a la DB y la guarda. Saca la mayoría de las lecturas de la DB (ver proyecto de caching).

### 7. CQRS / modelos de lectura denormalizados
Separar el modelo de escritura (normalizado) del de lectura (denormalizado, precalculado, en otra base o índice: Elasticsearch, una tabla materializada). Escala lecturas complejas sin JOINs.

### 8. Resharding online
Migrar de N a M shards sin downtime: doble escritura, backfill, verificación, cortar lecturas, cortar escrituras.

### 9. Bases que ya vienen distribuidas
- **NewSQL / SQL distribuido**: CockroachDB, YugabyteDB, Google Spanner, TiDB. SQL + transacciones + sharding automático.
- **Sharding sobre bases conocidas**: Vitess (MySQL, YouTube/Slack), Citus (Postgres).
- **NoSQL**: Cassandra, DynamoDB, MongoDB (con sharding nativo), ScyllaDB.

## Errores comunes

### 1. Malinterpretar CAP
Pensar que podés tener las tres, o que "CA" es una opción real en un sistema distribuido. Durante una partición elegís **C o A**.
→ Decidir explícitamente qué hace cada operación cuando un nodo no responde: ¿falla o devuelve dato viejo?

### 2. Replication lag: no ves lo que acabás de escribir
El usuario edita su perfil (va al leader), recarga (lee de una réplica atrasada) y ve el dato viejo.
→ **Read-your-writes**: leer del leader por un rato después de escribir, o leer de una réplica que ya tenga ese LSN/timestamp.

### 3. Celebrity problem / hot key
Sharding por `user_id` perfecto… hasta que Messi publica algo: todo el tráfico de likes y comentarios cae en **un solo shard**.
→ Salting de la key (`post_id#0..N`), caché agresiva para hot keys, tratamiento especial para cuentas grandes.

### 4. Fan-out de timelines con celebridades
"Push on write" (escribir el post en el timeline de cada seguidor) funciona hasta que alguien tiene 100M seguidores: un solo post = 100M escrituras.
→ **Híbrido**: push para usuarios normales, pull (merge al leer) para celebridades. Es lo que hizo Twitter.

### 5. Shard key mala
Shardear por rango de `created_at` o por un ID autoincremental: todas las escrituras nuevas van al **último shard**, los demás están ociosos.
→ Shard key con alta cardinalidad, distribución pareja y que coincida con el patrón de acceso (normalmente `tenant_id` o `user_id` hasheado).

### 6. `hash % N` y el resharding
Pasar de 4 a 5 shards con `hash(key) % N` mueve ~80% de las keys.
→ Consistent hashing, o muchas particiones lógicas fijas (ej. 1024) asignadas a pocos nodos físicos.

### 7. Queries cross-shard y scatter-gather
Un JOIN o un `WHERE email = ?` (cuando shardeaste por `user_id`) tiene que preguntarle a **todos** los shards. La latencia la define el shard más lento.
→ Diseñar para que las queries frecuentes toquen un solo shard; índices secundarios globales; denormalizar.

### 8. Transacciones distribuidas
Transferir plata de un usuario en shard A a otro en shard B: ya no hay `BEGIN/COMMIT` que cubra los dos.
→ 2PC (lento, bloqueante), **sagas** con compensaciones, o diseñar para que no haga falta (outbox pattern).

### 9. IDs autoincrementales con varios shards
Cada shard arranca su `SERIAL` en 1 → IDs duplicados.
→ UUIDs (v7 para que sean ordenables), Snowflake IDs, rangos por shard.

### 10. Split brain
El leader queda aislado por la red, se promueve un nuevo leader y ahora **hay dos** aceptando escrituras.
→ Consenso con quorum (Raft/Paxos, Patroni + etcd), **fencing tokens**, STONITH.

### 11. Perder datos en un failover asincrónico
Replicación asincrónica, el leader muere, se promueve una réplica que no tenía las últimas escrituras: se pierden (y a veces se reusan IDs, peor).
→ Al menos una réplica sincrónica (semi-sync), o aceptar y medir el RPO.

### 12. Conflictos en multi-leader con last-write-wins
Dos datacenters editan el mismo registro; gana el de timestamp mayor… pero los relojes no están sincronizados y se pierde la escritura "correcta".
→ Version vectors, CRDTs, o evitar multi-leader para datos con conflictos.

### 13. Agotar conexiones
Escalás la app a 200 pods con un pool de 20 cada uno = 4000 conexiones; la DB se cae aunque tenga CPU de sobra.
→ Pooler externo, pools chicos por instancia.

### 14. Escalar antes de optimizar
Shardear porque una query tarda 3 s… y le faltaba un índice.
→ `EXPLAIN ANALYZE`, índices, revisar N+1 en el ORM, caché. Sharding es el **último** recurso.

### 15. N+1 queries
El ORM hace 1 query para la lista y 1 por cada elemento. Con 1000 elementos son 1001 viajes a la DB. Con sharding o réplicas lejanas, es peor.
→ Eager loading / `JOIN` / `WHERE id IN (...)`.

## Cómo inspeccionar una base

```sql
-- Postgres: ¿qué queries son las más caras?
SELECT query, calls, mean_exec_time FROM pg_stat_statements ORDER BY total_exec_time DESC LIMIT 10;

-- ¿usa índice o hace seq scan?
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'x@y.com';

-- Lag de las réplicas (en el primary)
SELECT client_addr, state, replay_lag FROM pg_stat_replication;

-- Conexiones abiertas
SELECT count(*), state FROM pg_stat_activity GROUP BY state;
```

## Estructura

- `implementaciones/`: cada tipo de escalado con un ejemplo mínimo en Python (sin dependencias).
- `errores/`: cada error común reproducido y arreglado.

```bash
python3 implementaciones/08-consistent-hashing/consistent_hashing.py
python3 errores/03-celebrity-hot-key/main.py
```

## Plan del proyecto

1. **Vertical + optimización**: Postgres en Docker, una tabla con millones de filas, comparar con y sin índices.
2. **Réplicas**: primary + 2 réplicas con streaming replication, ver el lag y leer de las réplicas.
3. **Pooling**: PgBouncer delante, saturar con muchos clientes y comparar.
4. **Sharding a mano**: 3 Postgres y un router en la app con hash / consistent hashing.
5. **Citus o Vitess**: lo mismo pero con sharding gestionado.
6. **Romperla a propósito**: hot key, split brain (cortar la red entre nodos), resharding con `% N`, scatter-gather.
