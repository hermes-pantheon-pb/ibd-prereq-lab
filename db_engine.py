#!/usr/bin/env python3
"""
IBD Prerequisite Studio — Database, DDL Fault-Injection, Assertion & Structured Exercise Engine
Covers all prerequisites for "Projeto Lógico" (DCC222 / DCC011 - UFMG - Prof. Marcos André Gonçalves):
- Módulo 1: Arquitetura de SGBD, Esquemas, Instâncias e Independência de Dados (01-introducao.pdf)
- Módulo 2: Modelo Entidade-Relacionamento (ER), Cardinalidades (1:N vs min,max) e Entidades Fracas (ibd-parte2.pdf)
- Módulo 3: Modelo EER (Hierarquias d/o, Total/Parcial), Ternários e UML (ibd-parte2.pdf + ExercERRequisitos600.pdf)
- Módulo 4: Modelo Relacional Formal, Chaves, RIR (b, p, n) e Atualizações (ibd-parte3.pdf + exercicios_modelo_relacional.pdf)
- Módulo 5: Álgebra Relacional: Conjuntos, Divisão (÷) e Restrições Estruturais (ibd-parte3.pdf + ibd-parte5.pdf)
- Módulo 6: SQL DDL, Visões (Modificação de Consulta), CHECK e CREATE ASSERTION (ibd-parte4 + consultas_ProfMarcosG.pdf)
"""

import re
import sys
import json
import sqlite3
from typing import Dict, Any, List, Tuple, Optional

# =============================================================================
# CLASSIC ELMASRI & NAVATHE "COMPANY" DATABASE SETUP (Slides ibd-parte2/3/4/5)
# =============================================================================
COMPANY_SCHEMA_SETUP = """
PRAGMA foreign_keys = ON;

CREATE TABLE DEPARTMENT (
    DNAME VARCHAR(15) NOT NULL,
    DNUMBER INT NOT NULL,
    MGRSSN CHAR(9) NOT NULL,
    MGRSTARTDATE CHAR(10),
    PRIMARY KEY (DNUMBER),
    UNIQUE (DNAME)
);

CREATE TABLE EMPLOYEE (
    FNAME VARCHAR(15) NOT NULL,
    MINIT CHAR(1),
    LNAME VARCHAR(15) NOT NULL,
    SSN CHAR(9) NOT NULL,
    BDATE CHAR(10),
    ADDRESS VARCHAR(40),
    SEX CHAR(1),
    SALARY DECIMAL(10,2),
    SUPERSSN CHAR(9),
    DNO INT NOT NULL,
    PRIMARY KEY (SSN),
    FOREIGN KEY (SUPERSSN) REFERENCES EMPLOYEE(SSN) ON DELETE SET NULL,
    FOREIGN KEY (DNO) REFERENCES DEPARTMENT(DNUMBER)
);

CREATE TABLE DEPT_LOCATIONS (
    DNUMBER INT NOT NULL,
    DLOCATION VARCHAR(15) NOT NULL,
    PRIMARY KEY (DNUMBER, DLOCATION),
    FOREIGN KEY (DNUMBER) REFERENCES DEPARTMENT(DNUMBER) ON DELETE CASCADE
);

CREATE TABLE PROJECT (
    PNAME VARCHAR(20) NOT NULL,
    PNUMBER INT NOT NULL,
    PLOCATION VARCHAR(15),
    DNUM INT NOT NULL,
    PRIMARY KEY (PNUMBER),
    UNIQUE (PNAME),
    FOREIGN KEY (DNUM) REFERENCES DEPARTMENT(DNUMBER)
);

CREATE TABLE WORKS_ON (
    ESSN CHAR(9) NOT NULL,
    PNO INT NOT NULL,
    HOURS DECIMAL(4,1),
    PRIMARY KEY (ESSN, PNO),
    FOREIGN KEY (ESSN) REFERENCES EMPLOYEE(SSN),
    FOREIGN KEY (PNO) REFERENCES PROJECT(PNUMBER)
);

CREATE TABLE DEPENDENT (
    ESSN CHAR(9) NOT NULL,
    DEPENDENT_NAME VARCHAR(15) NOT NULL,
    SEX CHAR(1),
    BDATE CHAR(10),
    RELATIONSHIP VARCHAR(12),
    PRIMARY KEY (ESSN, DEPENDENT_NAME),
    FOREIGN KEY (ESSN) REFERENCES EMPLOYEE(SSN) ON DELETE CASCADE
);

INSERT INTO DEPARTMENT VALUES
('Research', 5, '333445555', '1988-05-22'),
('Administration', 4, '987654321', '1995-01-01'),
('Headquarters', 1, '888665555', '1981-06-19');

INSERT INTO EMPLOYEE VALUES
('James', 'E', 'Borg', '888665555', '1937-11-10', '450 Stone, Houston, TX', 'M', 55000.00, NULL, 1),
('Franklin', 'T', 'Wong', '333445555', '1955-12-08', '638 Voss, Houston, TX', 'M', 40000.00, '888665555', 5),
('Jennifer', 'S', 'Wallace', '987654321', '1941-06-20', '291 Berry, Bellaire, TX', 'F', 43000.00, '888665555', 4),
('John', 'B', 'Smith', '123456789', '1965-01-09', '731 Fondren, Houston, TX', 'M', 30000.00, '333445555', 5),
('Ramesh', 'K', 'Narayan', '666884444', '1962-09-15', '975 Fire Oak, Humble, TX', 'M', 38000.00, '333445555', 5),
('Joyce', 'A', 'English', '453453453', '1972-07-31', '5631 Rice, Houston, TX', 'F', 25000.00, '333445555', 5),
('Alicia', 'J', 'Zelaya', '999887777', '1968-01-19', '3321 Castle, Spring, TX', 'F', 25000.00, '987654321', 4),
('Ahmad', 'V', 'Jabbar', '987987987', '1969-03-29', '980 Dallas, Houston, TX', 'M', 25000.00, '987654321', 4);

INSERT INTO DEPT_LOCATIONS VALUES
(1, 'Houston'),
(4, 'Stafford'),
(5, 'Bellaire'),
(5, 'Sugarland'),
(5, 'Houston');

INSERT INTO PROJECT VALUES
('ProductX', 1, 'Bellaire', 5),
('ProductY', 2, 'Sugarland', 5),
('ProductZ', 3, 'Houston', 5),
('Computerization', 10, 'Stafford', 4),
('Reorganization', 20, 'Houston', 1),
('Newbenefits', 30, 'Stafford', 4);

INSERT INTO WORKS_ON VALUES
('123456789', 1, 32.5),
('123456789', 2, 7.5),
('666884444', 3, 40.0),
('453453453', 1, 20.0),
('453453453', 2, 20.0),
('333445555', 2, 10.0),
('333445555', 3, 10.0),
('333445555', 10, 10.0),
('333445555', 20, 10.0),
('999887777', 30, 30.0),
('999887777', 10, 10.0),
('987987987', 10, 35.0),
('987987987', 30, 5.0),
('987654321', 30, 20.0),
('987654321', 20, 15.0),
('888665555', 20, NULL);

INSERT INTO DEPENDENT VALUES
('333445555', 'Alice', 'F', '1986-04-05', 'Daughter'),
('333445555', 'Theodore', 'M', '1983-10-25', 'Son'),
('333445555', 'Joy', 'F', '1958-05-03', 'Spouse'),
('987654321', 'Abner', 'M', '1942-02-28', 'Spouse'),
('123456789', 'Michael', 'M', '1988-01-04', 'Son'),
('123456789', 'Alice', 'F', '1988-12-30', 'Daughter'),
('123456789', 'Elizabeth', 'F', '1967-05-05', 'Spouse');
"""

# Variant of COMPANY where an employee ('333445555' Franklin Wong) works on ALL projects
# and '123456789' (John Smith) has a homonymous dependent ('John') and '666884444' works on all dept 5 projects
COMPANY_PROFM_SETUP = COMPANY_SCHEMA_SETUP + """
-- Adições específicas para que todas as consultas de consultas_ProfMarcosG.pdf retornem linhas ricas:
-- 1) Empregado com mesmo primeiro nome do dependente (John Smith -> dependente John)
INSERT INTO DEPENDENT VALUES ('123456789', 'John', 'M', '1995-06-12', 'Son');
-- 2) Ramesh Narayan ('666884444') trabalha em TODOS os projetos do departamento 5 (1, 2, 3)
INSERT INTO WORKS_ON VALUES ('666884444', 1, 10.0);
INSERT INTO WORKS_ON VALUES ('666884444', 2, 10.0);
-- 3) Franklin Wong ('333445555') trabalha em TODOS os 6 projetos da empresa (já tem 2,3,10,20; adicionamos 1 e 30)
INSERT INTO WORKS_ON VALUES ('333445555', 1, 5.0);
INSERT INTO WORKS_ON VALUES ('333445555', 30, 5.0);
-- 4) Empregado sem nenhum projeto: Carla Mendes ('111222333')
INSERT INTO EMPLOYEE VALUES
('Carla', 'M', 'Mendes', '111222333', '1975-04-12', '100 Main, Houston, TX', 'F', 28000.00, '333445555', 5);
"""

# =============================================================================
# HIERARCHY & STRUCTURAL CONSTRAINTS DATABASE (ibd-parte5.pdf slides)
# =============================================================================
HIERARCHY_SETUP = """
PRAGMA foreign_keys = ON;

CREATE TABLE Departamento (
    NDept CHAR(2) NOT NULL PRIMARY KEY,
    NomeDept VARCHAR(30) NOT NULL UNIQUE
);

CREATE TABLE Empregado (
    NEmp CHAR(3) NOT NULL PRIMARY KEY,
    NomeEmp VARCHAR(30) NOT NULL,
    Salario DECIMAL(8,2) NOT NULL,
    NDept CHAR(2) NOT NULL,
    FOREIGN KEY (NDept) REFERENCES Departamento(NDept)
);

CREATE TABLE Gerente (
    NEmp CHAR(3) NOT NULL PRIMARY KEY,
    SalAd DECIMAL(8,2) NOT NULL,
    FOREIGN KEY (NEmp) REFERENCES Empregado(NEmp) ON DELETE CASCADE
);

CREATE TABLE Tecnico (
    NEmp CHAR(3) NOT NULL PRIMARY KEY,
    Formacao VARCHAR(10) NOT NULL,
    FOREIGN KEY (NEmp) REFERENCES Empregado(NEmp) ON DELETE CASCADE
);

CREATE TABLE Projeto (
    NProj CHAR(3) NOT NULL PRIMARY KEY,
    NomeProj VARCHAR(30) NOT NULL
);

CREATE TABLE Participa_de (
    NEmp CHAR(3) NOT NULL,
    NProj CHAR(3) NOT NULL,
    HsTrab INT,
    PRIMARY KEY (NEmp, NProj),
    FOREIGN KEY (NEmp) REFERENCES Empregado(NEmp) ON DELETE CASCADE,
    FOREIGN KEY (NProj) REFERENCES Projeto(NProj) ON DELETE CASCADE
);

INSERT INTO Departamento VALUES ('D1', 'Pesquisa'), ('D2', 'Engenharia');
INSERT INTO Empregado VALUES
('E01', 'Ana Costa', 8000.00, 'D1'),
('E02', 'Bruno Lima', 6500.00, 'D1'),
('E03', 'Carlos Souza', 7200.00, 'D2'),
('E04', 'Daniela Reis', 5800.00, 'D2');

INSERT INTO Gerente VALUES ('E01', 2000.00), ('E03', 1500.00);
INSERT INTO Tecnico VALUES ('E02', 'MSc'), ('E04', 'BSc');

INSERT INTO Projeto VALUES ('P10', 'Sistema Alpha'), ('P20', 'Motor Beta');
INSERT INTO Participa_de VALUES
('E01', 'P10', 20),
('E02', 'P10', 40),
('E03', 'P20', 30),
('E04', 'P20', 35);
"""


