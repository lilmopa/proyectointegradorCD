import random

class Jugador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.fichas = 100
        
        self.partidas = 0
        self.victorias = 0
        self.derrotas = 0
        
        self.estadisticas_juegos = {
            "Tragamonedas": {"victorias": 0, "derrotas": 0},
            "Adivina el número": {"victorias": 0, "derrotas": 0},
            "Ruleta": {"victorias": 0, "derrotas": 0}
        }
        
        self.numeros_jugados = set()
        self.historial_juegos = []
        
    def ganar_fichas(self, cantidad):
        self.fichas += cantidad

    def perder_fichas(self, cantidad):
        self.fichas -= cantidad

    def registrar_victoria(self, juego, apuesta, premio):
        self.partidas += 1
        self.victorias += 1
        self.estadisticas_juegos[juego]["victorias"] += 1
        self.historial_juegos.append({
            "juego": juego,
            "resultado": "Victoria",
            "apuesta": apuesta,
            "premio": premio
        })

    def registrar_derrota(self, juego, apuesta, perdida):
        self.partidas += 1
        self.derrotas += 1
        self.estadisticas_juegos[juego]["derrotas"] += 1
        self.historial_juegos.append({
            "juego": juego,
            "resultado": "Derrota",
            "apuesta": apuesta,
            "perdida": perdida
        })


