# -*- coding: utf-8 -*-
#Tudo certo por aqui
from tabuleiro import Tabuleiro

class Jogador:
    def __init__(self, tabuleiro : Tabuleiro, tipo : int):
        self.matriz = tabuleiro.matriz
        self.tabuleiro = tabuleiro
        self.tipo = tipo
        
      
    def getJogada(self) -> (int, int):
        pass