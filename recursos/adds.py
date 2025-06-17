import random

def frase_motivacional(pontos):
    frases = [
        "Continue assim, jovem viking!",
        "Você está indo muito bem!",
        "Aguente firme! O dragão está te testando.",
        "Uau, que habilidade!",
        "Vai virar uma lenda nos céus!"
    ]
    if pontos < 200:
        return frases[0]
    elif pontos < 500:
        return frases[1]
    elif pontos < 800:
        return frases[2]
    elif pontos < 1200:
        return frases[3]
    else:
        return frases[4]