# =============================================================================
# EXERCISES DATA REGISTRY
# Modes:
#   - "structured": Multi-field interactive conceptual/diagnostic/notation builder
#   - "sql_query": Live SQL / RA equivalence query execution & validation
#   - "sql_ddl": Live DDL execution + automated fault-injection test suite
#   - "sql_assertion": Standard SQL-92 CREATE ASSERTION transpiler + fault injection
# =============================================================================
EXERCISES_DATA: Dict[str, Dict[str, Any]] = {
    # =========================================================================
    # MÓDULO 1: ARQUITETURA DE SGBD, ESQUEMAS E INDEPENDÊNCIA DE DADOS
    # =========================================================================
    "T1.1": {
        "title": "Esquema (Intensão) vs. Instância (Extensão) e os 3 Níveis",
        "type": "treino",
        "mode": "structured",
        "setup": "",
        "fields": [
            {
                "id": "q1",
                "label": "1. A definição estrutural 'Estudantes(eid: string, nome: string, idade: int)' armazenada no catálogo do SGBD é:",
                "options": [
                    "Esquema Conceitual (Intensão do banco de dados)",
                    "Instância do Banco de Dados (Extensão no momento t)",
                    "Esquema Interno (Físico)",
                    "Esquema Externo (Visão de usuário)"
                ],
                "answer": "Esquema Conceitual (Intensão do banco de dados)",
                "explanation": "O Esquema Conceitual descreve 'O QUE' está armazenado (entidades, atributos, tipos e restrições) — é a intensão, que muda raramente."
            },
            {
                "id": "q2",
                "label": "2. O conjunto de 1.500 tuplas de alunos atualmente gravadas nas tabelas no instante t representa:",
                "options": [
                    "A Instância (ou Estado / Extensão) do banco de dados",
                    "O Esquema Lógico do banco de dados",
                    "O Meta-dado do catálogo",
                    "A Independência Física de Dados"
                ],
                "answer": "A Instância (ou Estado / Extensão) do banco de dados",
                "explanation": "Os dados presentes no BD em um determinado instante de tempo formam a Instância (ou Estado). Ela muda toda vez que fazemos INSERT, DELETE ou UPDATE."
            },
            {
                "id": "q3",
                "label": "3. 'Relações guardadas como arquivos desordenados (heap) com índice B-Tree na primeira coluna (eid)' pertence ao:",
                "options": [
                    "Nível Interno (Esquema Físico — COMO está armazenado)",
                    "Nível Conceitual (O QUE está armazenado)",
                    "Nível Externo (Visões parciais)",
                    "Modelo Entidade-Relacionamento"
                ],
                "answer": "Nível Interno (Esquema Físico — COMO está armazenado)",
                "explanation": "O Nível Interno descreve a estrutura física de armazenamento (arquivos, páginas, tamanhos em bytes/words e índices)."
            },
            {
                "id": "q4",
                "label": "4. 'Lista_Matricula(nome, cnome)' criada para a secretaria consultar apenas nomes de alunos e cursos sem ver notas nem salários pertence ao:",
                "options": [
                    "Nível Externo (Visão / Esquema Externo)",
                    "Nível Interno (Físico)",
                    "Nível Conceitual Global",
                    "Sistema Gerenciador de Arquivos"
                ],
                "answer": "Nível Externo (Visão / Esquema Externo)",
                "explanation": "O Nível Externo é composto por visões (views) adaptadas a grupos específicos de usuários, ocultando o restante do banco."
            }
        ]
    },
    "T1.2": {
        "title": "Diagnóstico de Independência de Dados: Lógica vs. Física",
        "type": "treino",
        "mode": "structured",
        "setup": "",
        "fields": [
            {
                "id": "q1",
                "label": "1. O DBA cria um novo índice hash e reorganiza os arquivos físicos de Empregado no disco para acelerar buscas, sem precisar alterar o Esquema Conceitual nem os programas de aplicação. Isso é garantido pela:",
                "options": [
                    "Independência de Dados Física (entre o Nível Interno e o Nível Conceitual)",
                    "Independência de Dados Lógica (entre o Nível Conceitual e o Nível Externo)",
                    "Restrição de Integridade Referencial",
                    "Redundância Controlada"
                ],
                "answer": "Independência de Dados Física (entre o Nível Interno e o Nível Conceitual)",
                "explanation": "Independência Física é a capacidade de alterar o Esquema Interno (físico) sem precisar alterar o Esquema Conceitual (nem o Externo)."
            },
            {
                "id": "q2",
                "label": "2. A empresa adiciona uma nova entidade 'Projeto_Social' e novos atributos ao Esquema Conceitual, mas as Visões Externas (Esquemas Externos) e programas antigos continuam funcionando sem modificação. Isso é:",
                "options": [
                    "Independência de Dados Lógica (entre o Nível Conceitual e o Nível Externo)",
                    "Independência de Dados Física (entre o Nível Interno e o Nível Conceitual)",
                    "Abstração de Armazenamento",
                    "Normalização Física"
                ],
                "answer": "Independência de Dados Lógica (entre o Nível Conceitual e o Nível Externo)",
                "explanation": "Independência Lógica é a capacidade de alterar o Esquema Conceitual (ex: adicionar entidades/atributos) sem alterar os Esquemas Externos ou os programas de aplicação."
            },
            {
                "id": "q3",
                "label": "3. Na arquitetura de 3 esquemas, a regra geral da Independência de Dados afirma que:",
                "options": [
                    "Altera-se o esquema em um nível mais baixo sem precisar alterar o esquema no nível imediatamente mais alto (apenas o mapeamento entre eles é ajustado)",
                    "Altera-se o nível externo e o banco muda automaticamente a estrutura física dos discos",
                    "O esquema físico depende diretamente da linguagem de programação (C ou Pascal) do usuário",
                    "Qualquer mudança no nível interno obriga a reescrever as consultas SQL das aplicações"
                ],
                "answer": "Altera-se o esquema em um nível mais baixo sem precisar alterar o esquema no nível imediatamente mais alto (apenas o mapeamento entre eles é ajustado)",
                "explanation": "Exatamente como no slide 55 de 01-introducao.pdf: Independência de dados é a capacidade de alterar o esquema em um determinado nível sem alterar o esquema do nível imediatamente mais alto."
            }
        ]
    },
    "E1.1": {
        "title": "[Oficial Slides 01] Sublinguagens do SGBD e Arquitetura de 3 Níveis",
        "type": "oficial",
        "mode": "structured",
        "setup": "",
        "fields": [
            {
                "id": "q1",
                "label": "1. No Exemplo 2 dos slides (Empregado), como são classificados respectivamente: (A) `struct Participante { char[30] Nome; int Departamento; }`, (B) `Empregado(NOME CHAR(30), SALARIO NUMERIC(5), ...)`, e (C) `RegistroEmpregado LENGTH=50, SAL TYPE=FULLWORD`?",
                "options": [
                    "(A) Esquema Externo, (B) Esquema Conceitual, (C) Esquema Interno",
                    "(A) Esquema Conceitual, (B) Esquema Externo, (C) Esquema Interno",
                    "(A) Esquema Interno, (B) Esquema Conceitual, (C) Esquema Externo",
                    "(A) Instância, (B) Esquema Físico, (C) Visão"
                ],
                "answer": "(A) Esquema Externo, (B) Esquema Conceitual, (C) Esquema Interno",
                "explanation": "No slide 53: (A) A struct em C/Pascal que omite Salário e Sexo é a Visão Externa daquele programa; (B) A definição lógica completa de Empregado é o Esquema Conceitual; (C) A especificação de bytes, FULLWORD e WORD é o Esquema Interno."
            },
            {
                "id": "q2",
                "label": "2. Qual sublinguagem do SGBD é usada pelo DBA e projetistas para definir o esquema conceitual (criar tabelas, chaves e restrições)?",
                "options": [
                    "DDL / LDD (Linguagem de Definição de Dados — ex: CREATE TABLE, ALTER TABLE)",
                    "DML / LMD (Linguagem de Manipulação de Dados — ex: INSERT, UPDATE, DELETE)",
                    "DQL (Linguagem de Consulta de Dados — ex: SELECT)",
                    "VDL (Linguagem de Definição de Visões)"
                ],
                "answer": "DDL / LDD (Linguagem de Definição de Dados — ex: CREATE TABLE, ALTER TABLE)",
                "explanation": "A LDD (DDL) define os esquemas e restrições que vão para o catálogo do SGBD."
            },
            {
                "id": "q3",
                "label": "3. Qual problema clássico dos sistemas de fichários (arquivos tradicionais) ocorre quando dois atendentes retiram a ficha do mesmo cliente ou não encontram a ficha e criam duplicatas inconsistentes?",
                "options": [
                    "Falta de Controle de Concorrência e Redundância/Inconsistência de Dados",
                    "Excesso de Independência Lógica de Dados",
                    "Uso de Chaves Estrangeiras com Propagação",
                    "Falta de Linguagem Procedural"
                ],
                "answer": "Falta de Controle de Concorrência e Redundância/Inconsistência de Dados",
                "explanation": "Sistemas de arquivos não possuem controle de concorrência integrado nem catálogo centralizado, gerando anomalias de atualização concorrente e duplicação."
            }
        ]
    },

    # =========================================================================
    # MÓDULO 2: MODELO ENTIDADE-RELACIONAMENTO (ER) — FUNDAMENTOS & (min, max)
    # =========================================================================
    "T2.1": {
        "title": "Classificação de Atributos no Modelo ER (Slides ibd-parte2)",
        "type": "treino",
        "mode": "structured",
        "setup": "",
        "fields": [
            {
                "id": "q1",
                "label": "1. O atributo 'Endereço', subdividido em Rua (Número, Nome_Rua, Apto), Cidade, Estado e CEP, é classificado como:",
                "options": [
                    "Atributo Composto (representado como uma árvore de sub-atributos ligados à elipse pai)",
                    "Atributo Multivalorado (elipse dupla)",
                    "Atributo Derivado (elipse tracejada)",
                    "Chave Parcial (sublinhado tracejado)"
                ],
                "answer": "Atributo Composto (representado como uma árvore de sub-atributos ligados à elipse pai)",
                "explanation": "Atributos compostos podem ser divididos em partes menores com significados independentes."
            },
            {
                "id": "q2",
                "label": "2. Um Departamento pode ter várias localizações ('Houston', 'Bellaire', 'Sugarland'). No diagrama ER, o atributo 'Locations' de DEPARTMENT é:",
                "options": [
                    "Atributo Multivalorado (desenhado com elipse de linha dupla)",
                    "Atributo Composto (elipses ramificadas)",
                    "Atributo Derivado (elipse tracejada)",
                    "Entidade Fraca"
                ],
                "answer": "Atributo Multivalorado (desenhado com elipse de linha dupla)",
                "explanation": "Quando uma mesma entidade pode ter múltiplos valores para o mesmo atributo simultaneamente (ex: vários telefones, vários ramais, várias localizações), ele é Multivalorado (elipse dupla)."
            },
            {
                "id": "q3",
                "label": "3. O atributo 'Numero_de_Empregados' de DEPARTMENT ou 'Idade' de EMPLOYEE (calculada a partir de Data_Nascimento) é:",
                "options": [
                    "Atributo Derivado (desenhado com elipse tracejada)",
                    "Atributo Armazenado Chave",
                    "Atributo Multivalorado (elipse dupla)",
                    "Atributo Composto"
                ],
                "answer": "Atributo Derivado (desenhado com elipse tracejada)",
                "explanation": "Atributos cujos valores podem ser calculados a partir de outros atributos ou relacionamentos existentes (como contar quantos empregados trabalham no depto) são Derivados (elipse tracejada)."
            },
            {
                "id": "q4",
                "label": "4. No Modelo ER, quando um empregado mora em uma casa (sem apartamento), o valor NULL em 'Numero_Apto' significa _____; já quando não sabemos o telefone residencial dele, o NULL significa _____:",
                "options": [
                    "Não aplicável / Desconhecido",
                    "Desconhecido / Não aplicável",
                    "Chave parcial / Chave estrangeira",
                    "Zero / String vazia"
                ],
                "answer": "Não aplicável / Desconhecido",
                "explanation": "Conforme o slide 8 de ibd-parte2.pdf, NULL tem duas semânticas principais: 'Não aplicável' (ex: apto para quem mora em casa) e 'Desconhecido' (existe, mas não foi informado)."
            }
        ]
    },
    "T2.2": {
        "title": "O Tradutor de Cardinalidades: Notação 1:N (Chen) ↔ Notação (min, max)",
        "type": "treino",
        "mode": "structured",
        "setup": "",
        "fields": [
            {
                "id": "q1",
                "label": "1. Regra de Negócio: 'Todo empregado deve trabalhar para exatamente um departamento, e cada departamento tem pelo menos 4 (ou vários) empregados'. Na notação tradicional (Chen), colocamos ___ perto de DEPARTMENT e ___ perto de EMPLOYEE, com linha dupla em EMPLOYEE:",
                "options": [
                    "1 perto de DEPARTMENT e N perto de EMPLOYEE",
                    "N perto de DEPARTMENT e 1 perto de EMPLOYEE",
                    "1 perto de DEPARTMENT e 1 perto de EMPLOYEE",
                    "M perto de DEPARTMENT e N perto de EMPLOYEE"
                ],
                "answer": "1 perto de DEPARTMENT e N perto de EMPLOYEE",
                "explanation": "Na notação 1:N tradicional, lê-se '1 Departamento emprega N Empregados', então o 1 fica do lado de DEPARTMENT e o N do lado de EMPLOYEE."
            },
            {
                "id": "q2",
                "label": "2. AGORA A PEGADINHA DE PROVA: Para a MESMA regra acima ('Todo empregado trabalha em exatamente 1 depto; todo depto tem de 4 a N empregados'), quais são os pares (min, max) colocados ao lado de EMPLOYEE e de DEPARTMENT?",
                "options": [
                    "EMPLOYEE: (1, 1)  |  DEPARTMENT: (4, N) ou (1, N)",
                    "EMPLOYEE: (1, N)  |  DEPARTMENT: (1, 1)",
                    "EMPLOYEE: (0, 1)  |  DEPARTMENT: (0, N)",
                    "EMPLOYEE: (4, N)  |  DEPARTMENT: (0, 1)"
                ],
                "answer": "EMPLOYEE: (1, 1)  |  DEPARTMENT: (4, N) ou (1, N)",
                "explanation": "ATENÇÃO TOTAL! Na notação (min, max) do Prof. Marcos André / Elmasri (slide 28 de ibd-parte2.pdf), o par (min, max) ao lado de uma entidade diz em quantas instâncias daquele relacionamento ELA participa! Cada EMPLOYEE participa de no mínimo 1 e no máximo 1 vínculo WORKS_FOR -> (1,1). Cada DEPARTMENT participa de 4 até N vínculos -> (4,N). Os lados do '1' e do 'N' se invertem em relação à notação tradicional!"
            },
            {
                "id": "q3",
                "label": "3. Regra: 'Um departamento é gerenciado por exatamente um empregado; mas um empregado pode gerenciar no máximo um departamento (ou nenhum)'. Quais são os pares (min, max) no relacionamento MANAGES?",
                "options": [
                    "Ao lado de EMPLOYEE: (0, 1)  |  Ao lado de DEPARTMENT: (1, 1)",
                    "Ao lado de EMPLOYEE: (1, 1)  |  Ao lado de DEPARTMENT: (0, 1)",
                    "Ao lado de EMPLOYEE: (1, N)  |  Ao lado de DEPARTMENT: (1, 1)",
                    "Ao lado de EMPLOYEE: (0, N)  |  Ao lado de DEPARTMENT: (0, 1)"
                ],
                "answer": "Ao lado de EMPLOYEE: (0, 1)  |  Ao lado de DEPARTMENT: (1, 1)",
                "explanation": "Nem todo empregado é gerente, então um EMPLOYEE participa de 0 ou 1 instância de MANAGES -> (0, 1) (participação parcial). Todo departamento TEM um gerente e apenas um -> DEPARTMENT tem (1, 1) (participação total)."
            },
            {
                "id": "q4",
                "label": "4. No relacionamento recursivo SUPERVISION em EMPLOYEE, o papel 1 é 'Supervisor' (chefe) e o papel 2 é 'Supervisionado' (subordinado). Se um empregado não precisa ser chefe de ninguém mas pode chefiar vários, e um empregado tem no máximo 1 chefe direto (o presidente não tem chefe), quais são os (min, max)?",
                "options": [
                    "Papel 1 (Supervisor): (0, N)  |  Papel 2 (Supervisionado): (0, 1)",
                    "Papel 1 (Supervisor): (0, 1)  |  Papel 2 (Supervisionado): (0, N)",
                    "Papel 1 (Supervisor): (1, 1)  |  Papel 2 (Supervisionado): (1, N)",
                    "Papel 1 (Supervisor): (1, N)  |  Papel 2 (Supervisionado): (1, 1)"
                ],
                "answer": "Papel 1 (Supervisor): (0, N)  |  Papel 2 (Supervisionado): (0, 1)",
                "explanation": "Slide 28 de ibd-parte2.pdf: No papel de Supervisor (1), um empregado supervisiona de 0 a N subordinados -> (0, N). No papel de Supervisionado (2), um empregado tem 0 (caso de James Borg) ou 1 supervisor direto -> (0, 1)."
            }
        ]
    },
    "T2.3": {
        "title": "Anatomia de Tipos de Entidade Fraca e Chave Parcial",
        "type": "treino",
        "mode": "structured",
        "setup": "",
        "fields": [
            {
                "id": "q1",
                "label": "1. Quando devemos modelar um conceito como um Tipo de Entidade Fraca (retângulo duplo) em vez de uma Entidade Forte?",
                "options": [
                    "Quando seus atributos próprios não bastam para identificá-la unicamente no banco; ela depende da identidade de outra entidade dona (identificadora) somada a uma chave parcial",
                    "Sempre que uma entidade tiver participação parcial (0, N) em um relacionamento",
                    "Sempre que uma tabela tiver menos de 3 colunas",
                    "Quando a entidade for uma subclasse em uma hierarquia de especialização"
                ],
                "answer": "Quando seus atributos próprios não bastam para identificá-la unicamente no banco; ela depende da identidade de outra entidade dona (identificadora) somada a uma chave parcial",
                "explanation": "Uma entidade fraca não possui chave primária própria; dois dependentes de empregados diferentes podem ter exatamente o mesmo nome ('Alice'), sexo e data de nascimento, sendo distinguidos pelo empregado dono."
            },
            {
                "id": "q2",
                "label": "2. Na prova de Projeto Lógico (ExercicioProjetoLogico.pdf), `TRECHO_VOO` tem retângulo duplo, `Trecho_num` tem sublinhado tracejado, e `TRECHOS` tem losango duplo ligado a `VOO` (chave `Numero`). O que significa essa notação?",
                "options": [
                    "TRECHO_VOO é entidade fraca identificada por VOO; Trecho_num é sua chave parcial; a chave completa de TRECHO_VOO no modelo relacional será (Numero_Voo, Trecho_num)",
                    "TRECHO_VOO é um atributo multivalorado de VOO e não vira tabela",
                    "Trecho_num é um atributo derivado calculado automaticamente",
                    "TRECHOS é um relacionamento M:N comum entre duas entidades fortes"
                ],
                "answer": "TRECHO_VOO é entidade fraca identificada por VOO; Trecho_num é sua chave parcial; a chave completa de TRECHO_VOO no modelo relacional será (Numero_Voo, Trecho_num)",
                "explanation": "O trecho número 1 existe no Voo 101 e também no Voo 202. Por isso `Trecho_num` é chave parcial (sublinhado tracejado) e `TRECHO_VOO` depende de `VOO` via relacionamento identificador `TRECHOS` (losango duplo)."
            },
            {
                "id": "q3",
                "label": "3. Qual é SEMPRE a restrição de participação de uma Entidade Fraca no seu Relacionamento Identificador (losango duplo)?",
                "options": [
                    "Participação TOTAL (linha dupla / min = 1), pois uma instância da entidade fraca não pode existir sem estar ligada a uma entidade dona",
                    "Participação PARCIAL (linha simples / min = 0), pois pode ficar órfã",
                    "Cardinalidade M:N com participação parcial em ambos os lados",
                    "Depende se a chave parcial é numérica ou texto"
                ],
                "answer": "Participação TOTAL (linha dupla / min = 1), pois uma instância da entidade fraca não pode existir sem estar ligada a uma entidade dona",
                "explanation": "Dependência de existência e identificação: toda entidade fraca tem participação TOTAL (1, 1) no relacionamento identificador com seu dono."
            }
        ]
    },
    "E2.1": {
        "title": "[Oficial Slides 02] Auditoria Completa do Esquema ER 'COMPANY'",
        "type": "oficial",
        "mode": "structured",
        "setup": "",
        "fields": [
            {
                "id": "q1",
                "label": "1. No esquema COMPANY, onde deve ficar o atributo 'Hours' (horas semanais que um empregado trabalha em um projeto) e por quê?",
                "options": [
                    "No relacionamento M:N WORKS_ON entre EMPLOYEE e PROJECT, pois a quantidade de horas depende do par (Empregado, Projeto) simultaneamente",
                    "Na entidade EMPLOYEE, pois é o empregado quem trabalha",
                    "Na entidade PROJECT, pois as horas pertencem ao projeto",
                    "Na entidade DEPARTMENT que controla o projeto"
                ],
                "answer": "No relacionamento M:N WORKS_ON entre EMPLOYEE e PROJECT, pois a quantidade de horas depende do par (Empregado, Projeto) simultaneamente",
                "explanation": "Em um relacionamento M:N, um empregado trabalha em vários projetos e um projeto tem vários empregados; 'Hours' é propriedade da associação entre um empregado específico e um projeto específico."
            },
            {
                "id": "q2",
                "label": "2. E o atributo 'Start_Date' (data em que o empregado começou a gerenciar o departamento) no relacionamento 1:1 MANAGES?",
                "options": [
                    "É um atributo do relacionamento MANAGES (e no mapeamento relacional otimizado pode migrar junto com a FK do gerente para DEPARTMENT)",
                    "É uma entidade fraca separada",
                    "É um atributo multivalorado de PROJECT",
                    "É a chave primária de DEPARTMENT"
                ],
                "answer": "É um atributo do relacionamento MANAGES (e no mapeamento relacional otimizado pode migrar junto com a FK do gerente para DEPARTMENT)",
                "explanation": "Conceitualmente no ER, Start_Date descreve o relacionamento MANAGES."
            },
            {
                "id": "q3",
                "label": "3. No relacionamento CONTROLS entre DEPARTMENT e PROJECT ('Um departamento controla vários projetos, mas cada projeto é controlado por exatamente um departamento; nem todo depto controla projetos'), quais são os pares (min, max)?",
                "options": [
                    "DEPARTMENT: (0, N)  |  PROJECT: (1, 1)",
                    "DEPARTMENT: (1, 1)  |  PROJECT: (0, N)",
                    "DEPARTMENT: (1, N)  |  PROJECT: (0, 1)",
                    "DEPARTMENT: (0, 1)  |  PROJECT: (1, N)"
                ],
                "answer": "DEPARTMENT: (0, N)  |  PROJECT: (1, 1)",
                "explanation": "Cada DEPARTMENT controla de 0 a N projetos -> (0, N). Cada PROJECT é controlado por exatamente 1 departamento -> (1, 1)."
            }
        ]
    },

    # =========================================================================
    # MÓDULO 3: MODELO EER (HIERARQUIAS), RELACIONAMENTOS TERNÁRIOS E UML
    # =========================================================================
    "T3.1": {
        "title": "Hierarquias EER: Disjunção (d vs. o), Completude (Total vs. Parcial) e Herança",
        "type": "treino",
        "mode": "structured",
        "setup": "",
        "fields": [
            {
                "id": "q1",
                "label": "1. Uma especialização de EMPLOYEE em {Secretary, Technician, Engineer} tem um círculo com a letra 'd' ligado por linha simples a EMPLOYEE. O que isso significa?",
                "options": [
                    "Disjunta e Parcial: um empregado pode ser no máximo um entre {Secretário, Técnico, Engenheiro}, e pode existir empregado que não seja nenhum dos três",
                    "Disjunta e Total: todo empregado é obrigatoriamente um e apenas um dos três",
                    "Sobreposta (Overlapping) e Parcial: um empregado pode ser Técnico e Engenheiro ao mesmo tempo",
                    "Derivada e Persistente: os atributos não são herdados"
                ],
                "answer": "Disjunta e Parcial: um empregado pode ser no máximo um entre {Secretário, Técnico, Engenheiro}, e pode existir empregado que não seja nenhum dos três",
                "explanation": "'d' significa Disjunta (subclasses mutuamente exclusivas: interseção vazia). Linha simples ligando à superclasse significa Completude Parcial (união das subclasses é um subconjunto próprio da superclasse)."
            },
            {
                "id": "q2",
                "label": "2. Uma peça (PART) na fábrica pode ser Fabricada (MANUFACTURED_PART), Comprada de fornecedor (PURCHASED_PART), ou AMBAS as coisas simultaneamente, e toda peça deve ser pelo menos uma das duas. Qual a notação EER?",
                "options": [
                    "Círculo com 'o' (Sobreposta / Overlapping) e Linha Dupla (Total) ligando a PART",
                    "Círculo com 'd' (Disjunta) e Linha Dupla (Total) ligando a PART",
                    "Círculo com 'o' (Sobreposta) e Linha Simples (Parcial) ligando a PART",
                    "Entidade fraca com losango duplo"
                ],
                "answer": "Círculo com 'o' (Sobreposta / Overlapping) e Linha Dupla (Total) ligando a PART",
                "explanation": "'o' (overlapping / sobreposta) permite que a mesma instância pertença a mais de uma subclasse. Linha dupla indica cobertura Total."
            },
            {
                "id": "q3",
                "label": "3. Sobre Herança de Tipo e Reticulados (Lattice) no EER, se 'Engineering_Manager' é subclasse tanto de 'Engineer' quanto de 'Manager':",
                "options": [
                    "É um Reticulado (herança múltipla): Engineering_Manager herda todos os atributos, a chave primária e todos os relacionamentos de Engineer, Manager e Employee",
                    "É proibido no modelo EER uma subclasse ter mais de uma superclasse",
                    "Engineering_Manager herda os atributos mas perde a chave primária de Employee",
                    "Engineering_Manager torna-se uma entidade fraca com duas chaves parciais"
                ],
                "answer": "É um Reticulado (herança múltipla): Engineering_Manager herda todos os atributos, a chave primária e todos os relacionamentos de Engineer, Manager e Employee",
                "explanation": "Nos slides 42-43 de ibd-parte2.pdf: Em uma Hierarquia (árvore), cada subclasse tem apenas uma superclasse; em um Lattice (reticulado), uma subclasse pode ter múltipla herança, herdando atributos e relacionamentos de todas as suas superclasses ancestrais."
            }
        ]
    },
    "T3.2": {
        "title": "Relacionamentos Ternários vs. Três Relacionamentos Binários",
        "type": "treino",
        "mode": "structured",
        "setup": "",
        "fields": [
            {
                "id": "q1",
                "label": "1. Considere o relacionamento ternário SUPPLIES(Supplier s, Part p, Project j) que registra: 'O fornecedor s fornece a peça p para o projeto j'. Se substituirmos por 3 relacionamentos binários M:N: CAN_SUPPLY(s, p), USES(j, p) e SUPPLIES_TO(s, j):",
                "options": [
                    "NÃO são equivalentes! Se s1 fornece p1, j1 usa p1 e s1 fornece para j1, os 3 binários podem estar presentes mesmo que s1 forneça apenas p2 para j1 (e quem forneça p1 para j1 seja s2)",
                    "São 100% equivalentes e sempre podemos trocar qualquer ternário por 3 binários M:N sem perda de informação",
                    "Os 3 binários guardam mais informação que o ternário",
                    "O ternário só pode representar cardinalidades 1:1:1"
                ],
                "answer": "NÃO são equivalentes! Se s1 fornece p1, j1 usa p1 e s1 fornece para j1, os 3 binários podem estar presentes mesmo que s1 forneça apenas p2 para j1 (e quem forneça p1 para j1 seja s2)",
                "explanation": "Slides 44-46 de ibd-parte2.pdf: Três relacionamentos binários M:N sofrem de 'junção espúria' (ciclo fechado falso) e não conseguem garantir que a tripla específica (s, p, j) ocorreu junta!"
            },
            {
                "id": "q2",
                "label": "2. Como podemos representar o relacionamento ternário SUPPLIES(Supplier, Part, Project) usando apenas relacionamentos binários SEM perder equivalência semântica?",
                "options": [
                    "Criando um Tipo de Entidade Fraca (ou Associativa) 'SUPPLY' identificada simultaneamente pelas 3 entidades fortes via 3 relacionamentos identificadores binários 1:N (SS, SP, SJ)",
                    "Apagando uma das três entidades do diagrama",
                    "Transformando Supplier em atributo multivalorado de Project",
                    "Usando uma hierarquia disjunta"
                ],
                "answer": "Criando um Tipo de Entidade Fraca (ou Associativa) 'SUPPLY' identificada simultaneamente pelas 3 entidades fortes via 3 relacionamentos identificadores binários 1:N (SS, SP, SJ)",
                "explanation": "Slide 45 de ibd-parte2.pdf: Cada instância da entidade fraca SUPPLY representa exatamente uma tripla (s, p, j), ligada com cardinalidade N:1 (participação total da fraca) a Supplier, Part e Project."
            }
        ]
    },
    "T3.3": {
        "title": "Modelagem usando UML: Multiplicidades, Agregação e Qualificadores",
        "type": "treino",
        "mode": "structured",
        "setup": "",
        "fields": [
            {
                "id": "q1",
                "label": "1. Em um Diagrama de Classes UML (slides 48-54 de ibd-parte2.pdf), na associação Works_for entre Employee e Department, onde fica a multiplicidade `1..1` (um departamento) e `4..*` (quatro ou mais empregados)?",
                "options": [
                    "`1..1` fica junto à classe Department e `4..*` fica junto à classe Employee (na extremidade oposta de quem lê, igual ao 1:N tradicional e OPOSTO ao (min,max) do ER!)",
                    "`1..1` fica junto a Employee e `4..*` fica junto a Department (igual ao (min,max) do ER)",
                    "Na UML não existem multiplicidades numéricas, apenas setas",
                    "Ambos ficam escritos dentro do nome da classe"
                ],
                "answer": "`1..1` fica junto à classe Department e `4..*` fica junto à classe Employee (na extremidade oposta de quem lê, igual ao 1:N tradicional e OPOSTO ao (min,max) do ER!)",
                "explanation": "Cuidado com essa diferença entre ER (min, max) e UML! Na UML (slide 49 de ibd-parte2.pdf), a multiplicidade fica na extremidade da classe destino: 1 Department tem `4..*` Employees, e 1 Employee trabalha em `1..1` Department."
            },
            {
                "id": "q2",
                "label": "2. Como uma Entidade Fraca (ex: Dependent identificada por Employee + Dependent_name) é representada em UML (slide 52 de ibd-parte2.pdf)?",
                "options": [
                    "Usando uma Associação Qualificada (um pequeno retângulo 'Qualificador' com `Dependent_name` colado na classe `Employee` na ponta da associação com `Dependent`)",
                    "Usando uma seta tracejada sem atributos",
                    "Usando um círculo com a letra 'd'",
                    "Não é possível representar entidades fracas em UML"
                ],
                "answer": "Usando uma Associação Qualificada (um pequeno retângulo 'Qualificador' com `Dependent_name` colado na classe `Employee` na ponta da associação com `Dependent`)",
                "explanation": "Slide 52 de ibd-parte2.pdf: O Qualificador UML (ex: `Dependent_name` na caixa junto a `Employee`) atua exatamente como a chave parcial (discriminador) da entidade fraca!"
            },
            {
                "id": "q3",
                "label": "3. No slide 51 de ibd-parte2.pdf (`Polygon 1 ◇--- 3..* Point`), o símbolo do losango na ponta de Polygon representa:",
                "options": [
                    "Agregação (relacionamento todo-parte entre o todo Polygon e as partes Point)",
                    "Generalização / Herança de superclasse",
                    "Entidade fraca recursiva",
                    "Atributo derivado"
                ],
                "answer": "Agregação (relacionamento todo-parte entre o todo Polygon e as partes Point)",
                "explanation": "O losango na extremidade da classe-todo em UML representa Agregação (todo-parte)."
            }
        ]
    },
    "E3.1": {
        "title": "[Oficial ExercERRequisitos600.pdf] Estudo de Caso: Georgia Tech Library (GLT)",
        "type": "oficial",
        "mode": "structured",
        "setup": "",
        "fields": [
            {
                "id": "q1",
                "label": "1. No enunciado da Biblioteca GLT ('Dois livros com o mesmo título podem ter diferentes ISBNs... Alguns livros podem ter o mesmo título, portanto o título não pode ser usado como identificação... a biblioteca possui em média 2,5 cópias/volumes por livro'), qual a modelagem correta de Livros e Cópias?",
                "options": [
                    "Separar LIVRO/TÍTULO (identificado por ISBN, contendo Título, Descrição, Categoria Emprestável/Não-Emprestável e multivalorado Autor) de EXEMPLAR/VOLUME (cópia física individual que é efetivamente emprestada ao sócio)",
                    "Usar Título como chave primária de Livro e ignorar o ISBN",
                    "Guardar todas as cópias como um atributo composto fixo Copia1, Copia2, Copia3",
                    "Não registrar os livros que não podem ser emprestados (mapas e referência)"
                ],
                "answer": "Separar LIVRO/TÍTULO (identificado por ISBN, contendo Título, Descrição, Categoria Emprestável/Não-Emprestável e multivalorado Autor) de EXEMPLAR/VOLUME (cópia física individual que é efetivamente emprestada ao sócio)",
                "explanation": "ISBN identifica a edição/título (`BOOK`), mas como a biblioteca tem múltiplos volumes físicos do mesmo ISBN e precisa saber quantas cópias estão disponíveis ou emprestadas em dado momento, `COPY/VOLUME` (frequentemente entidade fraca de `BOOK` ou entidade forte com código de barras) se relaciona com `BOOK`."
            },
            {
                "id": "q2",
                "label": "2. Sobre os Sócios e Funcionários da GLT ('Quando um novo docente ingressa no instituto, suas informações são preenchidas nos registros de empregados e ele é automaticamente considerado sócio... O pessoal da biblioteca divide-se em bibliotecário-chefe, associados, referência, verificação e assistentes'):",
                "options": [
                    "Temos hierarquia de Especialização/Generalização (ex: SÓCIO / MEMBRO e EMPREGADO compartilhando superclasse PESSOA ou Docente sendo subclasse de Sócio com regras distintas de prazo de 3 meses vs 21 dias, e Funcionários da biblioteca especializados em suas funções)",
                    "Docentes e Sócios não possuem nenhum atributo em comum e não podem fazer empréstimos",
                    "Todo sócio é obrigatoriamente um bibliotecário-chefe (hierarquia total disjunta)",
                    "SSN é um atributo derivado da foto do cartão"
                ],
                "answer": "Temos hierarquia de Especialização/Generalização (ex: SÓCIO / MEMBRO e EMPREGADO compartilhando superclasse PESSOA ou Docente sendo subclasse de Sócio com regras distintas de prazo de 3 meses vs 21 dias, e Funcionários da biblioteca especializados em suas funções)",
                "explanation": "O enunciado pede explicitamente para identificar as abstrações de especialização/generalização: Sócios (Comuns vs Professores/Docentes) e Pessoal da Biblioteca (Bibliotecário-chefe, Associado a depto, Referência, Verificação, Assistente)."
            },
            {
                "id": "q3",
                "label": "3. O enunciado pede: 'Liste os detalhes que eventualmente afetarão o projeto, mas que NÃO se referem ao projeto conceitual (diagrama EER)'. Quais itens do texto entram nessa lista?",
                "options": [
                    "Estatísticas de volume e frequência ('16 mil sócios, 100 mil títulos, 250 mil volumes, 10% emprestados, 1% dos sócios faz 15% dos empréstimos, 20% inativos') e regras temporais/procedurais de aplicação ('prazo de 21 dias vs 3 meses, notificação 1 mês antes de expirar o cartão de 4 anos')",
                    "O fato de um livro ter ISBN, título, autores e assunto",
                    "O fato de sócios terem SSN, endereço no campus/residencial e telefone",
                    "O relacionamento de empréstimo entre sócio e livro/exemplar"
                ],
                "answer": "Estatísticas de volume e frequência ('16 mil sócios, 100 mil títulos, 250 mil volumes, 10% emprestados, 1% dos sócios faz 15% dos empréstimos, 20% inativos') e regras temporais/procedurais de aplicação ('prazo de 21 dias vs 3 meses, notificação 1 mês antes de expirar o cartão de 4 anos')",
                "explanation": "Questão clássica do cap. 3/4 do Elmasri: estatísticas quantitativas (16 mil sócios, 10% emprestados) afetam o Projeto Físico (dimensionamento e índices), e regras de negócio procedurais/temporais (notificação 1 mês antes, limite de 5 livros por vez / 21 dias) são Restrições Semânticas / de Aplicação, não elementos estruturais do diagrama EER!"
            },
            {
                "id": "q4",
                "label": "4. 'Aos sócios é permitida a retirada de, no máximo, 5 livros por vez... Alguns sócios são totalmente inativos e nunca fazem empréstimos'. Qual a restrição (min, max) de SÓCIO no relacionamento EMPRÉSTIMO_ATUAL?",
                "options": [
                    "(0, 5) ao lado de SÓCIO e (0, 1) ao lado de EXEMPLAR_FÍSICO",
                    "(1, 5) ao lado de SÓCIO e (1, N) ao lado de EXEMPLAR_FÍSICO",
                    "(5, 5) ao lado de SÓCIO e (0, N) ao lado de EXEMPLAR_FÍSICO",
                    "(0, 1) ao lado de SÓCIO e (0, 5) ao lado de EXEMPLAR_FÍSICO"
                ],
                "answer": "(0, 5) ao lado de SÓCIO e (0, 1) ao lado de EXEMPLAR_FÍSICO",
                "explanation": "Um sócio pode ter 0 livros emprestados (inativo) até no máximo 5 livros por vez -> (0, 5). Cada exemplar físico está emprestado no momento para 0 (na estante) ou no máximo 1 sócio -> (0, 1)."
            }
        ]
    },

    # =========================================================================
    # MÓDULO 4: MODELO RELACIONAL FORMAL, CHAVES, RIR (b, p, n) E ATUALIZAÇÕES
    # =========================================================================
    "T4.1": {
        "title": "Superchave, Chave Candidata, Primária e Alternativa (exercicios_modelo_relacional.pdf Q1-Q4)",
        "type": "treino",
        "mode": "structured",
        "setup": "",
        "fields": [
            {
                "id": "q1",
                "label": "1. Na relação `Funcionario(CPF, Nome, Cargo, Departamento, Salario)`, onde apenas `CPF` é único por funcionário, qual das opções abaixo contém Três Superchaves válidas, sendo apenas a primeira uma Chave (Chave Candidata mínima)?",
                "options": [
                    "{CPF},  {CPF, Nome},  {CPF, Nome, Cargo, Departamento, Salario}",
                    "{CPF},  {Nome},  {Cargo, Departamento}",
                    "{Nome, Cargo},  {Departamento, Salario},  {Salario}",
                    "Apenas {CPF} é superchave; adicionar atributos destrói a propriedade de superchave"
                ],
                "answer": "{CPF},  {CPF, Nome},  {CPF, Nome, Cargo, Departamento, Salario}",
                "explanation": "Slide 10 de ibd-parte3.pdf e Questões 3 e 4 da lista: Qualquer conjunto de atributos SK que não se repete entre duas tuplas (t1[SK] ≠ t2[SK]) é uma Superchave (inclusive o conjunto de todos os atributos!). Uma Chave (ou Chave Candidata) é uma Superchave MÍNIMA — se removermos qualquer atributo dela, deixa de ser única. Logo {CPF} é chave candidata e superchave, enquanto {CPF, Nome} é superchave mas NÃO é chave!"
            },
            {
                "id": "q2",
                "label": "2. Se uma relação `Aluno(Matricula, CPF, Nome, Curso, AnoIngresso)` possui duas chaves candidatas (`{Matricula}` e `{CPF}`), e o projetista escolhe `Matricula` como Chave Primária (PK), o que `CPF` passa a ser no esquema relacional?",
                "options": [
                    "Chave Alternativa (implementada em SQL com a restrição UNIQUE)",
                    "Chave Estrangeira (FOREIGN KEY)",
                    "Chave Parcial (tracejada)",
                    "Superchave composta redundante"
                ],
                "answer": "Chave Alternativa (implementada em SQL com a restrição UNIQUE)",
                "explanation": "Slide 11 de ibd-parte3.pdf: Dentre as chaves candidatas de um esquema de relação, uma é escolhida como Chave Primária e todas as demais chaves candidatas constituem as Chaves Alternativas."
            },
            {
                "id": "q3",
                "label": "3. Qual característica fundamental diferencia uma Relação Matemática r(R) de um arquivo sequencial de registros em disco?",
                "options": [
                    "As tuplas de uma relação não possuem ordem intrínseca (é um conjunto de tuplas distintas) e todos os valores de atributos em uma tupla devem ser atômicos (1FN)",
                    "Uma relação permite atributos multivalorados e listas aninhadas dentro de uma mesma célula",
                    "As tuplas de uma relação são indexadas obrigatoriamente pela ordem física de inserção",
                    "Uma relação permite duas tuplas 100% idênticas em todos os atributos"
                ],
                "answer": "As tuplas de uma relação não possuem ordem intrínseca (é um conjunto de tuplas distintas) e todos os valores de atributos em uma tupla devem ser atômicos (1FN)",
                "explanation": "Slides 7 e 8 de ibd-parte3.pdf: Uma relação é um conjunto de tuplas (sem ordem entre linhas), e cada valor t[Ai] deve ser atômico (atributos compostos e multivalorados não são permitidos no modelo relacional plano)."
            }
        ]
    },
    "T4.2": {
        "title": "Auditoria de Violações de Integridade e Atualizações (exercicios_modelo_relacional.pdf Q8, Q11, Q12)",
        "type": "treino",
        "mode": "structured",
        "setup": "",
        "fields": [
            {
                "id": "q1",
                "label": "1. (Questão 8 da Lista) Dada `Produto(Codigo, Nome, Preco, QuantidadeEstoque)` com as tuplas: (101, 'Caneta Azul', 2.50, 50), (102, 'Caderno', -5.00, 30), (103, 'Borracha', 1.00, NULL), (104, 'Lapis', 0.80, 100). Quais registros violam restrições e quais são elas?",
                "options": [
                    "Registro 102 viola a Restrição de Domínio/Verificação (Preço -5.00 fora do domínio de preços positivos) e Registro 103 viola a Restrição de Valores Nulos (NOT NULL) caso QuantidadeEstoque seja obrigatória",
                    "Registro 101 viola a Integridade de Entidade e Registro 104 viola a Integridade Referencial",
                    "Nenhum registro viola restrições, pois os códigos 101 a 104 são distintos",
                    "Registro 102 viola a Chave Primária"
                ],
                "answer": "Registro 102 viola a Restrição de Domínio/Verificação (Preço -5.00 fora do domínio de preços positivos) e Registro 103 viola a Restrição de Valores Nulos (NOT NULL) caso QuantidadeEstoque seja obrigatória",
                "explanation": "Preço negativo (-5.00) viola o domínio semântico de valores monetários de produtos (Restrição de Domínio / CHECK > 0), e QuantidadeEstoque = NULL no produto 103 viola a restrição de não-nulidade de estoque."
            },
            {
                "id": "q2",
                "label": "2. (Questão 11 da Lista) Na tabela `Cliente(CPF, Nome, Endereco, Telefone)` onde `CPF` é a Chave Primária, tenta-se inserir `(NULL, 'Maria Souza', 'Rua B, 456', '99765-4321')`. O SGBD aceita ou rejeita?",
                "options": [
                    "Rejeita! Viola a Restrição de Integridade de Entidade, que proíbe que qualquer atributo participante da Chave Primária (PK) tenha valor NULL",
                    "Aceita, desde que exista apenas um cliente com CPF igual a NULL na tabela",
                    "Rejeita por violação de Integridade Referencial",
                    "Aceita e converte NULL para 000.000.000-00 automaticamente"
                ],
                "answer": "Rejeita! Viola a Restrição de Integridade de Entidade, que proíbe que qualquer atributo participante da Chave Primária (PK) tenha valor NULL",
                "explanation": "Slide 15 de ibd-parte3.pdf: Restrição de Integridade de Entidade determina que nenhum componente da Chave Primária pode ser nulo (pois a PK identifica unicamente cada tupla!)."
            },
            {
                "id": "q3",
                "label": "3. Sobre as Operações de Atualização (Insert, Delete, Modify — slides 22-25 de ibd-parte3.pdf), qual é a ÚNICA restrição de integridade que uma operação de Remoção (`DELETE`) pode violar?",
                "options": [
                    "Restrição de Integridade Referencial (quando a tupla removida em R2 está sendo referenciada por uma chave estrangeira FK em alguma tupla de R1)",
                    "Restrição de Domínio (valor fora do tipo de dado)",
                    "Restrição de Chave (duplicação de chave primária)",
                    "Restrição de Integridade de Entidade (chave primária nula)"
                ],
                "answer": "Restrição de Integridade Referencial (quando a tupla removida em R2 está sendo referenciada por uma chave estrangeira FK em alguma tupla de R1)",
                "explanation": "Slide 24 de ibd-parte3.pdf: Remover uma tupla jamais cria chave duplicada, valor fora de domínio ou PK nula. O único perigo do DELETE é deixar ponteiros/chaves estrangeiras órfãs em outras tabelas (Integridade Referencial)!"
            }
        ]
    },
    "E4.1": {
        "title": "[Oficial Lista Modelo Relacional Q5-Q10] Chaves Estrangeiras e Integridade Referencial",
        "type": "oficial",
        "mode": "structured",
        "setup": "",
        "fields": [
            {
                "id": "q1",
                "label": "1. (Questão 6 da Lista) Dadas `Pedido(NumPedido, Data, Valor, CPF_Cliente)` e `Cliente(CPF, Nome, Endereco, Telefone)`, como expressamos formalmente a Restrição de Integridade Referencial (RIR) na notação dos slides?",
                "options": [
                    "Pedido[CPF_Cliente] → Cliente[CPF]",
                    "Cliente[CPF] → Pedido[CPF_Cliente]",
                    "Pedido[NumPedido] → Cliente[CPF]",
                    "Cliente[CPF_Cliente] → Pedido[NumPedido]"
                ],
                "answer": "Pedido[CPF_Cliente] → Cliente[CPF]",
                "explanation": "Slide 18 de ibd-parte3.pdf: A notação é sempre R1[FK] → R2[PK], onde R1 é a relação que contém a chave estrangeira (Pedido) e R2 é a relação referenciada que possui a chave primária (Cliente)."
            },
            {
                "id": "q2",
                "label": "2. (Questão 10 da Lista) Dado o esquema: `Paciente(ID_Paciente, Nome, DataNascimento)`, `Medico(CRM, Nome, Especialidade)` e `Consulta(ID_Consulta, Data, ID_Paciente, CRM_Medico)`, quais são as RIRs formais?",
                "options": [
                    "Consulta[ID_Paciente] → Paciente[ID_Paciente]  e  Consulta[CRM_Medico] → Medico[CRM]",
                    "Paciente[ID_Paciente] → Consulta[ID_Paciente]  e  Medico[CRM] → Consulta[CRM_Medico]",
                    "Consulta[ID_Consulta] → Paciente[ID_Paciente]  e  Paciente[ID_Paciente] → Medico[CRM]",
                    "Medico[CRM] → Paciente[ID_Paciente]"
                ],
                "answer": "Consulta[ID_Paciente] → Paciente[ID_Paciente]  e  Consulta[CRM_Medico] → Medico[CRM]",
                "explanation": "A tabela Consulta possui duas chaves estrangeiras (ID_Paciente e CRM_Medico), cada uma referenciando a respectiva chave primária na tabela pai."
            },
            {
                "id": "q3",
                "label": "3. Para uma RIR `R1[FK] → R2[PK]`, a definição formal de integridade referencial exige que, para toda tupla t1 em R1:",
                "options": [
                    "Ou t1[FK] é igual a t2[PK] para alguma tupla existente t2 em R2, ou t1[FK] é NULL (caso FK não tenha restrição NOT NULL)",
                    "t1[FK] deve ser sempre diferente de qualquer t2[PK]",
                    "t1[FK] nunca pode se repetir em duas linhas de R1",
                    "t1[FK] nunca pode ser NULL em nenhuma circunstância, mesmo em relacionamentos opcionais"
                ],
                "answer": "Ou t1[FK] é igual a t2[PK] para alguma tupla existente t2 em R2, ou t1[FK] é NULL (caso FK não tenha restrição NOT NULL)",
                "explanation": "Slide 16 de ibd-parte3.pdf: Uma FK pode ser NULL (por exemplo, o presidente James Borg tem SUPERSSN = NULL), a menos que o atributo tenha restrição NOT NULL."
            }
        ]
    },
    "E4.2": {
        "title": "[Oficial Slides 03 & 05] Políticas de Remoção da RIR (b, p, n) no Esquema COMPANY",
        "type": "oficial",
        "mode": "structured",
        "setup": "",
        "fields": [
            {
                "id": "q1",
                "label": "1. Em `EMPLOYEE[SUPERSSN] → EMPLOYEE[SSN]` (auto-relacionamento de supervisão onde SUPERSSN aceita nulo), qual a opção de remoção usada nos slides quando um supervisor se aposenta/é removido?",
                "options": [
                    "n (substituição por nulos / ON DELETE SET NULL), pois os subordinados continuam na empresa e ficam temporariamente sem supervisor (SUPERSSN = NULL)",
                    "p (propagação / ON DELETE CASCADE), demitindo em cascata todos os subordinados",
                    "b (bloqueio / RESTRICT), proibindo qualquer remoção",
                    "Nenhuma, pois auto-relacionamento não tem RIR"
                ],
                "answer": "n (substituição por nulos / ON DELETE SET NULL), pois os subordinados continuam na empresa e ficam temporariamente sem supervisor (SUPERSSN = NULL)",
                "explanation": "Slide 20 de ibd-parte3.pdf: `EMPLOYEE[SUPERSSN] ->n EMPLOYEE[SSN]`. Como a supervisão é opcional (aceita NULL), remover o supervisor substitui a FK por NULL."
            },
            {
                "id": "q2",
                "label": "2. Em `DEPENDENT[ESSN] → EMPLOYEE[SSN]` (entidade fraca) e `DEPT_LOCATIONS[DNUMBER] → DEPARTMENT[DNUMBER]` (atributo multivalorado), qual a política de remoção obrigatória nos slides?",
                "options": [
                    "p (propagação / ON DELETE CASCADE) em ambos, pois dependentes e localizações de departamento não existem sem a entidade dona!",
                    "b (bloqueio) em ambos",
                    "n (substituição por nulos) em ambos, deixando a chave primária nula",
                    "b em DEPENDENT e n em DEPT_LOCATIONS"
                ],
                "answer": "p (propagação / ON DELETE CASCADE) em ambos, pois dependentes e localizações de departamento não existem sem a entidade dona!",
                "explanation": "Slides 20-21 de ibd-parte3.pdf e ibd-parte5.pdf: Entidades fracas (`DEPENDENT`), atributos multivalorados (`DEPT_LOCATIONS`), tabelas de relacionamento (`Participa-de`) e subclasses (`Gerente`/`Tecnico`) têm sempre política `p` (propagação)!"
            },
            {
                "id": "q3",
                "label": "3. E nas referências `EMPLOYEE[DNO] → DEPARTMENT[DNUMBER]`, `DEPARTMENT[MGRSSN] → EMPLOYEE[SSN]` e `PROJECT[DNUM] → DEPARTMENT[DNUMBER]`?",
                "options": [
                    "b (bloqueio / RESTRICT), pois não devemos apagar um departamento que ainda possui empregados ou projetos ativos, nem apagar o empregado que é gerente atual de um departamento sem antes trocar o gerente",
                    "p (propagação), apagando todos os empregados e projetos se um departamento for excluído",
                    "n (substituição por nulos), mesmo sendo colunas NOT NULL",
                    "Qualquer uma, pois são equivalentes"
                ],
                "answer": "b (bloqueio / RESTRICT), pois não devemos apagar um departamento que ainda possui empregados ou projetos ativos, nem apagar o empregado que é gerente atual de um departamento sem antes trocar o gerente",
                "explanation": "Slide 20-21 de ibd-parte3.pdf e slide 11 de ibd-parte5.pdf: Relacionamentos funcionais obrigatórios (`DNO(nn)`, `MGRSSN(nn)`, `DNUM(nn)`) usam `b` (bloqueio) para proteger a consistência."
            }
        ]
    },

    # =========================================================================
    # MÓDULO 5: ÁLGEBRA RELACIONAL AVANÇADA — CONJUNTOS, DIVISÃO (÷) E RESTRIÇÕES
    # =========================================================================
    "T5.1": {
        "title": "Operação de Diferença (R − S): Empregados Sem Dependentes",
        "type": "treino",
        "mode": "sql_query",
        "setup": COMPANY_SCHEMA_SETUP,
        "expected_columns": ["LNAME", "FNAME"],
        "expected_rows": [
            ["Borg", "James"],
            ["Narayan", "Ramesh"],
            ["English", "Joyce"],
            ["Zelaya", "Alicia"],
            ["Jabbar", "Ahmad"]
        ]
    },
    "T5.2": {
        "title": "Divisão Relacional (R ÷ S): Trabalham em Todos os Projetos de 'John Smith'",
        "type": "treino",
        "mode": "sql_query",
        "setup": COMPANY_SCHEMA_SETUP,
        "expected_columns": ["FNAME", "LNAME"],
        "expected_rows": [
            ["John", "Smith"],
            ["Joyce", "English"]
        ]
    },
    "T5.3": {
        "title": "Restrições Estruturais em Álgebra Relacional (Ponte para Projeto Lógico)",
        "type": "treino",
        "mode": "structured",
        "setup": "",
        "fields": [
            {
                "id": "q1",
                "label": "1. No mapeamento 1-1 de um relacionamento com Participação Total de Empregado em Trabalha-para (`Empregado(NEmp, ...)` e `Trabalha-para(NEmp, NDept)`), como expressamos em Álgebra Relacional que TODO empregado participa de Trabalha-para (slide 19 de ibd-parte5.pdf)?",
                "options": [
                    "π_{NEmp}(Empregado) = π_{NEmp}(Trabalha-para)",
                    "π_{NEmp}(Empregado) ∩ π_{NEmp}(Trabalha-para) = ∅",
                    "Empregado × Trabalha-para = ∅",
                    "σ_{NEmp = null}(Empregado) ≠ ∅"
                ],
                "answer": "π_{NEmp}(Empregado) = π_{NEmp}(Trabalha-para)",
                "explanation": "Slide 19 de ibd-parte5.pdf: A projeção da chave primária em Empregado deve ser igual à projeção da chave em Trabalha-para: `π_{NEmp}(Empregado) = π_{NEmp}(Trabalha-para)`."
            },
            {
                "id": "q2",
                "label": "2. Em uma hierarquia Disjunta e Total de `Empregado` em `Gerente(NEmp, SalAd)` e `Tecnico(NEmp, Formacao)` (mapeamento 1-1 em tabelas separadas, slide 24 de ibd-parte5.pdf), quais as DUAS equações em Álgebra Relacional que garantem Disjunção ('d') e Totalidade?",
                "options": [
                    "Disjunção: π_{NEmp}(Gerente) ∩ π_{NEmp}(Tecnico) = ∅   |   Totalidade: π_{NEmp}(Gerente) ∪ π_{NEmp}(Tecnico) = π_{NEmp}(Empregado)",
                    "Disjunção: π_{NEmp}(Gerente) ∪ π_{NEmp}(Tecnico) = ∅   |   Totalidade: π_{NEmp}(Gerente) - π_{NEmp}(Tecnico) = π_{NEmp}(Empregado)",
                    "Disjunção: Gerente ÷ Tecnico = ∅   |   Totalidade: Gerente ⨝ Tecnico = Empregado",
                    "Disjunção: π_{NEmp}(Gerente) = π_{NEmp}(Tecnico)   |   Totalidade: π_{NEmp}(Empregado) = ∅"
                ],
                "answer": "Disjunção: π_{NEmp}(Gerente) ∩ π_{NEmp}(Tecnico) = ∅   |   Totalidade: π_{NEmp}(Gerente) ∪ π_{NEmp}(Tecnico) = π_{NEmp}(Empregado)",
                "explanation": "Slide 24 de ibd-parte5.pdf: A interseção (∩) dos NEmp de Gerente e Tecnico deve ser vazia (∅) para garantir disjunção, e a união (∪) deve ser igual a todos os NEmp de Empregado para garantir completude total!"
            },
            {
                "id": "q3",
                "label": "3. E quando a mesma hierarquia Disjunta e Total é colapsada em uma ÚNICA tabela `Empregado(NEmp, Nome, Salario, SalAd, Formacao)` (mapeamento otimizado, slide 25 de ibd-parte5.pdf)? Como ficam as duas equações em Álgebra Relacional?",
                "options": [
                    "π_{NEmp}(σ_{SalAd ≠ nulo}(Empregado)) ∩ π_{NEmp}(σ_{Formacao ≠ nulo}(Empregado)) = ∅  e  π_{NEmp}(σ_{SalAd ≠ nulo}(Empregado)) ∪ π_{NEmp}(σ_{Formacao ≠ nulo}(Empregado)) = π_{NEmp}(Empregado)",
                    "π_{SalAd}(Empregado) ∩ π_{Formacao}(Empregado) = ∅",
                    "σ_{SalAd = nulo AND Formacao = nulo}(Empregado) = Empregado",
                    "Não é possível escrever restrições estruturais no mapeamento otimizado"
                ],
                "answer": "π_{NEmp}(σ_{SalAd ≠ nulo}(Empregado)) ∩ π_{NEmp}(σ_{Formacao ≠ nulo}(Empregado)) = ∅  e  π_{NEmp}(σ_{SalAd ≠ nulo}(Empregado)) ∪ π_{NEmp}(σ_{Formacao ≠ nulo}(Empregado)) = π_{NEmp}(Empregado)",
                "explanation": "Slide 25 de ibd-parte5.pdf: Na tabela única, identificamos quem é Gerente filtrando `σ_{SalAd ≠ nulo}(Empregado)` e quem é Técnico filtrando `σ_{Formacao ≠ nulo}(Empregado)`. Daí aplicamos exatamente a mesma interseção (= ∅) e união (= π_{NEmp}(Empregado))!"
            }
        ]
    },
    "E5.1": {
        "title": "[Oficial consultas_ProfMarcosG.pdf (d)] Empregados que Trabalham em TODOS os Projetos",
        "type": "oficial",
        "mode": "sql_query",
        "setup": COMPANY_PROFM_SETUP,
        "expected_columns": ["FNAME", "LNAME"],
        "expected_rows": [
            ["Franklin", "Wong"]
        ]
    },
    "E5.2": {
        "title": "[Oficial consultas_ProfMarcosG.pdf (e, f)] Gerentes de Departamento Sem Dependentes",
        "type": "oficial",
        "mode": "sql_query",
        "setup": COMPANY_PROFM_SETUP,
        "expected_columns": ["FNAME", "LNAME"],
        "expected_rows": [
            ["James", "Borg"]
        ]
    },

    # =========================================================================
    # MÓDULO 6: SQL AVANÇADO PARA PROJETO LÓGICO — DDL, VISÕES, CHECK & ASSERTION
    # =========================================================================
    "T6.1": {
        "title": "SQL DDL Completo: PRIMARY KEY, UNIQUE e FOREIGN KEY (ON DELETE b, p, n)",
        "type": "treino",
        "mode": "sql_ddl",
        "setup": "",
        "ddl_tests": [
            {
                "name": "Criação das tabelas Departamento, Empregado e Dependente",
                "type": "tables_exist",
                "tables": ["Departamento", "Empregado", "Dependente"]
            },
            {
                "name": "Restrição UNIQUE na Chave Alternativa NomeDept de Departamento",
                "type": "must_fail",
                "sql": """
                    INSERT INTO Departamento (NDept, NomeDept) VALUES ('D1', 'Pesquisa');
                    INSERT INTO Departamento (NDept, NomeDept) VALUES ('D2', 'Pesquisa');
                """,
                "hint": "Adicione UNIQUE (NomeDept) na tabela Departamento."
            },
            {
                "name": "Política de Bloqueio (b / RESTRICT) em Empregado[NDept] -> Departamento[NDept]",
                "type": "must_fail",
                "sql": """
                    INSERT INTO Departamento (NDept, NomeDept) VALUES ('D1', 'Pesquisa');
                    INSERT INTO Empregado (NEmp, NomeEmp, Salario, NDept) VALUES ('E01', 'Ana', 5000, 'D1');
                    DELETE FROM Departamento WHERE NDept = 'D1';
                """,
                "hint": "Defina FOREIGN KEY (NDept) REFERENCES Departamento(NDept) sem CASCADE (o padrão é RESTRICT/bloqueio)."
            },
            {
                "name": "Política de Propagação (p / ON DELETE CASCADE) em Dependente[NEmp] -> Empregado[NEmp]",
                "type": "cascade_check",
                "sql_setup": """
                    INSERT INTO Departamento (NDept, NomeDept) VALUES ('D1', 'Pesquisa');
                    INSERT INTO Empregado (NEmp, NomeEmp, Salario, NDept) VALUES ('E01', 'Ana', 5000, 'D1');
                    INSERT INTO Dependente (NEmp, NomeDep) VALUES ('E01', 'Lucas');
                    DELETE FROM Empregado WHERE NEmp = 'E01';
                """,
                "verify_query": "SELECT COUNT(*) FROM Dependente;",
                "expected_scalar": 0,
                "hint": "Na tabela Dependente, use FOREIGN KEY (NEmp) REFERENCES Empregado(NEmp) ON DELETE CASCADE."
            }
        ]
    },
    "T6.2": {
        "title": "Restrição CHECK de Tupla: Otimizando Hierarquia Disjunta e Total (ibd-parte5 Slide 37)",
        "type": "treino",
        "mode": "sql_ddl",
        "setup": "",
        "ddl_tests": [
            {
                "name": "Tabela Empregado criada com colunas NEmp, Nome, Salario, SalAd, Formacao",
                "type": "tables_exist",
                "tables": ["Empregado"]
            },
            {
                "name": "Aceita um Gerente válido (SalAd preenchido e Formacao NULL)",
                "type": "must_succeed",
                "sql": "INSERT INTO Empregado (NEmp, Nome, Salario, SalAd, Formacao) VALUES ('E01', 'Ana', 8000, 2000, NULL);"
            },
            {
                "name": "Aceita um Técnico válido (SalAd NULL e Formacao preenchida)",
                "type": "must_succeed",
                "sql": "INSERT INTO Empregado (NEmp, Nome, Salario, SalAd, Formacao) VALUES ('E02', 'Bruno', 6000, NULL, 'MSc');"
            },
            {
                "name": "Rejeita violação de Disjunção (SalAd e Formacao ambos preenchidos!)",
                "type": "must_fail",
                "sql": "INSERT INTO Empregado (NEmp, Nome, Salario, SalAd, Formacao) VALUES ('E03', 'Carlos', 7000, 1500, 'BSc');",
                "hint": "Sua cláusula CHECK deve rejeitar quando ambos SalAd e Formacao são NOT NULL."
            },
            {
                "name": "Rejeita violação de Totalidade (SalAd e Formacao ambos NULL!)",
                "type": "must_fail",
                "sql": "INSERT INTO Empregado (NEmp, Nome, Salario, SalAd, Formacao) VALUES ('E04', 'Daniela', 5000, NULL, NULL);",
                "hint": "Sua cláusula CHECK deve exigir: CHECK ((SalAd IS NOT NULL AND Formacao IS NULL) OR (SalAd IS NULL AND Formacao IS NOT NULL))."
            }
        ]
    },
    "T6.3": {
        "title": "Visões em SQL: Modificação da Consulta (Query Modification — ibd-parte4 Slide 36)",
        "type": "treino",
        "mode": "sql_query",
        "setup": COMPANY_SCHEMA_SETUP + """
            CREATE VIEW WORKS_ON1 AS
            SELECT FNAME, LNAME, PNAME, HOURS
            FROM EMPLOYEE, PROJECT, WORKS_ON
            WHERE SSN = ESSN AND PNO = PNUMBER;
        """,
        "expected_columns": ["LNAME", "HOURS"],
        "expected_rows": [
            ["Smith", 32.5],
            ["English", 20.0]
        ]
    },
    "E6.1": {
        "title": "[Oficial consultas_ProfMarcosG.pdf (a, b, c)] Depto 5 em ProductX, Homônimos e Franklin Wong",
        "type": "oficial",
        "mode": "sql_query",
        "setup": COMPANY_PROFM_SETUP,
        "expected_columns": ["CONSULTA", "FNAME", "LNAME"],
        "expected_rows": [
            ["a", "John", "Smith"],
            ["a", "Joyce", "English"],
            ["b", "John", "Smith"],
            ["c", "John", "Smith"],
            ["c", "Ramesh", "Narayan"],
            ["c", "Joyce", "English"],
            ["c", "Carla", "Mendes"]
        ]
    },
    "E6.2": {
        "title": "[Oficial Slides 04] CREATE ASSERTION SALARY_CONSTRAINT (Salário Empregado vs. Gerente)",
        "type": "oficial",
        "mode": "sql_assertion",
        "setup": COMPANY_SCHEMA_SETUP,
        "assertion_tests": [
            {
                "name": "Estado inicial válido da base COMPANY (nenhum empregado ganha mais que seu gerente)",
                "violation_sql": None,
                "should_pass": True
            },
            {
                "name": "Injeção de Falha 1: Empregado John Smith (Depto 5) passa a ganhar 45.000 (Gerente Franklin Wong ganha 40.000)",
                "violation_sql": "UPDATE EMPLOYEE SET SALARY = 45000.00 WHERE SSN = '123456789';",
                "should_pass": False,
                "hint": "Sua subconsulta dentro do NOT EXISTS deve buscar qualquer empregado E, departamento D e gerente M onde E.DNO = D.DNUMBER AND D.MGRSSN = M.SSN AND E.SALARY > M.SALARY."
            },
            {
                "name": "Injeção de Falha 2: Empregada Alicia Zelaya (Depto 4) passa a ganhar 50.000 (Gerente Jennifer Wallace ganha 43.000)",
                "violation_sql": "UPDATE EMPLOYEE SET SALARY = 50000.00 WHERE SSN = '999887777';",
                "should_pass": False,
                "hint": "Verifique se sua junção conecta E.DNO = D.DNUMBER e D.MGRSSN = M.SSN para qualquer departamento."
            }
        ]
    },
    "E6.3": {
        "title": "[Oficial Slides 05] CREATE ASSERTION para Totalidade e Disjunção em Hierarquias",
        "type": "oficial",
        "mode": "sql_assertion",
        "setup": HIERARCHY_SETUP,
        "assertion_tests": [
            {
                "name": "Estado inicial válido: E01 e E03 são Gerentes; E02 e E04 são Técnicos (Disjunta e Total)",
                "violation_sql": None,
                "should_pass": True
            },
            {
                "name": "Injeção de Falha 1 (Violação de Totalidade): Inserir empregado E05 que não está nem em Gerente nem em Tecnico",
                "violation_sql": "INSERT INTO Empregado VALUES ('E05', 'Fabio', 5000.00, 'D1');",
                "should_pass": False,
                "hint": "Para garantir a totalidade (Empregado-total), verifique se NOT EXISTS um Empregado cujo NEmp NOT IN (SELECT NEmp FROM Tecnico UNION SELECT NEmp FROM Gerente)."
            },
            {
                "name": "Injeção de Falha 2 (Violação de Disjunção): Inserir a gerente E01 também na tabela Tecnico",
                "violation_sql": "INSERT INTO Tecnico VALUES ('E01', 'PhD');",
                "should_pass": False,
                "hint": "Você pode escrever uma segunda CREATE ASSERTION Gerente_ou_Tecnico CHECK (NOT EXISTS (SELECT * FROM Gerente G, Tecnico T WHERE G.NEmp = T.NEmp)) ou combinar com UNION!"
            }
        ]
    },

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

}

