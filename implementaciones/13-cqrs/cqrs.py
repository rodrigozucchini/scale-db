from collections import defaultdict

# modelo de escritura: normalizado
users = {}
posts = []
eventos = []

# modelo de lectura: precalculado para la pantalla de perfil
perfil_view = defaultdict(lambda: {"nombre": None, "cant_posts": 0, "ultimos": []})

def crear_usuario(uid, nombre):
    users[uid] = nombre
    eventos.append(("usuario_creado", uid, nombre))

def publicar(uid, texto):
    posts.append((uid, texto))
    eventos.append(("post_publicado", uid, texto))

def proyectar():
    # consumidor de eventos (en la vida real: Kafka, Debezium, etc.)
    while eventos:
        tipo, uid, dato = eventos.pop(0)
        if tipo == "usuario_creado":
            perfil_view[uid]["nombre"] = dato
        elif tipo == "post_publicado":
            v = perfil_view[uid]
            v["cant_posts"] += 1
            v["ultimos"] = ([dato] + v["ultimos"])[:3]

crear_usuario(1, "Ana")
for i in range(5):
    publicar(1, f"post {i}")

print(dict(perfil_view[1]))  # vacío: todavía no se proyectó (consistencia eventual)
proyectar()
print(dict(perfil_view[1]))  # una sola lectura, sin JOIN ni COUNT
