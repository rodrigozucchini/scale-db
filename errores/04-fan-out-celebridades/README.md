# Fan-out de timelines con celebridades

Dos formas de armar el timeline de una red social:

- **Fan-out on write (push)**: cuando alguien publica, se copia el post al timeline precalculado de **cada seguidor**. Leer es instantáneo.
- **Fan-out on read (pull)**: al abrir el timeline, se buscan los últimos posts de cada cuenta que seguís y se mezclan. Escribir es barato, leer es caro.

Push funciona perfecto… hasta que publica alguien con 100M de seguidores: **un post = 100M escrituras**.

```
usuario normal (200 seguidores)   ─► 200 escrituras ✓
celebridad (100M seguidores)      ─► 100.000.000 escrituras 💥
```

**Fix (lo que hizo Twitter):** **híbrido**. Push para cuentas normales; las celebridades no se empujan: al leer, se mezcla el timeline precalculado con los posts recientes de las celebridades que seguís (que están en caché porque los lee todo el mundo).
