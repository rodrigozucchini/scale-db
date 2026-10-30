from collections import defaultdict

seguidores = defaultdict(set)   # autor -> seguidores
siguiendo = defaultdict(set)    # usuario -> a quién sigue
posts = defaultdict(list)       # autor -> sus posts
timelines = defaultdict(list)   # usuario -> timeline precalculado
escrituras = 0
UMBRAL_CELEBRIDAD = 10_000

def seguir(u, autor):
    seguidores[autor].add(u)
    siguiendo[u].add(autor)

def es_celebridad(autor):
    return len(seguidores[autor]) >= UMBRAL_CELEBRIDAD

def publicar(autor, texto, hibrido):
    global escrituras
    posts[autor].append(texto)
    if hibrido and es_celebridad(autor):
        return  # no se empuja: se busca al leer
    for s in seguidores[autor]:
        timelines[s].append(texto)
        escrituras += 1

def leer_timeline(u, hibrido):
    if not hibrido:
        return timelines[u]
    celebs = [a for a in siguiendo[u] if es_celebridad(a)]
    return timelines[u] + [p for c in celebs for p in posts[c][-10:]]

for i in range(50_000):
    seguir(f"fan{i}", "celebridad")
for i in range(100):
    seguir(f"fan{i}", "amigo")

for hibrido in [False, True]:
    escrituras = 0
    timelines.clear(); posts.clear()
    publicar("celebridad", "gol!", hibrido)
    publicar("amigo", "asado el sábado", hibrido)
    print(f"{'✅ híbrido' if hibrido else '❌ push   '}: {escrituras} escrituras | fan0 ve: {leer_timeline('fan0', hibrido)}")
