import pandas as pd
from collections import defaultdict


class Dados:
    # Contantes para controle na busca de dados
    __ID = 0
    __MATERIA = 1
    __TURMA = 2
    __PROFESSOR = 3
    __QUANTIDADE_AULAS = 4

    def __init__(self, dados=None):
        self.__dados = dados

    def add_dado(self, dado):
        self.__dados.append(dado)

    def get_all(self):
        return self.__dados

    def get_dado_by_id(self, id):
        return self.__get_by_key(self.__ID, id)

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
    # Contantes para controle na busca de dados
    __ID = 0
    __PROFESSOR = 1
    __RESTRICAO___HORARIO = 2
    __DIA_DA_SEMANA_RESTRICAO = 3

    def __init__(self, restricoes=None):
        self.__restricoes = restricoes

    def add_restricoes(self, restricao):
        self.__restricoes.append(restricao)

    def get_all(self):
        return self.__restricoes

    def get_restricao_by_id(self, professor):
        return self.__get_by_key(self.__PROFESSOR, professor)

    def get_restricao_by_professor(self, professor):
        return self.__get_by_key(self.__PROFESSOR, professor)

    def get_restricao_by_restricao_horario(self, restricao_horario):
        return self.__get_by_key(self.__RESTRICAO___HORARIO, restricao_horario)

    def get_restricao_by_dia_da_semana_restricao(self, dia_da_semana_restricao):
        return self.__get_by_key(self.__DIA_DA_SEMANA_RESTRICAO, dia_da_semana_restricao)

    def __get_by_key(self, key, value):
        return [restricao for restricao in self.__restricoes if restricao[key] == value]


class RestricoesTurma:
    # Contantes para controle na busca de dados
    __ID = 0
    __TURMA = 1
    __HORARIO_DA_RESTRICAO = 2
    __DIA_DA_SEMANA = 3

    def __init__(self, restricoes_turma=None):
        self.__restricoes_turma = restricoes_turma

    def add_restricoes_turma(self, restricao):
        self.__restricoes_turma.append(restricao)

    def get_all(self):
        return self.__restricoes_turma

    def get_restricao_turma_by_id(self, id):
        return self.__get_by_key(self.__ID, id)

    def get_restricao_turma_by_turma(self, turma):
        return self.__get_by_key(self.__TURMA, turma)

    def get_restricao_turma_by_horario_da_restricao(self, horario_da_restricao):
        return self.__get_by_key(self.__HORARIO_DA_RESTRICAO, horario_da_restricao)

    def get_restricao_turma_by_dia_da_semana(self, dia_da_semana):
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

    def get_preferencia_by_professor(self, professor):
        return self.__get_by_key(self.__PROFESSOR, professor)

    def get_preferencia_by_horario(self, horario):
        return self.__get_by_key(self.__HORARIO, horario)

    def get_preferencia_by_dia_da_semana(self, dia_da_semana):
        return self.__get_by_key(self.__DIA_DA_SEMANA, dia_da_semana)

    def __get_by_key(self, key, value):
        return [preferencia for preferencia in self.__preferencias if preferencia[key] == value]


class Grafo(object):
    """ Implementação básica de um grafo. """

    def __init__(self, arestas, direcionado=False):
        """Inicializa as estruturas base do grafo."""
        self.adj = defaultdict(set)
        self.direcionado = direcionado
        self.adiciona_arestas(arestas)

    def get_vertices(self):
        """ Retorna a lista de vértices do grafo. """
        return list(self.adj.keys())

    def get_arestas(self):
        """ Retorna a lista de arestas do grafo. """
        return [(k, v) for k in self.adj.keys() for v in self.adj[k]]

    def adiciona_arestas(self, arestas):
        """ Adiciona arestas ao grafo. """
        for u, v in arestas:
            self.adiciona_arco(u, v)

    def adiciona_arco(self, u, v):
        """ Adiciona uma ligação (arco) entre os nodos 'u' e 'v'. """
        self.adj[u].add(v)
        # Se o grafo é não-direcionado, precisamos adicionar arcos nos dois sentidos.
        if not self.direcionado:
            self.adj[v].add(u)

    def existe_aresta(self, u, v):
        """ Existe uma aresta entre os vértices 'u' e 'v'? """
        return u in self.adj and v in self.adj[u]

    def __len__(self):
        return len(self.adj)

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, dict(self.adj))

    def __getitem__(self, v):
        return self.adj[v]


def get_planilha_from_xlsx(xlsx, planilha):
    data_frame_dados = pd.read_excel(xlsx, sheet_name=planilha)
    dados_frame = data_frame_dados.values

    return [tuple([i] + list(dados_frame[i])) for i in range(len(dados_frame))]


def read_xlsx(path):
    return pd.ExcelFile(path)


def SimulatedAnnealing():
    pass


if __name__ == '__main__':
    xlsx = read_xlsx("./instances/Escola_A.xlsx")

    dados = Dados(get_planilha_from_xlsx(xlsx, 'Dados'))
    configuracoes = get_planilha_from_xlsx(xlsx, 'Configuracoes')
    restricoes = Restricoes(get_planilha_from_xlsx(xlsx, 'Restricao'))
    restricoes_turma = RestricoesTurma(get_planilha_from_xlsx(xlsx, 'Restricoes Turma'))
    preferencias = Preferencias(get_planilha_from_xlsx(xlsx, 'Preferencias'))

    # (professor, [lista de preferencias])
    professor_lista_de_preferencias = [
        tuple([professor, preferencias.get_preferencia_by_professor(professor)]) for
        professor in dados.get_professores()]

    # (professor, [lista de restricoes)
    professor_lista_de_restricoes = [
        tuple([professor, restricoes.get_restricao_by_professor(professor)]) for
        professor in dados.get_professores()]

    # (turma, [lista de restrições])
    turma_lista_de_restricoes = [
        tuple([turma, restricoes_turma.get_restricao_turma_by_turma(turma)]) for
        turma in dados.get_turmas()]

    # Cria a lista de arestas.
    # arestas = [('A', 'B'), ('B', 'C')]
    # arestas = [(tuple([1, 2, 3]), tuple([5, 2, 3])), (tuple([6, 2, 3]), tuple([7, 2, 3]))]

    # Cria e imprime o grafo.
    # grafo = Grafo(arestas, direcionado=True)
    # print(grafo.adj)
