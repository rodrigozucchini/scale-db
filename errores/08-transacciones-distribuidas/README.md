# Transacciones distribuidas

Transferir plata de Ana (shard A) a Beto (shard B). Con una sola base era un `BEGIN; UPDATE; UPDATE; COMMIT;`. Con dos shards no hay una transacción que cubra los dos: si falla en el medio, a Ana le descontaste y a Beto nunca le llegó.

**Opciones:**
- **2PC (two-phase commit)**: un coordinador pide "prepare" a todos y después "commit". Atómico, pero lento, y si el coordinador muere entre fases los participantes quedan bloqueados con locks tomados.
- **Saga**: una secuencia de transacciones locales, cada una con su **compensación** (si falla el paso 2, se ejecuta el "deshacer" del paso 1). Sin locks globales, pero con estados intermedios visibles.
- **Outbox pattern**: escribir el cambio y el evento en la **misma** transacción local; otro proceso publica el evento. Evita el "guardé en la DB pero no se mandó el mensaje".
- **Diseñar para evitarlo**: elegir la shard key para que lo que se modifica junto viva junto.
