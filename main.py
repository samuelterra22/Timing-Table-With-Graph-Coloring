import _pickle as cPickle
import random
import time
from math import exp

import pandas as pd


class Vertice:
    """

    """
    def __init__(self, identificador, professor, materia, turma, cor):
        self.id = identificador
        self.professor = professor
        self.materia = materia
        self.turma = turma
        self.cor = cor

    def __repr__(self):
        """

        :return:
        """
        return str(self.__dict__)


# ----------------------------------------------------------------------------------------------------------------------

def perturba_solucao(lista_de_arestas):
    """

    :param lista_de_arestas:
    :return:
    """
    lista_de_arestas.sort(key=lambda tup: len(tup[1]), reverse=True)
    indice_1 = random.randint(0, len(lista_de_arestas) // 2)
    indice_2 = random.randint(len(lista_de_arestas) // 2, len(lista_de_arestas) - 1)
    nova_lista_de_arestas = lista_de_arestas[indice_1:indice_2]
    random.shuffle(nova_lista_de_arestas)
    nova_lista_de_arestas = lista_de_arestas[0:indice_1] + nova_lista_de_arestas + lista_de_arestas[
                                                                                   indice_2: len(lista_de_arestas)]
    return nova_lista_de_arestas


def simulated_annealing(lista_de_vertices, lista_de_arestas, restricoes_professor, restricoes_turmas, preferencias,
                        temperatura_inicial, iteracoes, perturbacoes_iteracao, alpha, quantidade_aulas_dia):
    """

    :param lista_de_vertices:
    :param lista_de_arestas:
    :param restricoes_professor:
    :param restricoes_turmas:
    :param preferencias:
    :param temperatura_inicial:
    :param iteracoes:
    :param perturbacoes_iteracao:
    :param alpha:
    :param quantidade_aulas_dia:
    :return:
    """
    solucao_atual = cPickle.loads(cPickle.dumps(lista_de_arestas))
    best_solucao = cPickle.loads(cPickle.dumps(solucao_atual))
    vertices_solucao_best = colore_grafo(cPickle.loads(cPickle.dumps(lista_de_vertices)), best_solucao,
                                         restricoes_professor,
                                         restricoes_turmas)
    tempetura = temperatura_inicial

    for iteracao in range(iteracoes):
        for i in range(perturbacoes_iteracao):
            print(i, iteracao)
            S_i = perturba_solucao(cPickle.loads(cPickle.dumps(solucao_atual)))

            vertices_solucao_i = colore_grafo(cPickle.loads(cPickle.dumps(lista_de_vertices)), S_i,
                                              restricoes_professor, restricoes_turmas)
            cor_Si = calcula_quantidade_de_cores(vertices_solucao_i)
            f_Si = calcula_funcao_objetivo(quantidade_aulas_dia, vertices_solucao_i, preferencias)
            vertices_solucao_atual = colore_grafo(cPickle.loads(cPickle.dumps(lista_de_vertices)), solucao_atual,
                                                  restricoes_professor, restricoes_turmas)
            cor_S = calcula_quantidade_de_cores(vertices_solucao_atual)
            f_S = calcula_funcao_objetivo(quantidade_aulas_dia, vertices_solucao_atual, preferencias)

            # Calcula delta de Fi
            delta_fi = cor_Si - cor_S
            if delta_fi == 0:
                delta_fi = f_Si - f_S
            # Teste de aceitação de uma nova solução
            if (delta_fi <= 0) or (exp(-delta_fi / tempetura) > random.random()):
                solucao_atual = cPickle.loads(cPickle.dumps(S_i))
                if cor_S < calcula_quantidade_de_cores(vertices_solucao_best):
                    f_best = calcula_funcao_objetivo(quantidade_aulas_dia, vertices_solucao_best, preferencias)
                    if f_S < f_best:
                        best_solucao = cPickle.loads(cPickle.dumps(solucao_atual))
                        vertices_solucao_best = cPickle.loads(cPickle.dumps(vertices_solucao_atual))

        # Atualização da temperatura (Deicaimento geométrico)
        tempetura *= alpha

    # Retorna a solução
    return best_solucao, vertices_solucao_best


# ----------------------------------------------------------------------------------------------------------------------


def calcula_cor(configuracao, horario, dia):  # [11:40...], 7:00, Segunda
    """

    :param configuracao:
    :param horario:
    :param dia:
    :return:
    """
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
    """

    :param xlsx:
    :param planilha:
    :return:
    """
    data_frame_dados = pd.read_excel(xlsx, sheet_name=planilha)
    configuracao = pd.read_excel(xlsx, sheet_name='Configuracoes')

    resticoes = data_frame_dados.values
    configuracao = [configuracao[0].strftime("%H:%M") for configuracao in configuracao.values]

    lista = []

    for restricao in resticoes:
        if restricao[0] not in lista:
            lista.append(restricao[0])

    lista = [(elemento, []) for elemento in lista]

    for elemento in lista:
        for resticao in resticoes:
            if resticao[0] == elemento[0]:
                cor = calcula_cor(configuracao, resticao[1].strftime("%H:%M"), resticao[2])
                elemento[1].append(cor)

    return lista


def cria_vertices(xlsx):
    """

    :param xlsx:
    :return:
    """
    data_frame_dados = pd.read_excel(xlsx, sheet_name='Dados')

    lista_de_vertices = []
    i = 0

    for dado in data_frame_dados.values:
        for _ in range(dado[3]):
            lista_de_vertices.append(Vertice(i, dado[2], dado[0], dado[1], None))
            i += 1

    return lista_de_vertices


def cria_arestas(lista_de_vertices):
    """

    :param lista_de_vertices:
    :return:
    """
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


# ----------------------------------------------------------------------------------------------------------------------

def checa_factibilidade(lista_de_vertices, lista_de_arestas, restricoes_professor, restricoes_turma):
    """

    :param lista_de_vertices:
    :param lista_de_arestas:
    :param restricoes_professor:
    :param restricoes_turma:
    :return:
    """
    lista_de_adjacentes = []
    for vertice in lista_de_vertices:
        for aresta in lista_de_arestas:
            if aresta[0] == vertice.id:
                lista_de_adjacentes = aresta[1]
                break
        for adjacente in lista_de_adjacentes:
            if lista_de_vertices[adjacente].cor is not None:
                if lista_de_vertices[adjacente].cor == vertice.cor:
                    return False

    # Verifica se algum professor esta alocado em algum horario de restricao dele
    for vertice in lista_de_vertices:
        for restricao in restricoes_professor:
            for cor in restricao[1]:
                if restricao[0] == vertice.professor and vertice.cor == cor:
                    return False

    for vertice in lista_de_vertices:
        for restricao in restricoes_turma:
            for cor in restricao[1]:
                if restricao[0] == vertice.turma and vertice.cor == cor:
                    return False
    return True


# ----------------------------------------------------------------------------------------------------------------------

def colore_grafo_maior_restricao_professor(lista_de_vertices, lista_de_arestas, restricoes_professor, restricoes_turma,
                                           preferencias):
    """

    :param lista_de_vertices:
    :param lista_de_arestas:
    :param restricoes_professor:
    :param restricoes_turma:
    :param preferencias:
    :return:
    """
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
                    if checa_factibilidade(lista_de_vertices, lista_de_arestas, restricoes_professor, restricoes_turma):
                        break
                    else:
                        lista_de_vertices[aresta[0]].cor = None

    for e in ordem_arestas:
        cor = 1
        if lista_de_vertices[e[0]].cor is None:
            lista_de_vertices[e[0]].cor = cor
            while not checa_factibilidade(lista_de_vertices, lista_de_arestas, restricoes_professor, restricoes_turma):
                cor += 1
                lista_de_vertices[e[0]].cor = cor

    return lista_de_vertices, ordem_arestas


def colore_grafo_maior_grau(lista_de_vertices, lista_de_arestas, restricoes_professor, restricoes_turma, preferencias):
    """

    :param lista_de_vertices:
    :param lista_de_arestas:
    :param restricoes_professor:
    :param restricoes_turma:
    :param preferencias:
    :return:
    """
    ordem_arestas = cPickle.loads(cPickle.dumps(lista_de_arestas))
    ordem_arestas.sort(key=lambda tup: len(tup[1]), reverse=True)
    for dado in preferencias:
        for aresta in ordem_arestas:
            if lista_de_vertices[aresta[0]].professor == dado[0]:
                for cor in dado[1]:
                    lista_de_vertices[aresta[0]].cor = cor
                    if checa_factibilidade(lista_de_vertices, lista_de_arestas, restricoes_professor, restricoes_turma):
                        break
                    else:
                        lista_de_vertices[aresta[0]].cor = None

    for e in ordem_arestas:
        cor = 1
        if lista_de_vertices[e[0]].cor is None:
            lista_de_vertices[e[0]].cor = cor
            while not checa_factibilidade(lista_de_vertices, lista_de_arestas, restricoes_professor, restricoes_turma):
                cor += 1
                lista_de_vertices[e[0]].cor = cor

    return lista_de_vertices, ordem_arestas


def colore_grafo(lista_de_vertices, lista_de_arestas, restricoes_professor, restricoes_turma):
    """

    :param lista_de_vertices:
    :param lista_de_arestas:
    :param restricoes_professor:
    :param restricoes_turma:
    :return:
    """
    ordem_arestas = cPickle.loads(cPickle.dumps(lista_de_arestas))
    for e in ordem_arestas:
        cor = 1
        if lista_de_vertices[e[0]].cor is None:
            lista_de_vertices[e[0]].cor = cor
            while not checa_factibilidade(lista_de_vertices, lista_de_arestas, restricoes_professor, restricoes_turma):
                cor += 1
                lista_de_vertices[e[0]].cor = cor

    return lista_de_vertices


# ----------------------------------------------------------------------------------------------------------------------


def calcula_quantidade_de_cores(lista_de_vertices):
    """

    :param lista_de_vertices:
    :return:
    """
    cores = []
    for vertice in lista_de_vertices:
        if vertice.cor is None:
            cor = 99999
        else:
            cor = vertice.cor
        if cor not in cores:
            cores.append(cor)
    return len(cores)


def calcula_funcao_objetivo(quantidade_aulas_dia, lista_de_vertices, preferencias_professor):
    """

    :param quantidade_aulas_dia:
    :param lista_de_vertices:
    :param preferencias_professor:
    :return:
    """
    return get_prederencias_nao_atendidas(preferencias_professor, lista_de_vertices) + verifica_tres_aulas_seguidas(
        quantidade_aulas_dia, lista_de_vertices) + verifica_lacuna_aula(quantidade_aulas_dia, lista_de_vertices)


def get_prederencias_nao_atendidas(preferencias_professor, lista_de_vertices):
    """

    :param preferencias_professor:
    :param lista_de_vertices:
    :return:
    """
    preferencias_atendidas = 0
    for preferencia in preferencias_professor:
        for cor in preferencia[1]:
            for vertice in lista_de_vertices:
                if preferencia[0] == vertice.professor and vertice.cor == cor:
                    preferencias_atendidas += 1

    quantidade_preferencias = sum(len(preferencia[1]) for preferencia in preferencias_professor)

    return quantidade_preferencias - preferencias_atendidas


def verifica_tres_aulas_seguidas(quantidade_aulas_dia, lista_de_vertices):
    """

    :param quantidade_aulas_dia:
    :param lista_de_vertices:
    :return:
    """
    quantidade_tres_aulas_seguidas = 0
    for vertice_i in lista_de_vertices:
        for vertice_j in lista_de_vertices:
            for vertice_k in lista_de_vertices:
                if vertice_i.professor == vertice_j.professor \
                        and vertice_i.professor == vertice_k.professor \
                        and vertice_i.turma == vertice_j.turma \
                        and vertice_i.turma == vertice_k.turma \
                        and vertice_i.cor == vertice_j.cor - 1 \
                        and vertice_i.cor == vertice_k.cor - 2 \
                        and verifica_duas_cores_mesmo_dia(quantidade_aulas_dia, vertice_i.cor, vertice_j.cor) \
                        and verifica_duas_cores_mesmo_dia(quantidade_aulas_dia, vertice_i.cor, vertice_k.cor):
                    quantidade_tres_aulas_seguidas += 1
    return quantidade_tres_aulas_seguidas


def verifica_lacuna_aula(quantidade_de_aulas, lista_de_vertices):
    """

    :param quantidade_de_aulas:
    :param lista_de_vertices:
    :return:
    """
    quantidade_lacunas = 0
    for vertice in lista_de_vertices:
        if not verifica_existe_aula_cor(lista_de_vertices, vertice.professor, vertice.turma, vertice.cor + 1) \
                and verifica_existe_aula_cor(lista_de_vertices, vertice.professor, vertice.turma, vertice.cor + 2):
            if verifica_duas_cores_mesmo_dia(quantidade_de_aulas, vertice.cor, vertice.cor + 2):
                quantidade_lacunas += 1
    return quantidade_lacunas


def verifica_existe_aula_cor(lista_de_vertices, professor, turma, cor):
    """

    :param lista_de_vertices:
    :param professor:
    :param turma:
    :param cor:
    :return:
    """
    for vertice in lista_de_vertices:
        if vertice.professor == professor and vertice.turma == turma and vertice.cor == cor:
            return True
    return False


def verifica_duas_cores_mesmo_dia(quantidade_aulas_dia, cor_1, cor_2):
    """

    :param quantidade_aulas_dia:
    :param cor_1:
    :param cor_2:
    :return:
    """
    return (cor_1 - 1) // quantidade_aulas_dia == (cor_2 - 1) // quantidade_aulas_dia


# ----------------------------------------------------------------------------------------------------------------------

def main():
    """

    :return:
    """
    begin = time.time()
    # xlsx = pd.ExcelFile("./instances/Exemplo.xlsx")
    xlsx = pd.ExcelFile("./instances/Escola_A.xlsx")
    # xlsx = pd.ExcelFile("./instances/Escola_B.xlsx")
    # xlsx = pd.ExcelFile("./instances/Escola_C.xlsx")
    # xlsx = pd.ExcelFile("./instances/Escola_D.xlsx")

    restricoes_professor = le(xlsx, 'Restricao')
    preferencias_professor = le(xlsx, 'Preferencias')
    restricoes_turma = le(xlsx, 'Restricoes Turma')
    configuracao = pd.read_excel(xlsx, sheet_name='Configuracoes').values

    lista_de_vertices = cria_vertices(xlsx)
    lista_de_arestas = cria_arestas(lista_de_vertices)

    # solucao, lista_de_arestas = colore_grafo_maior_grau(cPickle.loads(cPickle.dumps(lista_de_vertices)),
    #                                                     lista_de_arestas, restricoes_professor,
    #                                                     restricoes_turma, preferencias_professor)

    # solucao, lista_de_arestas = colore_grafo_maior_restricao_professor(cPickle.loads(cPickle.dumps(lista_de_vertices)),
    #                                                                    lista_de_arestas, restricoes_professor,
    #                                                                    restricoes_turma, preferencias_professor)
    # print(calcula_quantidade_de_cores(solucao))
    # print(calcula_funcao_objetivo(len(configuracao), solucao, preferencias_professor))
    lista_de_arestas, lista_de_vertices = simulated_annealing(lista_de_vertices, lista_de_arestas, restricoes_professor,
                                                              restricoes_turma, preferencias_professor, 100, 2, 10,
                                                              0.85, len(configuracao))

    print(lista_de_arestas)
    print(calcula_quantidade_de_cores(lista_de_vertices))
    print(calcula_funcao_objetivo(len(configuracao), lista_de_vertices, preferencias_professor))
    print(lista_de_vertices)
    # print(restricoes_professor)

    print(time.time() - begin)


if __name__ == '__main__':
    main()
