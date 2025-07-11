# -*- coding: utf-8 -*-
from random import randint
from jogador import Jogador
from tabuleiro import Tabuleiro

class JogadorIA(Jogador):
    def __init__(self, tabuleiro : Tabuleiro, tipo : int):
        super().__init__(tabuleiro, tipo)
    
    def get_oponente(self):
        if self.tipo == Tabuleiro.JOGADOR_X:
            return Tabuleiro.JOGADOR_0
        return Tabuleiro.JOGADOR_X

    # Auxiliar para a Regra 1: Encontra uma linha com 2 marcações e um espaço vazio
    def encontrar_sequencia_de_dois(self, tipo_jogador):
        # Verificação das linhas
        for r in range(3):
            if self.matriz[r].count(tipo_jogador) == 2 and self.matriz[r].count(Tabuleiro.DESCONHECIDO) == 1:
                c = self.matriz[r].index(Tabuleiro.DESCONHECIDO)
                return (r, c)
        # Verificação das colunas
        for c in range(3):
            coluna = [self.matriz[0][c], self.matriz[1][c], self.matriz[2][c]]
            if coluna.count(tipo_jogador) == 2 and coluna.count(Tabuleiro.DESCONHECIDO) == 1:
                r = coluna.index(Tabuleiro.DESCONHECIDO)
                return (r, c)
        # Verificação das diagonais:
        diag1 = [self.matriz[i][i] for i in range(3)]
        if diag1.count(tipo_jogador) == 2 and diag1.count(Tabuleiro.DESCONHECIDO) == 1:
            i = diag1.index(Tabuleiro.DESCONHECIDO)
            return (i, i)
        
        diag2 = [self.matriz[i][2-i] for i in range(3)]
        if diag2.count(tipo_jogador) == 2 and diag2.count(Tabuleiro.DESCONHECIDO) == 1:
            i = diag2.index(Tabuleiro.DESCONHECIDO)
            return (i, 2-i)
        return None

    #Encontrar uma jogada que cria um "garfo" (duas ameaças)
    def encontrar_garfo(self):
        casas_vazias = []
        for r in range(3):
            for c in range(3):
                if self.matriz[r][c] == Tabuleiro.DESCONHECIDO:
                    casas_vazias.append((r, c))

        for r, c in casas_vazias:
            
            self.matriz[r][c] = self.tipo
            ameacas = 0
            
            # Conta quantas sequências de dois são criadas
            if self.encontrar_sequencia_de_dois(self.tipo) is not None:
                # É preciso verificar o número de ameaças criadas a partir da jogada
                # Iterando novamente pelas casas vazias para ver se há múltiplas linhas vencedoras
                ameacas_potenciais = []
                for r_inner, c_inner in casas_vazias:
                    if (r,c) != (r_inner, c_inner): # não contar a casa que acabamos de preencher
                         self.matriz[r_inner][c_inner] = self.tipo
                         if self.tabuleiro.tem_campeao() == self.tipo:
                             ameacas +=1
                         self.matriz[r_inner][c_inner] = Tabuleiro.DESCONHECIDO #desfaz

            
            self.matriz[r][c] = Tabuleiro.DESCONHECIDO

            if ameacas >= 2:
                return (r, c)
        return None

    def getJogada(self) -> (int, int):
        # R1: Marcar a casa restante no caso de duas marcações em sequência.
        # Prioridade 1: Vencer o jogo
        jogada = self.encontrar_sequencia_de_dois(self.tipo)
        if jogada:
            return jogada
        # Prioridade 2: Bloquear o oponente
        jogada = self.encontrar_sequencia_de_dois(self.get_oponente())
        if jogada:
            return jogada
            
        # R2. Se houver uma jogada que crie duas sequências de duas marcações, use-a. 
        jogada = self.encontrar_garfo()
        if jogada:
            return jogada

        # R3. Se o quadrado central estiver livre, marque-o. 
        if self.matriz[1][1] == Tabuleiro.DESCONHECIDO:
            return (1, 1)

        # R4. Em caso de o oponente marcar canto, marcar o oposto. 
        oponente = self.get_oponente()
        cantos_opostos = { (0,0): (2,2), (0,2): (2,0), (2,0): (0,2), (2,2): (0,0) }
        for r, c in cantos_opostos.keys():
            if self.matriz[r][c] == oponente:
                oposto_r, oposto_c = cantos_opostos[(r,c)]
                if self.matriz[oposto_r][oposto_c] == Tabuleiro.DESCONHECIDO:
                    return (oposto_r, oposto_c)

        # R5. Se houver um canto vazio, marque-o. 
        cantos = [(0, 0), (0, 2), (2, 0), (2, 2)]
        for r, c in cantos:
            if self.matriz[r][c] == Tabuleiro.DESCONHECIDO:
                return (r, c)

        # R6. Marca arbitrariamente um quadrado vazio. 
        lista = []
        for l in range(0,3):
            for c in range(0,3):
                if self.matriz[l][c] == Tabuleiro.DESCONHECIDO:
                    lista.append((l, c))
                    
        if(len(lista) > 0):
            p = randint(0, len(lista)-1)
            return lista[p]
        else:
           return None