def get_connection(ex_id: str) -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON;")
    if ex_id in EXERCISES_DATA and EXERCISES_DATA[ex_id].get("setup"):
        conn.executescript(EXERCISES_DATA[ex_id]["setup"])
    return conn


def validate_structured(ex_id: str, answers: Dict[str, str]) -> Dict[str, Any]:
    info = EXERCISES_DATA[ex_id]
    fields = info.get("fields", [])
    results = []
    all_correct = True

    for f in fields:
        fid = f["id"]
        user_val = (answers.get(fid) or "").strip()
        expected_val = f["answer"].strip()
        is_ok = (user_val == expected_val)
        if not is_ok:
            all_correct = False
        results.append({
            "id": fid,
            "correct": is_ok,
            "userAnswer": user_val,
            "expectedAnswer": expected_val,
            "explanation": f["explanation"]
        })

    correct_count = sum(1 for r in results if r["correct"])
    return {
        "matched": all_correct,
        "mode": "structured",
        "score": f"{correct_count}/{len(fields)}",
        "diffReason": (
            "Perfeito! Todas as análises conceituais e notações estão 100% corretas."
            if all_correct
            else f"Você acertou {correct_count} de {len(fields)} itens. Veja o diagnóstico detalhado em cada questão abaixo."
        ),
        "fieldResults": results
    }