class Casino:
    def __init__(self, jugador):
        self.jugador = jugador
        self.simbolos = ["Cereza", "Limón", "Campana", "Estrella", "7"]
        self.colores_ruleta = ("Rojo", "Negro")

    def validar_apuesta(self):
        while True:
            try:
                apuesta = int(input("¿Cuántas fichas quieres apostar? "))
                if apuesta <= 0:
                    print("La apuesta debe ser mayor que cero.")
                elif apuesta > self.jugador.fichas:
                    print("No tienes suficientes fichas.")
                else:
                    return apuesta
            except ValueError:
                print("Entrada inválida. Escribe un número entero.")        
                
    def tragamonedas(self):
        print("\n========= TRAGAMONEDAS =========")
        
        if self.jugador.fichas <= 0:
            print("No tienes fichas suficientes para jugar.")
            return

        apuesta = self.validar_apuesta()
        self.jugador.perder_fichas(apuesta)

        resultado = [
            random.choice(self.simbolos),
            random.choice(self.simbolos),
            random.choice(self.simbolos)
        ]

        print("\nGirando...")
        print(" | ".join(resultado))

        if resultado[0] == resultado[1] == resultado[2]:
            premio = apuesta * 5
            self.jugador.ganar_fichas(premio)
            self.jugador.registrar_victoria("Tragamonedas", apuesta, premio)
            print("\n¡JACKPOT!")
            print(f"Ganaste {premio} fichas.")

        elif (resultado[0] == resultado[1] or 
              resultado[0] == resultado[2] or 
              resultado[1] == resultado[2]):
            premio = apuesta * 2
            self.jugador.ganar_fichas(premio)
            self.jugador.registrar_victoria("Tragamonedas", apuesta, premio)
            print("\n¡Dos símbolos iguales!")
            print(f"Ganaste {premio} fichas.")

        else:
            self.jugador.registrar_derrota("Tragamonedas", apuesta, apuesta)
            print("\nTodos los símbolos son diferentes.")
            print(f"Perdiste {apuesta} fichas.")

        print(f"Fichas actuales: {self.jugador.fichas}")

    def adivina_numero(self):
        print("\n========= ADIVINA EL NÚMERO =========")
    
        if self.jugador.fichas <= 0:
            print("No tienes fichas suficientes para jugar.")
            return
    
        apuesta = self.validar_apuesta()

        rango_min, rango_max = 1, 5
        print(f"Estoy pensando en un número del {rango_min} al {rango_max}.")

        while True:
            try:
                eleccion = int(input("Tu elección: "))
                if rango_min <= eleccion <= rango_max:
                    break
                else:
                    print(f"Ingresa un número válido entre {rango_min} y {rango_max}.")
            except ValueError:
                print("Por favor, ingresa un número válido.")

        numero_ganador = random.randint(rango_min, rango_max)
        self.jugador.numeros_jugados.add(eleccion)
        print(f"Número ganador: {numero_ganador}")
    
        self.jugador.perder_fichas(apuesta)

        if eleccion == numero_ganador:
            premio = apuesta * 3
            print(f"¡Ganaste!\n+{premio} fichas")
            self.jugador.ganar_fichas(premio)
            self.jugador.registrar_victoria("Adivina el número", apuesta, premio)
        else:
            print(f":( Perdiste {apuesta} fichas.")
            self.jugador.registrar_derrota("Adivina el número", apuesta, apuesta)

        print(f"Fichas restantes: {self.jugador.fichas}")

    def ruleta(self):
        print("\n=========== RULETA ===========")

        if self.jugador.fichas <= 0:
            print("No tienes fichas suficientes para jugar.")
            return

        apuesta = self.validar_apuesta()
        opciones_ruleta = ("ROJO", "NEGRO", "NUMERO")

        print("\n1. Rojo")
        print("2. Negro")
        print("3. Número")

        while True:
            try:
                opcion = int(input("Selecciona: "))
                if 1 <= opcion <= 3:
                    break
                else:
                    print("Selecciona una opción del 1 al 3.")
            except ValueError:
                print("Entrada inválida.")

        tipo_apuesta = opciones_ruleta[opcion - 1]
        numero_apostado = None

        if opcion == 3:
            while True:
                try:
                    numero_apostado = int(input("¿A qué número apuestas (0 - 36)? "))
                    if 0 <= numero_apostado <= 36:
                        self.jugador.numeros_jugados.add(numero_apostado)
                        break
                    else:
                        print("El número debe estar entre 0 y 36.")
                except ValueError:
                    print("Por favor, ingresa un número válido.")

        print("\nLa ruleta está girando...")
        numero_ruleta = random.randint(0, 36)

        if numero_ruleta == 0:
            color_ruleta = "VERDE"
        elif numero_ruleta % 2 == 0:
            color_ruleta = "ROJO"
        else:
            color_ruleta = "NEGRO"

        print(f"\nResultado: {numero_ruleta} - {color_ruleta}")

        gano = False
        if tipo_apuesta == "ROJO" and color_ruleta == "ROJO":
            gano = True
        elif tipo_apuesta == "NEGRO" and color_ruleta == "NEGRO":
            gano = True
        elif tipo_apuesta == "NUMERO" and numero_apostado == numero_ruleta:
            gano = True

        self.jugador.perder_fichas(apuesta)

        if gano:
            premio = apuesta * 5 if opcion == 3 else apuesta * 2
            self.jugador.ganar_fichas(premio)
            self.jugador.registrar_victoria("Ruleta", apuesta, premio)
            print("\n¡Ganaste!")
            print(f"Ganaste {premio} fichas.")
        else:
            self.jugador.registrar_derrota("Ruleta", apuesta, apuesta)
            print(f"\nPerdiste {apuesta} fichas.")

        print(f"Fichas restantes: {self.jugador.fichas}")

    def consultar_fichas(self):
        print("\n=========== FICHAS ===========")
        print(f"Jugador: {self.jugador.nombre}")
        print(f"Fichas disponibles: {self.jugador.fichas}")

    def estadisticas(self):
        print("\n========= ESTADÍSTICAS =========")
        print(f"Jugador: {self.jugador.nombre}")
        print(f"Partidas jugadas: {self.jugador.partidas}")
        print(f"Victorias: {self.jugador.victorias}")
        print(f"Derrotas: {self.jugador.derrotas}")
        print(f"Fichas actuales: {self.jugador.fichas}")
        print("\n----- Estadísticas por juego -----")
        
        estadisticas = list(self.jugador.estadisticas_juegos.items())
        estadisticas.sort(key=lambda juego: juego[1]["victorias"], reverse=True)
            
        for juego, datos in estadisticas:
            print(f"{juego}: {datos['victorias']} victorias | {datos['derrotas']} derrotas")
            
        print("\nNúmeros jugados:")
        if self.jugador.numeros_jugados:
            print(self.jugador.numeros_jugados)
        else:
            print("Todavía no has jugado números.")

    def mostrar_menu(self):
        while True:
            print("\n" + "=" * 50)
            print("                  P Y C A S I N O")
            print("=" * 50)
            print(f"Jugador: {self.jugador.nombre}")
            print(f"Fichas: {self.jugador.fichas}\n")
            print("1. Tragamonedas")
            print("2. Adivina el número")
            print("3. Ruleta")
            print("4. Consultar fichas")
            print("5. Estadísticas")
            print("6. Salir")
            print("=" * 50)

            opcion = input("Selecciona una opción: ")

            if opcion == "1":
                self.tragamonedas()
            elif opcion == "2":
                self.adivina_numero()
            elif opcion == "3":
                self.ruleta()
            elif opcion == "4":
                self.consultar_fichas()
            elif opcion == "5":
                self.estadisticas()
            elif opcion == "6":
                print("\nGracias por jugar en PyCasino.")
                print(f"Te vas con {self.jugador.fichas} fichas.")
                break
            else:
                print("\nOpción inválida. Selecciona una opción del 1 al 6.")


def main():
    print("=" * 50)
    print("           BIENVENIDO A PYCASINO")
    print("=" * 50)

    while True:
        nombre = input("Ingresa tu nombre: ").strip()
        if nombre:
            break
        else:
            print("El nombre no puede estar vacío.")

    jugador = Jugador(nombre)
    casino = Casino(jugador)
    casino.mostrar_menu()


if __name__ == "__main__":
    main()