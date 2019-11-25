import pandas as pd


class Dados:
    # Contantes para controle na busca de dados
    __ID = 0
    __MATERIA = 1
    __TURMA = 2
    __PROFESSOR = 3
    QUANT__IDADE_AULAS = 4

    def __init__(self, dados=None):
        self.__dados = dados

    def add_dado(self, dado):
        self.__dados.append(dado)

    def get_all(self):
        return self.__dados

    def get_dado_by_id(self, id):
        return self.__get_by_key(self.__ID, id)

    def get_materia_from_dados(self, materia):
        return self.__get_by_key(self.__MATERIA, materia)

    def get_turma_from_dados(self, turma):
        return self.__get_by_key(self.__TURMA, turma)

    def get_professor_from_dados(self, professor):
        return self.__get_by_key(self.__PROFESSOR, professor)

    def __get_by_key(self, key, value):
        return [dado for dado in self.__dados if dado[key] == value]


class Restricoes:
    # Contantes para controle na busca de dados
    __ID = 0
    __PROFESSOR = 1
    __RESTRICAO___HORARIO = 2
    ____DIA_DA_SEMANA_RESTRICAO = 3

    def __init__(self, restricoes=None):
        self.__restricoes = restricoes

    def add_restricoes(self, restricao):
        self.__restricoes.append(restricao)

    def get_all(self):
        return self.__restricoes

    def get_restricao_by_id(self, professor):
        return self.__get_by_key(self.__PROFESSOR, professor)

    def get_professor_from_restricoes(self, professor):
        return self.__get_by_key(self.__PROFESSOR, professor)

    def get_restricao_horario_from_restricoes(self, restricao_horario):
        return self.__get_by_key(self.__RESTRICAO___HORARIO, restricao_horario)

    def get_dia_da_semana_restricao_from_restricoes(self, dia_da_semana_restricao):
        return self.__get_by_key(self.____DIA_DA_SEMANA_RESTRICAO, dia_da_semana_restricao)

    def __get_by_key(self, key, value):
        return [restricao for restricao in self.__restricoes if restricao[key] == value]


class RestricoesTurma:
    # Contantes para controle na busca de dados
    __ID = 0
    __TURMA = 1
    ____HORARIO_DA_RESTRICAO = 2
    __DIA_DA_SEMANA = 3

    def __init__(self, restricoes_turma=None):
        self.__restricoes_turma = restricoes_turma

    def add_restricoes_turma(self, restricao):
        self.__restricoes_turma.append(restricao)

    def get_all(self):
        return self.__restricoes_turma

    def get_restricao_turma_by_id(self, id):
        return self.__get_by_key(self.__ID, id)

    def get_turma_from_restricoes_turma(self, turma):
        return self.__get_by_key(self.__TURMA, turma)

    def get_horario_da_restricao_from_restricoes_turma(self, horario_da_restricao):
        return self.__get_by_key(self.____HORARIO_DA_RESTRICAO, horario_da_restricao)

    def get_dia_da_semana_from_restricoes_turma(self, dia_da_semana):
        return self.__get_by_key(self.__DIA_DA_SEMANA, dia_da_semana)

    def __get_by_key(self, key, value):
        return [restricao_turma for restricao_turma in self.__restricoes_turma if restricao_turma[key] == value]


class Preferencias:
    # Contantes para controle na busca de dados
    __ID = 0
    __PROFESSOR = 1
    __HORARIO = 2
    __DIA_DA_SEMANA = 3

    def __init__(self, preferencias=None):
        self.__preferencias = preferencias

    def add_preferencias(self, restricao):
        self.__preferencias.append(restricao)

    def get_all(self):
        return self.__preferencias

    def get_preferencia_by_id(self, id):
        return self.__get_by_key(self.__ID, id)

    def get_professor_from_preferencias(self, professor):
        return self.__get_by_key(self.__PROFESSOR, professor)

    def get_horario_from_preferencias_turma(self, horario):
        return self.__get_by_key(self.__HORARIO, horario)

    def get_dia_da_semana_from_preferencias(self, dia_da_semana):
        return self.__get_by_key(self.__DIA_DA_SEMANA, dia_da_semana)

    def __get_by_key(self, key, value):
        return [preferencia for preferencia in self.__preferencias if preferencia[key] == value]


def get_planilha_from_xlsx(xlsx, planilha):
    data_frame_dados = pd.read_excel(xlsx, sheet_name=planilha)
    dados_frame = data_frame_dados.values

    return [[i] + list(dados_frame[i]) for i in range(len(dados_frame))]


def read_xlsx(path):
    return pd.ExcelFile(path)


if __name__ == '__main__':
    xlsx = read_xlsx("./instances/Escola_A.xlsx")

    dados = Dados(get_planilha_from_xlsx(xlsx, 'Dados'))
    configuracoes = get_planilha_from_xlsx(xlsx, 'Configuracoes')
    restricao = Restricoes(get_planilha_from_xlsx(xlsx, 'Restricao'))
    restricoes_turma = RestricoesTurma(get_planilha_from_xlsx(xlsx, 'Restricoes Turma'))
    preferencias = Preferencias(get_planilha_from_xlsx(xlsx, 'Preferencias'))

    print(dados.get_professor_from_dados('Professor 1'))