def validate_ddl(ex_id: str, ddl_sql: str) -> Dict[str, Any]:
    if not ddl_sql.strip():
        return {"matched": False, "mode": "sql_ddl", "error": "Escreva os comandos CREATE TABLE para validar."}

    info = EXERCISES_DATA[ex_id]
    tests = info.get("ddl_tests", [])
    test_results = []
    all_passed = True

    # First check if the user's DDL itself parses and executes cleanly
    try:
        base_conn = sqlite3.connect(":memory:")
        base_conn.execute("PRAGMA foreign_keys = ON;")
        base_conn.executescript(ddl_sql)
    except Exception as e:
        return {
            "matched": False,
            "mode": "sql_ddl",
            "error": f"Erro de sintaxe ao executar seu DDL: {e}",
            "testResults": []
        }

    for t in tests:
        conn = sqlite3.connect(":memory:")
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.executescript(ddl_sql)
        cur = conn.cursor()

        t_type = t["type"]
        passed = False
        detail = ""

        try:
            if t_type == "tables_exist":
                cur.execute("SELECT lower(name) FROM sqlite_master WHERE type='table';")
                existing = {r[0] for r in cur.fetchall()}
                missing = [tbl for tbl in t["tables"] if tbl.lower() not in existing]
                if not missing:
                    passed = True
                    detail = f"Tabelas encontradas: {', '.join(t['tables'])}."
                else:
                    passed = False
                    detail = f"Tabelas ausentes: {', '.join(missing)}."

            elif t_type == "must_succeed":
                conn.executescript(t["sql"])
                passed = True
                detail = "Operação válida aceita pelo seu esquema com sucesso."

            elif t_type == "must_fail":
                try:
                    conn.executescript(t["sql"])
                    passed = False
                    detail = f"FALHA DE RESTRIÇÃO: O banco aceitou dados inválidos! Dica: {t.get('hint', '')}"
                except sqlite3.IntegrityError as ie:
                    passed = True
                    detail = f"Violação bloqueada corretamente pelo SGBD ({ie})."

            elif t_type == "cascade_check":
                conn.executescript(t["sql_setup"])
                cur.execute(t["verify_query"])
                val = cur.fetchone()[0]
                if val == t["expected_scalar"]:
                    passed = True
                    detail = f"Propagação verificada com sucesso (restaram {val} tuplas órfãs)."
                else:
                    passed = False
                    detail = f"Esperado {t['expected_scalar']} após remoção, mas obteve {val}. {t.get('hint', '')}"
        except Exception as ex:
            passed = False
            detail = f"Erro durante o teste: {ex}. {t.get('hint', '')}"

        if not passed:
            all_passed = False

        test_results.append({
            "name": t["name"],
            "passed": passed,
            "detail": detail
        })

    return {
        "matched": all_passed,
        "mode": "sql_ddl",
        "diffReason": (
            "Todas as baterias de Injeção de Falhas (PK, UNIQUE, CHECK e RIR ON DELETE) passaram com sucesso!"
            if all_passed
            else "Algumas restrições de integridade não bloquearam ou propagaram como esperado. Veja o relatório de testes abaixo."
        ),
        "testResults": test_results
    }


