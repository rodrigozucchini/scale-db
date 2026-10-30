# Malinterpretar CAP

CAP no es "elegí 2 de 3". En un sistema distribuido las particiones de red **van a pasar**, así que la pregunta real es: **cuando hay una partición, ¿priorizo C o A?**

- **CP**: si no puedo confirmar que tengo el último dato, devuelvo error. (Saldos bancarios, inventario, locks.)
- **AP**: respondo con lo que tengo, aunque esté viejo; después converge. (Likes, carrito, feed.)

```
cliente ─► nodo A ─╳─ nodo B (tiene la última escritura)
   CP: "503, no puedo garantizar el dato"
   AP: "acá tenés el valor que yo tengo (viejo)"
```

**Errores típicos:** decir "usamos Postgres, somos CA" (una Postgres con réplicas asincrónicas es otra cosa); elegir una base AP para algo que necesita consistencia (stock, pagos) o una CP para algo que necesita estar siempre arriba.

**Fix:** decidir **por operación** qué pasa durante una partición. Y acordarse de PACELC: aun sin particiones, consistencia cuesta latencia.
