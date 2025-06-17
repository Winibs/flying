import pygame
import random
import os
import sys
import math
import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime
import threading
import speech_recognition as sr
import pyttsx3
from recursos.adds import frase_motivacional



def falar_frase_motivacional(pontos):
    frase = frase_motivacional(pontos)
    falar(frase)

# Inicialização do pygame
pygame.init()


pygame.mixer.music.load("assets/moon.mp3")

pygame.mixer.music.play(-1)  # -1 faz a música repetir para sempre
pygame.mixer.music.set_volume(0.3)  # Volume entre 0.0 e 1.0


tamanho = (1000, 700)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode(tamanho)
pygame.display.set_caption("How to Train Your Dragon")
pygame.display.set_icon(pygame.image.load("assets/icon.jpg"))

# Criação dos retângulos (como "blocos" do Scratch)
dragao_rect = pygame.Rect(tamanho[0]-200, 100, 150, 150)
ataques = []

# Imagens
banguela = pygame.image.load("assets/bangs.png")
startgame = pygame.image.load("assets/startscreen.png")
fundo = pygame.image.load("assets/fundo.jpg")
d_screen = pygame.image.load("assets/end.png")
dragao_inimigo = pygame.image.load("assets/pesadelo2.png")
ataque_img = pygame.image.load("assets/ataque.png")
ataque_jogador_img = pygame.image.load("assets/contra_ataque.png").convert_alpha()
explosao_img = pygame.image.load("assets/explosao.png").convert_alpha()
stun_img = pygame.image.load("assets/stun.png").convert()





# ---- NUVEM DECORATIVA ----
nuvem_img = pygame.image.load("assets/nuvem.png").convert_alpha()
nuvem_img.set_alpha(50)  # Meio transparente


# Cores
white = (255, 255, 255)
black = (0, 0, 0)
blue = (27, 27, 73)

# Fontes
fonte_menu = pygame.font.SysFont("impact", 18)
fonte_morte = pygame.font.SysFont("impact", 120)
fonte = pygame.font.SysFont(None, 48)
fonte_menor = pygame.font.SysFont(None, 32)

# Sol pulsante
sol_base_raio = 40
sol_pos = (tamanho[0] - 80, 80)  # canto superior direito


def pedir_nome_jogador():
    """Abre uma janela estilizada para o jogador inserir seu nome e retorna esse nome."""
    tela.blit(startgame, (0, 0))
    pygame.display.update()
    nome_jogador = ""
    def obter_nome(event=None):
        nonlocal nome_jogador
        nome = entry_nome.get().strip()
        if not nome:
            messagebox.showwarning('Aviso', 'Por favor, insira um nome.')
        else:
            nome_jogador = nome
            root.destroy()

    root = tk.Tk()
    root.title("How to Train Your Dragon")
    root.resizable(False, False)

    largura_janela, altura_janela = 400, 150
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    pos_x = (largura_tela - largura_janela) // 2
    pos_y = (altura_tela - altura_janela) // 2
    root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

    # Cores e fontes
    cor_fundo = "#23235b"
    cor_texto = "#FFFFFF"
    fonte_titulo = ("Impact", 20)
    fonte_padrao = ("nunito", 14)

    root.configure(bg=cor_fundo)

    # Título
    label_titulo = tk.Label(
        root, text="Digite seu nome para começar!", 
        bg=cor_fundo, fg="#ffe44a",
        font=fonte_titulo, pady=10
    )
    label_titulo.pack()

    # Campo de entrada
    entry_nome = tk.Entry(root, font=fonte_padrao, justify="center", bg="#ddddff")
    entry_nome.pack(pady=(10, 10))
    entry_nome.focus_set()
    entry_nome.bind('<Return>', obter_nome)

    # Botão de enviar
    botao = tk.Button(
        root, text="Entrar no jogo!", 
        command=obter_nome, 
        font=fonte_padrao, 
        bg="#ffe44a", fg="#23235b", 
        activebackground="#000000"
    )
    botao.pack()

    root.mainloop()
    return nome_jogador




