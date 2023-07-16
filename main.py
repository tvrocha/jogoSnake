# Nessa parte, as bibliotecas pygame e random são importadas para permitir o uso de suas funcionalidades no código.
import pygame
import random

# Aqui, a função pygame.init() é chamada para inicializar o módulo Pygame.
# Em seguida, pygame.display.set_caption() define o título da janela do jogo como "Snake - Python".
# A variável largura representa a largura da tela do jogo, e a variável altura representa a altura.
# A função pygame.display.set_mode() cria uma janela do jogo com as dimensões especificadas.
# Por fim, a variável relogio é inicializada como um objeto Clock do Pygame, que será usado para controlar a velocidade de atualização do jogo.
pygame.init()
pygame.display.set_caption('Snake - Python')
largura, altura = 1200, 800
tela = pygame.display.set_mode((largura, altura))
relogio = pygame.time.Clock()

# Nesta parte, algumas cores são definidas usando o modelo RGB.
# As cores preto, branco, vermelha e verde são atribuídas a variáveis para facilitar o uso posteriormente no código.
preto = (0, 0, 0)
branco = (255, 255, 255)
vermelha = (255, 0, 0)
verde = (0, 255, 0)

# Aqui, são definidos os parâmetros da cobrinha.
# A variável 'tamanhoQuadrado' representa o tamanho de cada quadrado da cobra e a variável 'velocidadeAtualizacao' define a velocidade de atualização do jogo.
tamanhoQuadrado = 20
velocidadeAtualizacao = 15

# Esta função é responsável por desenhar a comida na tela.
# Ela usa a 'função pygame.draw.rect()' para desenhar um retângulo na posição especificada pelos parâmetros 'comida_x' e 'comida_y'
# e com o tamanho especificado pelo parâmetro 'tamanho'.
# A cor do retângulo é definida como 'verde'.
def desenharComida(tamanho, comida_x, comida_y):
    pygame.draw.rect(tela, verde, [comida_x, comida_y, tamanho, tamanho])

# Essa função desenha a cobra na tela.
# Ela percorre a lista de pixels que representam o corpo da cobra e desenha um retângulo branco para cada pixel na posição correta.
def desenharCobra(tamanho, pixels):
    for pixel in pixels:
        pygame.draw.rect(tela, branco, [pixel[0], pixel[1], tamanho, tamanho])

# Esta função é responsável por desenhar a pontuação na tela.
# Ela usa a função 'pygame.font.SysFont()' para criar uma fonte do sistema com o tamanho de '25' pixels.
# Em seguida, ela renderiza o texto com a pontuação atual usando a fonte criada e a cor 'vermelha'.
# O texto é então exibido na posição [10, 1] na tela usando a função 'tela.blit()'.
def desenharPontuacao(pontuacao):
    fonte = pygame.font.SysFont('Courier New', 25)
    texto = fonte.render(f'Pontos: {pontuacao}', True, vermelha)
    tela.blit(texto, [10, 1])

# Essa função recebe uma tecla como entrada e retorna as velocidades correspondentes para mover a cobra na direção desejada.
# A função 'selecionarVelocidade()' garantirá que a cobra não reverta instantaneamente para a direção oposta e não permitirá movimentos verticais que contradigam a direção atual da cobra.
def selecionarVelocidade(tecla, velocidade_x, velocidade_y):
    if tecla == pygame.K_DOWN and velocidade_y != -tamanhoQuadrado:
        velocidade_x = 0
        velocidade_y = tamanhoQuadrado
    elif tecla == pygame.K_UP and velocidade_y != tamanhoQuadrado:
        velocidade_x = 0
        velocidade_y = -tamanhoQuadrado
    elif tecla == pygame.K_LEFT and velocidade_x != tamanhoQuadrado:
        velocidade_x = -tamanhoQuadrado
        velocidade_y = 0
    elif tecla == pygame.K_RIGHT and velocidade_x != -tamanhoQuadrado:
        velocidade_x = tamanhoQuadrado
        velocidade_y = 0
    return velocidade_x, velocidade_y

# Esta função é responsável por gerar a posição aleatória da comida na tela.
# Ela usa a função 'random.randrange()' para gerar um número aleatório dentro de um intervalo adequado,
# e então o arredonda para um múltiplo do tamanho do quadrado da cobra.
# Isso garante que a comida seja posicionada corretamente dentro da grade formada pelos quadrados da cobra.
def gerarComida():
    comida_x = round(random.randrange(0, largura - tamanhoQuadrado) / float(tamanhoQuadrado)) * float(tamanhoQuadrado)
    comida_y = round(random.randrange(0, altura - tamanhoQuadrado) / float(tamanhoQuadrado)) * float(tamanhoQuadrado)
    return comida_x, comida_y

# Essa função contém o loop principal do jogo.
# Ela inicializa várias variáveis necessárias para o funcionamento do jogo, incluindo a posição inicial da cobra,
# as velocidades iniciais, o tamanho inicial da cobra e uma lista vazia para representar o corpo da cobra.
# A posição da comida também é gerada usando a função 'gerarComida()'.
# Em seguida, o loop principal começa e continua até que 'fimJogo' seja definido como True.
# Dentro do loop, a tela é preenchida com a cor preta, e os eventos são tratados. Se o evento 'pygame.QUIT' for acionado, 'fimJogo'.
def rodarJogo():
    fimJogo = False
    x = largura / 2
    y = altura / 2
    velocidade_x = 0
    velocidade_y = 0
    tamanhoCobra = 1
    pixels = []
    comida_x, comida_y = gerarComida()

    tecla_pressionada = None # Armazena a última tecla pressionada pelo jogador

    while not fimJogo:
        tela.fill(preto)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                fimJogo = True
            elif evento.type == pygame.KEYDOWN:
                if tecla_pressionada is None:
                    tecla_pressionada = evento.key
                    velocidade_x, velocidade_y = selecionarVelocidade(tecla_pressionada, velocidade_x, velocidade_y)
                elif tecla_pressionada != evento.key:  # Evita a inversão instantânea da direção
                    tecla_pressionada = evento.key
                    velocidade_x, velocidade_y = selecionarVelocidade(tecla_pressionada, velocidade_x, velocidade_y)

        desenharComida(tamanhoQuadrado, comida_x, comida_y)

        # atualizar a posição da cobra
        if x < 0 or x >= largura or y < 0 or y >= altura:
            fimJogo = True
        x += velocidade_x
        y += velocidade_y

        pixels.append([x, y])
        if len(pixels) > tamanhoCobra:
            del pixels[0]
        # se a cobra bateu no proprio corpo
        for pixel in pixels[:-1]:
            if pixel == [x, y]:
                fimJogo = True
        desenharCobra(tamanhoQuadrado, pixels)

        desenharPontuacao(tamanhoCobra - 1)

        pygame.display.update()

        if x == comida_x  and y == comida_y:
            tamanhoCobra += 1
            comida_x, comida_y = gerarComida()

        relogio.tick(velocidadeAtualizacao)

rodarJogo()
pygame.quit()