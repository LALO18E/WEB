from compilador import compilar_juego
from pacman_juego import PacmanJuego

print("Inicializando la lógica del juego Pac-Man...")
juego = PacmanJuego()

print("Comenzando la compilación del autómata...")
print("Este proceso puede tardar varios minutos dependiendo de la complejidad del juego...")

compilar_juego(juego)

print("\n¡Compilación terminada!")
print(f"Se ha creado la carpeta '{juego.nombre}' con los archivos 'automata.json' y 'auxiliares.js'.")
print("El siguiente paso es reemplazar 'pacman/auxiliares.js' y modificar 'interprete.html'.")