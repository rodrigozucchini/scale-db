storage = {"saldo": 100}
ultimo_token = 0

def escribir(quien, token, valor, con_fencing):
    global ultimo_token
    if con_fencing:
        if token < ultimo_token:
            print(f"  rechazado: {quien} tiene token {token} < {ultimo_token}")
            return
        ultimo_token = token
    storage["saldo"] = valor
    print(f"  {quien} escribió saldo={valor}")

for con_fencing in [False, True]:
    storage["saldo"], ultimo_token = 100, 0
    print("✅ con fencing" if con_fencing else "❌ sin fencing")
    viejo = {"nombre": "leader-viejo", "token": 1}
    escribir(viejo["nombre"], viejo["token"], 100, con_fencing)

    # partición: el cluster elige un leader nuevo con una época mayor
    nuevo = {"nombre": "leader-nuevo", "token": 2}
    escribir(nuevo["nombre"], nuevo["token"], 50, con_fencing)   # cliente B retira 50

    # el viejo no se enteró y sigue aceptando escrituras con su estado viejo
    escribir(viejo["nombre"], viejo["token"], 70, con_fencing)   # cliente A retira 30 sobre 100
    print("  saldo final:", storage["saldo"])