def falar(frase):
    engine = pyttsx3.init()
    engine.say(frase)
    engine.runAndWait()


def ouvir_quitar():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
    while True:
        try:
            with mic as source:
                print("Diga 'quitar' para fechar o jogo...")
                audio = recognizer.listen(source, timeout=1, phrase_time_limit=2)
            frase = recognizer.recognize_google(audio, language="pt-BR")
            print("Você disse:", frase)
            if "quitar" in frase.lower():
                print("Palavra 'quitar' detectada! Fechando o jogo.")
                falar("Saindo do jogo, até logo!")
                pygame.quit()
                sys.exit()
        except sr.WaitTimeoutError:
            continue
        except sr.UnknownValueError:
            continue
        except Exception as e:
            print("Erro no reconhecimento de voz:", e)
            continue


def tela_boas_vindas(nome):
    """Tela de boas-vindas com o botão à esquerda e explicações centralizadas."""
    rodando = True
    fonte = pygame.font.SysFont('impact', 32)  # Textos
    bem_vindo = fonte.render(f"Bem-vindo(a), {nome}!", True, blue)
    explicacao = fonte_menor.render("Desvie dos ataques do dragão!", True, blue)
    explicacao2 = fonte_menor.render("Use as setas para se mover.", True, blue)
    explicacao3 = fonte_menor.render("Ganhe pontos sobrevivendo!", True, blue)
    explicacao4 = fonte_menor.render("Pressione A para atacar!", True, (255, 100, 100))

    # Posições para centralizar explicações
    y_bemvindo = 140
    y_explica1 = 215
    y_explica2 = 265
    y_explica3 = 315
    y_explica4 = 365
    x_bemvindo = 635 
    x_explica1 = 590
    x_explica2 = 620
    x_explica3 = 605
    x_explica4 = 650  # mais à esquerda, pois o texto é longo
    x_botao = 240

    # Botão alinhado à esquerda (mesma altura das explicações)
    botao_largura = 200
    botao_altura = 60
    x_botao = 710
    y_botao = 423  # abaixado para não sobrepor o novo texto

    botao_rect = pygame.Rect(
        x_botao,
        y_botao,
        botao_largura,
        botao_altura
    )

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_rect.collidepoint(evento.pos):
                    rodando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    rodando = False

        tela.blit(startgame, (0, 0))
        # Centraliza explicações
        tela.blit(bem_vindo,   (x_bemvindo, y_bemvindo))
        tela.blit(explicacao,  (x_explica1, y_explica1))
        tela.blit(explicacao2, (x_explica2, y_explica2))
        tela.blit(explicacao3, (x_explica3, y_explica3))
        tela.blit(explicacao4, (x_explica4, y_explica4))  # novo aviso

        # Botão
        pygame.draw.rect(tela, (27, 27, 73), botao_rect)
        texto_botao = fonte.render("Iniciar!", True, white)
        tela.blit(
            texto_botao,
            (
                botao_rect.x + botao_rect.width // 2 - texto_botao.get_width() // 2,
                botao_rect.y + botao_rect.height // 2 - texto_botao.get_height() // 2
            )
        )

        pygame.display.update()


def salvar_ranking(nome, pontos):
    ranking_path = "log.dat"  # agora chama log.dat
    ranking = {}
    if os.path.exists(ranking_path):
        with open(ranking_path, "r") as file:
            try:
                ranking = json.load(file)
            except:
                ranking = {}
    if "registros" not in ranking:
        ranking["registros"] = []
    
    # Data e hora atual
    agora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    
    # Adiciona a pontuação ao histórico (lista) com data/hora
    ranking["registros"].append({
        "nome": nome,
        "pontos": pontos,
        "data_hora": agora
    })
    # Mantém só os últimos 50 para o arquivo não crescer demais
    ranking["registros"] = ranking["registros"][-50:]
    with open(ranking_path, "w") as file:
        json.dump(ranking, file, indent=4)


