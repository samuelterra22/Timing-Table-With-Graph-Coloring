import pandas as pd
from random import random
from math import exp


class Dados:
    __MATERIA = 0
    __TURMA = 1
    __PROFESSOR = 2
    __QUANTIDADE_AULAS = 3

    def __init__(self, dados=None):
        self.__dados = dados

    def add_dado(self, dado):
        self.__dados.append(dado)

    def get_all(self):
        return self.__dados

    def get_dados_by_materia(self, materia):
        return self.__get_by_key(self.__MATERIA, materia)

    def get_dados_by_turma(self, turma):
        return self.__get_by_key(self.__TURMA, turma)

    def get_dados_by_professor(self, professor):
        return self.__get_by_key(self.__PROFESSOR, professor)

    def get_dados_by_quantidade_aulas(self, quantidade_aulas):
        return self.__get_by_key(self.__QUANTIDADE_AULAS, quantidade_aulas)

    def get_professores(self):
        return list(set([dado[self.__PROFESSOR] for dado in self.__dados]))

    def get_turmas(self):
        return list(set([dado[self.__TURMA] for dado in self.__dados]))

    def __get_by_key(self, key, value):
        return [dado for dado in self.__dados if dado[key] == value]


class Restricoes:
    __PROFESSOR = 0
    __RESTRICAO___HORARIO = 1
    __DIA_DA_SEMANA_RESTRICAO = 2

    def __init__(self, restricoes=None):
        self.__restricoes = restricoes

    def add_restricoes(self, restricao):
        self.__restricoes.append(restricao)

    def get_all(self):
        return self.__restricoes

    def get_restricao_by_professor(self, professor):
        return [restricao[1:len(restricao)] for restricao in self.__restricoes if
                restricao[self.__PROFESSOR] == professor]

    def get_restricao_by_restricao_horario(self, restricao_horario):
        return self.__get_by_key(self.__RESTRICAO___HORARIO, restricao_horario)

    def get_restricao_by_dia_da_semana_restricao(self, dia_da_semana_restricao):
        return self.__get_by_key(self.__DIA_DA_SEMANA_RESTRICAO, dia_da_semana_restricao)

    def __get_by_key(self, key, value):
        return [restricao for restricao in self.__restricoes if restricao[key] == value]


class RestricoesTurma:
    __TURMA = 0
    __HORARIO_DA_RESTRICAO = 1
    __DIA_DA_SEMANA = 2

    def __init__(self, restricoes_turma=None):
        self.__restricoes_turma = restricoes_turma

    def add_restricoes_turma(self, restricao):
        self.__restricoes_turma.append(restricao)

    def get_all(self):
        return self.__restricoes_turma

    def get_dias_semana(self):
        return list(set([dado[self.__DIA_DA_SEMANA] for dado in self.__restricoes_turma]))

    def get_restricao_turma_by_turma(self, turma):
        return [restricao[1:len(restricao)] for restricao in self.__restricoes_turma if
                restricao[self.__TURMA] == turma]

    def get_restricao_turma_by_horario_da_restricao(self, horario_da_restricao):
        return self.__get_by_key(self.__HORARIO_DA_RESTRICAO, horario_da_restricao)

    def get_restricao_turma_by_dia_da_semana(self, dia_da_semana):
        return self.__get_by_key(self.__DIA_DA_SEMANA, dia_da_semana)

    def __get_by_key(self, key, value):
        return [restricao_turma for restricao_turma in self.__restricoes_turma if restricao_turma[key] == value]


class Preferencias:
    __PROFESSOR = 0
    __HORARIO = 1
    __DIA_DA_SEMANA = 2

    def __init__(self, preferencias=None):
        self.__preferencias = preferencias

    def add_preferencias(self, restricao):
        self.__preferencias.append(restricao)

    def get_all(self):
        return self.__preferencias

    def get_preferencia_by_professor(self, professor):
        ret = []
        for preferencia in self.__preferencias:
            if preferencia[self.__PROFESSOR] == professor:
                preferencia[1:len(preferencia)]

    def get_preferencia_by_horario(self, horario):
        return self.__get_by_key(self.__HORARIO, horario)

    def get_preferencia_by_dia_da_semana(self, dia_da_semana):
        return self.__get_by_key(self.__DIA_DA_SEMANA, dia_da_semana)

    def __get_by_key(self, key, value):
        return [preferencia for preferencia in self.__preferencias if preferencia[key] == value]


class Vertice:
    def __init__(self, id, professor, materia, turma, cor):
        self.id = id
        self.professor = professor
        self.materia = materia
        self.turma = turma
        self.cor = cor

    def update_cor(self, cor):
        self.cor = cor


def get_planilha_from_xlsx(xlsx, planilha):
    data_frame_dados = pd.read_excel(xlsx, sheet_name=planilha)
    dados_frame = data_frame_dados.values

    return [tuple(dados_frame) for dados_frame in dados_frame]


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


if __name__ == '__main__':
    xlsx = pd.ExcelFile("./instances/Escola_A.xlsx")

    professor_restricoes_turma = le(xlsx, 'Restricao')
    professor_preferecias = le(xlsx, 'Preferencias')
    restricoes_turma = le(xlsx, 'Restricoes Turma')

    print(professor_restricoes_turma)
    print(professor_preferecias)
    print(restricoes_turma)

    # dados = Dados(get_planilha_from_xlsx(xlsx, 'Dados'))
    # configuracao = get_planilha_from_xlsx(xlsx, 'Configuracoes')
    # restricoes = Restricoes(get_planilha_from_xlsx(xlsx, 'Restricao'))
    # preferencias = Preferencias(get_planilha_from_xlsx(xlsx, 'Preferencias'))

    # (professor, [lista de preferencias do professor])
    # professor_lista_de_preferencias = [
    #     tuple([professor, preferencias.get_preferencia_by_professor(professor)]) for
    #     professor in dados.get_professores()]

    # (professor, [lista de restricoes do professor)
    # professor_lista_de_restricoes = [
    #     tuple([professor, restricoes.get_restricao_by_professor(professor)]) for
    #     professor in dados.get_professores()]

    # (turma, [lista de restrições da turma])
    # turma_lista_de_restricoes = [
    #     tuple([turma, restricoes_turma.get_restricao_turma_by_turma(turma)]) for
    #     turma in dados.get_turmas()]

    # dias_da_semana = restricoes_turma.get_dias_semana()
    # print(calcula_cor(configuracao, datetime.time(7, 50), 'Segunda'))
    # print(professor_lista_de_preferencias)
