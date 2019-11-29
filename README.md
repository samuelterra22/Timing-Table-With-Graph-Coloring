# Timing Table With Graph Coloring


### Instalar dependências do Linux

```shell script
sudo apt update
sudo apt install build-essential \
                 software-properties-common \
                 python3-pip \
                 python3-distutils
```

### Criar ambiente e instalar dependências do Python

```shell script
pip3 install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Introdução

O planejamento de horários em instituições de ensino constitui um desafio para diretores e coordenadores pedagógicos. De fato, trata-se de uma tarefa passível a erros, devido ao seu caráter combinatório, e que exige demasiado tempo de elaboração. O problema consiste em designar horários a turmas já pré-estabelecidas, levando em conta as seguintes restrições obrigatórias:

- não é permitido a alocação de duas aulas para o mesmo professor no mesmo horário;
- não pode haver duas aulas para a mesma turma no mesmo horário;
- todas as aulas devem ser alocadas ao longo dos dias de funcionameno da escola e turnos de aula pré-determinados;
- professores não devem ser alocados m horários nos quais eles não podem estar presentes.

Algumas características são consideradas desejáveis, variando de acordo com as recomendações pedagógicas e cunho pessoal. Tais particularidades são listadas a seguir:

- uma turma não deverá ter três ou mais aulas geminadas da mesma disciplina, em horários sequenciais;
- não deverá haver horários de aula separados por grandes janelas entre aulas, para a mesma turma. Exemplo: suponha que durante o dia, os alunos tivessem 5 horários de aulas. Então, considere que no 1º e 2º horários houvesse aula, depois no 3º horários houvesse aula, depois no 3º houvesse uma janela, e nos 4º e 5º horários os alunos voltassem a ter aulas. Logo, a solução sofreria uma penalidade. O ideial seria ter 4 aulas sequenciais, e o 5º horário livre.
- deve-se buscar atender às preferências de cada professor em relação a dias ou horários em que possa lecionar.

A atividade em questão pode ser automatizada, e você, detentor de conhecimentos em Projeo de Análise de Algoritmos, pode contribuir para auxiliar os responsáveis pela elaboração de horários.

### Objetivo

Desenvolva um algoritmo eficiente que encontre a distribuição de horários para cada turma, minimizando o número de restrições desejáveis não atendidas. Para tanto, implemente uma abordagem baseada em coloração de vértices.

