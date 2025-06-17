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