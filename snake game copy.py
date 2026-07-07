import pygame
import random

# Inicialização
pygame.init()                   #inicia o pygame
pygame.mixer.init()             #inicia o mixer do pygame para sons



# Configurações da tela
LARGURA = 600
ALTURA = 400
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Snake Game")

# Cores
PRETO = (0, 0, 0)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
BRANCO = (255, 255, 255)

# Efeitos Sonoros
pygame.mixer.music.load("efeitos_sonoros/No Hope.mp3")
pygame.mixer.music.play(-1)

comer = pygame.mixer.Sound("efeitos_sonoros/SFX_Pickup_01.wav")
fim = pygame.mixer.Sound("efeitos_sonoros/game_over.wav")

# Tamanho do bloco
TAMANHO = 20

# Fonte
fonte = pygame.font.SysFont("Arial", 25)

clock = pygame.time.Clock() #serve para controlar a velocidade do jogo (FPS) e medir o tempo entre quadros.



def desenhar_cobra(lista_cobra):
    for bloco in lista_cobra:
        pygame.draw.rect(TELA, VERDE, [bloco[0], bloco[1], TAMANHO, TAMANHO], width= 0, border_radius=7)
    

    cabeça = lista_cobra[0]      

    centro_x = cabeça[0] + (TAMANHO//4)
    centro_y = cabeça[1] + (TAMANHO//4)
    raio_olho = 5

    pygame.draw.circle(TELA, PRETO, (centro_x, centro_y), raio_olho)


def mostrar_pontuacao(pontos): # é uma função criada pelo programador para exibir a pontuação do jogo na tela.
    texto = fonte.render(f"Pontos: {pontos}", True, BRANCO) #Esse trecho serve para criar o texto da pontuação e desenhá-lo na tela.
    TELA.blit(texto, [10, 10])

def jogo():
    x = LARGURA // 2
    y = ALTURA // 2

    dx = 0
    dy = 0

    cobra = []
    comprimento = 1

    comida_x = random.randrange(0, LARGURA - TAMANHO, TAMANHO)
    comida_y = random.randrange(0, ALTURA - TAMANHO, TAMANHO)

    rodando = True
    game_over = False

    while rodando:
        while game_over:
            TELA.fill(PRETO)
            msg = fonte.render("Game Over! Pressione C para continuar ou Q para sair", True, VERMELHO)
            TELA.blit(msg, [40, ALTURA // 2])
            mostrar_pontuacao(comprimento - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        rodando = False
                        game_over = False
                    if event.key == pygame.K_c:
                        jogo()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    dx = -TAMANHO
                    dy = 0
                elif event.key == pygame.K_RIGHT:
                    dx = TAMANHO
                    dy = 0
                elif event.key == pygame.K_UP:
                    dy = -TAMANHO
                    dx = 0
                elif event.key == pygame.K_DOWN:
                    dy = TAMANHO
                    dx = 0

        x += dx
        y += dy

        # Colisão com borda
        if x < 0 or x >= LARGURA or y < 0 or y >= ALTURA:
            game_over = True

        TELA.fill(PRETO)

        pygame.draw.rect(TELA, VERMELHO, [comida_x, comida_y, TAMANHO, TAMANHO])

        cabeca = []
        cabeca.append(x)
        cabeca.append(y)
        cobra.append(cabeca)

        if len(cobra) > comprimento:
            del cobra[0]

        # Colisão com o próprio corpo
        for bloco in cobra[:-1]:
            if bloco == cabeca:
                game_over = True

        desenhar_cobra(cobra)
        mostrar_pontuacao(comprimento - 1)

        pygame.display.update()

        # Comer comida
        if x == comida_x and y == comida_y:
            
            comida_x = random.randrange(0, LARGURA - TAMANHO, TAMANHO)
            comida_y = random.randrange(0, ALTURA - TAMANHO, TAMANHO)
            comprimento += 1
            comer.play()

        if game_over:
            pygame.mixer.music.stop()
            fim.play()


        clock.tick(10)

    pygame.quit()

# Iniciar o jogo
jogo()