from compilador import compilar_juego
from hanoi_juego import HanoiJuego

print("Inicializando la lógica del juego Torres de Hanói...")
# Con 3 discos, hay 3^3 = 27 estados. Con 4 discos, 3^4 = 81 estados.
juego = HanoiJuego()

print("Comenzando la compilación del autómata...")
print(f"Explorando los {3**juego.NUM_DISCOS} estados posibles para {juego.NUM_DISCOS} discos.")

compilar_juego(juego)

print("\n¡Compilación terminada!")
print(f"Se ha creado la carpeta '{juego.nombre}' con 'automata.json' y 'auxiliares.js'.")