def get_ultimos_registros(qtd=5):
    ranking_path = "log.dat"
    if os.path.exists(ranking_path):
        with open(ranking_path, "r") as file:
            try:
                ranking = json.load(file)
            except:
                return []
        registros = ranking.get("registros", [])
        return registros[-qtd:][::-1]  # do mais recente para o mais antigo
    else:
        return []

def exibir_game_over(pontos, nome):
    tela.blit(d_screen, (0, 0))
    texto_game_over = fonte_morte.render("Game Over", True, white)
    texto_pontos = fonte_menu.render(f"Pontuação: {pontos}", True, white)
    texto_nome = fonte_menu.render(f"Jogador: {nome}", True, white)
    tela.blit(texto_game_over, (tamanho[0] // 2 - texto_game_over.get_width() // 2, 80))
    tela.blit(texto_pontos, (tamanho[0] // 2 - texto_pontos.get_width() // 2, 240))
    tela.blit(texto_nome, (tamanho[0] // 2 - texto_nome.get_width() // 2, 280))

    ultimos = get_ultimos_registros(5)
    titulo = fonte_menu.render("Últimas 5 partidas:", True, (255, 255, 0))
    tela.blit(titulo, (tamanho[0] // 2 - titulo.get_width() // 2, 340))
    for i, reg in enumerate(ultimos):
        texto = f"{reg['nome']}: {reg['pontos']} pts"
        if "data_hora" in reg:
            texto += f" - {reg['data_hora']}"
        txt = fonte_menu.render(texto, True, white)
        tela.blit(txt, (tamanho[0] // 2 - txt.get_width() // 2, 380 + 30 * i))

    motivacao = frase_motivacional(pontos)
    texto_motivacional = fonte_menu.render(motivacao, True, (255, 255, 0))
    tela.blit(texto_motivacional, (tamanho[0] // 2 - texto_motivacional.get_width() // 2, 530))

    pygame.display.update()
    pygame.time.wait(5000)

def perguntar_jogar_novamente():
    resposta = None

    def sim():
        nonlocal resposta
        resposta = True
        root.destroy()

    def nao():
        nonlocal resposta
        resposta = False
        root.destroy()

    root = tk.Tk()
    root.title("Jogar Novamente?")
    root.resizable(False, False)

    # Tamanho fixo e centralização rápida
    largura, altura = 400, 200
    x = root.winfo_screenwidth() // 2 - largura // 2
    y = root.winfo_screenheight() // 2 - altura // 2
    root.geometry(f"{largura}x{altura}+{x}+{y}")

    # Estilo simples e bonito
    root.configure(bg="#1e1e2e")

    label_titulo = tk.Label(
        root, text="FIM DE JOGO!", font=("Impact", 24),
        fg="#ffe44a", bg="#1e1e2e", pady=10
    )
    label_titulo.pack()

    label_pergunta = tk.Label(
        root, text="Deseja jogar novamente?", font=("Arial", 13),
        fg="white", bg="#1e1e2e"
    )
    label_pergunta.pack(pady=(0, 20))

    frame_botoes = tk.Frame(root, bg="#1e1e2e")
    frame_botoes.pack()

    estilo_botao = {
        "width": 10,
        "height": 2,
        "font": ("Arial", 12),
        "fg": "white",
        "bd": 0,
        "relief": "flat",
        "cursor": "hand2"
    }

    botao_sim = tk.Button(
        frame_botoes, text="Sim 😄", bg="#4caf50",
        activebackground="#388e3c", command=sim, **estilo_botao
    )
    botao_sim.pack(side="left", padx=15)

    botao_nao = tk.Button(
        frame_botoes, text="Não 😢", bg="#f44336",
        activebackground="#c62828", command=nao, **estilo_botao
    )
    botao_nao.pack(side="left", padx=15)

    # Rodapé opcional
    rodape = tk.Label(
        root, text="How to Train Your Dragon", font=("Arial", 9, "italic"),
        fg="#888", bg="#1e1e2e"
    )
    rodape.pack(side="bottom", pady=10)

    # Exibir imediatamente
    root.after(10, lambda: root.deiconify())
    root.mainloop()
    return resposta



def loop_jogo(nome):
    posicaoX = 10
    posicaoY = 275
    velocidade = 5
    movimento_y = 0
    pontos = 0

    dragao_rect = dragao_inimigo.get_rect(topleft=(tamanho[0] - 200, 100))
    ataques.clear()
    ataque_timer = 0

    ataques_jogador = []
    explosoes = []

    tempo_ultimo_ataque = 0
    tempo_recarga = 7000

    dragao_stunnado = False
    tempo_stun = 0
    stun_duracao = 3500

    ataque_velocidade = 10
    min_tempo_ataque = 30
    max_tempo_ataque = 180
    tempo_ataque_aleatorio = random.randint(min_tempo_ataque, max_tempo_ataque)
    dragao_direcao = 3
    pausado = False

    # Nuvem
    nuvem_img.set_alpha(120)  # Mais visível
    nuvem_x = random.randint(0, tamanho[0] - nuvem_img.get_width())
    nuvem_y = random.randint(0, tamanho[1] // 2)
    nuvem_vel_x = random.choice([-1, 1]) * random.uniform(0.5, 1.5)
    nuvem_vel_y = random.choice([-0.3, 0.3])

    # Máscaras
    mask_banguela = pygame.mask.from_surface(banguela)
    mask_dragao = pygame.mask.from_surface(dragao_inimigo)
    mask_ataque_inimigo = pygame.mask.from_surface(ataque_img)
    mask_ataque_jogador = pygame.mask.from_surface(ataque_jogador_img)

    rodando = True

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    movimento_y = -velocidade
                elif evento.key == pygame.K_DOWN:
                    movimento_y = velocidade
                elif evento.key == pygame.K_SPACE:
                    pausado = not pausado
                elif evento.key == pygame.K_a:
                    agora = pygame.time.get_ticks()
                    if agora - tempo_ultimo_ataque >= tempo_recarga:
                        ataque_j = ataque_jogador_img.get_rect(topleft=(posicaoX + 40, posicaoY + 10))
                        ataques_jogador.append(ataque_j)
                        tempo_ultimo_ataque = agora
            elif evento.type == pygame.KEYUP:
                if evento.key in (pygame.K_UP, pygame.K_DOWN):
                    movimento_y = 0

        if pausado:
            texto_pause = fonte.render("PAUSADO", True, white)
            tela.blit(texto_pause, (tamanho[0] // 2 - texto_pause.get_width() // 2, tamanho[1] // 2))
            pygame.display.update()
            relogio.tick(15)
            continue

        posicaoY += movimento_y
        posicaoY = max(0, min(posicaoY, tamanho[1] - banguela.get_height()))
        pontos += 1

        if pontos % 500 == 0:
            if ataque_velocidade < 25:
                ataque_velocidade += 1
            if min_tempo_ataque > 10:
                min_tempo_ataque -= 2
            if max_tempo_ataque > 40:
                max_tempo_ataque -= 10
            if dragao_direcao < 10:
                dragao_direcao += 1

        agora = pygame.time.get_ticks()
        if dragao_stunnado:
            if agora - tempo_stun >= stun_duracao:
                dragao_stunnado = False
        else:
            dragao_rect.y += dragao_direcao
            if dragao_rect.y <= 0 or dragao_rect.y >= tamanho[1] - dragao_rect.height:
                dragao_direcao *= -1

        ataque_timer += 1
        if not dragao_stunnado and ataque_timer > tempo_ataque_aleatorio:
            ataque_rect = ataque_img.get_rect(topleft=(dragao_rect.x + 50, dragao_rect.y + 70))
            ataques.append(ataque_rect)
            ataque_timer = 0
            tempo_ataque_aleatorio = random.randint(min_tempo_ataque, max_tempo_ataque)

        # === DESENHO ===
        tela.fill(white)
        tela.blit(fundo, (0, 0))

        # Nuvem
        nuvem_x += nuvem_vel_x
        nuvem_y += nuvem_vel_y
        if nuvem_x < -nuvem_img.get_width():
            nuvem_x = tamanho[0]
        elif nuvem_x > tamanho[0]:
            nuvem_x = -nuvem_img.get_width()
        if nuvem_y < 0 or nuvem_y > tamanho[1] // 2:
            nuvem_vel_y *= -1
        tela.blit(nuvem_img, (nuvem_x, nuvem_y))

        # Personagens
        banguela_rect = banguela.get_rect(topleft=(posicaoX, posicaoY))
        tela.blit(banguela, banguela_rect)
        tela.blit(dragao_inimigo, dragao_rect)

        # STUN SIMPLES VISÍVEL
        if dragao_stunnado:
            stun_rect = stun_img.get_rect(center=(dragao_rect.centerx, dragao_rect.y - 40))
            tela.blit(stun_img, stun_rect)

        # HUD
        texto = fonte_menu.render("Pontos: " + str(pontos), True, white)
        tela.blit(texto, (10, 10))
        texto_pause = fonte_menor.render("Pressione ESPAÇO para pausar", True, white)
        tela.blit(texto_pause, (180, 14))

        tempo_restante = max(0, tempo_recarga - (agora - tempo_ultimo_ataque))
        segundos = tempo_restante / 1000
        cor_recarga = (0, 255, 0) if segundos <= 0 else (255, 0, 0)
        texto_recarga = fonte_menu.render(f"Recarga: {segundos:.1f}s", True, cor_recarga)
        tela.blit(texto_recarga, (10, 40))

        # Ataques inimigos
        for ataque in ataques[:]:
            ataque.x -= ataque_velocidade
            tela.blit(ataque_img, ataque)
            offset = (ataque.x - banguela_rect.x, ataque.y - banguela_rect.y)
            if mask_banguela.overlap(mask_ataque_inimigo, offset):
                salvar_ranking(nome, pontos)
                exibir_game_over(pontos, nome)
                return
            if ataque.x < -ataque.width:
                ataques.remove(ataque)

        # Ataques do jogador
        for ataque_j in ataques_jogador[:]:
            ataque_j.x += 15
            tela.blit(ataque_jogador_img, ataque_j)

            # Colisão ataque x ataque
            for ataque in ataques[:]:
                offset = (ataque.x - ataque_j.x, ataque.y - ataque_j.y)
                if mask_ataque_jogador.overlap(mask_ataque_inimigo, offset):
                    explosoes.append((ataque_j.center, pygame.time.get_ticks()))
                    try:
                        ataques.remove(ataque)
                        ataques_jogador.remove(ataque_j)
                    except:
                        pass

            # Colisão com dragão
            offset = (ataque_j.x - dragao_rect.x, ataque_j.y - dragao_rect.y)
            if not dragao_stunnado and mask_dragao.overlap(mask_ataque_jogador, offset):
                dragao_stunnado = True
                tempo_stun = pygame.time.get_ticks()
                try:
                    ataques_jogador.remove(ataque_j)
                except:
                    pass

        # Explosões
        for posicao, tempo_inicio in explosoes[:]:
            if pygame.time.get_ticks() - tempo_inicio < 300:
                tela.blit(explosao_img, (posicao[0] - 32, posicao[1] - 32))
            else:
                explosoes.remove((posicao, tempo_inicio))

        # Sol pulsante
        tempo_atual = pygame.time.get_ticks() / 500
        raio = sol_base_raio + 10 * math.sin(tempo_atual)
        pygame.draw.circle(tela, (255, 255, 0), sol_pos, int(raio))

        pygame.display.update()
        relogio.tick(60)













def main():
    threading.Thread(target=ouvir_quitar, daemon=True).start()
    nome = pedir_nome_jogador()
    if not nome:
        print("Por favor insira um nome.")
        return

    falar(f"Olá, {nome}!")
    tela_boas_vindas(nome)

    while True:
        loop_jogo(nome)
        resposta = perguntar_jogar_novamente()
        if not resposta:
            pygame.quit()
            sys.exit()



if __name__ == "__main__":
    main()
