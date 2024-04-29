import random
import time
import os

grid = []

highscore = []

jogador = {
    "nome": "AAA",
    "x": 19,
    "y": 3,
    "vida": 3,
    "pontos": 0,
    "vida_boss": 6,
    "contador": 1
}

inimigos = list("💖👼👾👽👹💣🧠🟥")



# Função para preencher o grid com blocos pretos
def preenche_grid():
    for i in range(20):
        grid.append([])
        for j in range(7):
            grid[i].append("⬛")

# Função para imprimir o grid
def imprime_grid():
    os.system("cls")
    for i in range(20):
        for j in range(7):
            print(grid[i][j], end="")
        print()

# Função para mover o jogador
def move_jogador(direcao):
    grid[jogador["x"]][jogador["y"]] = "⬛"
    if direcao == "4" or direcao == "a":
        jogador["y"] -= 1
        if jogador["y"] < 0:
            jogador["y"] = 6
    elif direcao == "6" or direcao == "d":
        jogador["y"] += 1
        if jogador["y"] > 6:
            jogador["y"] = 0
    else:
        print("Direção inválida")
    grid[jogador["x"]][jogador["y"]] = "🗼"

# Função para spawnar inimigos
def spawn_inimigo():
    if random.randint(1, 100) < 60:
        y = random.randint(0, 6)
        aleatorio = random.randint(1, 1000)
        if aleatorio <= 20:
            grid[0][y] = inimigos[0]
        elif aleatorio <= 100:
            grid[0][y] = inimigos[1]
        elif aleatorio <= 800:
            grid[0][y] = inimigos[2]
        elif aleatorio <= 905:
            grid[0][y] = inimigos[3]
        elif aleatorio <= 989:
            grid[0][y] = inimigos[4]
        elif aleatorio <= 1000:
            grid[0][y] = inimigos[5] 
    if jogador["pontos"] >= 100 and jogador["pontos"] // 100 == jogador["contador"]:
        spawna_chefe()
        jogador["contador"] += 1

# Função para mover os inimigos
def move_inimigos():
    for i in range(19, -1, -1):
        for j in range(6, -1, -1):
            if grid[i][j] in inimigos:
                if i == 18:
                    if grid[i][j] == "💖":
                        jogador["vida"] += 1
                    elif grid[i][j] == "👼":
                        jogador["pontos"] += 5
                    else:
                        jogador["vida"] -= 1
                        if jogador["vida"] == 0:
                            gameover()
                    grid[i][j] = "⬛"
                elif grid[i+1][j] == "🗼":
                    jogador["vida"] -= 1
                    if jogador["vida"] == 0:
                        gameover()
                    grid[i][j] = "⬛"
                else:
                    if grid[i][j] == "👹" or grid[i][j] == "👼":
                        if grid[i+2][j] in inimigos or grid[i+1][j] in inimigos:
                            grid[i+1][j] = grid[i][j]
                        else:
                            grid[i+2][j] = grid[i][j]
                    elif grid[i][j] == "👽":
                        grid[i+1][j] = grid[i][j]
                        if random.randint(1, 100) < 40:
                            if i != 18:
                                grid[i+2][j] = "👾"

                    else:
                        grid[i+1][j] = grid[i][j]
                    grid[i][j] = "⬛"

def spawna_chefe():
    grid[0][2] = "🟥"
    grid[0][3] = "🟥"
    grid[0][4] = "🟥"
    grid[1][2] = "🟥"
    grid[1][3] = "🧠"
    grid[1][4] = "🟥"
    grid[2][2] = "🟥"
    grid[2][3] = "🟥"
    grid[2][4] = "🟥"

# Função para verificar colisão do tiro com os inimigos
def colisao(x, y):
    if grid[x][y] in inimigos:
        if grid[x][y] == "💖":
            jogador["vida"] += 1
        elif grid[x][y] == "👼":
            jogador["pontos"] -= 5
        elif grid[x][y] == "👹":
            jogador["pontos"] += 5
        elif grid[x][y] == "💣":
            grid[x][y] = "⬛"
            bomba()
        elif grid[x][y] == "👽":
            jogador["pontos"] += 2
        elif grid[x][y] == "🧠":
            jogador["vida_boss"] -= 1
            if jogador["vida_boss"] == 0:
                grid[x-1][y-1] = "⬛"
                grid[x-1][y] = "⬛"
                grid[x-1][y+1] = "⬛"
                grid[x][y-1] = "⬛"
                grid[x][y] = "⬛"
                grid[x][y+1] = "⬛"
                grid[x+1][y-1] = "⬛"
                grid[x+1][y+1] = "⬛"
                jogador["pontos"] += 30
                jogador["vida_boss"] = 3
                bomba()
        elif grid[x][y] == "🟥":
            jogador["pontos"] += 0
        else:
            jogador["pontos"] += 1
        if grid[x][y] != "🧠":
            grid[x][y] = "🎇"
            if grid[x+1][y] == "🔸":
                grid[x+1][y] = "⬛"
            imprime_grid()
            time.sleep(0.2)
            grid[x][y] = "⬛"
            return True

# Função para atirar
def atira():
    x = jogador["x"] - 1
    y = jogador["y"]
    while x >= 0:
        if grid[x][y] in inimigos:
            colisao(x, y)
            break
        grid[x][y] = "🔸"
        if colisao(x-1, y):
            grid[x][y] = "⬛"
            break
        imprime_grid()
        time.sleep(0.01)
        grid[x][y] = "⬛"
        x -= 1
        
