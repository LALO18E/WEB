from JuegoInterfaz import JuegoInterfaz

NUM_DISCOS = 3 # Puedes cambiar esto a 4 o 5, pero la compilación tardará más

class HanoiJuego(JuegoInterfaz):
    def __init__(self):
        self._nombre = "hanoi"
        self.NUM_DISCOS = NUM_DISCOS # <-- AÑADE ESTA LÍNEA
        # El alfabeto son todos los movimientos posibles: "01" es de torre 0 a 1
        self._alfabeto = {f"{i}{j}" for i in range(3) for j in range(3) if i != j}
        
        # El estado inicial es una tupla de tuplas.
        # (torre_0, torre_1, torre_2)
        # Los discos se representan por su tamaño (números más grandes son más grandes)
        torre_inicial = tuple(range(NUM_DISCOS, 0, -1)) # (3, 2, 1)
        self._q_inicial = (torre_inicial, tuple(), tuple())

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def alfabeto(self) -> set[str]:
        return self._alfabeto

    @property
    def q_inicial(self):
        return self._q_inicial

    def estado_a_str(self, q: tuple[tuple[int, ...], ...]) -> str:
        # Representa el estado como un string: "3,2,1||"
        return "|".join([",".join(map(str, torre)) for torre in q])

    def es_final(self, q: tuple[tuple[int, ...], ...]) -> bool:
        # El juego termina si todos los discos están en la última torre
        torre_objetivo = tuple(range(NUM_DISCOS, 0, -1))
        return q[2] == torre_objetivo

    def aplicar_entrada(self, q: tuple[tuple[int, ...], ...], entrada: str):
        if self.es_final(q):
            return q

        try:
            torre_origen_idx = int(entrada[0])
            torre_destino_idx = int(entrada[1])
        except (ValueError, IndexError):
            return q # Entrada inválida, no cambia el estado

        # Convertir a listas para poder modificarlas
        torres = [list(torre) for torre in q]

        # --- Validar el movimiento ---
        # 1. La torre de origen no puede estar vacía
        if not torres[torre_origen_idx]:
            return q

        disco_a_mover = torres[torre_origen_idx][-1]

        # 2. Si la torre destino no está vacía, el disco de encima debe ser más grande
        if torres[torre_destino_idx]:
            disco_superior_destino = torres[torre_destino_idx][-1]
            if disco_a_mover > disco_superior_destino:
                return q # Movimiento inválido

        # --- Ejecutar el movimiento ---
        disco = torres[torre_origen_idx].pop()
        torres[torre_destino_idx].append(disco)

        # Devolver el nuevo estado como una tupla de tuplas
        return tuple(tuple(torre) for torre in torres)