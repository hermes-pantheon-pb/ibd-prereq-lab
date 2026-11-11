"""
Append Módulos 7 e 8 em db_engine.py
"""

import sys

NEW_EXERCISES_CODE = '''
    # =========================================================================
    # MÓDULO 7: MAPEAMENTO ER/EER PARA ESQUEMA RELACIONAL (TRANSFORMAÇÃO)
    # =========================================================================
    "T7.1": {
        "title": "Mapeamento das 7 Regras Básicas: Entidades, Multivalorados e Fracas",
        "type": "treino",
        "mode": "structured",
        "setup": "",
        "fields": [
            {
                "id": "q1",
                "label": "1. [Regra 1 e 2] Dado o tipo de entidade DEPARTAMENTO com atributos simples DNumber (PK), DName (chave alternativa) e o atributo MULTIVALORADO Locations {Houston, Stafford, Bellaire}. Como esses dados são mapeados para o modelo relacional?",
                "options": [
                    "Cria-se a relação DEPARTAMENTO(DNumber(nn), DName(nn)) e uma relação separada DEPT_LOCATIONS(DNumber(nn), DLocation(nn)) com PK composta (DNumber, DLocation) e RIR DEPT_LOCATIONS[DNumber] -p-> DEPARTAMENTO[DNumber] (política p/CASCADE obrigatória)",
                    "Cria-se apenas a relação DEPARTAMENTO com colunas DLocation1, DLocation2, DLocation3",
                    "DEPT_LOCATIONS vira uma chave estrangeira simples dentro de DEPARTAMENTO",
                    "Atributos multivalorados são ignorados no modelo relacional por violarem a 1FN"
                ],
                "answer": "Cria-se a relação DEPARTAMENTO(DNumber(nn), DName(nn)) e uma relação separada DEPT_LOCATIONS(DNumber(nn), DLocation(nn)) com PK composta (DNumber, DLocation) e RIR DEPT_LOCATIONS[DNumber] -p-> DEPARTAMENTO[DNumber] (política p/CASCADE obrigatória)",
                "explanation": "Slide 14 de ibd-parte5.pdf: Cada atributo multivalorado de uma entidade gera uma nova tabela própria cuja chave primária é composta pela PK da entidade dona + o próprio valor do atributo, com política de remoção p (propagação / CASCADE)."
            },
            {
                "id": "q2",
                "label": "2. [Regra 3] Uma Entidade Fraca DEPENDENT (chave parcial Dependent_Name) subordinada à entidade dona EMPLOYEE (chave SSN) via relacionamento identificador DEPENDENTS_OF. Qual é a chave primária de DEPENDENT e sua RIR?",
                "options": [
                    "Chave Primária composta: (ESSN, Dependent_Name), onde ESSN referencia EMPLOYEE(SSN) com política p (propagação / ON DELETE CASCADE)",
                    "Chave Primária simples: Dependent_Name, e ESSN é chave estrangeira opcional com política b",
                    "DEPENDENT não vira tabela, vira atributo de EMPLOYEE",
                    "Chave Primária: ESSN sozinho"
                ],
                "answer": "Chave Primária composta: (ESSN, Dependent_Name), onde ESSN referencia EMPLOYEE(SSN) com política p (propagação / ON DELETE CASCADE)",
                "explanation": "Slide 15 de ibd-parte5.pdf: Uma entidade fraca é identificada pelo par (PK do dono + discriminador/chave parcial). A exclusão do empregado dono obriga a propagação (p) da remoção de seus dependentes."
            },
            {
                "id": "q3",
                "label": "3. [Regra 4 e 5] No relacionamento 1:N WORKS_FOR entre EMPLOYEE (lado N, participação total) e DEPARTMENT (lado 1). No mapeamento otimizado (slide 18 de ibd-parte5.pdf):",
                "options": [
                    "A chave primária DNumber de DEPARTMENT migra como Chave Estrangeira DNO para a tabela EMPLOYEE, com restrição NOT NULL (devido à participação total) e política b (bloqueio)",
                    "Cria-se uma tabela intermediária WORKS_FOR com duas chaves estrangeiras",
                    "A chave SSN de EMPLOYEE migra para DEPARTMENT",
                    "Ambas as tabelas são fundidas em uma única relação"
                ],
                "answer": "A chave primária DNumber de DEPARTMENT migra como Chave Estrangeira DNO para a tabela EMPLOYEE, com restrição NOT NULL (devido à participação total) e política b (bloqueio)",
                "explanation": "Em relacionamentos funcionais N:1, o mapeamento otimizado migra a chave do lado 1 para o lado N. Como todo empregado trabalha para um departamento, DNO é NOT NULL."
            }
        ]
    },
    "T7.2": {
        "title": "Mapeamento de Relacionamentos M:N e Agregações EER",
        "type": "treino",
        "mode": "structured",
        "setup": "",
        "fields": [
            {
                "id": "q1",
                "label": "1. No relacionamento M:N WORKS_ON entre EMPLOYEE(SSN) e PROJECT(PNumber), com atributo de relacionamento Hours. Qual é o esquema relacional resultante?",
                "options": [
                    "WORKS_ON(ESSN(nn), PNO(nn), Hours), com PK composta (ESSN, PNO), WORKS_ON[ESSN] -p-> EMPLOYEE[SSN] e WORKS_ON[PNO] -p-> PROJECT[PNumber]",
                    "Adiciona-se PNO e Hours como colunas da tabela EMPLOYEE",
                    "Adiciona-se ESSN e Hours como colunas da tabela PROJECT",
                    "Cria-se uma tabela para cada valor de Hours"
                ],
                "answer": "WORKS_ON(ESSN(nn), PNO(nn), Hours), com PK composta (ESSN, PNO), WORKS_ON[ESSN] -p-> EMPLOYEE[SSN] e WORKS_ON[PNO] -p-> PROJECT[PNumber]",
                "explanation": "Slide 21 de ibd-parte5.pdf: Um relacionamento M:N sempre gera uma relação separada com as chaves primárias de ambas as entidades formando a chave primária composta, com opções de remoção p (propagação)."
            },
            {
                "id": "q2",
                "label": "2. No slide 40 de ibd-parte5.pdf, a agregação `Executa` conecta o relacionamento `Participa-de(Empregado, Projeto)` com a entidade `Tarefa(CodTar, Desc)`. Como `Tarefa` é representada no modelo relacional?",
                "options": [
                    "Tarefa(CodTar(nn), Desc, NEmp(nn), NProj(nn)) com a RIR Tarefa[NEmp, NProj] -b-> Participa-de[NEmp, NProj]",
                    "Tarefa(CodTar(nn), Desc) sem chaves estrangeiras",
                    "Participa-de recebe CodTar como chave estrangeira simples",
                    "Uma agregação não pode ser representada no modelo relacional"
                ],
                "answer": "Tarefa(CodTar(nn), Desc, NEmp(nn), NProj(nn)) com a RIR Tarefa[NEmp, NProj] -b-> Participa-de[NEmp, NProj]",
                "explanation": "Slide 40 de ibd-parte5.pdf: Quando uma entidade Tarefa se relaciona com a agregação do relacionamento Participa-de, Tarefa recebe a chave primária composta de Participa-de (NEmp, NProj) como chave estrangeira referenciando Participa-de!"
            }
        ]
    },
    "E7.1": {
        "title": "[Oficial ExercicioProjetoLogico.pdf] Mapeamento Relacional Completo do Sistema Aéreo",
        "type": "oficial",
        "mode": "structured",
        "setup": "",
        "fields": [
            {
                "id": "q1",
                "label": "1. Considere o tipo de entidade fraca `TRECHO_VOO` (chave parcial `Trecho_num`), identificada pelo voo dono `VOO` (chave primária `Numero`). Além disso, `TRECHO_VOO` possui relacionamentos N:1 `AEROPORTO_PARTIDA` e `AEROPORTO_CHEGADA` com `AEROPORTO` (chave `Codigo_aeroporto`). Qual é o esquema relacional correto de `TRECHO_VOO`?",
                "options": [
                    "TRECHO_VOO(Numero_voo(nn), Trecho_num(nn), Cod_aeroporto_partida(nn), Cod_aeroporto_chegada(nn), Horario_partida_previsto, Horario_chegada_previsto), com PK (Numero_voo, Trecho_num) e FKs para VOO e AEROPORTO",
                    "TRECHO_VOO(Trecho_num(nn), Cod_aeroporto_partida, Cod_aeroporto_chegada) com PK Trecho_num",
                    "TRECHO_VOO(Numero_voo(nn), Cod_aeroporto(nn))",
                    "VOO recebe Trecho_num como atributo multivalorado"
                ],
                "answer": "TRECHO_VOO(Numero_voo(nn), Trecho_num(nn), Cod_aeroporto_partida(nn), Cod_aeroporto_chegada(nn), Horario_partida_previsto, Horario_chegada_previsto), com PK (Numero_voo, Trecho_num) e FKs para VOO e AEROPORTO",
                "explanation": "ExercicioProjetoLogico.pdf: Como TRECHO_VOO é fraca de VOO, sua PK é (Numero_voo, Trecho_num). Como cada trecho parte de um aeroporto e chega em outro, recebe duas FKs para AEROPORTO mais os atributos de horário."
            },
            {
                "id": "q2",
                "label": "2. Analise a entidade fraca de segundo nível `INSTANCIA_TRECHO` (chave parcial `Data`), identificada por `TRECHO_VOO` via relacionamento `INSTANCIA_DE`. Além disso, ela se relaciona N:1 com `AERONAVE` (relacionamento `DESIGNADA`). Qual é o esquema relacional de `INSTANCIA_TRECHO`?",
                "options": [
                    "INSTANCIA_TRECHO(Numero_voo(nn), Trecho_num(nn), Data(nn), Cod_aeronave(nn), Hora_partida, Hora_chegada, Numero_assentos_disponiveis), com PK composta de 3 atributos (Numero_voo, Trecho_num, Data)",
                    "INSTANCIA_TRECHO(Data(nn), Cod_aeronave(nn))",
                    "INSTANCIA_TRECHO(Numero_voo(nn), Data(nn))",
                    "AERONAVE recebe a data do voo como atributo"
                ],
                "answer": "INSTANCIA_TRECHO(Numero_voo(nn), Trecho_num(nn), Data(nn), Cod_aeronave(nn), Hora_partida, Hora_chegada, Numero_assentos_disponiveis), com PK composta de 3 atributos (Numero_voo, Trecho_num, Data)",
                "explanation": "Cadeia de entidades fracas: TRECHO_VOO herda Numero_voo de VOO; INSTANCIA_TRECHO herda (Numero_voo, Trecho_num) de TRECHO_VOO somada à sua data! A PK de INSTANCIA_TRECHO possui portanto 3 atributos."
            },
            {
                "id": "q3",
                "label": "3. No relacionamento M:N `PODE_POUSAR` entre `AEROPORTO` (chave `Codigo_aeroporto`) e `TIPO_AERONAVE` (chave `Tipo_nome`). Como ele é representado?",
                "options": [
                    "PODE_POUSAR(Codigo_aeroporto(nn), Tipo_nome(nn)), com PK composta (Codigo_aeroporto, Tipo_nome) e políticas p (CASCADE) para ambas as entidades fortes",
                    "AEROPORTO recebe Tipo_nome como chave estrangeira simples",
                    "TIPO_AERONAVE recebe Codigo_aeroporto como chave estrangeira simples",
                    "Cria-se uma visão em SQL sem persistência de tabela"
                ],
                "answer": "PODE_POUSAR(Codigo_aeroporto(nn), Tipo_nome(nn)), com PK composta (Codigo_aeroporto, Tipo_nome) e políticas p (CASCADE) para ambas as entidades fortes",
                "explanation": "Relacionamento M:N puro entre entidades fortes: gera tabela própria com as PKs de ambas as entidades formando a PK composta."
            }
        ]
    },

    # =========================================================================
    # MÓDULO 8: NORMALIZAÇÃO DE DADOS: DF, FECHAMENTO, 1FN, 2FN E 3FN
    # =========================================================================
    "T8.1": {
        "title": "Algoritmo de Fechamento de Atributos (X+) e Determinação de Chaves",
        "type": "treino",
        "mode": "structured",
        "setup": "",
        "fields": [
            {
                "id": "q1",
                "label": "1. Dado o esquema R(A, B, C, D) e o conjunto de dependências funcionais F = {A -> B, B -> C, C -> D}. Qual é o fechamento de A, ou seja, {A}+ ?",
                "options": [
                    "{A}+ = {A, B, C, D}. Como contém todos os atributos de R, A é superchave (e chave candidata minimal)",
                    "{A}+ = {A, B} apenas",
                    "{A}+ = {A, D} por eliminação",
                    "{A}+ = ∅ (vazio)"
                ],
                "answer": "{A}+ = {A, B, C, D}. Como contém todos os atributos de R, A é superchave (e chave candidata minimal)",
                "explanation": "Inicia com X+ = {A}. Pela regra transitiva ou aplicação do Algoritmo 14.1 (ibd-parte6.pdf): A -> B adiciona B; B -> C adiciona C; C -> D adiciona D. Logo {A}+ = {A, B, C, D}."
            },
            {
                "id": "q2",
                "label": "2. Dado R(A, B, C, D) com F = {A -> B, C -> D}. Qual é o fechamento {A}+ e qual conjunto forma a chave candidata de R?",
                "options": [
                    "{A}+ = {A, B} (não cobre C e D). A chave candidata de R é {A, C}, pois {A, C}+ = {A, B, C, D}",
                    "{A}+ cobre todos os atributos",
                    "{B, D} é a chave candidata",
                    "R não possui nenhuma chave candidata"
                ],
                "answer": "{A}+ = {A, B} (não cobre C e D). A chave candidata de R é {A, C}, pois {A, C}+ = {A, B, C, D}",
                "explanation": "Atributos que nunca aparecem no lado direito de nenhuma dependência funcional (como A e C) devem obrigatoriamente fazer parte de toda chave candidata de R! Calculando {A, C}+ obtemos {A, B, C, D}."
            }
        ]
    },
    "T8.2": {
        "title": "Diagnóstico de Violações de 2FN e 3FN (Slides ibd-parte6)",
        "type": "treino",
        "mode": "structured",
        "setup": "",
        "fields": [
            {
                "id": "q1",
                "label": "1. Considere a relação EMP_PROJ(SSN, PNumber, Hours, EName, PName, PLocation) com chave primária composta {SSN, PNumber} e dependências: {SSN, PNumber} -> Hours, SSN -> EName, PNumber -> {PName, PLocation}. Por que ela viola a 2FN?",
                "options": [
                    "Porque EName depende parcialmente de parte da chave (SSN), e PName/PLocation dependem parcialmente de PNumber. Na 2FN, todo atributo não-primo deve depender TOTALMENTE de toda a chave primária!",
                    "Porque Hours é um número decimal",
                    "Porque existem tuplas duplicadas",
                    "Porque viola a integridade referencial"
                ],
                "answer": "Porque EName depende parcialmente de parte da chave (SSN), e PName/PLocation dependem parcialmente de PNumber. Na 2FN, todo atributo não-primo deve depender TOTALMENTE de toda a chave primária!",
                "explanation": "Slide 21 de ibd-parte6.pdf: Dependência parcial ocorre quando um atributo não-primo depende de um subconjunto próprio de uma chave candidata composta."
            },
            {
                "id": "q2",
                "label": "2. Considere EMP_DEPT(SSN, EName, BDate, Address, DNumber, DName, DMgrSSN) com chave primária simples SSN e dependências: SSN -> {EName, BDate, Address, DNumber} e DNumber -> {DName, DMgrSSN}. Ela está na 2FN, mas viola a 3FN por quê?",
                "options": [
                    "Porque há uma dependência transitiva: SSN -> DNumber e DNumber -> {DName, DMgrSSN}, onde DNumber não é chave candidata de R",
                    "Porque viola a primeira forma normal",
                    "Porque a chave primária tem mais de um atributo",
                    "Porque DMgrSSN aceita nulo"
                ],
                "answer": "Porque há uma dependência transitiva: SSN -> DNumber e DNumber -> {DName, DMgrSSN}, onde DNumber não é chave candidata de R",
                "explanation": "Slide 24 de ibd-parte6.pdf: Uma dependência funcional X -> Y viola a 3FN quando X não é uma superchave e Y não é atributo primo (dependência transitiva a partir da PK)."
            }
        ]
    },
    "E8.1": {
        "title": "[Oficial Lista Normalização Q1] Chaves Candidatas em R(A, B, C, D, E)",
        "type": "oficial",
        "mode": "structured",
        "setup": "",
        "fields": [
            {
                "id": "q1",
                "label": "1. (Questão 1 da Lista Oficial) Considere a relação R(A, B, C, D, E) com as dependências funcionais: AB -> C  e  CD -> E. Pergunta: AB é chave candidata dessa relação? Se não, ABD é?",
                "options": [
                    "AB NÃO é chave candidata (pois {AB}+ = {A, B, C}, não alcança D nem E). Já ABD É chave candidata, pois {ABD}+ = {A, B, C, D, E} e nenhum subconjunto próprio de ABD cobre todos os atributos!",
                    "AB é chave candidata porque determina C",
                    "ABD não é chave porque possui 3 atributos",
                    "Apenas {A, B, C, D, E} juntos podem ser chave"
                ],
                "answer": "AB NÃO é chave candidata (pois {AB}+ = {A, B, C}, não alcança D nem E). Já ABD É chave candidata, pois {ABD}+ = {A, B, C, D, E} e nenhum subconjunto próprio de ABD cobre todos os atributos!",
                "explanation": "Exercícios de Normalização (Q1): {AB}+ = {A, B, C}. Faltam D e E. Como D nunca aparece em lado direito de nenhuma dependência, D deve pertencer à chave. Testando {ABD}+: por AB->C temos {A,B,C,D}; por CD->E temos {A,B,C,D,E}. Como {AB}+, {AD}+ e {BD}+ não cobrem R, ABD é chave mínima!"
            }
        ]
    },
    "E8.2": {
        "title": "[Oficial Lista Normalização Q2] Decomposição em 2FN e 3FN de R(A..J)",
        "type": "oficial",
        "mode": "structured",
        "setup": "",
        "fields": [
            {
                "id": "q1",
                "label": "1. (Questão 2 da Lista Oficial) Dada R(A, B, C, D, E, F, G, H, I, J) com F = {AB -> C, A -> DE, B -> F, F -> GH, D -> IJ}. Qual é a ÚNICA chave candidata de R?",
                "options": [
                    "A chave de R é {A, B}, pois {AB}+ = {A, B, C, D, E, F, G, H, I, J}",
                    "A chave de R é {A, B, D}",
                    "A chave de R é {F, D}",
                    "A chave de R é {A, B, C}"
                ],
                "answer": "A chave de R é {A, B}, pois {AB}+ = {A, B, C, D, E, F, G, H, I, J}",
                "explanation": "Calculando o fechamento de {AB}: AB->C; A->DE adiciona D,E; D->IJ adiciona I,J; B->F adiciona F; F->GH adiciona G,H. Todos os 10 atributos pertencem a {AB}+. Como nem {A}+ nem {B}+ cobrem R, {AB} é a chave candidata única!"
            },
            {
                "id": "q2",
                "label": "2. Decomponha R em relações na 2FN (eliminando dependências parciais da chave composta {A, B}):",
                "options": [
                    "R1(A, B, C),  R2(A, D, E, I, J),  R3(B, F, G, H)",
                    "R1(A, B),  R2(C, D, E),  R3(F, G, H, I, J)",
                    "R1(A, B, C, D, E),  R2(F, G, H, I, J)",
                    "A relação R já está na 2FN"
                ],
                "answer": "R1(A, B, C),  R2(A, D, E, I, J),  R3(B, F, G, H)",
                "explanation": "Na chave composta {AB}, A->DEIJ é dependência parcial (vai para R2 com chave A) e B->FGH é dependência parcial (vai para R3 com chave B). Em R1 fica a chave {AB} com o atributo C que depende totalmente dela!"
            },
            {
                "id": "q3",
                "label": "3. Agora decomponha as relações resultantes na 3FN (eliminando as dependências transitivas D -> IJ em R2 e F -> GH em R3):",
                "options": [
                    "R1(A, B, C),  R21(A, D, E),  R22(D, I, J),  R31(B, F),  R32(F, G, H)",
                    "R1(A, B, C),  R2(A, D, E, I, J),  R3(B, F, G, H)",
                    "R1(A, B),  R2(D, I),  R3(F, G)",
                    "Todas as relações já estavam na 3FN"
                ],
                "answer": "R1(A, B, C),  R21(A, D, E),  R22(D, I, J),  R31(B, F),  R32(F, G, H)",
                "explanation": "Em R2(A, D, E, I, J), a chave é A e temos a dependência transitiva D -> IJ (onde D não é chave). Decompõe-se em R21(A, D, E) com PK A e R22(D, I, J) com PK D. Em R3(B, F, G, H), a chave é B e temos a transitiva F -> GH. Decompõe-se em R31(B, F) com PK B e R32(F, G, H) com PK F!"
            }
        ]
    },
    "E8.3": {
        "title": "[Oficial Lista Normalização Q3] Sistema Acadêmico de Cursos e Turmas",
        "type": "oficial",
        "mode": "structured",
        "setup": "",
        "fields": [
            {
                "id": "q1",
                "label": "1. (Questão 3 da Lista Oficial) Dada R = (CourseNo, SecNo, OfferDept, CredHours, CourseLevel, ISSN, Sem, Year, Days_Hours, RoomNo, NoOfStuds) com DF1: {CourseNo} -> {OfferDept, CredHours, CourseLevel}, DF2: {CourseNo, SecNo, Sem, Year} -> {Days_Hours, RoomNo, NoOfStuds, ISSN}, e DF3: {RoomNo, Days_Hours, Sem, Year} -> {ISSN, CourseNo, SecNo}. Quais conjuntos formam as chaves candidatas de R?",
                "options": [
                    "Duas chaves candidatas: K1 = {CourseNo, SecNo, Sem, Year} e K2 = {RoomNo, Days_Hours, Sem, Year}",
                    "Apenas {CourseNo, SecNo, Sem, Year}",
                    "Apenas {CourseNo}",
                    "Todos os 11 atributos juntos formam a única chave"
                ],
                "answer": "Duas chaves candidatas: K1 = {CourseNo, SecNo, Sem, Year} e K2 = {RoomNo, Days_Hours, Sem, Year}",
                "explanation": "DF2 determina todos os atributos restantes a partir de K1 = {CourseNo, SecNo, Sem, Year} (usando também DF1). DF3 determina CourseNo e SecNo a partir de K2 = {RoomNo, Days_Hours, Sem, Year}, que então alcança os demais atributos por DF1 e DF2! Logo há duas chaves candidatas legítimas."
            },
            {
                "id": "q2",
                "label": "2. Na decomposição para a 2FN adotando K1 como chave primária, qual relação isola a dependência parcial {CourseNo} -> {OfferDept, CredHours, CourseLevel}?",
                "options": [
                    "R_CURSO(CourseNo, OfferDept, CredHours, CourseLevel) com PK CourseNo, e R_TURMA com os demais atributos tendo PK (CourseNo, SecNo, Sem, Year)",
                    "Isola-se SecNo em uma tabela separada",
                    "R já está na 2FN",
                    "Separa-se Sem e Year em outra tabela"
                ],
                "answer": "R_CURSO(CourseNo, OfferDept, CredHours, CourseLevel) com PK CourseNo, e R_TURMA com os demais atributos tendo PK (CourseNo, SecNo, Sem, Year)",
                "explanation": "Como CourseNo é parte da chave K1, os atributos do curso dependem apenas de parte da chave. Criar R_CURSO(CourseNo, ...) remove a dependência parcial e coloca o esquema na 2FN!"
            }
        ]
    }
'''

# Read db_engine.py
with open("db_engine.py", "r", encoding="utf-8") as f:
    engine_code = f.read()

# Insert before `def get_connection`
target = "def get_connection("
if target in engine_code:
    parts = engine_code.split(target)
    # The dictionary closing brace `}\n\n` is just before target
    dict_end_pos = parts[0].rfind("}")
    new_engine = parts[0][:dict_end_pos] + NEW_EXERCISES_CODE + "\n}\n\n" + target + parts[1]
    with open("db_engine.py", "w", encoding="utf-8") as f:
        f.write(new_engine)
    print("db_engine.py updated with Modules 7 & 8 exercises!")
else:
    print("Target not found in db_engine.py!")