def bomba():
    for i in range(19, -1, -1):
        for j in range(7):
            colisao(i, j)
                

# Função do loop do jogo
def game_loop():
    preenche_grid()
    grid[jogador["x"]][jogador["y"]] = "🗼"
    while True:
        move_inimigos()
        spawn_inimigo()
        imprime_grid()
        print(f"Vida: {jogador['vida']} Pontos: {jogador['pontos']}")
        direcao = input("Digite a direção: ")
        if direcao == "":
            atira()
        else:
            move_jogador(direcao)
        imprime_grid()
        print(f"Vida: {jogador['vida']} Pontos: {jogador['pontos']}")
        time.sleep(0.1)

# Funções de menu de controles
def mostra_controles():
    os.system("cls")
    print("+" + "-"*40 + "+")
    print("|" + "Controles".center(40) + "|")
    print("+" + "-"*40 + "+")
    print("|"+"4 ou a + ENTER - Move nave para esquerda".ljust(40)+"|")
    print("|"+"6 ou d + ENTER - Move nave para Direita".ljust(40)+"|")
    print("|"+"ENTER - Atirar".ljust(40)+"|")
    print("+" + "-"*40 + "+")
    input("Pressione Enter para voltar")

# Função para mostrar as regras
def mostra_regras():
    os.system("cls")
    print("+" + "-"*80 + "+")
    print("|" + "Regras".center(80) + "|")
    print("+" + "-"*80 + "+")
    print("|"+"- O objetivo do jogo é pontuar o máximo possível".ljust(80)+"|")
    print("|"+"- Evite que os monstros cheguem até o final, com exceção do anjo".ljust(80)+"|")
    print("|"+"- 👾 concede 1 ponto".ljust(79)+"|")
    print("|"+"- 👽 concede 2 pontos, chance de invocar inimigos como escudo".ljust(79)+"|")
    print("|"+"- 👹 concede 5 pontos, andam 2 espaços".ljust(79)+"|")
    print("|"+"- 👼 concede -5 pontos se acertado e +5 se chegarem no jogador, andam 2 espaços".ljust(79)+"|")
    print("|"+"- 💖 concede 1 vida".ljust(79)+"|")
    print("+" + "-"*80 + "+")
    input("Pressione Enter para voltar")

# Função para mostrar a tela de Game Over
def gameover():
    os.system("cls")
    print("+" + "-"*12 + "+")
    print("|" + "Game Over".center(12) + "|")
    print("+" + "-"*12 + "+")
    print("|" + "Pontuação: ".center(12) + "|")
    print("|" + str(jogador["pontos"]).center(12) + "|")
    print("+" + "-"*12 + "+")
    while True:
        nome = input("Digite seu nome para salvar no HighScore: ").upper()
        if len(nome) != 3:
            print("Nome deve ter 3 caracteres")
        else:
            jogador["nome"] = nome
            grava_highscore()
            carrega_highscore()
            mostra_highscore()
            break
    exit()

# Função para gravar o highscore
def grava_highscore():
    highscore = []
    with open("highscore.txt", "a") as arq:
        arq.write(f"{jogador['nome']};{jogador['pontos']}\n")

# Função para carregar o highscore
def carrega_highscore():
    if not os.path.isfile("highscore.txt"):
        return
    with open("highscore.txt", "r") as arq:
        dados = arq.readlines()
        for linha in dados:
            partes = linha.split(";")
            highscore.append({"nome": partes[0], "pontos": int(partes[1])})

# Função para ser usada no sorted para ordenar o highscore pelo pontos
def ordena_highscore(a):
    return a["pontos"]

# Função para mostrar o highscore
def mostra_highscore():
    os.system("cls")
    ordem = sorted(highscore, key=ordena_highscore, reverse=True)
    print("+" + "-"*12 + "+")
    print("|" + "HighScore".center(12) + "|")
    print("+" + "-"*12 + "+")
    for i in range(10):
        if i < len(ordem):
            print("|"+f"{ordem[i]['nome']} - {ordem[i]['pontos']}".ljust(12)+"|")
    print("+" + "-"*12 + "+")
    input("Pressione Enter para sair")

# Funucao para mostrar o menu
def mostra_menu():
    os.system("cls")
    print("+" + "-"*22 + "+")
    print("|" + "☾⋆Space Shooter⋆⁺₊".center(22) + "|")
    print("+" + "-"*22 + "+")
    print("|"+"1 - Jogar".ljust(22)+"|")
    print("|"+"2 - Controles".ljust(22)+"|")
    print("|"+"3 - Regras".ljust(22)+"|")
    print("|"+"4 - HighScore".ljust(22)+"|")
    print("|"+"5 - Sair".ljust(22)+"|")
    print("+" + "-"*22 + "+")
    opcao = input("Escolha uma opção: ")
    return opcao    

# loop principal
while True:
    opcao = mostra_menu()
    if opcao == "1":
        game_loop()
    elif opcao == "2":
        mostra_controles()
    elif opcao == "3":
        mostra_regras()
    elif opcao == "4":
        carrega_highscore()
        mostra_highscore()
    elif opcao == "5":
        exit()
    else:
        print("Opção inválida")
        
