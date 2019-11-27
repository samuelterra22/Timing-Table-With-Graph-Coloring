import pandas as pd
from random import random
from math import exp


class Vertice:
    def __init__(self, id, professor, materia, turma, cor):
        self.id = id
        self.professor = professor
        self.materia = materia
        self.turma = turma
        self.cor = cor

    def update_cor(self, cor):
        self.cor = cor

    def __repr__(self):
        return str(self.__dict__)


def f(solucao):
    return 0


def perturba(solucao):
    return 0


def simulated_annealing(S0, T0, M, P, L, alpha):
    S = S0
    T = T0
    j = 1

    while True:
        i = 1
        n_success = 0

        while True:
            S_i = perturba(S)
            delta_fi = f(S_i) - f(S)

            # Teste de aceitação de uma nova solução
            if (delta_fi <= 0) or (exp(-delta_fi / T) > random()):
                S = S_i
                n_success = n_success + 1

            i += 1

            if (n_success >= L) or (i > P):
                break

        # Atualização da temperatura (Deicaimento geométrico)
        T = alpha * T

        # Atualização do contador de iterações
        j += 1

        if (n_success == 0) or (j > M):
            break

    # Retorna a solução
    return S


def atualiza(lista):
    pass
    # for time


def calcula_cor(configuracao, horario, dia):  # [11:40...], 7:00, Segunda
    dia_index = 0
    if dia == 'Segunda':
        dia_index = 0
    elif dia == 'Terça':
        dia_index = 1
    elif dia == 'Quarta':
        dia_index = 2
    elif dia == 'Quinta':
        dia_index = 3
    elif dia == 'Sexta':
        dia_index = 4

    return configuracao.index(horario) + 1 + (len(configuracao) * dia_index)


def le(xlsx, planilha):
    data_frame_dados = pd.read_excel(xlsx, sheet_name=planilha)
    configuracao = pd.read_excel(xlsx, sheet_name='Configuracoes')

    resticoes = data_frame_dados.values
    configuracao = [configuracao[0].strftime("%H:%M") for configuracao in configuracao.values]

    professores = []

    for restricao in resticoes:
        if restricao[0] not in professores:
            professores.append(restricao[0])

    professores = [(str(professor), []) for professor in professores]

    for professor in professores:
        for resticao in resticoes:
            if resticao[0] == professor[0]:
                cor = calcula_cor(configuracao, resticao[1].strftime("%H:%M"), resticao[2])
                professor[1].append(cor)

    return professores


def cria_vertices(xlsx):
    data_frame_dados = pd.read_excel(xlsx, sheet_name='Dados')

    lista_de_vertices = []
    i = 0

    for dado in data_frame_dados.values:
        for _ in range(dado[3]):
            lista_de_vertices.append(Vertice(i, dado[2], dado[0], dado[1], None))
            i += 1

    return lista_de_vertices


def cria_arestas(lista_de_vertices):
    lista_de_arestas = []

    for vertice in lista_de_vertices:
        lista_de_arestas.append((vertice.id, []))

    for vertice_i in lista_de_vertices:
        for vertice_j in lista_de_vertices:
            if vertice_i.id != vertice_j.id:
                if vertice_i.professor == vertice_j.professor \
                        or vertice_i.turma == vertice_j.turma:
                    lista_de_arestas[vertice_i.id][1].append(vertice_j.id)

    return lista_de_arestas


def checa_factibilidade(lista_de_vertices, lista_de_arestas):
    for vertice in lista_de_vertices:
        lista_de_adjacentes = lista_de_arestas[vertice.id][1]
        for adjacente in lista_de_adjacentes:
            if lista_de_vertices[adjacente].cor is not None:
                if lista_de_vertices[adjacente].cor == vertice.cor:
                    return False
    return True


def colore_grafo_maior_restricao_professor(lista_de_vertices, lista_de_arestas, restricoes_professor, preferencias):
    ordem_arestas = []
    restricoes_professor.sort(key=lambda tup: len(tup[1]), reverse=True)
    for restricao in restricoes_professor:
        for e in lista_de_arestas:
            if lista_de_vertices[e[0]].professor == restricao[0]:
                ordem_arestas.append(e)
    for e in lista_de_arestas:
        if e not in ordem_arestas:
            ordem_arestas.append(e)

    for dado in preferencias:
        for aresta in ordem_arestas:
            if lista_de_vertices[aresta[0]].professor == dado[0]:
                for cor in dado[1]:
                    lista_de_vertices[aresta[0]].cor = cor
                    if checa_factibilidade(lista_de_vertices, lista_de_arestas):
                        break
                    else:
                        lista_de_vertices[aresta[0]].cor = None

    for e in lista_de_arestas:
        cor = 1
        if lista_de_vertices[e[0]].cor is None:
            lista_de_vertices[e[0]].cor = cor
            while not checa_factibilidade(lista_de_vertices, lista_de_arestas):
                cor += 1
                lista_de_vertices[e[0]].cor = cor

    return lista_de_vertices


if __name__ == '__main__':
    # xlsx = pd.ExcelFile("./instances/Escola_A.xlsx")
    xlsx = pd.ExcelFile("./instances/Exemplo.xlsx")

    professor_restricoes = le(xlsx, 'Restricao')
    professor_preferecias = le(xlsx, 'Preferencias')
    restricoes_turma = le(xlsx, 'Restricoes Turma')

    lista_de_vertices = cria_vertices(xlsx)
    lista_de_arestas = cria_arestas(lista_de_vertices)

    print(lista_de_vertices)
    # print(lista_de_arestas)
    colore_grafo_maior_restricao_professor(lista_de_vertices, lista_de_arestas, professor_restricoes,
                                           professor_preferecias)
