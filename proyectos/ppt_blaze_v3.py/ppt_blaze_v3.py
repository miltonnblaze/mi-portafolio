import random
from colorama import Fore, Style, init

init(autoreset=True)

opciones_base = ['piedra', 'papel', 'tijeras']
opciones_completas = opciones_base + ['armadura']

def obtener_nombre_jugador():
    nombre = input("¡Bienvenido! ¿Cuál es tu nombre? (Escribe tu apodo): ").strip()
    if not nombre:
        nombre = "Jugador"  # Nombre predeterminado si no escribe nada
    print(f"\n¡Hola, {Fore.CYAN}{nombre}{Style.RESET_ALL}! ¡Listo para jugar!")
    return nombre

def validar_respuesta_si_no(prompt):
    while True:
        respuesta = input(prompt).strip().lower()
        if respuesta == 'si':
            return True
        elif respuesta == 'sí':
            return True
        elif respuesta == 'no':
            return False
        else:
            print(Fore.RED + "Respuesta inválida. Escribe 'sí' o 'no'." + Style.RESET_ALL)


def obtener_eleccion_jugador(nombre, puede_usar_armadura=False):
    opciones_disponibles = opciones_completas if puede_usar_armadura else opciones_base
    prompt = f"{nombre}, elige {', '.join(opciones_disponibles)} (o 'salir' para terminar): "
    eleccion = input(prompt).lower()
    while eleccion not in opciones_disponibles and eleccion != 'salir':
        eleccion = input(f"Opción inválida. {nombre}, elige {', '.join(opciones_disponibles)}: ").lower()
    return eleccion

def obtener_eleccion_computadora(dificultad, eleccion_jugador=None):
    if dificultad == 'difícil':
        # 80% chance de que gane contra el jugador, 20% aleatorio
        if random.random() < 0.8:
            if eleccion_jugador == 'piedra':
                return 'papel'
            elif eleccion_jugador == 'papel':
                return 'tijeras'
            elif eleccion_jugador == 'tijeras':
                return 'piedra'
            else:
                return random.choice(opciones_base)
        else:
            return random.choice(opciones_base)
    else:
        return random.choice(opciones_base)

def determinar_ganador(jugador1, jugador2):
    if jugador1 == jugador2:
        return "empate"
    if jugador1 == 'armadura':
        if jugador2 in ['piedra', 'tijeras']:
            return "jugador1"
        elif jugador2 == 'papel':
            return "jugador2"
    if jugador2 == 'armadura':
        if jugador1 in ['piedra', 'tijeras']:
            return "jugador2"
        elif jugador1 == 'papel':
            return "jugador1"
    if (jugador1 == "piedra" and jugador2 == "tijeras") or \
       (jugador1 == "papel" and jugador2 == "piedra") or \
       (jugador1 == "tijeras" and jugador2 == "papel"):
        return "jugador1"
    else:
        return "jugador2"

def mostrar_resultado(nombre, jugador1, jugador2, ganador):
    print(f"\n{nombre} eligió: {Fore.CYAN}{jugador1}{Style.RESET_ALL}")
    print(f"La computadora eligió: {Fore.MAGENTA}{jugador2}{Style.RESET_ALL}")
    if ganador == "empate":
        print(Fore.YELLOW + "¡Es un empate!" + Style.RESET_ALL)
    elif ganador == "jugador1":
        print(Fore.GREEN + f"¡Ganó {nombre}!" + Style.RESET_ALL)
    else:
        print(Fore.RED + "¡Ganó la computadora!" + Style.RESET_ALL)
    print("-" * 30)

def jugar_vs_computadora():
    nombre = obtener_nombre_jugador()
    print("\nElige dificultad:")
    print("1 - Fácil")
    print("2 - Normal")
    print("3 - Difícil")
    dificultad = input("Escribe 1, 2 o 3: ")
    while dificultad not in ['1', '2', '3']:
        dificultad = input(Fore.RED + "Opción inválida. Escribe 1, 2 o 3: " + Style.RESET_ALL)
    dificultad = {'1': 'fácil', '2': 'normal', '3': 'difícil'}[dificultad]

    puntos_jugador = 0
    puntos_computadora = 0
    comodin_revancha = True
    escudo = True
    armadura_desbloqueada = False

    while True:
        puede_usar_armadura = armadura_desbloqueada

        jugador = obtener_eleccion_jugador(nombre, puede_usar_armadura)
        if jugador == 'salir':
            print(Fore.BLUE + "Gracias por jugar. ¡Nos vemos!" + Style.RESET_ALL)
            break

        computadora = obtener_eleccion_computadora(dificultad, jugador)
        ganador = determinar_ganador(jugador, computadora)

        if ganador == "jugador2" and escudo:
            usar_escudo = validar_respuesta_si_no("¡Perdiste! ¿Quieres usar tu escudo para salvar la ronda? (sí/no): ")
            if usar_escudo:
                print(Fore.CYAN + "¡Escudo activado! No pierdes puntos." + Style.RESET_ALL)
                ganador = "empate"
                escudo = False

        if ganador == "jugador2" and comodin_revancha:
            usar_comodin = validar_respuesta_si_no("¿Quieres usar tu comodín revancha para forzar a la computadora a jugar aleatorio? (sí/no): ")
            if usar_comodin:
                print(Fore.CYAN + "¡Comodín revancha activado!" + Style.RESET_ALL)
                computadora = random.choice(opciones_base)
                ganador = determinar_ganador(jugador, computadora)
                comodin_revancha = False

        mostrar_resultado(nombre, jugador, computadora, ganador)

        if ganador == "jugador1":
            puntos_jugador += 1
        elif ganador == "jugador2":
            puntos_computadora += 1

        print(f"Puntaje: {nombre} = {puntos_jugador} | Computadora = {puntos_computadora}")
        print(f"Habilidades restantes: Comodín revancha = {'Sí' if comodin_revancha else 'No'}, Escudo = {'Sí' if escudo else 'No'}")

        if not armadura_desbloqueada and puntos_jugador >= 3:
            armadura_desbloqueada = True
            print(Fore.MAGENTA + "¡Desbloqueaste 'Armadura'!" + Style.RESET_ALL)

if __name__ == "__main__":
    jugar_vs_computadora()
