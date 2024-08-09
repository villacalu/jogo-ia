import pygame
import heapq

TAMANHO = 50
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
ROSA = (255, 0, 127)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)
LARANJA = (255, 100, 0)


def retangulo(x, y):
    return pygame.Rect(
        x * TAMANHO + 5,
        y * TAMANHO + 5,
        TAMANHO - 10,
        TAMANHO - 10,
    )


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.tela = pygame.display.set_mode((10 * TAMANHO, 10 * TAMANHO))
        self.rodando = True
        self.fps = pygame.time.Clock()
        self.mapa = [[0 for _ in range(10)] for _ in range(10)]
        self.barreiras = [
            (5, 6),
            (4, 6),
            (3, 6),
            (2, 6),
            (1, 6),
            (0, 6),
            (6, 6),
            (7, 6),
            (8, 6),
            (9, 6),
            (2, 0),
            (2, 1),
            (3, 1),
            (4, 1),
            (4, 2),
            (6, 4),
            (8, 4),
            (7, 4),
            (9, 4),
            (4, 4),
            (7, 0),
            (7, 1),
            (7, 2),
        ]
        self.heroi = (0, 0)
        self.inimigo = (7, 7)
        self.vitoria = (9, 9)
        self.fruta = (3, 0)
        self.abertos = []
        self.fechados = []
        self.caminho = []
        self.distancias = {}
        self.nos_anteriores = {}
        self.objetivo = self.vitoria
        self.tem_poder = False

        self.iniciar_distancias()

    def calcular_distancia(self, a, b):
        return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5

    def achar_vizinhos(self, no):
        direcoes = [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1),
            (1, 1),
            (1, -1),
            (-1, 1),
            (-1, -1),
        ]
        vizinhos = []
        for direcao in direcoes:
            vizinho = (no[0] + direcao[0], no[1] + direcao[1])
            if 0 <= vizinho[0] < 10 and 0 <= vizinho[1] < 10:
                vizinhos.append(vizinho)
        return vizinhos

    # Inicializa as distâncias de todos os nós como infinito, exceto o nó inicial
    def iniciar_distancias(self):
        for x in range(10):
            for y in range(10):
                self.distancias[(x, y)] = float("inf")
        self.distancias[self.heroi] = 0

    def seguir_caminho(self, no_final):
        caminho = []
        while no_final in self.nos_anteriores:
            caminho.append(no_final)
            no_final = self.nos_anteriores[no_final]
        print(caminho)
        self.caminho = caminho
        self.fechados = []
        self.abertos = []

    # Move o jogador para o próximo nó no caminho
    def mover_heroi(self):
        if self.caminho:
            print("Moving player")
            self.heroi = self.caminho.pop(-1)
            self.caminho = []
            self.abertos = []
            self.fechados = []
            self.distancias = {}
            self.nos_anteriores = {}
            self.iniciar_distancias()
            self.mover_inimigo()
            if self.heroi == self.fruta:
                self.tem_poder = True
            return

        lista_prioridade = []
        heapq.heappush(lista_prioridade, (0, self.heroi))

        while lista_prioridade:
            no_atual = heapq.heappop(lista_prioridade)[1]

            if no_atual == self.objetivo:
                self.seguir_caminho(no_atual)
                break

            if no_atual in self.fechados:
                continue

            self.fechados.append(no_atual)
            vizinhos = self.achar_vizinhos(no_atual)

            for vizinho in vizinhos:
                if (
                    vizinho in self.fechados
                    or (vizinho in self.barreiras and not self.tem_poder)
                    or vizinho in self.abertos
                    or vizinho == self.inimigo
                ):
                    continue

                g_cost = self.calcular_distancia(no_atual, vizinho)
                h_cost = self.calcular_distancia(vizinho, self.objetivo)
                f_cost = g_cost + h_cost

                if f_cost < self.distancias[vizinho]:
                    self.distancias[vizinho] = f_cost
                    self.nos_anteriores[vizinho] = no_atual
                    heapq.heappush(lista_prioridade, (f_cost, vizinho))

            self.abertos = [no for _, no in lista_prioridade]
            pygame.display.flip()

        if not self.caminho:
            # Se não houver caminho por causa de barreiras, mude o objetivo para a fruta
            if self.objetivo == self.vitoria:
                self.objetivo = self.fruta
            else:
                self.objetivo = self.vitoria
            self.abertos = []
            self.fechados = []
            self.distancias = {}
            self.nos_anteriores = {}
            self.iniciar_distancias()

    # Desenha os objetos na tela
    def desenhar_objetos(self):
        self.tela.fill((0, 0, 0))

        for i in range(10):
            for j in range(10):
                if (i, j) in self.barreiras and not self.tem_poder:
                    pygame.draw.rect(
                        self.tela,
                        LARANJA,
                        retangulo(i, j),
                        0,
                        0,
                    )

                elif (i, j) == self.heroi:
                    pygame.draw.rect(
                        self.tela,
                        ROSA,
                        retangulo(i, j),
                        0,
                        0,
                    )

                elif (i, j) == self.inimigo:
                    pygame.draw.rect(
                        self.tela,
                        VERMELHO,
                        retangulo(i, j),
                        0,
                        0,
                    )

                elif (i, j) == self.vitoria:
                    pygame.draw.rect(
                        self.tela,
                        AZUL,
                        retangulo(i, j),
                        0,
                        0,
                    )

                elif (i, j) == self.fruta and not self.tem_poder:
                    pygame.draw.rect(
                        self.tela,
                        BRANCO,
                        retangulo(i, j),
                        0,
                        0,
                    )

                else:
                    pygame.draw.rect(
                        self.tela,
                        PRETO,
                        (
                            i * TAMANHO,
                            j * TAMANHO,
                            TAMANHO,
                            TAMANHO,
                        ),
                        0,
                    )

    # Move o inimigo para cima ou para baixo
    def mover_inimigo(self):
        enemyY = -1 if self.inimigo[1] % 2 == 0 else 1
        self.inimigo = (self.inimigo[0], self.inimigo[1] + enemyY)

    def loop(self):
        while self.rodando:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.rodando = False

            self.desenhar_objetos()

            pygame.display.flip()

            if self.heroi != self.vitoria:
                self.mover_heroi()

            self.fps.tick(10)  # 10 Frames por segundo

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.loop()
