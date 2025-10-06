import random
from JuegoInterfaz import JuegoInterfaz

# --- Constantes del Juego ---
ANCHO = 20
ALTO = 10
NUM_PUNTOS = 20
NUM_PODERES = 4
DURACION_PODER = 10 # El poder dura 10 movimientos

MAPA = [
    "####################",
    "#..................#",
    "#.##.###.##.###.##.#",
    "#P..o.......o....P.#",
    "#.##.###.##.###.##.#",
    "#..................#",
    "#.##.###.##.###.##.#",
    "#P..o.......o....P.#",
    "#..................#",
    "####################",
]

class PacmanJuego(JuegoInterfaz):
    def __init__(self):
        self._nombre = "pacman"
        self._alfabeto = {'w', 'a', 's', 'd'}
        
        # Generar posiciones iniciales aleatorias para puntos y poderes
        posiciones_libres = []
        for y in range(ALTO):
            for x in range(ANCHO):
                if MAPA[y][x] == '.':
                    posiciones_libres.append((x, y))

        random.shuffle(posiciones_libres)
        
        # Posiciones iniciales
        self.pacman_inicial = posiciones_libres.pop()
        self.fantasmas_iniciales = [posiciones_libres.pop(), posiciones_libres.pop()]
        
        puntos_iniciales = set()
        for _ in range(NUM_PUNTOS):
            if posiciones_libres:
                puntos_iniciales.add(posiciones_libres.pop())
        
        poderes_iniciales = set()
        for _ in range(NUM_PODERES):
             if posiciones_libres:
                poderes_iniciales.add(posiciones_libres.pop())

        # El estado inicial q_0
        self._q_inicial = (
            self.pacman_inicial,
            tuple(self.fantasmas_iniciales),
            frozenset(puntos_iniciales),
            frozenset(poderes_iniciales),
            0  # Temporizador del poder (0 = inactivo)
        )

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def alfabeto(self) -> set[str]:
        return self._alfabeto

    @property
    def q_inicial(self):
        return self._q_inicial

    def estado_a_str(self, q) -> str:
        # El estado se representa como un string único para el autómata
        pacman, fantasmas, puntos, poderes, timer = q
        
        # Ordenamos las tuplas de puntos y poderes para que el string sea consistente
        puntos_str = ",".join(sorted([f"{x}-{y}" for x, y in puntos]))
        poderes_str = ",".join(sorted([f"{x}-{y}" for x, y in poderes]))
        fantasmas_str = ",".join([f"{x}-{y}" for x, y in fantasmas])

        return f"{pacman[0]}-{pacman[1]}|{fantasmas_str}|{puntos_str}|{poderes_str}|{timer}"

    def es_final(self, q) -> bool:
        pacman, fantasmas, puntos, _, timer_poder = q
        
        # Condición de victoria: no quedan puntos
        if not puntos:
            return True
        
        # Condición de derrota: Pac-Man es atrapado por un fantasma cuando no tiene poder
        if timer_poder == 0:
            for fantasma in fantasmas:
                if pacman == fantasma:
                    return True
        return False

    def aplicar_entrada(self, q, entrada: str):
        # Si ya estamos en un estado final, no hacemos nada
        if self.es_final(q):
            return q
        
        pacman, fantasmas, puntos, poderes, timer_poder = q
        px, py = pacman
        
        # 1. Mover a Pac-Man
        if entrada == 'w':
            py -= 1
        elif entrada == 's':
            py += 1
        elif entrada == 'a':
            px -= 1
        elif entrada == 'd':
            px += 1
        
        # Validar movimiento contra muros
        if MAPA[py][px] == '#':
            px, py = pacman # Revertir si choca
        
        nuevo_pacman = (px, py)
        
        # Convertir a sets para poder modificarlos
        nuevos_puntos = set(puntos)
        nuevos_poderes = set(poderes)
        
        # 2. Recoger puntos y poderes
        if nuevo_pacman in nuevos_puntos:
            nuevos_puntos.remove(nuevo_pacman)
        
        nuevo_timer = timer_poder
        if nuevo_pacman in nuevos_poderes:
            nuevos_poderes.remove(nuevo_pacman)
            nuevo_timer = DURACION_PODER # Activar poder
            
        # Decrementar el timer si está activo
        if nuevo_timer > 0:
            nuevo_timer -= 1
        
        # 3. Mover fantasmas
        nuevos_fantasmas = []
        fantasmas_comidos_indices = []

        # Comprobar colisiones antes de mover fantasmas
        if nuevo_timer > 0:
            for i, fantasma in enumerate(fantasmas):
                if nuevo_pacman == fantasma:
                    fantasmas_comidos_indices.append(i)

        for i, fantasma in enumerate(fantasmas):
            if i in fantasmas_comidos_indices:
                # Si un fantasma es comido, lo mandamos a su posición inicial
                nuevos_fantasmas.append(self.fantasmas_iniciales[i])
                continue

        fx, fy = fantasma
        objetivo_x, objetivo_y = nuevo_pacman
        huyendo = nuevo_timer > 0

        # Calcular la dirección deseada (delta)
        dx = 0
        if fx < objetivo_x: dx = 1
        elif fx > objetivo_x: dx = -1

        dy = 0
        if fy < objetivo_y: dy = 1
        elif fy > objetivo_y: dy = -1

        # Si está huyendo, invierte la dirección
        if huyendo:
            dx = -dx
            dy = -dy

        # Intenta moverse horizontalmente primero, verificando LÍMITES y MUROS
        if dx != 0 and 0 <= fx + dx < ANCHO and MAPA[fy][fx + dx] != '#':
            fx += dx
        # Si no se pudo mover horizontal, intenta verticalmente, verificando LÍMITES y MUROS
        elif dy != 0 and 0 <= fy + dy < ALTO and MAPA[fy + dy][fx] != '#':
            fy += dy

        nuevos_fantasmas.append((fx, fy))

        # Componer el nuevo estado
        return (
            nuevo_pacman,
            tuple(nuevos_fantasmas),
            frozenset(nuevos_puntos),
            frozenset(nuevos_poderes),
            nuevo_timer
        )