def extract_assertion_subqueries(sql_text: str) -> List[Tuple[str, str]]:
    """
    Extracts (assertion_name, inner_select_query) from SQL-92 CREATE ASSERTION statements:
    CREATE ASSERTION <name> CHECK (NOT EXISTS (<select_query>))
    Supports multiple CREATE ASSERTION statements in the same editor.
    """
    cleaned = re.sub(r"--.*?$", "", sql_text, flags=re.MULTILINE).strip()
    if not cleaned:
        return []

    # Split by semicolon if multiple assertions
    stmts = [s.strip() for s in cleaned.split(";") if s.strip()]
    extracted = []

    for stmt in stmts:
        m = re.match(
            r"CREATE\s+ASSERTION\s+([A-Za-z0-9_\-]+)\s+CHECK\s*\(\s*NOT\s+EXISTS\s*\((.*)\)\s*\)\s*$",
            stmt,
            flags=re.IGNORECASE | re.DOTALL
        )
        if m:
            name = m.group(1)
            subq = m.group(2).strip()
            extracted.append((name, subq))
        else:
            raise ValueError(
                "Formato esperado: CREATE ASSERTION <nome> CHECK (NOT EXISTS (SELECT ...));"
            )
    return extracted


def validate_assertion(ex_id: str, assertion_sql: str) -> Dict[str, Any]:
    if not assertion_sql.strip():
        return {"matched": False, "mode": "sql_assertion", "error": "Escreva o comando CREATE ASSERTION para validar."}

    try:
        assertions = extract_assertion_subqueries(assertion_sql)
    except ValueError as ve:
        return {"matched": False, "mode": "sql_assertion", "error": str(ve), "testResults": []}

    info = EXERCISES_DATA[ex_id]
    tests = info.get("assertion_tests", [])
    test_results = []
    all_passed = True

    for t in tests:
        conn = get_connection(ex_id)
        cur = conn.cursor()
        try:
            if t.get("violation_sql"):
                conn.executescript(t["violation_sql"])

            # Evaluate all assertions: an assertion holds iff NOT EXISTS (subq) is true (i.e., subq returns 0 rows)
            assertion_holds = True
            triggered_by = []
            for name, subq in assertions:
                cur.execute(subq)
                violating_rows = cur.fetchall()
                if len(violating_rows) > 0:
                    assertion_holds = False
                    triggered_by.append(f"{name} ({len(violating_rows)} tupla(s) violadora(s) detectada(s))")

            should_pass = t["should_pass"]
            passed = (assertion_holds == should_pass)

            if should_pass:
                detail = (
                    "Banco válido: Nenhuma violação falsa reportada pela sua asserção."
                    if passed
                    else f"Falso positivo! Sua asserção acusou erro no banco válido: {', '.join(triggered_by)}"
                )
            else:
                detail = (
                    f"Violação capturada com sucesso por: {', '.join(triggered_by)}!"
                    if passed
                    else f"Violação passou despercebida (NOT EXISTS retornou verdadeiro)! {t.get('hint', '')}"
                )
        except Exception as e:
            passed = False
            detail = f"Erro ao executar a subconsulta da asserção: {e}"

        if not passed:
            all_passed = False

        test_results.append({
            "name": t["name"],
            "passed": passed,
            "detail": detail
        })

    return {
        "matched": all_passed,
        "mode": "sql_assertion",
        "diffReason": (
            "Asserção SQL-92 validada! Capturou todas as violações injetadas sem falsos positivos."
            if all_passed
            else "A asserção não passou em todos os cenários de teste. Confira os detalhes abaixo."
        ),
        "testResults": test_results
    }


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] == "list":
        print("Exercícios disponíveis no IBD Prerequisite Studio:")
        for k, v in EXERCISES_DATA.items():
            print(f"  {k:6s} [{v['mode']:13s}] - {v['title']}")
    elif sys.argv[1] == "schema" and len(sys.argv) >= 3:
        ex_id = sys.argv[2]
        conn = get_connection(ex_id)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        for (tname,) in cur.fetchall():
            print(f"\n=== Tabela: {tname} ===")
            cur.execute(f"SELECT * FROM {tname};")
            for row in cur.fetchall():
                print(" ", row)

