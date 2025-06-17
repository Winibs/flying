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