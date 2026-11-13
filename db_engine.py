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
EXERCISES_DATA: Dict[str, Dict[str, Any]] = {'T1.1': {'title': 'Esquema (Intensão) vs. Instância (Extensão) e os 3 Níveis',
          'type': 'treino',
          'mode': 'structured',
          'setup': '',
          'fields': [{'id': 'q1',
                      'label': "1. A definição estrutural 'Estudantes(eid: string, nome: string, idade: "
                               "int)' armazenada no catálogo do SGBD corresponde a qual conceito?",
                      'options': ['Instância do Banco de Dados (Extensão no instante t)',
                                  'Esquema Interno de Armazenamento (Nível Físico)',
                                  'Esquema Conceitual do Banco (Intensão no catálogo)',
                                  'Esquema Externo de Usuário (Visão personalizada)'],
                      'answer': 'Esquema Conceitual do Banco (Intensão no catálogo)',
                      'explanation': "O Esquema Conceitual descreve 'O QUE' está armazenado (entidades, "
                                     'atributos, tipos e restrições) — é a intensão, que muda raramente.'},
                     {'id': 'q2',
                      'label': '2. O conjunto de 1.500 tuplas de alunos efetivamente gravadas nas tabelas em '
                               'um dado instante t representa:',
                      'options': ['A Instância (ou Estado / Extensão) do banco de dados',
                                  'O Esquema Lógico Global definido pela linguagem DDL',
                                  'O Metadado estrutural armazenado no dicionário do SGBD',
                                  'A Independência Lógica entre o esquema e a aplicação'],
                      'answer': 'A Instância (ou Estado / Extensão) do banco de dados',
                      'explanation': 'Os dados presentes no BD em um determinado instante de tempo formam a '
                                     'Instância (ou Estado/Extensão). Ela muda a cada INSERT, DELETE ou '
                                     'UPDATE.'},
                     {'id': 'q3',
                      'label': "3. A especificação 'Relações guardadas como arquivos heap desordenados com "
                               "índice B-Tree na coluna eid' pertence ao:",
                      'options': ['Nível Conceitual (descrição lógica das entidades e chaves)',
                                  'Nível Externo (definição de visões parciais por usuário)',
                                  'Nível de Aplicação (estruturas de registros na linguagem C)',
                                  'Nível Interno (Esquema Físico — como está armazenado)'],
                      'answer': 'Nível Interno (Esquema Físico — como está armazenado)',
                      'explanation': 'O Nível Interno descreve a estrutura física de armazenamento em disco '
                                     '(arquivos, páginas, tamanhos em bytes/words e índices).'},
                     {'id': 'q4',
                      'label': "4. A definição 'Lista_Matricula(nome, cnome)' criada para a secretaria "
                               'consultar alunos e cursos sem ver notas ou salários pertence ao:',
                      'options': ['Nível Interno (organização física de blocos e índices)',
                                  'Nível Externo (Visão / Esquema Externo de comunidade)',
                                  'Nível Conceitual Global (estrutura comunitária completa)',
                                  'Nível de Dicionário Físico (catálogo interno do SGBD)'],
                      'answer': 'Nível Externo (Visão / Esquema Externo de comunidade)',
                      'explanation': 'O Nível Externo é composto por visões (views) adaptadas a grupos '
                                     'específicos de usuários, ocultando o restante do banco.'}]},
 'T1.2': {'title': 'Diagnóstico de Independência de Dados: Lógica vs. Física',
          'type': 'treino',
          'mode': 'structured',
          'setup': '',
          'fields': [{'id': 'q1',
                      'label': '1. O DBA cria um novo índice hash e reorganiza os arquivos físicos de '
                               'Empregado no disco sem precisar alterar o Esquema Conceitual nem as '
                               'aplicações. Isso exemplifica a:',
                      'options': ['Independência de Dados Lógica (entre o Nível Conceitual e o Nível '
                                  'Externo)',
                                  'Independência de Dados Física (entre o Nível Interno e o Nível '
                                  'Conceitual)',
                                  'Restrição de Integridade Referencial (entre chaves estrangeiras e '
                                  'primárias)',
                                  'Abstração de Modelo Conceitual (mapeamento direto entre ER e linguagem '
                                  'C)'],
                      'answer': 'Independência de Dados Física (entre o Nível Interno e o Nível Conceitual)',
                      'explanation': 'Independência Física é a capacidade de alterar o Esquema Interno '
                                     '(físico) sem precisar alterar o Esquema Conceitual (nem o Externo).'},
                     {'id': 'q2',
                      'label': "2. A empresa adiciona uma nova entidade 'Projeto_Social' e novos atributos "
                               'ao Esquema Conceitual, mas as Visões Externas e aplicações antigas continuam '
                               'funcionando sem alterações. Isso é:',
                      'options': ['Independência de Dados Física (entre o Nível Interno e o Nível '
                                  'Conceitual)',
                                  'Isolamento Transacional de Concorrência (controle de bloqueio de '
                                  'arquivos)',
                                  'Normalização Estrutural de Relações (decomposição para terceira forma '
                                  'normal)',
                                  'Independência de Dados Lógica (entre o Nível Conceitual e o Nível '
                                  'Externo)'],
                      'answer': 'Independência de Dados Lógica (entre o Nível Conceitual e o Nível Externo)',
                      'explanation': 'Independência Lógica é a capacidade de alterar o Esquema Conceitual '
                                     '(ex: adicionar entidades/atributos) sem alterar os Esquemas Externos '
                                     'ou programas que não usam os novos elementos.'},
                     {'id': 'q3',
                      'label': '3. Na arquitetura ANSI/SPARC de 3 esquemas, a definição formal de '
                               'Independência de Dados estabelece a capacidade de:',
                      'options': ['Alterar o esquema em um nível mais baixo sem precisar alterar o esquema '
                                  'no nível mais alto',
                                  'Alterar o esquema no nível externo e propagar a mudança automaticamente '
                                  'aos arquivos físicos',
                                  'Vincular as estruturas físicas de disco diretamente às declarações de '
                                  'variáveis da aplicação',
                                  'Substituir o catálogo central do SGBD por arquivos sequenciais '
                                  'independentes em cada programa'],
                      'answer': 'Alterar o esquema em um nível mais baixo sem precisar alterar o esquema no '
                                'nível mais alto',
                      'explanation': 'Slide 55 de 01-introducao.pdf: Independência de dados é a capacidade '
                                     'de alterar o esquema em um determinado nível sem alterar o esquema do '
                                     'nível imediatamente mais alto (apenas o mapeamento entre eles é '
                                     'ajustado).'}]},
 'E1.1': {'title': '[Oficial Slides 01] Sublinguagens do SGBD e Arquitetura de 3 Níveis',
          'type': 'oficial',
          'mode': 'structured',
          'setup': '',
          'fields': [{'id': 'q1',
                      'label': '1. No Exemplo 2 dos slides (Empregado), como são classificados: (A) `struct '
                               'Participante { char[30] Nome; int Departamento; }`, (B) `Empregado(NOME '
                               'CHAR(30), SALARIO NUMERIC(5), ...)`, e (C) `RegistroEmpregado LENGTH=50, SAL '
                               'TYPE=FULLWORD`?',
                      'options': ['(A) Esquema Conceitual, (B) Esquema Externo, (C) Esquema Interno',
                                  '(A) Esquema Interno, (B) Esquema Conceitual, (C) Esquema Externo',
                                  '(A) Esquema Externo, (B) Esquema Conceitual, (C) Esquema Interno',
                                  '(A) Esquema Externo, (B) Esquema Interno, (C) Esquema Conceitual'],
                      'answer': '(A) Esquema Externo, (B) Esquema Conceitual, (C) Esquema Interno',
                      'explanation': 'Slide 53: (A) A struct em C/Pascal que omite Salário e Sexo é a Visão '
                                     'Externa daquele programa; (B) A definição lógica completa de Empregado '
                                     'é o Esquema Conceitual; (C) A especificação de bytes, FULLWORD e WORD '
                                     'é o Esquema Interno.'},
                     {'id': 'q2',
                      'label': '2. Qual sublinguagem do SGBD é responsável por especificar os esquemas '
                               'conceituais (tabelas, atributos e restrições) no catálogo?',
                      'options': ['DML / LMD (Linguagem de Manipulação de Dados — ex: INSERT, UPDATE, '
                                  'DELETE)',
                                  'DQL (Linguagem de Consulta de Dados — ex: SELECT ... FROM ... WHERE)',
                                  'SDL (Linguagem de Definição de Armazenamento — parâmetros físicos de '
                                  'blocos)',
                                  'DDL / LDD (Linguagem de Definição de Dados — ex: CREATE TABLE, ALTER '
                                  'TABLE)'],
                      'answer': 'DDL / LDD (Linguagem de Definição de Dados — ex: CREATE TABLE, ALTER TABLE)',
                      'explanation': 'A LDD (DDL) define os esquemas e restrições que vão para o catálogo do '
                                     'SGBD.'},
                     {'id': 'q3',
                      'label': '3. Qual problema clássico dos sistemas de fichários ocorre quando dois '
                               'usuários acessam a mesma ficha simultaneamente e geram cópias divergentes?',
                      'options': ['Excesso de Independência Lógica entre o esquema conceitual e as visões',
                                  'Ausência de Controle de Concorrência e Redundância/Inconsistência de '
                                  'Dados',
                                  'Bloqueio automático provocado por Restrições de Integridade Referencial',
                                  'Sobrecarga de compilação da Linguagem de Definição de Dados no catálogo'],
                      'answer': 'Ausência de Controle de Concorrência e Redundância/Inconsistência de Dados',
                      'explanation': 'Slide 10 de 01-introducao.pdf: Sistemas de arquivos tradicionais não '
                                     'possuem controle de concorrência integrado nem catálogo centralizado, '
                                     'gerando anomalias de acesso concorrente e duplicação.'}]},
 'T2.1': {'title': 'Classificação de Atributos no Modelo ER (Slides ibd-parte2)',
          'type': 'treino',
          'mode': 'structured',
          'setup': '',
          'fields': [{'id': 'q1',
                      'label': "1. O atributo 'Endereço', subdividido em Rua (Número, Nome_Rua, Apto), "
                               'Cidade, Estado e CEP, é classificado e desenhado no ER como:',
                      'options': ['Atributo Multivalorado (representado por uma elipse de linha dupla no '
                                  'diagrama)',
                                  'Atributo Derivado (representado por uma elipse de linha tracejada no '
                                  'diagrama)',
                                  'Atributo Composto (elipse ligada a uma árvore de sub-atributos '
                                  'componentes)',
                                  'Atributo Discriminador (elipse com nome sublinhado por uma linha '
                                  'tracejada)'],
                      'answer': 'Atributo Composto (elipse ligada a uma árvore de sub-atributos componentes)',
                      'explanation': 'Atributos compostos podem ser divididos em partes menores com '
                                     'significados independentes, formando uma hierarquia/árvore de '
                                     'elipses.'},
                     {'id': 'q2',
                      'label': "2. Um Departamento pode possuir várias localizações ('Houston', 'Bellaire', "
                               "'Sugarland'). No diagrama ER, 'Locations' é um:",
                      'options': ['Atributo Multivalorado (desenhado com elipse de linha dupla)',
                                  'Atributo Composto (desenhado com sub-elipses em ramificação)',
                                  'Atributo Derivado (desenhado com elipse de linha tracejada)',
                                  'Atributo Chave Parcial (desenhado com sublinhado tracejado)'],
                      'answer': 'Atributo Multivalorado (desenhado com elipse de linha dupla)',
                      'explanation': 'Quando uma mesma entidade pode ter múltiplos valores para o mesmo '
                                     'atributo simultaneamente (ex: vários telefones, vários ramais, várias '
                                     'localizações), ele é Multivalorado (elipse dupla).'},
                     {'id': 'q3',
                      'label': "3. O atributo 'Numero_de_Empregados' de DEPARTMENT ou 'Idade' de EMPLOYEE "
                               '(obtida a partir de Data_Nascimento) é classificado como:',
                      'options': ['Atributo Armazenado Monovalorado (elipse de linha contínua simples)',
                                  'Atributo Composto Hierárquico (elipse dividida em Dia, Mês e Ano)',
                                  'Atributo Derivado (desenhado com elipse de linha tracejada)',
                                  'Atributo Multivalorado Temporal (elipse de linha dupla contínua)'],
                      'answer': 'Atributo Derivado (desenhado com elipse de linha tracejada)',
                      'explanation': 'Atributos cujos valores podem ser calculados a partir de outros '
                                     'atributos ou relacionamentos existentes (como contar quantos '
                                     'empregados trabalham no depto) são Derivados (elipse tracejada).'},
                     {'id': 'q4',
                      'label': '4. No Modelo ER, quando um empregado mora em uma casa (sem apto), o NULL em '
                               "'Numero_Apto' significa _____; já quando não sabemos seu telefone "
                               'residencial, o NULL significa _____:',
                      'options': ['Não aplicável (inexistente) / Desconhecido (existente)',
                                  'Desconhecido (existente) / Não aplicável (inexistente)',
                                  'Chave parcial ausente / Chave estrangeira órfã',
                                  'Domínio atômico vazio / Atributo derivado nulo'],
                      'answer': 'Não aplicável (inexistente) / Desconhecido (existente)',
                      'explanation': "Slide 8 de ibd-parte2.pdf: NULL tem duas semânticas principais: 'Não "
                                     "aplicável' (ex: número de apto para quem mora em casa) e "
                                     "'Desconhecido' (o valor existe no mundo real, mas não foi "
                                     'informado).'}]},
 'T2.2': {'title': 'O Tradutor de Cardinalidades: Notação 1:N (Chen) ↔ Notação (min, max)',
          'type': 'treino',
          'mode': 'structured',
          'setup': '',
          'fields': [{'id': 'q1',
                      'label': "1. Regra: 'Todo empregado trabalha para exatamente um departamento, e cada "
                               "departamento tem de 4 a N empregados'. Na notação tradicional (Chen), onde "
                               'ficam o 1 e o N?',
                      'options': ['N perto de DEPARTMENT e 1 perto de EMPLOYEE',
                                  '1 perto de DEPARTMENT e 1 perto de EMPLOYEE',
                                  'M perto de DEPARTMENT e N perto de EMPLOYEE',
                                  '1 perto de DEPARTMENT e N perto de EMPLOYEE'],
                      'answer': '1 perto de DEPARTMENT e N perto de EMPLOYEE',
                      'explanation': "Na notação 1:N tradicional (Chen), lê-se '1 Departamento emprega N "
                                     "Empregados', então o 1 fica do lado de DEPARTMENT e o N do lado de "
                                     'EMPLOYEE.'},
                     {'id': 'q2',
                      'label': "2. Para a MESMA regra acima ('Todo empregado trabalha em exatamente 1 depto; "
                               "todo depto tem de 4 a N empregados'), quais são os pares na notação (min, "
                               'max)?',
                      'options': ['EMPLOYEE: (4, N)  |  DEPARTMENT: (1, 1)',
                                  'EMPLOYEE: (1, 1)  |  DEPARTMENT: (4, N)',
                                  'EMPLOYEE: (0, 1)  |  DEPARTMENT: (1, N)',
                                  'EMPLOYEE: (1, N)  |  DEPARTMENT: (0, 1)'],
                      'answer': 'EMPLOYEE: (1, 1)  |  DEPARTMENT: (4, N)',
                      'explanation': 'Na notação (min, max) do Prof. Marcos André / Elmasri (slide 28 de '
                                     'ibd-parte2.pdf), o par (min, max) ao lado de uma entidade indica em '
                                     'quantas instâncias daquele relacionamento ELA participa! Cada EMPLOYEE '
                                     'participa de exatamente 1 vínculo -> (1,1). Cada DEPARTMENT participa '
                                     "de 4 a N vínculos -> (4,N). Os lados do '1' e do 'N' se invertem em "
                                     'relação à notação tradicional!'},
                     {'id': 'q3',
                      'label': "3. Regra: 'Um departamento é gerenciado por exatamente um empregado; mas um "
                               "empregado gerencia no máximo um departamento (ou nenhum)'. Quais os pares "
                               '(min, max) em MANAGES?',
                      'options': ['Ao lado de EMPLOYEE: (1, 1)  |  Ao lado de DEPARTMENT: (0, 1)',
                                  'Ao lado de EMPLOYEE: (0, 1)  |  Ao lado de DEPARTMENT: (1, 1)',
                                  'Ao lado de EMPLOYEE: (1, N)  |  Ao lado de DEPARTMENT: (1, 1)',
                                  'Ao lado de EMPLOYEE: (0, N)  |  Ao lado de DEPARTMENT: (0, 1)'],
                      'answer': 'Ao lado de EMPLOYEE: (0, 1)  |  Ao lado de DEPARTMENT: (1, 1)',
                      'explanation': 'Nem todo empregado é gerente, então um EMPLOYEE participa de 0 ou 1 '
                                     'instância de MANAGES -> (0, 1). Todo departamento TEM exatamente um '
                                     'gerente -> DEPARTMENT tem (1, 1).'},
                     {'id': 'q4',
                      'label': '4. No relacionamento recursivo SUPERVISION em EMPLOYEE, o papel 1 é '
                               "'Supervisor' e o papel 2 é 'Supervisionado'. Se um chefe supervisiona de 0 a "
                               'N subordinados e cada empregado tem no máximo 1 chefe direto, quais os (min, '
                               'max)?',
                      'options': ['Papel 1 (Supervisor): (0, 1)  |  Papel 2 (Supervisionado): (0, N)',
                                  'Papel 1 (Supervisor): (1, 1)  |  Papel 2 (Supervisionado): (1, N)',
                                  'Papel 1 (Supervisor): (1, N)  |  Papel 2 (Supervisionado): (1, 1)',
                                  'Papel 1 (Supervisor): (0, N)  |  Papel 2 (Supervisionado): (0, 1)'],
                      'answer': 'Papel 1 (Supervisor): (0, N)  |  Papel 2 (Supervisionado): (0, 1)',
                      'explanation': 'Slide 28 de ibd-parte2.pdf: No papel de Supervisor (1), um empregado '
                                     'supervisiona de 0 a N subordinados -> (0, N). No papel de '
                                     'Supervisionado (2), um empregado tem 0 (caso do presidente) ou 1 '
                                     'supervisor direto -> (0, 1).'}]},
 'T2.3': {'title': 'Anatomia de Tipos de Entidade Fraca e Chave Parcial',
          'type': 'treino',
          'mode': 'structured',
          'setup': '',
          'fields': [{'id': 'q1',
                      'label': '1. Quando um conceito do mini-mundo deve ser modelado como um Tipo de '
                               'Entidade Fraca (retângulo duplo) no diagrama ER?',
                      'options': ['Quando seus atributos próprios não a identificam unicamente sem a chave '
                                  'de uma entidade dona',
                                  'Quando a entidade possui participação parcial (0, N) em todos os seus '
                                  'relacionamentos binários',
                                  'Quando a entidade representa uma subclasse opcional em uma hierarquia de '
                                  'especialização parcial',
                                  'Quando a entidade possui apenas atributos simples e nenhum atributo '
                                  'composto ou multivalorado'],
                      'answer': 'Quando seus atributos próprios não a identificam unicamente sem a chave de '
                                'uma entidade dona',
                      'explanation': 'Uma entidade fraca não possui chave primária própria; suas instâncias '
                                     'são identificadas pelo relacionamento identificador com uma entidade '
                                     'dona somado à sua chave parcial.'},
                     {'id': 'q2',
                      'label': '2. No diagrama da prova (`ExercicioProjetoLogico.pdf`), `TRECHO_VOO` tem '
                               'retângulo duplo, `Trecho_num` tem sublinhado tracejado, e `TRECHOS` tem '
                               'losango duplo ligado a `VOO` (chave `Numero`). O que isso define?',
                      'options': ['TRECHO_VOO é um atributo composto multivalorado de VOO cujo identificador '
                                  'global é apenas Trecho_num',
                                  'TRECHOS é um relacionamento M:N entre duas entidades fortes independentes '
                                  'com chaves Numero e Trecho_num',
                                  'TRECHO_VOO é entidade fraca de VOO com chave parcial Trecho_num e chave '
                                  'completa (Numero, Trecho_num)',
                                  'TRECHO_VOO é uma subclasse herdada de VOO através de uma generalização '
                                  'disjunta e parcial'],
                      'answer': 'TRECHO_VOO é entidade fraca de VOO com chave parcial Trecho_num e chave '
                                'completa (Numero, Trecho_num)',
                      'explanation': 'Retângulo duplo = entidade fraca; losango duplo = relacionamento '
                                     'identificador; sublinhado tracejado = chave parcial (discriminador). A '
                                     'PK de TRECHO_VOO combina a PK do dono (Numero) com a chave parcial '
                                     '(Trecho_num).'},
                     {'id': 'q3',
                      'label': '3. Qual é obrigatoriamente a restrição de participação de uma Entidade Fraca '
                               'no seu Relacionamento Identificador (losango duplo)?',
                      'options': ['Participação PARCIAL (linha simples / min = 0), pois a entidade fraca '
                                  'pode existir sem um dono',
                                  'Cardinalidade M:N com participação parcial em ambos os lados do '
                                  'relacionamento identificador',
                                  'Participação condicional variável, dependendo de a chave parcial ser '
                                  'numérica ou alfanumérica',
                                  'Participação TOTAL (linha dupla / min = 1), pois a entidade fraca não '
                                  'existe sem a entidade dona'],
                      'answer': 'Participação TOTAL (linha dupla / min = 1), pois a entidade fraca não '
                                'existe sem a entidade dona',
                      'explanation': 'Por definição de dependência de existência e de identificação, toda '
                                     'entidade fraca tem participação TOTAL (linha dupla) no relacionamento '
                                     'identificador com seu proprietário.'}]},
 'E2.1': {'title': "[Oficial Slides 02] Auditoria Completa do Esquema ER 'COMPANY'",
          'type': 'oficial',
          'mode': 'structured',
          'setup': '',
          'fields': [{'id': 'q1',
                      'label': "1. No esquema COMPANY, onde deve ser posicionado o atributo 'Hours' (horas "
                               'semanais trabalhadas pelo empregado em um projeto) e por quê?',
                      'options': ['Na entidade EMPLOYEE, pois é o empregado quem realiza o trabalho '
                                  'semanalmente',
                                  'No relacionamento M:N WORKS_ON, pois o valor depende do par (EMPLOYEE, '
                                  'PROJECT)',
                                  'Na entidade PROJECT, pois o controle de horas pertence ao escopo de cada '
                                  'projeto',
                                  'No relacionamento 1:N CONTROLS, pois o departamento gerencia a carga '
                                  'horária'],
                      'answer': 'No relacionamento M:N WORKS_ON, pois o valor depende do par (EMPLOYEE, '
                                'PROJECT)',
                      'explanation': 'Em um relacionamento M:N, um empregado trabalha em vários projetos e '
                                     "um projeto tem vários empregados; 'Hours' descreve a associação "
                                     'específica entre um empregado e um projeto.'},
                     {'id': 'q2',
                      'label': "2. Como é modelado o atributo 'Start_Date' (data em que o empregado assumiu "
                               'a gerência do departamento) no diagrama ER da companhia?',
                      'options': ['Como um tipo de entidade fraca subordinada simultaneamente a EMPLOYEE e '
                                  'PROJECT',
                                  'Como um atributo multivalorado (elipse dupla) anexado à entidade PROJECT',
                                  'Como um atributo do relacionamento 1:1 MANAGES entre EMPLOYEE e '
                                  'DEPARTMENT',
                                  'Como a chave parcial discriminadora da entidade forte DEPARTMENT'],
                      'answer': 'Como um atributo do relacionamento 1:1 MANAGES entre EMPLOYEE e DEPARTMENT',
                      'explanation': 'No esquema ER conceitual, Start_Date é atributo do relacionamento '
                                     'MANAGES (e no mapeamento relacional otimizado migra junto com MGRSSN '
                                     'para DEPARTMENT).'},
                     {'id': 'q3',
                      'label': "3. No relacionamento CONTROLS ('Um departamento controla de 0 a N projetos, "
                               "mas cada projeto é controlado por exatamente 1 departamento'), quais são os "
                               'pares (min, max)?',
                      'options': ['DEPARTMENT: (0, N)  |  PROJECT: (1, 1)',
                                  'DEPARTMENT: (1, 1)  |  PROJECT: (0, N)',
                                  'DEPARTMENT: (1, N)  |  PROJECT: (0, 1)',
                                  'DEPARTMENT: (0, 1)  |  PROJECT: (1, N)'],
                      'answer': 'DEPARTMENT: (0, N)  |  PROJECT: (1, 1)',
                      'explanation': 'Cada DEPARTMENT controla de 0 a N projetos -> (0, N). Cada PROJECT é '
                                     'controlado por exatamente 1 departamento -> (1, 1).'}]},
 'T3.1': {'title': 'Hierarquias EER: Disjunção (d vs. o), Completude (Total vs. Parcial) e Herança',
          'type': 'treino',
          'mode': 'structured',
          'setup': '',
          'fields': [{'id': 'q1',
                      'label': '1. Uma especialização de EMPLOYEE em {Secretary, Technician, Engineer} '
                               "possui um círculo com a letra 'd' ligado por linha simples a EMPLOYEE. O que "
                               'isso significa?',
                      'options': ['Disjunta e Total: todo empregado pertence obrigatoriamente a exatamente '
                                  'uma das três subclasses',
                                  'Sobreposta e Parcial: um empregado pode ser Técnico e Engenheiro '
                                  'simultaneamente ou nenhum deles',
                                  'Disjunta e Parcial: um empregado pertence a no máximo uma subclasse, '
                                  'podendo não pertencer a nenhuma',
                                  'Sobreposta e Total: todo empregado pertence a pelo menos uma subclasse, '
                                  'podendo acumular mais de uma'],
                      'answer': 'Disjunta e Parcial: um empregado pertence a no máximo uma subclasse, '
                                'podendo não pertencer a nenhuma',
                      'explanation': "'d' significa Disjunta (subclasses mutuamente exclusivas: interseção "
                                     'vazia). Linha simples ligando à superclasse significa Completude '
                                     'Parcial (um empregado pode não pertencer a nenhuma das três).'},
                     {'id': 'q2',
                      'label': '2. Uma peça (PART) pode ser Fabricada (MANUFACTURED_PART), Comprada '
                               '(PURCHASED_PART), ou AMBAS simultaneamente, e toda peça deve ser pelo menos '
                               'uma das duas. Qual a notação EER?',
                      'options': ["Círculo com 'o' (Sobreposta / Overlapping) e Linha Dupla (Total) ligando "
                                  'a PART',
                                  "Círculo com 'd' (Disjunta) e Linha Dupla (Total) ligando à superclasse "
                                  'PART',
                                  "Círculo com 'o' (Sobreposta / Overlapping) e Linha Simples (Parcial) "
                                  'ligando a PART',
                                  "Círculo com 'd' (Disjunta) e Linha Simples (Parcial) ligando à "
                                  'superclasse PART'],
                      'answer': "Círculo com 'o' (Sobreposta / Overlapping) e Linha Dupla (Total) ligando a "
                                'PART',
                      'explanation': "'o' (overlapping / sobreposta) permite que a mesma instância pertença "
                                     'a mais de uma subclasse. Linha dupla indica completude Total.'},
                     {'id': 'q3',
                      'label': '3. Sobre Herança de Tipo e Reticulados (Lattice) no modelo EER, se '
                               "'Engineering_Manager' é subclasse tanto de 'Engineer' quanto de 'Manager':",
                      'options': ['É proibido no modelo EER que uma subclasse possua mais de uma superclasse '
                                  'imediata',
                                  'Engineering_Manager herda os atributos específicos de Engineer, mas perde '
                                  'a chave de Employee',
                                  'Engineering_Manager torna-se uma entidade fraca com duas chaves parciais '
                                  'independentes',
                                  'É um Reticulado (herança múltipla) e herda atributos e relacionamentos de '
                                  'ambas as superclasses'],
                      'answer': 'É um Reticulado (herança múltipla) e herda atributos e relacionamentos de '
                                'ambas as superclasses',
                      'explanation': 'Slides 42-43 de ibd-parte2.pdf: Em uma Hierarquia (árvore), cada '
                                     'subclasse tem apenas uma superclasse; em um Lattice (reticulado), uma '
                                     'subclasse participa de mais de um relacionamento classe/subclasse '
                                     '(múltipla herança).'}]},
 'T3.2': {'title': 'Relacionamentos Ternários vs. Três Relacionamentos Binários',
          'type': 'treino',
          'mode': 'structured',
          'setup': '',
          'fields': [{'id': 'q1',
                      'label': '1. Considere o relacionamento ternário SUPPLIES(Supplier s, Part p, Project '
                               'j). Se o substituirmos por 3 relacionamentos binários M:N: CAN_SUPPLY(s, p), '
                               'USES(j, p) e SUPPLIES_TO(s, j):',
                      'options': ['As duas modelagens são 100% equivalentes e representam exatamente as '
                                  'mesmas instâncias ternárias',
                                  'NÃO são equivalentes, pois os 3 binários permitem ciclos falsos (junções '
                                  'espúrias) entre s, p e j',
                                  'Os 3 relacionamentos binários N:M têm mais poder expressivo que o '
                                  'relacionamento ternário original',
                                  'A decomposição em 3 binários só perde informação quando uma das entidades '
                                  'participantes é fraca'],
                      'answer': 'NÃO são equivalentes, pois os 3 binários permitem ciclos falsos (junções '
                                'espúrias) entre s, p e j',
                      'explanation': 'Slides 44-46 de ibd-parte2.pdf: Se s1 fornece p1 (para j2), j1 usa p1 '
                                     '(de s2) e s1 fornece p2 para j1, os 3 relacionamentos binários '
                                     'existem, mas s1 NUNCA forneceu p1 para j1!'},
                     {'id': 'q2',
                      'label': '2. Como podemos representar o ternário SUPPLIES(Supplier, Part, Project) '
                               'usando apenas relacionamentos binários SEM perder equivalência semântica?',
                      'options': ['Substituindo Supplier por um atributo multivalorado composto dentro da '
                                  'entidade forte Project',
                                  "Criando um Tipo de Entidade Fraca 'SUPPLY' identificada pelas 3 entidades "
                                  'via 3 relações N:1',
                                  'Mantendo apenas dois relacionamentos binários M:N e descartando o '
                                  'terceiro relacionamento',
                                  'Transformando Part e Project em subclasses disjuntas totais herdadas da '
                                  'superclasse Supplier'],
                      'answer': "Criando um Tipo de Entidade Fraca 'SUPPLY' identificada pelas 3 entidades "
                                'via 3 relações N:1',
                      'explanation': 'Slide 45 de ibd-parte2.pdf: Cada instância da entidade fraca SUPPLY '
                                     'materializa uma tripla (s, p, j) exata, ligada por 3 relacionamentos '
                                     'identificadores binários N:1 (SS, SP, SJ) às entidades donas.'}]},
 'T3.3': {'title': 'Modelagem usando UML: Multiplicidades, Agregação e Qualificadores',
          'type': 'treino',
          'mode': 'structured',
          'setup': '',
          'fields': [{'id': 'q1',
                      'label': '1. Em um Diagrama de Classes UML (slides 48-54 de ibd-parte2.pdf), na '
                               'associação Works_for entre Employee (4..* empregados) e Department (1..1 '
                               'departamento), onde ficam as multiplicidades?',
                      'options': ['`1..1` fica junto a Employee e `4..*` fica junto a Department (mesma '
                                  'posição do (min,max) no ER)',
                                  '`1..1` e `4..*` ficam escritos dentro do compartimento de atributos '
                                  'internos da classe Department',
                                  'Na notação de classes UML não se representam limites mínimos de '
                                  'participação, apenas asteriscos',
                                  '`1..1` fica junto a Department e `4..*` fica junto a Employee (ponta '
                                  'oposta ao (min,max) do ER)'],
                      'answer': '`1..1` fica junto a Department e `4..*` fica junto a Employee (ponta oposta '
                                'ao (min,max) do ER)',
                      'explanation': 'Slide 49 de ibd-parte2.pdf: Na UML, a multiplicidade fica na '
                                     'extremidade da classe destino (igual à posição do 1:N tradicional de '
                                     'Chen e oposta à posição do (min, max) do ER).'},
                     {'id': 'q2',
                      'label': '2. Como uma Entidade Fraca (ex: Dependent identificada por Employee + '
                               'Dependent_name) é representada em um Diagrama de Classes UML (slide 52 de '
                               'ibd-parte2.pdf)?',
                      'options': ["Por meio de uma Associação Qualificada (caixa 'Qualificador' com "
                                  '`Dependent_name` junto a `Employee`)',
                                  'Por meio de uma seta de generalização triangular vazada apontando da '
                                  'classe `Dependent` para `Employee`',
                                  'Por meio de um estereótipo textual `<<multivalued>>` declarado no '
                                  'compartimento de métodos de `Employee`',
                                  'Por meio de duas linhas tracejadas paralelas sem multiplicidade '
                                  'conectando `Employee` até `Dependent`'],
                      'answer': "Por meio de uma Associação Qualificada (caixa 'Qualificador' com "
                                '`Dependent_name` junto a `Employee`)',
                      'explanation': 'Slide 52 de ibd-parte2.pdf: O Qualificador UML (ex: `Dependent_name` '
                                     'na pequena caixa colada em `Employee`) atua exatamente como a chave '
                                     'parcial (discriminador) da entidade fraca.'},
                     {'id': 'q3',
                      'label': '3. No slide 51 de ibd-parte2.pdf (`Polygon 1 ◇--- 3..* Point`), o símbolo do '
                               'losango vazado na extremidade de Polygon representa:',
                      'options': ['Generalização / Herança entre superclasse e subclasse',
                                  'Relacionamento identificador de entidade fraca recursiva',
                                  'Agregação (associação todo-parte entre Polygon e Point)',
                                  'Dependência funcional transitiva entre atributos derivados'],
                      'answer': 'Agregação (associação todo-parte entre Polygon e Point)',
                      'explanation': 'O losango na extremidade da classe-todo em UML representa Agregação '
                                     '(todo-parte).'}]},
 'E3.1': {'title': '[Oficial ExercERRequisitos600.pdf] Estudo de Caso: Georgia Tech Library (GLT)',
          'type': 'oficial',
          'mode': 'structured',
          'setup': '',
          'fields': [{'id': 'q1',
                      'label': "1. Na Biblioteca GLT ('Dois livros com o mesmo título podem ter diferentes "
                               'ISBNs... a biblioteca possui em média 2,5 volumes por livro e precisa saber '
                               "quantas cópias estão disponíveis ou emprestadas'), qual a modelagem correta?",
                      'options': ['Modelar uma única entidade LIVRO com chave primária Título e atributo '
                                  'simples Quantidade_Copias',
                                  'Modelar ISBN como atributo multivalorado de SÓCIO e descartar os livros '
                                  'de referência do acervo',
                                  'Criar três atributos fixos Copia_1, Copia_2 e Copia_3 dentro da entidade '
                                  'única CATALOGO_GERAL',
                                  'Separar LIVRO/EDIÇÃO (chave ISBN, Título, Autores) de EXEMPLAR/VOLUME '
                                  '(cópia física emprestada)'],
                      'answer': 'Separar LIVRO/EDIÇÃO (chave ISBN, Título, Autores) de EXEMPLAR/VOLUME '
                                '(cópia física emprestada)',
                      'explanation': 'ISBN identifica o título/edição (`BOOK`), enquanto cada exemplar '
                                     'físico (`COPY`/`VOLUME`, entidade fraca ou forte associada a `BOOK`) '
                                     'representa o volume individual que é retirado pelo sócio.'},
                     {'id': 'q2',
                      'label': "2. Sobre os Sócios e Funcionários da GLT ('Docentes são automaticamente "
                               'sócios com prazo de 3 meses em vez de 21 dias; o pessoal da biblioteca '
                               'divide-se em bibliotecário-chefe, associados, referência, verificação e '
                               "assistentes'):",
                      'options': ['Docentes e Funcionários não podem ser representados no EER porque possuem '
                                  'regras de prazo distintas',
                                  'Modelam-se hierarquias EER de Especialização/Generalização para Sócios e '
                                  'para Pessoal da Biblioteca',
                                  'Todo Sócio deve ser obrigatoriamente um Bibliotecário de Referência em '
                                  'uma hierarquia total disjunta',
                                  'As diferentes funções da biblioteca devem ser modeladas como chaves '
                                  'parciais da entidade fraca LIVRO'],
                      'answer': 'Modelam-se hierarquias EER de Especialização/Generalização para Sócios e '
                                'para Pessoal da Biblioteca',
                      'explanation': 'O estudo de caso 4.20 exige explicitar as abstrações de '
                                     'generalização/especialização: Sócios (Comuns vs Docentes/Professores) '
                                     'e Funcionários da biblioteca em suas subcategorias.'},
                     {'id': 'q3',
                      'label': "3. O exercício 4.20 pede: 'Liste os detalhes que afetarão o projeto "
                               "eventual, mas que NÃO fazem parte do projeto conceitual (diagrama EER)'. "
                               'Quais itens do enunciado entram nessa lista?',
                      'options': ['Os atributos descritivos ISBN, Título, Autor, Assunto e Descrição do '
                                  'catálogo de livros do acervo',
                                  'Os dados cadastrais obrigatórios de Sócios: SSN, Endereço '
                                  'residencial/campus e Número de telefone',
                                  'Estatísticas quantitativas (16 mil sócios, 100 mil títulos, 10% '
                                  'emprestados) e rotinas de cobrança',
                                  'O relacionamento de empréstimo corrente associando os exemplares físicos '
                                  'do acervo aos sócios ativos'],
                      'answer': 'Estatísticas quantitativas (16 mil sócios, 100 mil títulos, 10% '
                                'emprestados) e rotinas de cobrança',
                      'explanation': 'Estatísticas de volume e frequência (16 mil sócios, 250 mil volumes, '
                                     '1% faz 15% dos empréstimos) são parâmetros de Projeto Físico, e '
                                     'prazos/notificações (21 dias, aviso 1 mês antes) são restrições '
                                     'semânticas/de aplicação.'},
                     {'id': 'q4',
                      'label': "4. 'Aos sócios é permitida a retirada de, no máximo, 5 livros por vez... "
                               "Cerca de 20% dos sócios são totalmente inativos'. Qual a restrição (min, "
                               'max) no relacionamento EMPRÉSTIMO_ATUAL?',
                      'options': ['(0, 5) ao lado de SÓCIO e (0, 1) ao lado de EXEMPLAR_FÍSICO',
                                  '(1, 5) ao lado de SÓCIO e (1, N) ao lado de EXEMPLAR_FÍSICO',
                                  '(5, 5) ao lado de SÓCIO e (0, N) ao lado de EXEMPLAR_FÍSICO',
                                  '(0, 1) ao lado de SÓCIO e (0, 5) ao lado de EXEMPLAR_FÍSICO'],
                      'answer': '(0, 5) ao lado de SÓCIO e (0, 1) ao lado de EXEMPLAR_FÍSICO',
                      'explanation': 'Um sócio pode ter de 0 (inativo) a 5 exemplares emprestados '
                                     'simultaneamente -> (0, 5). Cada exemplar físico específico está '
                                     'emprestado no momento para 0 (na estante) ou 1 sócio -> (0, 1).'}]},
 'T4.1': {'title': 'Superchave, Chave Candidata, Primária e Alternativa (exercicios_modelo_relacional.pdf '
                   'Q1-Q4)',
          'type': 'treino',
          'mode': 'structured',
          'setup': '',
          'fields': [{'id': 'q1',
                      'label': '1. Na relação `Funcionario(CPF, Nome, Cargo, Departamento, Salario)`, onde '
                               'apenas `CPF` é único, qual opção lista três Superchaves válidas, sendo '
                               'apenas a primeira uma Chave Candidata (mínima)?',
                      'options': ['{CPF},  {Nome, Cargo},  {Departamento, Salario}',
                                  '{CPF, Nome},  {CPF, Cargo},  {Nome, Departamento, Salario}',
                                  '{CPF},  {CPF, Nome},  {CPF, Nome, Cargo, Departamento, Salario}',
                                  '{Nome},  {Cargo, Departamento},  {CPF, Salario}'],
                      'answer': '{CPF},  {CPF, Nome},  {CPF, Nome, Cargo, Departamento, Salario}',
                      'explanation': 'Qualquer conjunto que contenha uma chave candidata (como {CPF, Nome} '
                                     'ou todos os atributos da relação) garante unicidade e portanto é '
                                     'Superchave. Já {CPF} é Superchave MÍNIMA (Chave Candidata).'},
                     {'id': 'q2',
                      'label': '2. Se `Aluno(Matricula, CPF, Nome, Curso, AnoIngresso)` possui duas chaves '
                               'candidatas (`{Matricula}` e `{CPF}`), e `Matricula` é escolhida como Chave '
                               'Primária (PK), o que `CPF` passa a ser?',
                      'options': ['Chave Alternativa (implementada em SQL via UNIQUE)',
                                  'Chave Estrangeira (implementada em SQL via FOREIGN KEY)',
                                  'Chave Parcial Discriminadora (implementada via CHECK)',
                                  'Superchave Composta Redundante (sem restrição no SQL)'],
                      'answer': 'Chave Alternativa (implementada em SQL via UNIQUE)',
                      'explanation': 'Slide 11 de ibd-parte3.pdf: Dentre as chaves candidatas de um esquema '
                                     'de relação, uma é escolhida como Chave Primária e as demais constituem '
                                     'as Chaves Alternativas (declaradas com UNIQUE no SQL).'},
                     {'id': 'q3',
                      'label': '3. Qual propriedade formal caracteriza uma Relação Matemática r(R) no modelo '
                               'relacional de Codd?',
                      'options': ['As tuplas possuem ordenação física fixa e permitem listas multivaloradas '
                                  'na mesma célula',
                                  'A relação exige que todas as colunas aceitem valores nulos, inclusive os '
                                  'atributos da chave primária',
                                  'A relação armazena ponteiros físicos diretos de disco em vez de chaves '
                                  'estrangeiras lógicas',
                                  'As tuplas não possuem ordem entre si, são distintas e todos os valores de '
                                  'atributos são atômicos'],
                      'answer': 'As tuplas não possuem ordem entre si, são distintas e todos os valores de '
                                'atributos são atômicos',
                      'explanation': 'Slides 7 e 8 de ibd-parte3.pdf: Uma relação é um conjunto de tuplas '
                                     '(sem ordem entre linhas, sem tuplas duplicadas) e cada valor deve ser '
                                     'atômico (1FN).'}]},
 'T4.2': {'title': 'Auditoria de Violações de Integridade e Atualizações (exercicios_modelo_relacional.pdf '
                   'Q8, Q11, Q12)',
          'type': 'treino',
          'mode': 'structured',
          'setup': '',
          'fields': [{'id': 'q1',
                      'label': '1. (Questão 8 da Lista) Dada `Produto(Codigo, Nome, Preco, '
                               "QuantidadeEstoque)` com: (101, 'Caneta', 2.50, 50), (102, 'Caderno', -5.00, "
                               "30), (103, 'Borracha', 1.00, NULL). Quais restrições foram violadas em 102 e "
                               '103?',
                      'options': ['102 viola a Integridade de Entidade (PK nula) e 103 viola a Restrição de '
                                  'Chave Candidata Única',
                                  '102 viola a Restrição de Domínio/Verificação (preço < 0) e 103 viola a '
                                  'Restrição de Não-Nulidade',
                                  '102 viola a Integridade Referencial (FK órfã) e 103 viola a Primeira '
                                  'Forma Normal (valor atômico)',
                                  '102 viola a Restrição de Chave Alternativa (UNIQUE) e 103 viola a '
                                  'Dependência Funcional Transitiva'],
                      'answer': '102 viola a Restrição de Domínio/Verificação (preço < 0) e 103 viola a '
                                'Restrição de Não-Nulidade',
                      'explanation': 'Preço negativo (-5.00) viola o domínio válido de preços (Restrição de '
                                     'Domínio / CHECK > 0), e QuantidadeEstoque = NULL viola a restrição de '
                                     'valores nulos (NOT NULL).'},
                     {'id': 'q2',
                      'label': '2. (Questão 11 da Lista) Na tabela `Cliente(CPF, Nome, Endereco, Telefone)` '
                               "onde `CPF` é a Chave Primária, tenta-se inserir `(NULL, 'Maria Souza', 'Rua "
                               "B', '99765-4321')`. Qual o diagnóstico?",
                      'options': ['Aceito normalmente, desde que exista no máximo uma tupla com CPF igual a '
                                  'NULL na tabela',
                                  'Rejeitado por violação da Restrição de Integridade de Entidade (PK nunca '
                                  'pode conter NULL)',
                                  'Rejeitado por violação da Restrição de Integridade Referencial na tabela '
                                  'pai Cliente',
                                  'Aceito pelo SGBD, que substitui automaticamente o NULL por uma chave '
                                  'parcial sequencial'],
                      'answer': 'Rejeitado por violação da Restrição de Integridade de Entidade (PK nunca '
                                'pode conter NULL)',
                      'explanation': 'Slide 15 de ibd-parte3.pdf: A Restrição de Integridade de Entidade '
                                     'estabelece que nenhum atributo que participe da Chave Primária (PK) '
                                     'pode assumir valor nulo.'},
                     {'id': 'q3',
                      'label': '3. Dentre as operações de atualização (`Insert`, `Delete`, `Modify` — slides '
                               '22-25 de ibd-parte3.pdf), qual é a ÚNICA restrição que uma operação `DELETE` '
                               'pode violar?',
                      'options': ['Restrição de Domínio (geração de valor fora do tipo de dado declarado na '
                                  'coluna)',
                                  'Restrição de Unicidade de Chave (criação de duas tuplas com a mesma chave '
                                  'primária)',
                                  'Restrição de Integridade de Entidade (atribuição de valor nulo à chave '
                                  'primária)',
                                  'Restrição de Integridade Referencial (tupla removida é referenciada em '
                                  'outra tabela)'],
                      'answer': 'Restrição de Integridade Referencial (tupla removida é referenciada em '
                                'outra tabela)',
                      'explanation': 'Slide 24 de ibd-parte3.pdf: Remover uma tupla jamais cria chave '
                                     'duplicada, valor fora de domínio ou PK nula. O único risco do DELETE é '
                                     'deixar chaves estrangeiras órfãs (Integridade Referencial).'}]},
 'E4.1': {'title': '[Oficial Lista Modelo Relacional Q5-Q10] Chaves Estrangeiras e Integridade Referencial',
          'type': 'oficial',
          'mode': 'structured',
          'setup': '',
          'fields': [{'id': 'q1',
                      'label': '1. (Questão 6 da Lista) Dadas `Pedido(NumPedido, Data, Valor, CPF_Cliente)` '
                               'e `Cliente(CPF, Nome, Endereco, Telefone)`, qual é a notação formal da '
                               'Restrição de Integridade Referencial (RIR)?',
                      'options': ['Pedido[CPF_Cliente] → Cliente[CPF]',
                                  'Cliente[CPF] → Pedido[CPF_Cliente]',
                                  'Pedido[NumPedido] → Cliente[CPF]',
                                  'Cliente[CPF_Cliente] → Pedido[NumPedido]'],
                      'answer': 'Pedido[CPF_Cliente] → Cliente[CPF]',
                      'explanation': 'Slide 18 de ibd-parte3.pdf: A notação é R1[FK] → R2[PK], onde R1 é a '
                                     'relação que contém a chave estrangeira (Pedido) e R2 é a relação '
                                     'referenciada que possui a chave primária (Cliente).'},
                     {'id': 'q2',
                      'label': '2. (Questão 10 da Lista) Dado o esquema `Paciente(ID_Paciente, Nome, '
                               'DataNasc)`, `Medico(CRM, Nome, Especialidade)` e `Consulta(ID_Consulta, '
                               'Data, ID_Paciente, CRM_Medico)`, quais são as RIRs?',
                      'options': ['Paciente[ID_Paciente] → Consulta[ID_Paciente]  e  Medico[CRM] → '
                                  'Consulta[CRM_Medico]',
                                  'Consulta[ID_Consulta] → Paciente[ID_Paciente]  e  Consulta[ID_Consulta] → '
                                  'Medico[CRM]',
                                  'Consulta[ID_Paciente] → Paciente[ID_Paciente]  e  Consulta[CRM_Medico] → '
                                  'Medico[CRM]',
                                  'Consulta[ID_Paciente] → Medico[CRM]  e  Consulta[CRM_Medico] → '
                                  'Paciente[ID_Paciente]'],
                      'answer': 'Consulta[ID_Paciente] → Paciente[ID_Paciente]  e  Consulta[CRM_Medico] → '
                                'Medico[CRM]',
                      'explanation': 'A tabela Consulta possui duas chaves estrangeiras (ID_Paciente e '
                                     'CRM_Medico), cada uma referenciando a chave primária da respectiva '
                                     'tabela pai.'},
                     {'id': 'q3',
                      'label': '3. Para uma RIR `R1[FK] → R2[PK]`, a definição formal de integridade '
                               'referencial exige que, para toda tupla t1 em R1:',
                      'options': ['t1[FK] seja obrigatoriamente diferente de qualquer valor t2[PK] presente '
                                  'em R2',
                                  't1[FK] nunca se repita em duas tuplas de R1, atuando sempre como chave '
                                  'primária de R1',
                                  't1[FK] nunca assuma o valor NULL, mesmo em relacionamentos de '
                                  'participação parcial',
                                  't1[FK] seja igual a t2[PK] para alguma tupla t2 em R2, ou t1[FK] seja '
                                  'NULL (se permitido)'],
                      'answer': 't1[FK] seja igual a t2[PK] para alguma tupla t2 em R2, ou t1[FK] seja NULL '
                                '(se permitido)',
                      'explanation': 'Slide 16 de ibd-parte3.pdf: Uma FK deve referenciar uma PK existente '
                                     'em R2 ou ser NULL (caso o relacionamento seja parcial/opcional e a FK '
                                     'não tenha restrição NOT NULL).'}]},
 'E4.2': {'title': '[Oficial Slides 03 & 05] Políticas de Remoção da RIR (b, p, n) no Esquema COMPANY',
          'type': 'oficial',
          'mode': 'structured',
          'setup': '',
          'fields': [{'id': 'q1',
                      'label': '1. Em `EMPLOYEE[SUPERSSN] → EMPLOYEE[SSN]` (auto-relacionamento de '
                               'supervisão onde SUPERSSN aceita nulo), qual a opção de remoção usada nos '
                               'slides quando um supervisor é removido?',
                      'options': ['p (propagação / ON DELETE CASCADE), removendo em cascata todos os seus '
                                  'subordinados',
                                  'n (substituição por nulos / ON DELETE SET NULL), deixando os subordinados '
                                  'com SUPERSSN = NULL',
                                  'b (bloqueio / RESTRICT), impedindo a demissão de qualquer empregado que '
                                  'seja supervisor',
                                  'd (descarte de restrição / DROP FOREIGN KEY), desativando a checagem '
                                  'referencial na tabela'],
                      'answer': 'n (substituição por nulos / ON DELETE SET NULL), deixando os subordinados '
                                'com SUPERSSN = NULL',
                      'explanation': 'Slide 20 de ibd-parte3.pdf: `EMPLOYEE[SUPERSSN] ->n EMPLOYEE[SSN]`. '
                                     'Como a supervisão é opcional (aceita NULL), remover o supervisor '
                                     'substitui a FK por NULL.'},
                     {'id': 'q2',
                      'label': '2. Em `DEPENDENT[ESSN] → EMPLOYEE[SSN]` (entidade fraca) e '
                               '`DEPT_LOCATIONS[DNUMBER] → DEPARTMENT[DNUMBER]` (atributo multivalorado), '
                               'qual a política de remoção usada nos slides?',
                      'options': ['b (bloqueio / RESTRICT) em ambos, exigindo remoção manual prévia de cada '
                                  'atributo',
                                  'n (substituição por nulos / ON DELETE SET NULL) em ambos, anulando parte '
                                  'da PK composta',
                                  'p (propagação / ON DELETE CASCADE) em ambos, pois não existem sem a '
                                  'entidade dona',
                                  'b (bloqueio) em DEPENDENT e n (substituição por nulos) em DEPT_LOCATIONS'],
                      'answer': 'p (propagação / ON DELETE CASCADE) em ambos, pois não existem sem a '
                                'entidade dona',
                      'explanation': 'Slides 20-21 de ibd-parte3.pdf e ibd-parte5.pdf: Entidades fracas '
                                     '(`DEPENDENT`), atributos multivalorados (`DEPT_LOCATIONS`), tabelas de '
                                     'relacionamento (`Participa-de`) e subclasses (`Gerente`/`Tecnico`) '
                                     'usam política `p` (propagação).'},
                     {'id': 'q3',
                      'label': '3. Nas referências funcionais obrigatórias `EMPLOYEE[DNO] → '
                               'DEPARTMENT[DNUMBER]`, `DEPARTMENT[MGRSSN] → EMPLOYEE[SSN]` e `PROJECT[DNUM] '
                               '→ DEPARTMENT[DNUMBER]`, qual a política adotada nos slides?',
                      'options': ['b (bloqueio / RESTRICT), impedindo a exclusão enquanto houver vínculos '
                                  'ativos referenciando-o',
                                  'p (propagação / ON DELETE CASCADE), apagando todos os empregados e '
                                  'projetos do departamento',
                                  'n (substituição por nulos / ON DELETE SET NULL), atribuindo NULL às '
                                  'colunas obrigatórias (nn)',
                                  'p (propagação em cascata) para PROJECT e n (substituição por nulos) para '
                                  'EMPLOYEE e DEPARTMENT'],
                      'answer': 'b (bloqueio / RESTRICT), impedindo a exclusão enquanto houver vínculos '
                                'ativos referenciando-o',
                      'explanation': 'Slide 20-21 de ibd-parte3.pdf e slide 11 de ibd-parte5.pdf: '
                                     'Relacionamentos funcionais obrigatórios (`DNO(nn)`, `MGRSSN(nn)`, '
                                     '`DNUM(nn)`) usam `b` (bloqueio) para impedir exclusões acidentais.'}]},
 'T5.1': {'title': 'Operação de Diferença (R − S): Empregados Sem Dependentes',
          'type': 'treino',
          'mode': 'sql_query',
          'setup': '\n'
                   'PRAGMA foreign_keys = ON;\n'
                   '\n'
                   'CREATE TABLE DEPARTMENT (\n'
                   '    DNAME VARCHAR(15) NOT NULL,\n'
                   '    DNUMBER INT NOT NULL,\n'
                   '    MGRSSN CHAR(9) NOT NULL,\n'
                   '    MGRSTARTDATE CHAR(10),\n'
                   '    PRIMARY KEY (DNUMBER),\n'
                   '    UNIQUE (DNAME)\n'
                   ');\n'
                   '\n'
                   'CREATE TABLE EMPLOYEE (\n'
                   '    FNAME VARCHAR(15) NOT NULL,\n'
                   '    MINIT CHAR(1),\n'
                   '    LNAME VARCHAR(15) NOT NULL,\n'
                   '    SSN CHAR(9) NOT NULL,\n'
                   '    BDATE CHAR(10),\n'
                   '    ADDRESS VARCHAR(40),\n'
                   '    SEX CHAR(1),\n'
                   '    SALARY DECIMAL(10,2),\n'
                   '    SUPERSSN CHAR(9),\n'
                   '    DNO INT NOT NULL,\n'
                   '    PRIMARY KEY (SSN),\n'
                   '    FOREIGN KEY (SUPERSSN) REFERENCES EMPLOYEE(SSN) ON DELETE SET NULL,\n'
                   '    FOREIGN KEY (DNO) REFERENCES DEPARTMENT(DNUMBER)\n'
                   ');\n'
                   '\n'
                   'CREATE TABLE DEPT_LOCATIONS (\n'
                   '    DNUMBER INT NOT NULL,\n'
                   '    DLOCATION VARCHAR(15) NOT NULL,\n'
                   '    PRIMARY KEY (DNUMBER, DLOCATION),\n'
                   '    FOREIGN KEY (DNUMBER) REFERENCES DEPARTMENT(DNUMBER) ON DELETE CASCADE\n'
                   ');\n'
                   '\n'
                   'CREATE TABLE PROJECT (\n'
                   '    PNAME VARCHAR(20) NOT NULL,\n'
                   '    PNUMBER INT NOT NULL,\n'
                   '    PLOCATION VARCHAR(15),\n'
                   '    DNUM INT NOT NULL,\n'
                   '    PRIMARY KEY (PNUMBER),\n'
                   '    UNIQUE (PNAME),\n'
                   '    FOREIGN KEY (DNUM) REFERENCES DEPARTMENT(DNUMBER)\n'
                   ');\n'
                   '\n'
                   'CREATE TABLE WORKS_ON (\n'
                   '    ESSN CHAR(9) NOT NULL,\n'
                   '    PNO INT NOT NULL,\n'
                   '    HOURS DECIMAL(4,1),\n'
                   '    PRIMARY KEY (ESSN, PNO),\n'
                   '    FOREIGN KEY (ESSN) REFERENCES EMPLOYEE(SSN),\n'
                   '    FOREIGN KEY (PNO) REFERENCES PROJECT(PNUMBER)\n'
                   ');\n'
                   '\n'
                   'CREATE TABLE DEPENDENT (\n'
                   '    ESSN CHAR(9) NOT NULL,\n'
                   '    DEPENDENT_NAME VARCHAR(15) NOT NULL,\n'
                   '    SEX CHAR(1),\n'
                   '    BDATE CHAR(10),\n'
                   '    RELATIONSHIP VARCHAR(12),\n'
                   '    PRIMARY KEY (ESSN, DEPENDENT_NAME),\n'
                   '    FOREIGN KEY (ESSN) REFERENCES EMPLOYEE(SSN) ON DELETE CASCADE\n'
                   ');\n'
                   '\n'
                   'INSERT INTO DEPARTMENT VALUES\n'
                   "('Research', 5, '333445555', '1988-05-22'),\n"
                   "('Administration', 4, '987654321', '1995-01-01'),\n"
                   "('Headquarters', 1, '888665555', '1981-06-19');\n"
                   '\n'
                   'INSERT INTO EMPLOYEE VALUES\n'
                   "('James', 'E', 'Borg', '888665555', '1937-11-10', '450 Stone, Houston, TX', 'M', "
                   '55000.00, NULL, 1),\n'
                   "('Franklin', 'T', 'Wong', '333445555', '1955-12-08', '638 Voss, Houston, TX', 'M', "
                   "40000.00, '888665555', 5),\n"
                   "('Jennifer', 'S', 'Wallace', '987654321', '1941-06-20', '291 Berry, Bellaire, TX', 'F', "
                   "43000.00, '888665555', 4),\n"
                   "('John', 'B', 'Smith', '123456789', '1965-01-09', '731 Fondren, Houston, TX', 'M', "
                   "30000.00, '333445555', 5),\n"
                   "('Ramesh', 'K', 'Narayan', '666884444', '1962-09-15', '975 Fire Oak, Humble, TX', 'M', "
                   "38000.00, '333445555', 5),\n"
                   "('Joyce', 'A', 'English', '453453453', '1972-07-31', '5631 Rice, Houston, TX', 'F', "
                   "25000.00, '333445555', 5),\n"
                   "('Alicia', 'J', 'Zelaya', '999887777', '1968-01-19', '3321 Castle, Spring, TX', 'F', "
                   "25000.00, '987654321', 4),\n"
                   "('Ahmad', 'V', 'Jabbar', '987987987', '1969-03-29', '980 Dallas, Houston, TX', 'M', "
                   "25000.00, '987654321', 4);\n"
                   '\n'
                   'INSERT INTO DEPT_LOCATIONS VALUES\n'
                   "(1, 'Houston'),\n"
                   "(4, 'Stafford'),\n"
                   "(5, 'Bellaire'),\n"
                   "(5, 'Sugarland'),\n"
                   "(5, 'Houston');\n"
                   '\n'
                   'INSERT INTO PROJECT VALUES\n'
                   "('ProductX', 1, 'Bellaire', 5),\n"
                   "('ProductY', 2, 'Sugarland', 5),\n"
                   "('ProductZ', 3, 'Houston', 5),\n"
                   "('Computerization', 10, 'Stafford', 4),\n"
                   "('Reorganization', 20, 'Houston', 1),\n"
                   "('Newbenefits', 30, 'Stafford', 4);\n"
                   '\n'
                   'INSERT INTO WORKS_ON VALUES\n'
                   "('123456789', 1, 32.5),\n"
                   "('123456789', 2, 7.5),\n"
                   "('666884444', 3, 40.0),\n"
                   "('453453453', 1, 20.0),\n"
                   "('453453453', 2, 20.0),\n"
                   "('333445555', 2, 10.0),\n"
                   "('333445555', 3, 10.0),\n"
                   "('333445555', 10, 10.0),\n"
                   "('333445555', 20, 10.0),\n"
                   "('999887777', 30, 30.0),\n"
                   "('999887777', 10, 10.0),\n"
                   "('987987987', 10, 35.0),\n"
                   "('987987987', 30, 5.0),\n"
                   "('987654321', 30, 20.0),\n"
                   "('987654321', 20, 15.0),\n"
                   "('888665555', 20, NULL);\n"
                   '\n'
                   'INSERT INTO DEPENDENT VALUES\n'
                   "('333445555', 'Alice', 'F', '1986-04-05', 'Daughter'),\n"
                   "('333445555', 'Theodore', 'M', '1983-10-25', 'Son'),\n"
                   "('333445555', 'Joy', 'F', '1958-05-03', 'Spouse'),\n"
                   "('987654321', 'Abner', 'M', '1942-02-28', 'Spouse'),\n"
                   "('123456789', 'Michael', 'M', '1988-01-04', 'Son'),\n"
                   "('123456789', 'Alice', 'F', '1988-12-30', 'Daughter'),\n"
                   "('123456789', 'Elizabeth', 'F', '1967-05-05', 'Spouse');\n",
          'expected_columns': ['LNAME', 'FNAME'],
          'expected_rows': [['Borg', 'James'],
                            ['Narayan', 'Ramesh'],
                            ['English', 'Joyce'],
                            ['Zelaya', 'Alicia'],
                            ['Jabbar', 'Ahmad']]},
 'T5.2': {'title': "Divisão Relacional (R ÷ S): Trabalham em Todos os Projetos de 'John Smith'",
          'type': 'treino',
          'mode': 'sql_query',
          'setup': '\n'
                   'PRAGMA foreign_keys = ON;\n'
                   '\n'
                   'CREATE TABLE DEPARTMENT (\n'
                   '    DNAME VARCHAR(15) NOT NULL,\n'
                   '    DNUMBER INT NOT NULL,\n'
                   '    MGRSSN CHAR(9) NOT NULL,\n'
                   '    MGRSTARTDATE CHAR(10),\n'
                   '    PRIMARY KEY (DNUMBER),\n'
                   '    UNIQUE (DNAME)\n'
                   ');\n'
                   '\n'
                   'CREATE TABLE EMPLOYEE (\n'
                   '    FNAME VARCHAR(15) NOT NULL,\n'
                   '    MINIT CHAR(1),\n'
                   '    LNAME VARCHAR(15) NOT NULL,\n'
                   '    SSN CHAR(9) NOT NULL,\n'
                   '    BDATE CHAR(10),\n'
                   '    ADDRESS VARCHAR(40),\n'
                   '    SEX CHAR(1),\n'
                   '    SALARY DECIMAL(10,2),\n'
                   '    SUPERSSN CHAR(9),\n'
                   '    DNO INT NOT NULL,\n'
                   '    PRIMARY KEY (SSN),\n'
                   '    FOREIGN KEY (SUPERSSN) REFERENCES EMPLOYEE(SSN) ON DELETE SET NULL,\n'
                   '    FOREIGN KEY (DNO) REFERENCES DEPARTMENT(DNUMBER)\n'
                   ');\n'
                   '\n'
                   'CREATE TABLE DEPT_LOCATIONS (\n'
                   '    DNUMBER INT NOT NULL,\n'
                   '    DLOCATION VARCHAR(15) NOT NULL,\n'
                   '    PRIMARY KEY (DNUMBER, DLOCATION),\n'
                   '    FOREIGN KEY (DNUMBER) REFERENCES DEPARTMENT(DNUMBER) ON DELETE CASCADE\n'
                   ');\n'
                   '\n'
                   'CREATE TABLE PROJECT (\n'
                   '    PNAME VARCHAR(20) NOT NULL,\n'
                   '    PNUMBER INT NOT NULL,\n'
                   '    PLOCATION VARCHAR(15),\n'
                   '    DNUM INT NOT NULL,\n'
                   '    PRIMARY KEY (PNUMBER),\n'
                   '    UNIQUE (PNAME),\n'
                   '    FOREIGN KEY (DNUM) REFERENCES DEPARTMENT(DNUMBER)\n'
                   ');\n'
                   '\n'
                   'CREATE TABLE WORKS_ON (\n'
                   '    ESSN CHAR(9) NOT NULL,\n'
                   '    PNO INT NOT NULL,\n'
                   '    HOURS DECIMAL(4,1),\n'
                   '    PRIMARY KEY (ESSN, PNO),\n'
                   '    FOREIGN KEY (ESSN) REFERENCES EMPLOYEE(SSN),\n'
                   '    FOREIGN KEY (PNO) REFERENCES PROJECT(PNUMBER)\n'
                   ');\n'
                   '\n'
                   'CREATE TABLE DEPENDENT (\n'
                   '    ESSN CHAR(9) NOT NULL,\n'
                   '    DEPENDENT_NAME VARCHAR(15) NOT NULL,\n'
                   '    SEX CHAR(1),\n'
                   '    BDATE CHAR(10),\n'
                   '    RELATIONSHIP VARCHAR(12),\n'
                   '    PRIMARY KEY (ESSN, DEPENDENT_NAME),\n'
                   '    FOREIGN KEY (ESSN) REFERENCES EMPLOYEE(SSN) ON DELETE CASCADE\n'
                   ');\n'
                   '\n'
                   'INSERT INTO DEPARTMENT VALUES\n'
                   "('Research', 5, '333445555', '1988-05-22'),\n"
                   "('Administration', 4, '987654321', '1995-01-01'),\n"
                   "('Headquarters', 1, '888665555', '1981-06-19');\n"
                   '\n'
                   'INSERT INTO EMPLOYEE VALUES\n'
                   "('James', 'E', 'Borg', '888665555', '1937-11-10', '450 Stone, Houston, TX', 'M', "
                   '55000.00, NULL, 1),\n'
                   "('Franklin', 'T', 'Wong', '333445555', '1955-12-08', '638 Voss, Houston, TX', 'M', "
                   "40000.00, '888665555', 5),\n"
                   "('Jennifer', 'S', 'Wallace', '987654321', '1941-06-20', '291 Berry, Bellaire, TX', 'F', "
                   "43000.00, '888665555', 4),\n"
                   "('John', 'B', 'Smith', '123456789', '1965-01-09', '731 Fondren, Houston, TX', 'M', "
                   "30000.00, '333445555', 5),\n"
                   "('Ramesh', 'K', 'Narayan', '666884444', '1962-09-15', '975 Fire Oak, Humble, TX', 'M', "
                   "38000.00, '333445555', 5),\n"
                   "('Joyce', 'A', 'English', '453453453', '1972-07-31', '5631 Rice, Houston, TX', 'F', "
                   "25000.00, '333445555', 5),\n"
                   "('Alicia', 'J', 'Zelaya', '999887777', '1968-01-19', '3321 Castle, Spring, TX', 'F', "
                   "25000.00, '987654321', 4),\n"
                   "('Ahmad', 'V', 'Jabbar', '987987987', '1969-03-29', '980 Dallas, Houston, TX', 'M', "
                   "25000.00, '987654321', 4);\n"
                   '\n'
                   'INSERT INTO DEPT_LOCATIONS VALUES\n'
                   "(1, 'Houston'),\n"
                   "(4, 'Stafford'),\n"
                   "(5, 'Bellaire'),\n"
                   "(5, 'Sugarland'),\n"
                   "(5, 'Houston');\n"
                   '\n'
                   'INSERT INTO PROJECT VALUES\n'
                   "('ProductX', 1, 'Bellaire', 5),\n"
                   "('ProductY', 2, 'Sugarland', 5),\n"
                   "('ProductZ', 3, 'Houston', 5),\n"
                   "('Computerization', 10, 'Stafford', 4),\n"
                   "('Reorganization', 20, 'Houston', 1),\n"
                   "('Newbenefits', 30, 'Stafford', 4);\n"
                   '\n'
                   'INSERT INTO WORKS_ON VALUES\n'
                   "('123456789', 1, 32.5),\n"
                   "('123456789', 2, 7.5),\n"
                   "('666884444', 3, 40.0),\n"
                   "('453453453', 1, 20.0),\n"
                   "('453453453', 2, 20.0),\n"
                   "('333445555', 2, 10.0),\n"
                   "('333445555', 3, 10.0),\n"
                   "('333445555', 10, 10.0),\n"
                   "('333445555', 20, 10.0),\n"
                   "('999887777', 30, 30.0),\n"
                   "('999887777', 10, 10.0),\n"
                   "('987987987', 10, 35.0),\n"
                   "('987987987', 30, 5.0),\n"
                   "('987654321', 30, 20.0),\n"
                   "('987654321', 20, 15.0),\n"
                   "('888665555', 20, NULL);\n"
                   '\n'
                   'INSERT INTO DEPENDENT VALUES\n'
                   "('333445555', 'Alice', 'F', '1986-04-05', 'Daughter'),\n"
                   "('333445555', 'Theodore', 'M', '1983-10-25', 'Son'),\n"
                   "('333445555', 'Joy', 'F', '1958-05-03', 'Spouse'),\n"
                   "('987654321', 'Abner', 'M', '1942-02-28', 'Spouse'),\n"
                   "('123456789', 'Michael', 'M', '1988-01-04', 'Son'),\n"
                   "('123456789', 'Alice', 'F', '1988-12-30', 'Daughter'),\n"
                   "('123456789', 'Elizabeth', 'F', '1967-05-05', 'Spouse');\n",
          'expected_columns': ['FNAME', 'LNAME'],
          'expected_rows': [['John', 'Smith'], ['Joyce', 'English']]},
 'T5.3': {'title': 'Restrições Estruturais em Álgebra Relacional (Ponte para Projeto Lógico)',
          'type': 'treino',
          'mode': 'structured',
          'setup': '',
          'fields': [{'id': 'q1',
                      'label': '1. No mapeamento 1-1 de um relacionamento com Participação Total de '
                               'Empregado em Trabalha-para (`Empregado(NEmp, ...)` e `Trabalha-para(NEmp, '
                               'NDept)`), como expressamos a totalidade em Álgebra Relacional (slide 19 de '
                               'ibd-parte5.pdf)?',
                      'options': ['π_{NEmp}(Empregado) ∩ π_{NEmp}(Trabalha-para) = ∅',
                                  'π_{NDept}(Empregado) ∪ π_{NEmp}(Trabalha-para) = ∅',
                                  'π_{NEmp}(Empregado) = π_{NEmp}(Trabalha-para)',
                                  'σ_{NEmp = nulo}(Empregado) = π_{NEmp}(Trabalha-para)'],
                      'answer': 'π_{NEmp}(Empregado) = π_{NEmp}(Trabalha-para)',
                      'explanation': 'Slide 19 de ibd-parte5.pdf: A projeção da chave primária em Empregado '
                                     'deve ser igual à projeção da chave estrangeira em Trabalha-para: '
                                     '`π_{NEmp}(Empregado) = π_{NEmp}(Trabalha-para)`.'},
                     {'id': 'q2',
                      'label': '2. Em uma hierarquia Disjunta e Total de `Empregado` em `Gerente(NEmp, '
                               'SalAd)` e `Tecnico(NEmp, Formacao)` (mapeamento 1-1 em tabelas separadas, '
                               "slide 24 de ibd-parte5.pdf), quais equações garantem Disjunção ('d') e "
                               'Totalidade?',
                      'options': ['Disjunção: π_{NEmp}(Gerente) ∩ π_{NEmp}(Tecnico) = ∅   |   Totalidade: '
                                  'π_{NEmp}(Gerente) ∪ π_{NEmp}(Tecnico) = π_{NEmp}(Empregado)',
                                  'Disjunção: π_{NEmp}(Gerente) ∪ π_{NEmp}(Tecnico) = ∅   |   Totalidade: '
                                  'π_{NEmp}(Gerente) - π_{NEmp}(Tecnico) = π_{NEmp}(Empregado)',
                                  'Disjunção: π_{NEmp}(Gerente) = π_{NEmp}(Tecnico)   |   Totalidade: '
                                  'π_{NEmp}(Gerente) ∩ π_{NEmp}(Tecnico) = π_{NEmp}(Empregado)',
                                  'Disjunção: π_{NEmp}(Gerente) ÷ π_{NEmp}(Tecnico) = ∅   |   Totalidade: '
                                  'π_{NEmp}(Gerente) × π_{NEmp}(Tecnico) = π_{NEmp}(Empregado)'],
                      'answer': 'Disjunção: π_{NEmp}(Gerente) ∩ π_{NEmp}(Tecnico) = ∅   |   Totalidade: '
                                'π_{NEmp}(Gerente) ∪ π_{NEmp}(Tecnico) = π_{NEmp}(Empregado)',
                      'explanation': 'Slide 24 de ibd-parte5.pdf: A interseção (∩) dos NEmp de Gerente e '
                                     'Tecnico deve ser vazia (∅) para garantir disjunção, e a união (∪) deve '
                                     'ser igual a todos os NEmp de Empregado para garantir completude '
                                     'total.'},
                     {'id': 'q3',
                      'label': '3. Quando a mesma hierarquia Disjunta e Total é colapsada em uma ÚNICA '
                               'tabela `Empregado(NEmp, Nome, Salario, SalAd, Formacao)` (mapeamento '
                               'otimizado, slide 25 de ibd-parte5.pdf), como ficam as duas equações em '
                               'Álgebra Relacional?',
                      'options': ['π_{NEmp}(σ_{SalAd = nulo}(Empregado)) ∩ π_{NEmp}(σ_{Formacao = '
                                  'nulo}(Empregado)) = ∅  e  π_{NEmp}(σ_{SalAd = nulo}(Empregado)) ∪ '
                                  'π_{NEmp}(σ_{Formacao = nulo}(Empregado)) = π_{NEmp}(Empregado)',
                                  'π_{NEmp}(σ_{SalAd ≠ nulo}(Empregado)) ∪ π_{NEmp}(σ_{Formacao ≠ '
                                  'nulo}(Empregado)) = ∅  e  π_{NEmp}(σ_{SalAd ≠ nulo}(Empregado)) - '
                                  'π_{NEmp}(σ_{Formacao ≠ nulo}(Empregado)) = π_{NEmp}(Empregado)',
                                  'π_{NEmp}(σ_{SalAd ≠ nulo}(Empregado)) - π_{NEmp}(σ_{Formacao ≠ '
                                  'nulo}(Empregado)) = ∅  e  π_{NEmp}(σ_{SalAd ≠ nulo}(Empregado)) ∩ '
                                  'π_{NEmp}(σ_{Formacao ≠ nulo}(Empregado)) = π_{NEmp}(Empregado)',
                                  'π_{NEmp}(σ_{SalAd ≠ nulo}(Empregado)) ∩ π_{NEmp}(σ_{Formacao ≠ '
                                  'nulo}(Empregado)) = ∅  e  π_{NEmp}(σ_{SalAd ≠ nulo}(Empregado)) ∪ '
                                  'π_{NEmp}(σ_{Formacao ≠ nulo}(Empregado)) = π_{NEmp}(Empregado)'],
                      'answer': 'π_{NEmp}(σ_{SalAd ≠ nulo}(Empregado)) ∩ π_{NEmp}(σ_{Formacao ≠ '
                                'nulo}(Empregado)) = ∅  e  π_{NEmp}(σ_{SalAd ≠ nulo}(Empregado)) ∪ '
                                'π_{NEmp}(σ_{Formacao ≠ nulo}(Empregado)) = π_{NEmp}(Empregado)',
                      'explanation': 'Slide 25 de ibd-parte5.pdf: Na tabela única, identificamos os gerentes '
                                     'filtrando `σ_{SalAd ≠ nulo}(Empregado)` e os técnicos filtrando '
                                     '`σ_{Formacao ≠ nulo}(Empregado)`, aplicando a interseção vazia (= ∅) e '
                                     'a união total (= π_{NEmp}(Empregado)).'}]},
 'E5.1': {'title': '[Oficial consultas_ProfMarcosG.pdf (d)] Empregados que Trabalham em TODOS os Projetos',
          'type': 'oficial',
          'mode': 'sql_query',
          'setup': '\n'
                   'PRAGMA foreign_keys = ON;\n'
                   '\n'
                   'CREATE TABLE DEPARTMENT (\n'
                   '    DNAME VARCHAR(15) NOT NULL,\n'
                   '    DNUMBER INT NOT NULL,\n'
                   '    MGRSSN CHAR(9) NOT NULL,\n'
                   '    MGRSTARTDATE CHAR(10),\n'
                   '    PRIMARY KEY (DNUMBER),\n'
                   '    UNIQUE (DNAME)\n'
                   ');\n'
                   '\n'
                   'CREATE TABLE EMPLOYEE (\n'
                   '    FNAME VARCHAR(15) NOT NULL,\n'
                   '    MINIT CHAR(1),\n'
                   '    LNAME VARCHAR(15) NOT NULL,\n'
                   '    SSN CHAR(9) NOT NULL,\n'
                   '    BDATE CHAR(10),\n'
                   '    ADDRESS VARCHAR(40),\n'
                   '    SEX CHAR(1),\n'
                   '    SALARY DECIMAL(10,2),\n'
                   '    SUPERSSN CHAR(9),\n'
                   '    DNO INT NOT NULL,\n'
                   '    PRIMARY KEY (SSN),\n'
                   '    FOREIGN KEY (SUPERSSN) REFERENCES EMPLOYEE(SSN) ON DELETE SET NULL,\n'
                   '    FOREIGN KEY (DNO) REFERENCES DEPARTMENT(DNUMBER)\n'
                   ');\n'
                   '\n'
                   'CREATE TABLE DEPT_LOCATIONS (\n'
                   '    DNUMBER INT NOT NULL,\n'
                   '    DLOCATION VARCHAR(15) NOT NULL,\n'
                   '    PRIMARY KEY (DNUMBER, DLOCATION),\n'
                   '    FOREIGN KEY (DNUMBER) REFERENCES DEPARTMENT(DNUMBER) ON DELETE CASCADE\n'
                   ');\n'
                   '\n'
                   'CREATE TABLE PROJECT (\n'
                   '    PNAME VARCHAR(20) NOT NULL,\n'
                   '    PNUMBER INT NOT NULL,\n'
                   '    PLOCATION VARCHAR(15),\n'
                   '    DNUM INT NOT NULL,\n'
                   '    PRIMARY KEY (PNUMBER),\n'
                   '    UNIQUE (PNAME),\n'
                   '    FOREIGN KEY (DNUM) REFERENCES DEPARTMENT(DNUMBER)\n'
                   ');\n'
                   '\n'
                   'CREATE TABLE WORKS_ON (\n'
                   '    ESSN CHAR(9) NOT NULL,\n'
                   '    PNO INT NOT NULL,\n'
                   '    HOURS DECIMAL(4,1),\n'
                   '    PRIMARY KEY (ESSN, PNO),\n'
                   '    FOREIGN KEY (ESSN) REFERENCES EMPLOYEE(SSN),\n'
                   '    FOREIGN KEY (PNO) REFERENCES PROJECT(PNUMBER)\n'
                   ');\n'
                   '\n'
                   'CREATE TABLE DEPENDENT (\n'
                   '    ESSN CHAR(9) NOT NULL,\n'
                   '    DEPENDENT_NAME VARCHAR(15) NOT NULL,\n'
                   '    SEX CHAR(1),\n'
                   '    BDATE CHAR(10),\n'
                   '    RELATIONSHIP VARCHAR(12),\n'
                   '    PRIMARY KEY (ESSN, DEPENDENT_NAME),\n'
                   '    FOREIGN KEY (ESSN) REFERENCES EMPLOYEE(SSN) ON DELETE CASCADE\n'
                   ');\n'
                   '\n'
                   'INSERT INTO DEPARTMENT VALUES\n'
                   "('Research', 5, '333445555', '1988-05-22'),\n"
                   "('Administration', 4, '987654321', '1995-01-01'),\n"
                   "('Headquarters', 1, '888665555', '1981-06-19');\n"
                   '\n'
                   'INSERT INTO EMPLOYEE VALUES\n'
                   "('James', 'E', 'Borg', '888665555', '1937-11-10', '450 Stone, Houston, TX', 'M', "
                   '55000.00, NULL, 1),\n'
                   "('Franklin', 'T', 'Wong', '333445555', '1955-12-08', '638 Voss, Houston, TX', 'M', "
                   "40000.00, '888665555', 5),\n"
                   "('Jennifer', 'S', 'Wallace', '987654321', '1941-06-20', '291 Berry, Bellaire, TX', 'F', "
                   "43000.00, '888665555', 4),\n"
                   "('John', 'B', 'Smith', '123456789', '1965-01-09', '731 Fondren, Houston, TX', 'M', "
                   "30000.00, '333445555', 5),\n"
                   "('Ramesh', 'K', 'Narayan', '666884444', '1962-09-15', '975 Fire Oak, Humble, TX', 'M', "
                   "38000.00, '333445555', 5),\n"
                   "('Joyce', 'A', 'English', '453453453', '1972-07-31', '5631 Rice, Houston, TX', 'F', "
                   "25000.00, '333445555', 5),\n"
                   "('Alicia', 'J', 'Zelaya', '999887777', '1968-01-19', '3321 Castle, Spring, TX', 'F', "
                   "25000.00, '987654321', 4),\n"
                   "('Ahmad', 'V', 'Jabbar', '987987987', '1969-03-29', '980 Dallas, Houston, TX', 'M', "
                   "25000.00, '987654321', 4);\n"
                   '\n'
                   'INSERT INTO DEPT_LOCATIONS VALUES\n'
                   "(1, 'Houston'),\n"
                   "(4, 'Stafford'),\n"
                   "(5, 'Bellaire'),\n"
                   "(5, 'Sugarland'),\n"
                   "(5, 'Houston');\n"
                   '\n'
                   'INSERT INTO PROJECT VALUES\n'
                   "('ProductX', 1, 'Bellaire', 5),\n"
                   "('ProductY', 2, 'Sugarland', 5),\n"
                   "('ProductZ', 3, 'Houston', 5),\n"
                   "('Computerization', 10, 'Stafford', 4),\n"
                   "('Reorganization', 20, 'Houston', 1),\n"
                   "('Newbenefits', 30, 'Stafford', 4);\n"
                   '\n'
                   'INSERT INTO WORKS_ON VALUES\n'
                   "('123456789', 1, 32.5),\n"
                   "('123456789', 2, 7.5),\n"
                   "('666884444', 3, 40.0),\n"
                   "('453453453', 1, 20.0),\n"
                   "('453453453', 2, 20.0),\n"
                   "('333445555', 2, 10.0),\n"
                   "('333445555', 3, 10.0),\n"
                   "('333445555', 10, 10.0),\n"
                   "('333445555', 20, 10.0),\n"
                   "('999887777', 30, 30.0),\n"
                   "('999887777', 10, 10.0),\n"
                   "('987987987', 10, 35.0),\n"
                   "('987987987', 30, 5.0),\n"
                   "('987654321', 30, 20.0),\n"
                   "('987654321', 20, 15.0),\n"
                   "('888665555', 20, NULL);\n"
                   '\n'
                   'INSERT INTO DEPENDENT VALUES\n'
                   "('333445555', 'Alice', 'F', '1986-04-05', 'Daughter'),\n"
                   "('333445555', 'Theodore', 'M', '1983-10-25', 'Son'),\n"
                   "('333445555', 'Joy', 'F', '1958-05-03', 'Spouse'),\n"
                   "('987654321', 'Abner', 'M', '1942-02-28', 'Spouse'),\n"
                   "('123456789', 'Michael', 'M', '1988-01-04', 'Son'),\n"
                   "('123456789', 'Alice', 'F', '1988-12-30', 'Daughter'),\n"
                   "('123456789', 'Elizabeth', 'F', '1967-05-05', 'Spouse');\n"
                   '\n'
                   '-- Adições específicas para que todas as consultas de consultas_ProfMarcosG.pdf retornem '
                   'linhas ricas:\n'
                   '-- 1) Empregado com mesmo primeiro nome do dependente (John Smith -> dependente John)\n'
                   "INSERT INTO DEPENDENT VALUES ('123456789', 'John', 'M', '1995-06-12', 'Son');\n"
                   "-- 2) Ramesh Narayan ('666884444') trabalha em TODOS os projetos do departamento 5 (1, "
                   '2, 3)\n'
                   "INSERT INTO WORKS_ON VALUES ('666884444', 1, 10.0);\n"
                   "INSERT INTO WORKS_ON VALUES ('666884444', 2, 10.0);\n"
                   "-- 3) Franklin Wong ('333445555') trabalha em TODOS os 6 projetos da empresa (já tem "
                   '2,3,10,20; adicionamos 1 e 30)\n'
                   "INSERT INTO WORKS_ON VALUES ('333445555', 1, 5.0);\n"
                   "INSERT INTO WORKS_ON VALUES ('333445555', 30, 5.0);\n"
                   "-- 4) Empregado sem nenhum projeto: Carla Mendes ('111222333')\n"
                   'INSERT INTO EMPLOYEE VALUES\n'
                   "('Carla', 'M', 'Mendes', '111222333', '1975-04-12', '100 Main, Houston, TX', 'F', "
                   "28000.00, '333445555', 5);\n",
          'expected_columns': ['FNAME', 'LNAME'],
          'expected_rows': [['Franklin', 'Wong']]},
 'E5.2': {'title': '[Oficial consultas_ProfMarcosG.pdf (e, f)] Gerentes de Departamento Sem Dependentes',
          'type': 'oficial',
          'mode': 'sql_query',
          'setup': '\n'
                   'PRAGMA foreign_keys = ON;\n'
                   '\n'
                   'CREATE TABLE DEPARTMENT (\n'
                   '    DNAME VARCHAR(15) NOT NULL,\n'
                   '    DNUMBER INT NOT NULL,\n'
                   '    MGRSSN CHAR(9) NOT NULL,\n'
                   '    MGRSTARTDATE CHAR(10),\n'
                   '    PRIMARY KEY (DNUMBER),\n'
                   '    UNIQUE (DNAME)\n'
                   ');\n'
                   '\n'
                   'CREATE TABLE EMPLOYEE (\n'
                   '    FNAME VARCHAR(15) NOT NULL,\n'
                   '    MINIT CHAR(1),\n'
                   '    LNAME VARCHAR(15) NOT NULL,\n'
                   '    SSN CHAR(9) NOT NULL,\n'
                   '    BDATE CHAR(10),\n'
                   '    ADDRESS VARCHAR(40),\n'
                   '    SEX CHAR(1),\n'
                   '    SALARY DECIMAL(10,2),\n'
                   '    SUPERSSN CHAR(9),\n'
                   '    DNO INT NOT NULL,\n'
                   '    PRIMARY KEY (SSN),\n'
                   '    FOREIGN KEY (SUPERSSN) REFERENCES EMPLOYEE(SSN) ON DELETE SET NULL,\n'
                   '    FOREIGN KEY (DNO) REFERENCES DEPARTMENT(DNUMBER)\n'
                   ');\n'
                   '\n'
                   'CREATE TABLE DEPT_LOCATIONS (\n'
                   '    DNUMBER INT NOT NULL,\n'
                   '    DLOCATION VARCHAR(15) NOT NULL,\n'
                   '    PRIMARY KEY (DNUMBER, DLOCATION),\n'
                   '    FOREIGN KEY (DNUMBER) REFERENCES DEPARTMENT(DNUMBER) ON DELETE CASCADE\n'
                   ');\n'
                   '\n'
                   'CREATE TABLE PROJECT (\n'
                   '    PNAME VARCHAR(20) NOT NULL,\n'
                   '    PNUMBER INT NOT NULL,\n'
                   '    PLOCATION VARCHAR(15),\n'
                   '    DNUM INT NOT NULL,\n'
                   '    PRIMARY KEY (PNUMBER),\n'
                   '    UNIQUE (PNAME),\n'
                   '    FOREIGN KEY (DNUM) REFERENCES DEPARTMENT(DNUMBER)\n'
                   ');\n'
                   '\n'
                   'CREATE TABLE WORKS_ON (\n'
                   '    ESSN CHAR(9) NOT NULL,\n'
                   '    PNO INT NOT NULL,\n'
                   '    HOURS DECIMAL(4,1),\n'
                   '    PRIMARY KEY (ESSN, PNO),\n'
                   '    FOREIGN KEY (ESSN) REFERENCES EMPLOYEE(SSN),\n'
                   '    FOREIGN KEY (PNO) REFERENCES PROJECT(PNUMBER)\n'
                   ');\n'
                   '\n'
                   'CREATE TABLE DEPENDENT (\n'
                   '    ESSN CHAR(9) NOT NULL,\n'
                   '    DEPENDENT_NAME VARCHAR(15) NOT NULL,\n'
                   '    SEX CHAR(1),\n'
                   '    BDATE CHAR(10),\n'
                   '    RELATIONSHIP VARCHAR(12),\n'
                   '    PRIMARY KEY (ESSN, DEPENDENT_NAME),\n'
                   '    FOREIGN KEY (ESSN) REFERENCES EMPLOYEE(SSN) ON DELETE CASCADE\n'
                   ');\n'
                   '\n'
                   'INSERT INTO DEPARTMENT VALUES\n'
                   "('Research', 5, '333445555', '1988-05-22'),\n"
                   "('Administration', 4, '987654321', '1995-01-01'),\n"
                   "('Headquarters', 1, '888665555', '1981-06-19');\n"
                   '\n'
                   'INSERT INTO EMPLOYEE VALUES\n'
                   "('James', 'E', 'Borg', '888665555', '1937-11-10', '450 Stone, Houston, TX', 'M', "
                   '55000.00, NULL, 1),\n'
                   "('Franklin', 'T', 'Wong', '333445555', '1955-12-08', '638 Voss, Houston, TX', 'M', "
                   "40000.00, '888665555', 5),\n"
                   "('Jennifer', 'S', 'Wallace', '987654321', '1941-06-20', '291 Berry, Bellaire, TX', 'F', "
                   "43000.00, '888665555', 4),\n"
                   "('John', 'B', 'Smith', '123456789', '1965-01-09', '731 Fondren, Houston, TX', 'M', "
                   "30000.00, '333445555', 5),\n"
                   "('Ramesh', 'K', 'Narayan', '666884444', '1962-09-15', '975 Fire Oak, Humble, TX', 'M', "
                   "38000.00, '333445555', 5),\n"
                   "('Joyce', 'A', 'English', '453453453', '1972-07-31', '5631 Rice, Houston, TX', 'F', "
                   "25000.00, '333445555', 5),\n"
                   "('Alicia', 'J', 'Zelaya', '999887777', '1968-01-19', '3321 Castle, Spring, TX', 'F', "
                   "25000.00, '987654321', 4),\n"
                   "('Ahmad', 'V', 'Jabbar', '987987987', '1969-03-29', '980 Dallas, Houston, TX', 'M', "
                   "25000.00, '987654321', 4);\n"
                   '\n'
                   'INSERT INTO DEPT_LOCATIONS VALUES\n'
                   "(1, 'Houston'),\n"
                   "(4, 'Stafford'),\n"
                   "(5, 'Bellaire'),\n"
                   "(5, 'Sugarland'),\n"
                   "(5, 'Houston');\n"
                   '\n'
                   'INSERT INTO PROJECT VALUES\n'
                   "('ProductX', 1, 'Bellaire', 5),\n"
                   "('ProductY', 2, 'Sugarland', 5),\n"
                   "('ProductZ', 3, 'Houston', 5),\n"
                   "('Computerization', 10, 'Stafford', 4),\n"
                   "('Reorganization', 20, 'Houston', 1),\n"
                   "('Newbenefits', 30, 'Stafford', 4);\n"
                   '\n'
                   'INSERT INTO WORKS_ON VALUES\n'
                   "('123456789', 1, 32.5),\n"
                   "('123456789', 2, 7.5),\n"
                   "('666884444', 3, 40.0),\n"
                   "('453453453', 1, 20.0),\n"
                   "('453453453', 2, 20.0),\n"
                   "('333445555', 2, 10.0),\n"
                   "('333445555', 3, 10.0),\n"
                   "('333445555', 10, 10.0),\n"
                   "('333445555', 20, 10.0),\n"
                   "('999887777', 30, 30.0),\n"
                   "('999887777', 10, 10.0),\n"
                   "('987987987', 10, 35.0),\n"
                   "('987987987', 30, 5.0),\n"
                   "('987654321', 30, 20.0),\n"
                   "('987654321', 20, 15.0),\n"
                   "('888665555', 20, NULL);\n"
                   '\n'
                   'INSERT INTO DEPENDENT VALUES\n'
                   "('333445555', 'Alice', 'F', '1986-04-05', 'Daughter'),\n"
                   "('333445555', 'Theodore', 'M', '1983-10-25', 'Son'),\n"
                   "('333445555', 'Joy', 'F', '1958-05-03', 'Spouse'),\n"
                   "('987654321', 'Abner', 'M', '1942-02-28', 'Spouse'),\n"
                   "('123456789', 'Michael', 'M', '1988-01-04', 'Son'),\n"
                   "('123456789', 'Alice', 'F', '1988-12-30', 'Daughter'),\n"
                   "('123456789', 'Elizabeth', 'F', '1967-05-05', 'Spouse');\n"
                   '\n'
                   '-- Adições específicas para que todas as consultas de consultas_ProfMarcosG.pdf retornem '
                   'linhas ricas:\n'
                   '-- 1) Empregado com mesmo primeiro nome do dependente (John Smith -> dependente John)\n'
                   "INSERT INTO DEPENDENT VALUES ('123456789', 'John', 'M', '1995-06-12', 'Son');\n"
                   "-- 2) Ramesh Narayan ('666884444') trabalha em TODOS os projetos do departamento 5 (1, "
                   '2, 3)\n'
                   "INSERT INTO WORKS_ON VALUES ('666884444', 1, 10.0);\n"
                   "INSERT INTO WORKS_ON VALUES ('666884444', 2, 10.0);\n"
                   "-- 3) Franklin Wong ('333445555') trabalha em TODOS os 6 projetos da empresa (já tem "
                   '2,3,10,20; adicionamos 1 e 30)\n'
                   "INSERT INTO WORKS_ON VALUES ('333445555', 1, 5.0);\n"
                   "INSERT INTO WORKS_ON VALUES ('333445555', 30, 5.0);\n"
                   "-- 4) Empregado sem nenhum projeto: Carla Mendes ('111222333')\n"
                   'INSERT INTO EMPLOYEE VALUES\n'
                   "('Carla', 'M', 'Mendes', '111222333', '1975-04-12', '100 Main, Houston, TX', 'F', "
                   "28000.00, '333445555', 5);\n",
          'expected_columns': ['FNAME', 'LNAME'],
          'expected_rows': [['James', 'Borg']]},
 'T6.1': {'title': 'SQL DDL Completo: PRIMARY KEY, UNIQUE e FOREIGN KEY (ON DELETE b, p, n)',
          'type': 'treino',
          'mode': 'sql_ddl',
          'setup': '',
          'ddl_tests': [{'name': 'Criação das tabelas Departamento, Empregado e Dependente',
                         'type': 'tables_exist',
                         'tables': ['Departamento', 'Empregado', 'Dependente']},
                        {'name': 'Restrição UNIQUE na Chave Alternativa NomeDept de Departamento',
                         'type': 'must_fail',
                         'sql': '\n'
                                '                    INSERT INTO Departamento (NDept, NomeDept) VALUES '
                                "('D1', 'Pesquisa');\n"
                                '                    INSERT INTO Departamento (NDept, NomeDept) VALUES '
                                "('D2', 'Pesquisa');\n"
                                '                ',
                         'hint': 'Adicione UNIQUE (NomeDept) na tabela Departamento.'},
                        {'name': 'Política de Bloqueio (b / RESTRICT) em Empregado[NDept] -> '
                                 'Departamento[NDept]',
                         'type': 'must_fail',
                         'sql': '\n'
                                '                    INSERT INTO Departamento (NDept, NomeDept) VALUES '
                                "('D1', 'Pesquisa');\n"
                                '                    INSERT INTO Empregado (NEmp, NomeEmp, Salario, NDept) '
                                "VALUES ('E01', 'Ana', 5000, 'D1');\n"
                                "                    DELETE FROM Departamento WHERE NDept = 'D1';\n"
                                '                ',
                         'hint': 'Defina FOREIGN KEY (NDept) REFERENCES Departamento(NDept) sem CASCADE (o '
                                 'padrão é RESTRICT/bloqueio).'},
                        {'name': 'Política de Propagação (p / ON DELETE CASCADE) em Dependente[NEmp] -> '
                                 'Empregado[NEmp]',
                         'type': 'cascade_check',
                         'sql_setup': '\n'
                                      '                    INSERT INTO Departamento (NDept, NomeDept) VALUES '
                                      "('D1', 'Pesquisa');\n"
                                      '                    INSERT INTO Empregado (NEmp, NomeEmp, Salario, '
                                      "NDept) VALUES ('E01', 'Ana', 5000, 'D1');\n"
                                      '                    INSERT INTO Dependente (NEmp, NomeDep) VALUES '
                                      "('E01', 'Lucas');\n"
                                      "                    DELETE FROM Empregado WHERE NEmp = 'E01';\n"
                                      '                ',
                         'verify_query': 'SELECT COUNT(*) FROM Dependente;',
                         'expected_scalar': 0,
                         'hint': 'Na tabela Dependente, use FOREIGN KEY (NEmp) REFERENCES Empregado(NEmp) ON '
                                 'DELETE CASCADE.'}]},
 'T6.2': {'title': 'Restrição CHECK de Tupla: Otimizando Hierarquia Disjunta e Total (ibd-parte5 Slide 37)',
          'type': 'treino',
          'mode': 'sql_ddl',
          'setup': '',
          'ddl_tests': [{'name': 'Tabela Empregado criada com colunas NEmp, Nome, Salario, SalAd, Formacao',
                         'type': 'tables_exist',
                         'tables': ['Empregado']},
                        {'name': 'Aceita um Gerente válido (SalAd preenchido e Formacao NULL)',
                         'type': 'must_succeed',
                         'sql': "INSERT INTO Empregado (NEmp, Nome, Salario, SalAd, Formacao) VALUES ('E01', "
                                "'Ana', 8000, 2000, NULL);"},
                        {'name': 'Aceita um Técnico válido (SalAd NULL e Formacao preenchida)',
                         'type': 'must_succeed',
                         'sql': "INSERT INTO Empregado (NEmp, Nome, Salario, SalAd, Formacao) VALUES ('E02', "
                                "'Bruno', 6000, NULL, 'MSc');"},
                        {'name': 'Rejeita violação de Disjunção (SalAd e Formacao ambos preenchidos!)',
                         'type': 'must_fail',
                         'sql': "INSERT INTO Empregado (NEmp, Nome, Salario, SalAd, Formacao) VALUES ('E03', "
                                "'Carlos', 7000, 1500, 'BSc');",
                         'hint': 'Sua cláusula CHECK deve rejeitar quando ambos SalAd e Formacao são NOT '
                                 'NULL.'},
                        {'name': 'Rejeita violação de Totalidade (SalAd e Formacao ambos NULL!)',
                         'type': 'must_fail',
                         'sql': "INSERT INTO Empregado (NEmp, Nome, Salario, SalAd, Formacao) VALUES ('E04', "
                                "'Daniela', 5000, NULL, NULL);",
                         'hint': 'Sua cláusula CHECK deve exigir: CHECK ((SalAd IS NOT NULL AND Formacao IS '
                                 'NULL) OR (SalAd IS NULL AND Formacao IS NOT NULL)).'}]},
 'T6.3': {'title': 'Visões em SQL: Modificação da Consulta (Query Modification — ibd-parte4 Slide 36)',
          'type': 'treino',
          'mode': 'sql_query',
          'setup': '\n'
                   'PRAGMA foreign_keys = ON;\n'
                   '\n'
                   'CREATE TABLE DEPARTMENT (\n'
                   '    DNAME VARCHAR(15) NOT NULL,\n'
                   '    DNUMBER INT NOT NULL,\n'
                   '    MGRSSN CHAR(9) NOT NULL,\n'
                   '    MGRSTARTDATE CHAR(10),\n'
                   '    PRIMARY KEY (DNUMBER),\n'
                   '    UNIQUE (DNAME)\n'
                   ');\n'
                   '\n'
                   'CREATE TABLE EMPLOYEE (\n'
                   '    FNAME VARCHAR(15) NOT NULL,\n'
                   '    MINIT CHAR(1),\n'
                   '    LNAME VARCHAR(15) NOT NULL,\n'
                   '    SSN CHAR(9) NOT NULL,\n'
                   '    BDATE CHAR(10),\n'
                   '    ADDRESS VARCHAR(40),\n'
                   '    SEX CHAR(1),\n'
                   '    SALARY DECIMAL(10,2),\n'
                   '    SUPERSSN CHAR(9),\n'
                   '    DNO INT NOT NULL,\n'
                   '    PRIMARY KEY (SSN),\n'
                   '    FOREIGN KEY (SUPERSSN) REFERENCES EMPLOYEE(SSN) ON DELETE SET NULL,\n'
                   '    FOREIGN KEY (DNO) REFERENCES DEPARTMENT(DNUMBER)\n'
                   ');\n'
                   '\n'
                   'CREATE TABLE DEPT_LOCATIONS (\n'
                   '    DNUMBER INT NOT NULL,\n'
                   '    DLOCATION VARCHAR(15) NOT NULL,\n'
                   '    PRIMARY KEY (DNUMBER, DLOCATION),\n'
                   '    FOREIGN KEY (DNUMBER) REFERENCES DEPARTMENT(DNUMBER) ON DELETE CASCADE\n'
                   ');\n'
                   '\n'
                   'CREATE TABLE PROJECT (\n'
                   '    PNAME VARCHAR(20) NOT NULL,\n'
                   '    PNUMBER INT NOT NULL,\n'
                   '    PLOCATION VARCHAR(15),\n'
                   '    DNUM INT NOT NULL,\n'
                   '    PRIMARY KEY (PNUMBER),\n'
                   '    UNIQUE (PNAME),\n'
                   '    FOREIGN KEY (DNUM) REFERENCES DEPARTMENT(DNUMBER)\n'
                   ');\n'
                   '\n'
                   'CREATE TABLE WORKS_ON (\n'
                   '    ESSN CHAR(9) NOT NULL,\n'
                   '    PNO INT NOT NULL,\n'
                   '    HOURS DECIMAL(4,1),\n'
                   '    PRIMARY KEY (ESSN, PNO),\n'
                   '    FOREIGN KEY (ESSN) REFERENCES EMPLOYEE(SSN),\n'
                   '    FOREIGN KEY (PNO) REFERENCES PROJECT(PNUMBER)\n'
                   ');\n'
                   '\n'
                   'CREATE TABLE DEPENDENT (\n'
                   '    ESSN CHAR(9) NOT NULL,\n'
                   '    DEPENDENT_NAME VARCHAR(15) NOT NULL,\n'
                   '    SEX CHAR(1),\n'
                   '    BDATE CHAR(10),\n'
                   '    RELATIONSHIP VARCHAR(12),\n'
                   '    PRIMARY KEY (ESSN, DEPENDENT_NAME),\n'
                   '    FOREIGN KEY (ESSN) REFERENCES EMPLOYEE(SSN) ON DELETE CASCADE\n'
                   ');\n'
                   '\n'
                   'INSERT INTO DEPARTMENT VALUES\n'
                   "('Research', 5, '333445555', '1988-05-22'),\n"
                   "('Administration', 4, '987654321', '1995-01-01'),\n"
                   "('Headquarters', 1, '888665555', '1981-06-19');\n"
                   '\n'
                   'INSERT INTO EMPLOYEE VALUES\n'
                   "('James', 'E', 'Borg', '888665555', '1937-11-10', '450 Stone, Houston, TX', 'M', "
                   '55000.00, NULL, 1),\n'
                   "('Franklin', 'T', 'Wong', '333445555', '1955-12-08', '638 Voss, Houston, TX', 'M', "
                   "40000.00, '888665555', 5),\n"
                   "('Jennifer', 'S', 'Wallace', '987654321', '1941-06-20', '291 Berry, Bellaire, TX', 'F', "
                   "43000.00, '888665555', 4),\n"
                   "('John', 'B', 'Smith', '123456789', '1965-01-09', '731 Fondren, Houston, TX', 'M', "
                   "30000.00, '333445555', 5),\n"
                   "('Ramesh', 'K', 'Narayan', '666884444', '1962-09-15', '975 Fire Oak, Humble, TX', 'M', "
                   "38000.00, '333445555', 5),\n"
                   "('Joyce', 'A', 'English', '453453453', '1972-07-31', '5631 Rice, Houston, TX', 'F', "
                   "25000.00, '333445555', 5),\n"
                   "('Alicia', 'J', 'Zelaya', '999887777', '1968-01-19', '3321 Castle, Spring, TX', 'F', "
                   "25000.00, '987654321', 4),\n"
                   "('Ahmad', 'V', 'Jabbar', '987987987', '1969-03-29', '980 Dallas, Houston, TX', 'M', "
                   "25000.00, '987654321', 4);\n"
                   '\n'
                   'INSERT INTO DEPT_LOCATIONS VALUES\n'
                   "(1, 'Houston'),\n"
                   "(4, 'Stafford'),\n"
                   "(5, 'Bellaire'),\n"
                   "(5, 'Sugarland'),\n"
                   "(5, 'Houston');\n"
                   '\n'
                   'INSERT INTO PROJECT VALUES\n'
                   "('ProductX', 1, 'Bellaire', 5),\n"
                   "('ProductY', 2, 'Sugarland', 5),\n"
                   "('ProductZ', 3, 'Houston', 5),\n"
                   "('Computerization', 10, 'Stafford', 4),\n"
                   "('Reorganization', 20, 'Houston', 1),\n"
                   "('Newbenefits', 30, 'Stafford', 4);\n"
                   '\n'
                   'INSERT INTO WORKS_ON VALUES\n'
                   "('123456789', 1, 32.5),\n"
                   "('123456789', 2, 7.5),\n"
                   "('666884444', 3, 40.0),\n"
                   "('453453453', 1, 20.0),\n"
                   "('453453453', 2, 20.0),\n"
                   "('333445555', 2, 10.0),\n"
                   "('333445555', 3, 10.0),\n"
                   "('333445555', 10, 10.0),\n"
                   "('333445555', 20, 10.0),\n"
                   "('999887777', 30, 30.0),\n"
                   "('999887777', 10, 10.0),\n"
                   "('987987987', 10, 35.0),\n"
                   "('987987987', 30, 5.0),\n"
                   "('987654321', 30, 20.0),\n"
                   "('987654321', 20, 15.0),\n"
                   "('888665555', 20, NULL);\n"
                   '\n'
                   'INSERT INTO DEPENDENT VALUES\n'
                   "('333445555', 'Alice', 'F', '1986-04-05', 'Daughter'),\n"
                   "('333445555', 'Theodore', 'M', '1983-10-25', 'Son'),\n"
                   "('333445555', 'Joy', 'F', '1958-05-03', 'Spouse'),\n"
                   "('987654321', 'Abner', 'M', '1942-02-28', 'Spouse'),\n"
                   "('123456789', 'Michael', 'M', '1988-01-04', 'Son'),\n"
                   "('123456789', 'Alice', 'F', '1988-12-30', 'Daughter'),\n"
                   "('123456789', 'Elizabeth', 'F', '1967-05-05', 'Spouse');\n"
                   '\n'
                   '            CREATE VIEW WORKS_ON1 AS\n'
                   '            SELECT FNAME, LNAME, PNAME, HOURS\n'
                   '            FROM EMPLOYEE, PROJECT, WORKS_ON\n'
                   '            WHERE SSN = ESSN AND PNO = PNUMBER;\n'
                   '        ',
          'expected_columns': ['LNAME', 'HOURS'],
          'expected_rows': [['Smith', 32.5], ['English', 20.0]]},
 'E6.1': {'title': '[Oficial consultas_ProfMarcosG.pdf (a, b, c)] Depto 5 em ProductX, Homônimos e Franklin '
                   'Wong',
          'type': 'oficial',
          'mode': 'sql_query',
          'setup': '\n'
                   'PRAGMA foreign_keys = ON;\n'
                   '\n'
                   'CREATE TABLE DEPARTMENT (\n'
                   '    DNAME VARCHAR(15) NOT NULL,\n'
                   '    DNUMBER INT NOT NULL,\n'
                   '    MGRSSN CHAR(9) NOT NULL,\n'
                   '    MGRSTARTDATE CHAR(10),\n'
                   '    PRIMARY KEY (DNUMBER),\n'
                   '    UNIQUE (DNAME)\n'
                   ');\n'
                   '\n'
                   'CREATE TABLE EMPLOYEE (\n'
                   '    FNAME VARCHAR(15) NOT NULL,\n'
                   '    MINIT CHAR(1),\n'
                   '    LNAME VARCHAR(15) NOT NULL,\n'
                   '    SSN CHAR(9) NOT NULL,\n'
                   '    BDATE CHAR(10),\n'
                   '    ADDRESS VARCHAR(40),\n'
                   '    SEX CHAR(1),\n'
                   '    SALARY DECIMAL(10,2),\n'
                   '    SUPERSSN CHAR(9),\n'
                   '    DNO INT NOT NULL,\n'
                   '    PRIMARY KEY (SSN),\n'
                   '    FOREIGN KEY (SUPERSSN) REFERENCES EMPLOYEE(SSN) ON DELETE SET NULL,\n'
                   '    FOREIGN KEY (DNO) REFERENCES DEPARTMENT(DNUMBER)\n'
                   ');\n'
                   '\n'
                   'CREATE TABLE DEPT_LOCATIONS (\n'
                   '    DNUMBER INT NOT NULL,\n'
                   '    DLOCATION VARCHAR(15) NOT NULL,\n'
                   '    PRIMARY KEY (DNUMBER, DLOCATION),\n'
                   '    FOREIGN KEY (DNUMBER) REFERENCES DEPARTMENT(DNUMBER) ON DELETE CASCADE\n'
                   ');\n'
                   '\n'
                   'CREATE TABLE PROJECT (\n'
                   '    PNAME VARCHAR(20) NOT NULL,\n'
                   '    PNUMBER INT NOT NULL,\n'
                   '    PLOCATION VARCHAR(15),\n'
                   '    DNUM INT NOT NULL,\n'
                   '    PRIMARY KEY (PNUMBER),\n'
                   '    UNIQUE (PNAME),\n'
                   '    FOREIGN KEY (DNUM) REFERENCES DEPARTMENT(DNUMBER)\n'
                   ');\n'
                   '\n'
                   'CREATE TABLE WORKS_ON (\n'
                   '    ESSN CHAR(9) NOT NULL,\n'
                   '    PNO INT NOT NULL,\n'
                   '    HOURS DECIMAL(4,1),\n'
                   '    PRIMARY KEY (ESSN, PNO),\n'
                   '    FOREIGN KEY (ESSN) REFERENCES EMPLOYEE(SSN),\n'
                   '    FOREIGN KEY (PNO) REFERENCES PROJECT(PNUMBER)\n'
                   ');\n'
                   '\n'
                   'CREATE TABLE DEPENDENT (\n'
                   '    ESSN CHAR(9) NOT NULL,\n'
                   '    DEPENDENT_NAME VARCHAR(15) NOT NULL,\n'
                   '    SEX CHAR(1),\n'
                   '    BDATE CHAR(10),\n'
                   '    RELATIONSHIP VARCHAR(12),\n'
                   '    PRIMARY KEY (ESSN, DEPENDENT_NAME),\n'
                   '    FOREIGN KEY (ESSN) REFERENCES EMPLOYEE(SSN) ON DELETE CASCADE\n'
                   ');\n'
                   '\n'
                   'INSERT INTO DEPARTMENT VALUES\n'
                   "('Research', 5, '333445555', '1988-05-22'),\n"
                   "('Administration', 4, '987654321', '1995-01-01'),\n"
                   "('Headquarters', 1, '888665555', '1981-06-19');\n"
                   '\n'
                   'INSERT INTO EMPLOYEE VALUES\n'
                   "('James', 'E', 'Borg', '888665555', '1937-11-10', '450 Stone, Houston, TX', 'M', "
                   '55000.00, NULL, 1),\n'
                   "('Franklin', 'T', 'Wong', '333445555', '1955-12-08', '638 Voss, Houston, TX', 'M', "
                   "40000.00, '888665555', 5),\n"
                   "('Jennifer', 'S', 'Wallace', '987654321', '1941-06-20', '291 Berry, Bellaire, TX', 'F', "
                   "43000.00, '888665555', 4),\n"
                   "('John', 'B', 'Smith', '123456789', '1965-01-09', '731 Fondren, Houston, TX', 'M', "
                   "30000.00, '333445555', 5),\n"
                   "('Ramesh', 'K', 'Narayan', '666884444', '1962-09-15', '975 Fire Oak, Humble, TX', 'M', "
                   "38000.00, '333445555', 5),\n"
                   "('Joyce', 'A', 'English', '453453453', '1972-07-31', '5631 Rice, Houston, TX', 'F', "
                   "25000.00, '333445555', 5),\n"
                   "('Alicia', 'J', 'Zelaya', '999887777', '1968-01-19', '3321 Castle, Spring, TX', 'F', "
                   "25000.00, '987654321', 4),\n"
                   "('Ahmad', 'V', 'Jabbar', '987987987', '1969-03-29', '980 Dallas, Houston, TX', 'M', "
                   "25000.00, '987654321', 4);\n"
                   '\n'
                   'INSERT INTO DEPT_LOCATIONS VALUES\n'
                   "(1, 'Houston'),\n"
                   "(4, 'Stafford'),\n"
                   "(5, 'Bellaire'),\n"
                   "(5, 'Sugarland'),\n"
                   "(5, 'Houston');\n"
                   '\n'
                   'INSERT INTO PROJECT VALUES\n'
                   "('ProductX', 1, 'Bellaire', 5),\n"
                   "('ProductY', 2, 'Sugarland', 5),\n"
                   "('ProductZ', 3, 'Houston', 5),\n"
                   "('Computerization', 10, 'Stafford', 4),\n"
                   "('Reorganization', 20, 'Houston', 1),\n"
                   "('Newbenefits', 30, 'Stafford', 4);\n"
                   '\n'
                   'INSERT INTO WORKS_ON VALUES\n'
                   "('123456789', 1, 32.5),\n"
                   "('123456789', 2, 7.5),\n"
                   "('666884444', 3, 40.0),\n"
                   "('453453453', 1, 20.0),\n"
                   "('453453453', 2, 20.0),\n"
                   "('333445555', 2, 10.0),\n"
                   "('333445555', 3, 10.0),\n"
                   "('333445555', 10, 10.0),\n"
                   "('333445555', 20, 10.0),\n"
                   "('999887777', 30, 30.0),\n"
                   "('999887777', 10, 10.0),\n"
                   "('987987987', 10, 35.0),\n"
                   "('987987987', 30, 5.0),\n"
                   "('987654321', 30, 20.0),\n"
                   "('987654321', 20, 15.0),\n"
                   "('888665555', 20, NULL);\n"
                   '\n'
                   'INSERT INTO DEPENDENT VALUES\n'
                   "('333445555', 'Alice', 'F', '1986-04-05', 'Daughter'),\n"
                   "('333445555', 'Theodore', 'M', '1983-10-25', 'Son'),\n"
                   "('333445555', 'Joy', 'F', '1958-05-03', 'Spouse'),\n"
                   "('987654321', 'Abner', 'M', '1942-02-28', 'Spouse'),\n"
                   "('123456789', 'Michael', 'M', '1988-01-04', 'Son'),\n"
                   "('123456789', 'Alice', 'F', '1988-12-30', 'Daughter'),\n"
                   "('123456789', 'Elizabeth', 'F', '1967-05-05', 'Spouse');\n"
                   '\n'
                   '-- Adições específicas para que todas as consultas de consultas_ProfMarcosG.pdf retornem '
                   'linhas ricas:\n'
                   '-- 1) Empregado com mesmo primeiro nome do dependente (John Smith -> dependente John)\n'
                   "INSERT INTO DEPENDENT VALUES ('123456789', 'John', 'M', '1995-06-12', 'Son');\n"
                   "-- 2) Ramesh Narayan ('666884444') trabalha em TODOS os projetos do departamento 5 (1, "
                   '2, 3)\n'
                   "INSERT INTO WORKS_ON VALUES ('666884444', 1, 10.0);\n"
                   "INSERT INTO WORKS_ON VALUES ('666884444', 2, 10.0);\n"
                   "-- 3) Franklin Wong ('333445555') trabalha em TODOS os 6 projetos da empresa (já tem "
                   '2,3,10,20; adicionamos 1 e 30)\n'
                   "INSERT INTO WORKS_ON VALUES ('333445555', 1, 5.0);\n"
                   "INSERT INTO WORKS_ON VALUES ('333445555', 30, 5.0);\n"
                   "-- 4) Empregado sem nenhum projeto: Carla Mendes ('111222333')\n"
                   'INSERT INTO EMPLOYEE VALUES\n'
                   "('Carla', 'M', 'Mendes', '111222333', '1975-04-12', '100 Main, Houston, TX', 'F', "
                   "28000.00, '333445555', 5);\n",
          'expected_columns': ['CONSULTA', 'FNAME', 'LNAME'],
          'expected_rows': [['a', 'John', 'Smith'],
                            ['a', 'Joyce', 'English'],
                            ['b', 'John', 'Smith'],
                            ['c', 'John', 'Smith'],
                            ['c', 'Ramesh', 'Narayan'],
                            ['c', 'Joyce', 'English'],
                            ['c', 'Carla', 'Mendes']]},
 'E6.2': {'title': '[Oficial Slides 04] CREATE ASSERTION SALARY_CONSTRAINT (Salário Empregado vs. Gerente)',
          'type': 'oficial',
          'mode': 'sql_assertion',
          'setup': '\n'
                   'PRAGMA foreign_keys = ON;\n'
                   '\n'
                   'CREATE TABLE DEPARTMENT (\n'
                   '    DNAME VARCHAR(15) NOT NULL,\n'
                   '    DNUMBER INT NOT NULL,\n'
                   '    MGRSSN CHAR(9) NOT NULL,\n'
                   '    MGRSTARTDATE CHAR(10),\n'
                   '    PRIMARY KEY (DNUMBER),\n'
                   '    UNIQUE (DNAME)\n'
                   ');\n'
                   '\n'
                   'CREATE TABLE EMPLOYEE (\n'
                   '    FNAME VARCHAR(15) NOT NULL,\n'
                   '    MINIT CHAR(1),\n'
                   '    LNAME VARCHAR(15) NOT NULL,\n'
                   '    SSN CHAR(9) NOT NULL,\n'
                   '    BDATE CHAR(10),\n'
                   '    ADDRESS VARCHAR(40),\n'
                   '    SEX CHAR(1),\n'
                   '    SALARY DECIMAL(10,2),\n'
                   '    SUPERSSN CHAR(9),\n'
                   '    DNO INT NOT NULL,\n'
                   '    PRIMARY KEY (SSN),\n'
                   '    FOREIGN KEY (SUPERSSN) REFERENCES EMPLOYEE(SSN) ON DELETE SET NULL,\n'
                   '    FOREIGN KEY (DNO) REFERENCES DEPARTMENT(DNUMBER)\n'
                   ');\n'
                   '\n'
                   'CREATE TABLE DEPT_LOCATIONS (\n'
                   '    DNUMBER INT NOT NULL,\n'
                   '    DLOCATION VARCHAR(15) NOT NULL,\n'
                   '    PRIMARY KEY (DNUMBER, DLOCATION),\n'
                   '    FOREIGN KEY (DNUMBER) REFERENCES DEPARTMENT(DNUMBER) ON DELETE CASCADE\n'
                   ');\n'
                   '\n'
                   'CREATE TABLE PROJECT (\n'
                   '    PNAME VARCHAR(20) NOT NULL,\n'
                   '    PNUMBER INT NOT NULL,\n'
                   '    PLOCATION VARCHAR(15),\n'
                   '    DNUM INT NOT NULL,\n'
                   '    PRIMARY KEY (PNUMBER),\n'
                   '    UNIQUE (PNAME),\n'
                   '    FOREIGN KEY (DNUM) REFERENCES DEPARTMENT(DNUMBER)\n'
                   ');\n'
                   '\n'
                   'CREATE TABLE WORKS_ON (\n'
                   '    ESSN CHAR(9) NOT NULL,\n'
                   '    PNO INT NOT NULL,\n'
                   '    HOURS DECIMAL(4,1),\n'
                   '    PRIMARY KEY (ESSN, PNO),\n'
                   '    FOREIGN KEY (ESSN) REFERENCES EMPLOYEE(SSN),\n'
                   '    FOREIGN KEY (PNO) REFERENCES PROJECT(PNUMBER)\n'
                   ');\n'
                   '\n'
                   'CREATE TABLE DEPENDENT (\n'
                   '    ESSN CHAR(9) NOT NULL,\n'
                   '    DEPENDENT_NAME VARCHAR(15) NOT NULL,\n'
                   '    SEX CHAR(1),\n'
                   '    BDATE CHAR(10),\n'
                   '    RELATIONSHIP VARCHAR(12),\n'
                   '    PRIMARY KEY (ESSN, DEPENDENT_NAME),\n'
                   '    FOREIGN KEY (ESSN) REFERENCES EMPLOYEE(SSN) ON DELETE CASCADE\n'
                   ');\n'
                   '\n'
                   'INSERT INTO DEPARTMENT VALUES\n'
                   "('Research', 5, '333445555', '1988-05-22'),\n"
                   "('Administration', 4, '987654321', '1995-01-01'),\n"
                   "('Headquarters', 1, '888665555', '1981-06-19');\n"
                   '\n'
                   'INSERT INTO EMPLOYEE VALUES\n'
                   "('James', 'E', 'Borg', '888665555', '1937-11-10', '450 Stone, Houston, TX', 'M', "
                   '55000.00, NULL, 1),\n'
                   "('Franklin', 'T', 'Wong', '333445555', '1955-12-08', '638 Voss, Houston, TX', 'M', "
                   "40000.00, '888665555', 5),\n"
                   "('Jennifer', 'S', 'Wallace', '987654321', '1941-06-20', '291 Berry, Bellaire, TX', 'F', "
                   "43000.00, '888665555', 4),\n"
                   "('John', 'B', 'Smith', '123456789', '1965-01-09', '731 Fondren, Houston, TX', 'M', "
                   "30000.00, '333445555', 5),\n"
                   "('Ramesh', 'K', 'Narayan', '666884444', '1962-09-15', '975 Fire Oak, Humble, TX', 'M', "
                   "38000.00, '333445555', 5),\n"
                   "('Joyce', 'A', 'English', '453453453', '1972-07-31', '5631 Rice, Houston, TX', 'F', "
                   "25000.00, '333445555', 5),\n"
                   "('Alicia', 'J', 'Zelaya', '999887777', '1968-01-19', '3321 Castle, Spring, TX', 'F', "
                   "25000.00, '987654321', 4),\n"
                   "('Ahmad', 'V', 'Jabbar', '987987987', '1969-03-29', '980 Dallas, Houston, TX', 'M', "
                   "25000.00, '987654321', 4);\n"
                   '\n'
                   'INSERT INTO DEPT_LOCATIONS VALUES\n'
                   "(1, 'Houston'),\n"
                   "(4, 'Stafford'),\n"
                   "(5, 'Bellaire'),\n"
                   "(5, 'Sugarland'),\n"
                   "(5, 'Houston');\n"
                   '\n'
                   'INSERT INTO PROJECT VALUES\n'
                   "('ProductX', 1, 'Bellaire', 5),\n"
                   "('ProductY', 2, 'Sugarland', 5),\n"
                   "('ProductZ', 3, 'Houston', 5),\n"
                   "('Computerization', 10, 'Stafford', 4),\n"
                   "('Reorganization', 20, 'Houston', 1),\n"
                   "('Newbenefits', 30, 'Stafford', 4);\n"
                   '\n'
                   'INSERT INTO WORKS_ON VALUES\n'
                   "('123456789', 1, 32.5),\n"
                   "('123456789', 2, 7.5),\n"
                   "('666884444', 3, 40.0),\n"
                   "('453453453', 1, 20.0),\n"
                   "('453453453', 2, 20.0),\n"
                   "('333445555', 2, 10.0),\n"
                   "('333445555', 3, 10.0),\n"
                   "('333445555', 10, 10.0),\n"
                   "('333445555', 20, 10.0),\n"
                   "('999887777', 30, 30.0),\n"
                   "('999887777', 10, 10.0),\n"
                   "('987987987', 10, 35.0),\n"
                   "('987987987', 30, 5.0),\n"
                   "('987654321', 30, 20.0),\n"
                   "('987654321', 20, 15.0),\n"
                   "('888665555', 20, NULL);\n"
                   '\n'
                   'INSERT INTO DEPENDENT VALUES\n'
                   "('333445555', 'Alice', 'F', '1986-04-05', 'Daughter'),\n"
                   "('333445555', 'Theodore', 'M', '1983-10-25', 'Son'),\n"
                   "('333445555', 'Joy', 'F', '1958-05-03', 'Spouse'),\n"
                   "('987654321', 'Abner', 'M', '1942-02-28', 'Spouse'),\n"
                   "('123456789', 'Michael', 'M', '1988-01-04', 'Son'),\n"
                   "('123456789', 'Alice', 'F', '1988-12-30', 'Daughter'),\n"
                   "('123456789', 'Elizabeth', 'F', '1967-05-05', 'Spouse');\n",
          'assertion_tests': [{'name': 'Estado inicial válido da base COMPANY (nenhum empregado ganha mais '
                                       'que seu gerente)',
                               'violation_sql': None,
                               'should_pass': True},
                              {'name': 'Injeção de Falha 1: Empregado John Smith (Depto 5) passa a ganhar '
                                       '45.000 (Gerente Franklin Wong ganha 40.000)',
                               'violation_sql': 'UPDATE EMPLOYEE SET SALARY = 45000.00 WHERE SSN = '
                                                "'123456789';",
                               'should_pass': False,
                               'hint': 'Sua subconsulta dentro do NOT EXISTS deve buscar qualquer empregado '
                                       'E, departamento D e gerente M onde E.DNO = D.DNUMBER AND D.MGRSSN = '
                                       'M.SSN AND E.SALARY > M.SALARY.'},
                              {'name': 'Injeção de Falha 2: Empregada Alicia Zelaya (Depto 4) passa a ganhar '
                                       '50.000 (Gerente Jennifer Wallace ganha 43.000)',
                               'violation_sql': 'UPDATE EMPLOYEE SET SALARY = 50000.00 WHERE SSN = '
                                                "'999887777';",
                               'should_pass': False,
                               'hint': 'Verifique se sua junção conecta E.DNO = D.DNUMBER e D.MGRSSN = M.SSN '
                                       'para qualquer departamento.'}]},
 'E6.3': {'title': '[Oficial Slides 05] CREATE ASSERTION para Totalidade e Disjunção em Hierarquias',
          'type': 'oficial',
          'mode': 'sql_assertion',
          'setup': '\n'
                   'PRAGMA foreign_keys = ON;\n'
                   '\n'
                   'CREATE TABLE Departamento (\n'
                   '    NDept CHAR(2) NOT NULL PRIMARY KEY,\n'
                   '    NomeDept VARCHAR(30) NOT NULL UNIQUE\n'
                   ');\n'
                   '\n'
                   'CREATE TABLE Empregado (\n'
                   '    NEmp CHAR(3) NOT NULL PRIMARY KEY,\n'
                   '    NomeEmp VARCHAR(30) NOT NULL,\n'
                   '    Salario DECIMAL(8,2) NOT NULL,\n'
                   '    NDept CHAR(2) NOT NULL,\n'
                   '    FOREIGN KEY (NDept) REFERENCES Departamento(NDept)\n'
                   ');\n'
                   '\n'
                   'CREATE TABLE Gerente (\n'
                   '    NEmp CHAR(3) NOT NULL PRIMARY KEY,\n'
                   '    SalAd DECIMAL(8,2) NOT NULL,\n'
                   '    FOREIGN KEY (NEmp) REFERENCES Empregado(NEmp) ON DELETE CASCADE\n'
                   ');\n'
                   '\n'
                   'CREATE TABLE Tecnico (\n'
                   '    NEmp CHAR(3) NOT NULL PRIMARY KEY,\n'
                   '    Formacao VARCHAR(10) NOT NULL,\n'
                   '    FOREIGN KEY (NEmp) REFERENCES Empregado(NEmp) ON DELETE CASCADE\n'
                   ');\n'
                   '\n'
                   'CREATE TABLE Projeto (\n'
                   '    NProj CHAR(3) NOT NULL PRIMARY KEY,\n'
                   '    NomeProj VARCHAR(30) NOT NULL\n'
                   ');\n'
                   '\n'
                   'CREATE TABLE Participa_de (\n'
                   '    NEmp CHAR(3) NOT NULL,\n'
                   '    NProj CHAR(3) NOT NULL,\n'
                   '    HsTrab INT,\n'
                   '    PRIMARY KEY (NEmp, NProj),\n'
                   '    FOREIGN KEY (NEmp) REFERENCES Empregado(NEmp) ON DELETE CASCADE,\n'
                   '    FOREIGN KEY (NProj) REFERENCES Projeto(NProj) ON DELETE CASCADE\n'
                   ');\n'
                   '\n'
                   "INSERT INTO Departamento VALUES ('D1', 'Pesquisa'), ('D2', 'Engenharia');\n"
                   'INSERT INTO Empregado VALUES\n'
                   "('E01', 'Ana Costa', 8000.00, 'D1'),\n"
                   "('E02', 'Bruno Lima', 6500.00, 'D1'),\n"
                   "('E03', 'Carlos Souza', 7200.00, 'D2'),\n"
                   "('E04', 'Daniela Reis', 5800.00, 'D2');\n"
                   '\n'
                   "INSERT INTO Gerente VALUES ('E01', 2000.00), ('E03', 1500.00);\n"
                   "INSERT INTO Tecnico VALUES ('E02', 'MSc'), ('E04', 'BSc');\n"
                   '\n'
                   "INSERT INTO Projeto VALUES ('P10', 'Sistema Alpha'), ('P20', 'Motor Beta');\n"
                   'INSERT INTO Participa_de VALUES\n'
                   "('E01', 'P10', 20),\n"
                   "('E02', 'P10', 40),\n"
                   "('E03', 'P20', 30),\n"
                   "('E04', 'P20', 35);\n",
          'assertion_tests': [{'name': 'Estado inicial válido: E01 e E03 são Gerentes; E02 e E04 são '
                                       'Técnicos (Disjunta e Total)',
                               'violation_sql': None,
                               'should_pass': True},
                              {'name': 'Injeção de Falha 1 (Violação de Totalidade): Inserir empregado E05 '
                                       'que não está nem em Gerente nem em Tecnico',
                               'violation_sql': "INSERT INTO Empregado VALUES ('E05', 'Fabio', 5000.00, "
                                                "'D1');",
                               'should_pass': False,
                               'hint': 'Para garantir a totalidade (Empregado-total), verifique se NOT '
                                       'EXISTS um Empregado cujo NEmp NOT IN (SELECT NEmp FROM Tecnico UNION '
                                       'SELECT NEmp FROM Gerente).'},
                              {'name': 'Injeção de Falha 2 (Violação de Disjunção): Inserir a gerente E01 '
                                       'também na tabela Tecnico',
                               'violation_sql': "INSERT INTO Tecnico VALUES ('E01', 'PhD');",
                               'should_pass': False,
                               'hint': 'Você pode escrever uma segunda CREATE ASSERTION Gerente_ou_Tecnico '
                                       'CHECK (NOT EXISTS (SELECT * FROM Gerente G, Tecnico T WHERE G.NEmp = '
                                       'T.NEmp)) ou combinar com UNION!'}]},
 'T7.1': {'title': 'Mapeamento das 7 Regras Básicas: Entidades, Multivalorados e Fracas',
          'type': 'treino',
          'mode': 'structured',
          'setup': '',
          'fields': [{'id': 'q1',
                      'label': '1. [Regra 1 e 2] Dado DEPARTAMENTO com DNumber (PK), DName (chave '
                               'alternativa) e o atributo MULTIVALORADO Locations. Qual é o mapeamento '
                               'relacional correto (slide 14 de ibd-parte5.pdf)?',
                      'options': ['DEPARTAMENTO(DNumber(nn), DName(nn), DLocation1, DLocation2, DLocation3) '
                                  'em relação única sem criar chaves estrangeiras adicionais',
                                  'DEPARTAMENTO(DNumber(nn), DName(nn)) e DEPT_LOCATIONS(DNumber(nn), '
                                  'DLocation(nn)) com PK (DNumber, DLocation) e RIR com política p',
                                  'DEPARTAMENTO(DNumber(nn), DName(nn)) e DEPT_LOCATIONS(DLocation(nn), '
                                  'DNumber) com PK simples DLocation e RIR com política b (bloqueio)',
                                  'DEPARTAMENTO(DNumber(nn), DLocation(nn), DName(nn)) com PK composta '
                                  '(DNumber, DLocation) diretamente na relação principal do departamento'],
                      'answer': 'DEPARTAMENTO(DNumber(nn), DName(nn)) e DEPT_LOCATIONS(DNumber(nn), '
                                'DLocation(nn)) com PK (DNumber, DLocation) e RIR com política p',
                      'explanation': 'Slide 14 de ibd-parte5.pdf: Cada atributo multivalorado gera uma nova '
                                     'relação cuja chave primária é composta pela PK da entidade dona + o '
                                     'próprio atributo, com política de remoção p (propagação / CASCADE).'},
                     {'id': 'q2',
                      'label': '2. [Regra 3] A Entidade Fraca DEPENDENT (chave parcial Dependent_Name) é '
                               'identificada por EMPLOYEE (chave SSN). Qual é o esquema e a RIR de DEPENDENT '
                               '(slide 15 de ibd-parte5.pdf)?',
                      'options': ['DEPENDENT(Dependent_Name(nn), ESSN(nn), DataNasc) com PK simples '
                                  'Dependent_Name e RIR DEPENDENT[ESSN] -b-> EMPLOYEE[SSN]',
                                  'DEPENDENT(ESSN(nn), Dependent_Name(nn), DataNasc) com PK composta (ESSN, '
                                  'Dependent_Name) e RIR DEPENDENT[ESSN] -p-> EMPLOYEE[SSN]',
                                  'DEPENDENT(ESSN(nn), Dependent_Name, DataNasc) com PK simples ESSN e RIR '
                                  'DEPENDENT[ESSN] -n-> EMPLOYEE[SSN]',
                                  'DEPENDENT(Dependent_Name(nn), ESSN, DataNasc) com PK composta (ESSN, '
                                  'Dependent_Name) e RIR DEPENDENT[ESSN] -n-> EMPLOYEE[SSN]'],
                      'answer': 'DEPENDENT(ESSN(nn), Dependent_Name(nn), DataNasc) com PK composta (ESSN, '
                                'Dependent_Name) e RIR DEPENDENT[ESSN] -p-> EMPLOYEE[SSN]',
                      'explanation': 'Slide 15 de ibd-parte5.pdf: Uma entidade fraca tem chave primária '
                                     'composta por (PK do dono + chave parcial), ambos NOT NULL, e sua FK '
                                     'para o dono possui obrigatoriamente política p (propagação).'},
                     {'id': 'q3',
                      'label': '3. [Regra 4] No relacionamento N:1 Trabalha-para entre Empregado (lado N, '
                               'participação total) e Departamento (lado 1), como fica o mapeamento '
                               'otimizado (slide 18 de ibd-parte5.pdf)?',
                      'options': ['Departamento recebe NEmp(nn) como chave estrangeira com política de '
                                  'remoção p (propagação)',
                                  'Cria-se obrigatoriamente a tabela Trabalha-para(NEmp(nn), NDept(nn)) com '
                                  'política n (substituição por nulos)',
                                  'Empregado recebe NDept como chave estrangeira anulável (NULL permitido) '
                                  'com política n (substituição por nulos)',
                                  'Empregado recebe NDept(nn) como chave estrangeira NOT NULL com RIR '
                                  'Empregado[NDept] -b-> Departamento[NDept]'],
                      'answer': 'Empregado recebe NDept(nn) como chave estrangeira NOT NULL com RIR '
                                'Empregado[NDept] -b-> Departamento[NDept]',
                      'explanation': 'Slide 18 de ibd-parte5.pdf: No mapeamento otimizado de N:1, a PK do '
                                     'lado 1 (NDept) migra para a tabela do lado N (Empregado). Como a '
                                     'participação de Empregado é total, NDept é (nn) e a política é b '
                                     '(bloqueio).'}]},
 'T7.2': {'title': 'Mapeamento de Relacionamentos M:N e Agregações EER',
          'type': 'treino',
          'mode': 'structured',
          'setup': '',
          'fields': [{'id': 'q1',
                      'label': '1. No relacionamento M:N `Participa-de` entre `Empregado(NEmp)` e '
                               '`Projeto(NProj)` com atributo `HsTrab` (slide 21 de ibd-parte5.pdf), qual é '
                               'o esquema relacional?',
                      'options': ['Participa-de(NEmp(nn), NProj(nn), HsTrab) com PK (NEmp, NProj) e RIRs com '
                                  'política p (propagação) para Empregado e Projeto',
                                  'Participa-de(NEmp(nn), NProj(nn), HsTrab) com PK simples NEmp e RIRs com '
                                  'política b (bloqueio) para Empregado e Projeto',
                                  'Empregado recebe os atributos NProj(nn) e HsTrab como chaves estrangeiras '
                                  'diretas com política n (substituição por nulos)',
                                  'Projeto recebe os atributos NEmp(nn) e HsTrab como chaves estrangeiras '
                                  'diretas com política b (bloqueio)'],
                      'answer': 'Participa-de(NEmp(nn), NProj(nn), HsTrab) com PK (NEmp, NProj) e RIRs com '
                                'política p (propagação) para Empregado e Projeto',
                      'explanation': 'Slide 21 de ibd-parte5.pdf: Um relacionamento M:N sempre gera uma '
                                     'relação própria cuja PK é composta pelas PKs das entidades '
                                     'participantes (NEmp, NProj), com política p (propagação) em ambas as '
                                     'RIRs.'},
                     {'id': 'q2',
                      'label': '2. No slide 40 de ibd-parte5.pdf, a agregação `Executa` (1:N) liga o '
                               'relacionamento `Participa-de(Empregado, Projeto)` à entidade `Tarefa(CodTar, '
                               'Desc)`. Como `Tarefa` é mapeada?',
                      'options': ['Tarefa(CodTar(nn), Desc, NEmp(nn)) referenciando apenas Empregado[NEmp] '
                                  'com política p (propagação)',
                                  'Tarefa(CodTar(nn), Desc, NProj(nn)) referenciando apenas Projeto[NProj] '
                                  'com política n (nulos)',
                                  'Tarefa(CodTar(nn), Desc, NEmp(nn), NProj(nn)) com RIR Tarefa[NEmp, NProj] '
                                  '-b-> Participa-de[NEmp, NProj]',
                                  'Participa-de(NEmp(nn), NProj(nn), CodTar(nn)) absorvendo CodTar na chave '
                                  'primária de Participa-de'],
                      'answer': 'Tarefa(CodTar(nn), Desc, NEmp(nn), NProj(nn)) com RIR Tarefa[NEmp, NProj] '
                                '-b-> Participa-de[NEmp, NProj]',
                      'explanation': 'Slide 40 de ibd-parte5.pdf: Como cada Tarefa é executada por uma '
                                     'instância da agregação Participa-de (1:N), a chave primária composta '
                                     'de Participa-de (NEmp, NProj) migra como FK para Tarefa com política '
                                     'b.'}]},
 'T7.3': {'title': 'Mapeamento Otimizado de Hierarquias (d vs. o, Total vs. Parcial)',
          'type': 'treino',
          'mode': 'structured',
          'setup': '',
          'fields': [{'id': 'q1',
                      'label': '1. Ao mapear uma hierarquia DISJUNTA e TOTAL de `Empregado(NEmp, Nome, '
                               'Salario)` em `Gerente(SalAd)` e `Tecnico(Formacao)` em uma ÚNICA tabela '
                               '(slide 37 de ibd-parte5.pdf), qual cláusula CHECK garante ambas as '
                               'restrições?',
                      'options': ['CHECK ((SalAd IS NOT NULL AND Formacao IS NOT NULL) OR (SalAd IS NULL AND '
                                  'Formacao IS NULL))',
                                  'CHECK ((SalAd IS NULL AND Formacao IS NULL) OR (SalAd IS NOT NULL AND '
                                  'Formacao IS NOT NULL))',
                                  'CHECK ((SalAd IS NOT NULL OR Formacao IS NOT NULL) AND (SalAd IS NOT NULL '
                                  'AND Formacao IS NOT NULL))',
                                  'CHECK ((SalAd IS NOT NULL AND Formacao IS NULL) OR (SalAd IS NULL AND '
                                  'Formacao IS NOT NULL))'],
                      'answer': 'CHECK ((SalAd IS NOT NULL AND Formacao IS NULL) OR (SalAd IS NULL AND '
                                'Formacao IS NOT NULL))',
                      'explanation': 'Slide 37 de ibd-parte5.pdf: O XOR lógico `(A IS NOT NULL AND B IS '
                                     'NULL) OR (A IS NULL AND B IS NOT NULL)` garante simultaneamente que '
                                     'ninguém tenha ambos (disjunção) e ninguém fique sem nenhum '
                                     '(totalidade).'},
                     {'id': 'q2',
                      'label': "2. No slide 29 de ibd-parte5.pdf, `Part` tem especialização SOBREPOSTA ('o') "
                               'e TOTAL em `Manufactured_Part(DrawingNo, BatchNo)` e '
                               '`Purchased_Part(SupplierName, ListPrice)` usando flags `MFlag` e `PFlag` na '
                               'tabela única. Qual condição deve valer?',
                      'options': ['Apenas uma das flags (MFlag ou PFlag) pode ser verdadeira em cada tupla, '
                                  'proibindo que ambas sejam verdadeiras',
                                  'Pelo menos uma das flags (MFlag ou PFlag) deve ser verdadeira em cada '
                                  'tupla, podendo ambas ser verdadeiras',
                                  'Ambas as flags (MFlag e PFlag) podem ser falsas simultaneamente na mesma '
                                  'tupla da tabela Part',
                                  'Ambas as flags (MFlag e PFlag) devem ser obrigatoriamente verdadeiras em '
                                  'todas as tuplas de Part'],
                      'answer': 'Pelo menos uma das flags (MFlag ou PFlag) deve ser verdadeira em cada '
                                'tupla, podendo ambas ser verdadeiras',
                      'explanation': 'Como a hierarquia de Part é Total (linha dupla), toda peça deve ser '
                                     'fabricada OU comprada (pelo menos uma flag verdadeira). Como é '
                                     "Sobreposta ('o'), uma peça pode ser ambas ao mesmo tempo!"}]},
 'E7.1': {'title': '[Oficial Exame UFMG] Sistema Aéreo: Voo, Trecho_Voo e Aeroporto',
          'type': 'oficial',
          'mode': 'structured',
          'setup': '',
          'fields': [{'id': 'q1',
                      'label': '1. (`ExercicioProjetoLogico.pdf`) `TRECHO_VOO` (chave parcial `Trecho_num`) '
                               'é entidade fraca de `VOO` (chave `Numero`) e possui dois relacionamentos N:1 '
                               '(`AEROPORTO_PARTIDA` e `AEROPORTO_CHEGADA`) com `AEROPORTO`. Qual é o '
                               'esquema relacional de `TRECHO_VOO`?',
                      'options': ['TRECHO_VOO(Trecho_num(nn), Numero_voo(nn), Cod_aero_partida(nn), '
                                  'Cod_aero_chegada(nn), Horario_partida_previsto, Horario_chegada_previsto) '
                                  'com PK simples (Trecho_num)',
                                  'TRECHO_VOO(Numero_voo(nn), Cod_aero_partida(nn), Cod_aero_chegada(nn), '
                                  'Trecho_num(nn), Horario_partida_previsto, Horario_chegada_previsto) com '
                                  'PK (Numero_voo, Cod_aero_partida)',
                                  'TRECHO_VOO(Numero_voo(nn), Trecho_num(nn), Cod_aero_partida(nn), '
                                  'Cod_aero_chegada(nn), Horario_partida_previsto, Horario_chegada_previsto) '
                                  'com PK (Numero_voo, Trecho_num)',
                                  'TRECHO_VOO(Cod_aero_partida(nn), Cod_aero_chegada(nn), Numero_voo, '
                                  'Trecho_num, Horario_partida_previsto, Horario_chegada_previsto) com PK '
                                  '(Cod_aero_partida, Cod_aero_chegada)'],
                      'answer': 'TRECHO_VOO(Numero_voo(nn), Trecho_num(nn), Cod_aero_partida(nn), '
                                'Cod_aero_chegada(nn), Horario_partida_previsto, Horario_chegada_previsto) '
                                'com PK (Numero_voo, Trecho_num)',
                      'explanation': 'Como TRECHO_VOO é entidade fraca de VOO, sua PK é composta por '
                                     '(Numero_voo, Trecho_num) com política p para VOO. E como participa no '
                                     'lado N de AEROPORTO_PARTIDA e AEROPORTO_CHEGADA, recebe duas FKs para '
                                     'AEROPORTO com política b.'},
                     {'id': 'q2',
                      'label': '2. Analise a entidade fraca de 2º nível `INSTANCIA_TRECHO` (chave parcial '
                               '`Data`), identificada por `TRECHO_VOO` via `INSTANCIA_DE`, e ligada N:1 a '
                               '`AERONAVE` (`DESIGNADA`) e a `AEROPORTO` (`PARTIDA` e `CHEGADA`). Qual é a '
                               'sua PK e esquema?',
                      'options': ['PK (Numero_voo, Trecho_num, Data) em INSTANCIA_TRECHO(Numero_voo(nn), '
                                  'Trecho_num(nn), Data(nn), Numero_assentos_disponiveis, Cod_aeronave, '
                                  'Cod_aero_partida, Hora_partida, Cod_aero_chegada, Hora_chegada)',
                                  'PK (Trecho_num, Data) em INSTANCIA_TRECHO(Numero_voo(nn), Trecho_num(nn), '
                                  'Data(nn), Numero_assentos_disponiveis, Cod_aeronave, Cod_aero_partida, '
                                  'Hora_partida, Cod_aero_chegada, Hora_chegada)',
                                  'PK (Numero_voo, Data) em INSTANCIA_TRECHO(Numero_voo(nn), Trecho_num(nn), '
                                  'Data(nn), Numero_assentos_disponiveis, Cod_aeronave, Cod_aero_partida, '
                                  'Hora_partida, Cod_aero_chegada, Hora_chegada)',
                                  'PK (Cod_aeronave, Numero_voo, Data) em INSTANCIA_TRECHO(Cod_aeronave(nn), '
                                  'Data(nn), Numero_voo(nn), Trecho_num(nn), Numero_assentos_disponiveis, '
                                  'Cod_aero_partida, Hora_partida, Cod_aero_chegada, Hora_chegada)'],
                      'answer': 'PK (Numero_voo, Trecho_num, Data) em INSTANCIA_TRECHO(Numero_voo(nn), '
                                'Trecho_num(nn), Data(nn), Numero_assentos_disponiveis, Cod_aeronave, '
                                'Cod_aero_partida, Hora_partida, Cod_aero_chegada, Hora_chegada)',
                      'explanation': 'Em uma cadeia de entidades fracas (VOO -> TRECHO_VOO -> '
                                     'INSTANCIA_TRECHO), a PK de INSTANCIA_TRECHO herda a PK completa de '
                                     'TRECHO_VOO (Numero_voo, Trecho_num) somada à sua chave parcial (Data), '
                                     'além das FKs dos relacionamentos N:1 (DESIGNADA, PARTIDA, CHEGADA).'}]},
 'E7.2': {'title': '[Oficial Exame UFMG] Sistema Aéreo: Aeronave, Tipo_Aeronave e Pode_Pousar',
          'type': 'oficial',
          'mode': 'structured',
          'setup': '',
          'fields': [{'id': 'q1',
                      'label': '1. No diagrama do exame, como deve ser mapeado o relacionamento M:N '
                               '`PODE_POUSAR` entre `AEROPORTO` (`Codigo_aeroporto`) e `TIPO_AERONAVE` '
                               '(`Tipo_nome`)?',
                      'options': ['Adiciona-se a coluna Tipo_nome(nn) como chave estrangeira diretamente na '
                                  'tabela AEROPORTO com política b',
                                  'Adiciona-se a coluna Codigo_aeroporto(nn) como chave estrangeira '
                                  'diretamente na tabela TIPO_AERONAVE com política b',
                                  'Cria-se PODE_POUSAR(Codigo_aeroporto(nn), Tipo_nome(nn)) com PK '
                                  '(Codigo_aeroporto, Tipo_nome) e duas RIRs com política p',
                                  'Cria-se PODE_POUSAR(Codigo_aeroporto(nn), Tipo_nome) com PK simples '
                                  'Codigo_aeroporto e RIR com política n'],
                      'answer': 'Cria-se PODE_POUSAR(Codigo_aeroporto(nn), Tipo_nome(nn)) com PK '
                                '(Codigo_aeroporto, Tipo_nome) e duas RIRs com política p',
                      'explanation': 'Todo relacionamento M:N vira uma tabela própria com chave primária '
                                     'composta pelas chaves das entidades participantes e política de '
                                     'remoção p (propagação) em ambas as RIRs.'},
                     {'id': 'q2',
                      'label': '2. No relacionamento N:1 `TIPO` entre `AERONAVE` (`Cod_aeronave`, lado N com '
                               'participação total) e `TIPO_AERONAVE` (`Tipo_nome`, lado 1), qual é o '
                               'mapeamento otimizado?',
                      'options': ['AERONAVE(Cod_aeronave(nn), Numero_total_assentos, Tipo_nome(nn)) com RIR '
                                  'AERONAVE[Tipo_nome] -b-> TIPO_AERONAVE[Tipo_nome]',
                                  'TIPO_AERONAVE recebe Cod_aeronave(nn) como chave estrangeira com RIR de '
                                  'política p (propagação)',
                                  'AERONAVE(Cod_aeronave(nn), Numero_total_assentos, Tipo_nome) com RIR '
                                  'AERONAVE[Tipo_nome] -n-> TIPO_AERONAVE[Tipo_nome]',
                                  'Fundem-se AERONAVE e TIPO_AERONAVE em uma única relação com chave '
                                  'primária composta (Cod_aeronave, Tipo_nome)'],
                      'answer': 'AERONAVE(Cod_aeronave(nn), Numero_total_assentos, Tipo_nome(nn)) com RIR '
                                'AERONAVE[Tipo_nome] -b-> TIPO_AERONAVE[Tipo_nome]',
                      'explanation': 'Em um relacionamento N:1 com participação total do lado N (linha dupla '
                                     'em AERONAVE), a chave do lado 1 (Tipo_nome) migra como FK NOT NULL '
                                     '(nn) para AERONAVE com política b (bloqueio).'}]},
 'E7.3': {'title': '[Oficial Exame UFMG] Sistema Aéreo: Reserva, Assento e Tarifa',
          'type': 'oficial',
          'mode': 'structured',
          'setup': '',
          'fields': [{'id': 'q1',
                      'label': '1. `ASSENTO` (chave parcial `Numero_assento`) é entidade fraca identificada '
                               'por `INSTANCIA_TRECHO` via relacionamento identificador `RESERVA` (que '
                               'possui os atributos `Nome_cliente` e `Cliente_tel`). Qual o esquema de '
                               '`ASSENTO`?',
                      'options': ['ASSENTO(Numero_assento(nn), Data(nn), Nome_cliente, Cliente_tel) com PK '
                                  'composta de 2 atributos (Data, Numero_assento)',
                                  'ASSENTO(Numero_voo(nn), Numero_assento(nn), Nome_cliente, Cliente_tel) '
                                  'com PK composta de 2 atributos (Numero_voo, Numero_assento)',
                                  'ASSENTO(Trecho_num(nn), Data(nn), Numero_assento(nn), Nome_cliente, '
                                  'Cliente_tel) com PK de 3 atributos (Trecho_num, Data, Numero_assento)',
                                  'ASSENTO(Numero_voo(nn), Trecho_num(nn), Data(nn), Numero_assento(nn), '
                                  'Nome_cliente, Cliente_tel) com PK de 4 atributos e política p'],
                      'answer': 'ASSENTO(Numero_voo(nn), Trecho_num(nn), Data(nn), Numero_assento(nn), '
                                'Nome_cliente, Cliente_tel) com PK de 4 atributos e política p',
                      'explanation': 'ASSENTO é entidade fraca de 3º nível (VOO -> TRECHO_VOO -> '
                                     'INSTANCIA_TRECHO -> ASSENTO). Sua PK acumula a PK completa de '
                                     'INSTANCIA_TRECHO (Numero_voo, Trecho_num, Data) + sua chave parcial '
                                     '(Numero_assento), totalizando 4 atributos na PK!'},
                     {'id': 'q2',
                      'label': '2. `TARIFA` (chave parcial `Codigo`, atributos `Quantidade` e `Restricoes`) '
                               'é entidade fraca identificada por `VOO` (`Numero`) via relacionamento '
                               '`TARIFADO`. Qual é o seu esquema e RIR?',
                      'options': ['TARIFA(Codigo(nn), Numero_voo(nn), Quantidade, Restricoes) com PK simples '
                                  'Codigo e RIR TARIFA[Numero_voo] -b-> VOO[Numero]',
                                  'TARIFA(Numero_voo(nn), Codigo(nn), Quantidade, Restricoes) com PK '
                                  '(Numero_voo, Codigo) e RIR TARIFA[Numero_voo] -p-> VOO[Numero]',
                                  'TARIFA(Numero_voo(nn), Codigo(nn), Quantidade, Restricoes) com PK '
                                  '(Numero_voo, Codigo) e RIR TARIFA[Numero_voo] -n-> VOO[Numero]',
                                  'VOO absorve Codigo, Quantidade e Restricoes como colunas diretas, pois '
                                  'TARIFADO é um relacionamento 1:N'],
                      'answer': 'TARIFA(Numero_voo(nn), Codigo(nn), Quantidade, Restricoes) com PK '
                                '(Numero_voo, Codigo) e RIR TARIFA[Numero_voo] -p-> VOO[Numero]',
                      'explanation': 'TARIFA é entidade fraca de VOO: sua chave primária é composta por '
                                     '(Numero_voo, Codigo) e a RIR para a entidade dona VOO tem '
                                     'obrigatoriamente política p (propagação).'}]},
 'T8.1': {'title': 'Algoritmo de Fechamento de Atributos (X+) e Determinação de Chaves',
          'type': 'treino',
          'mode': 'structured',
          'setup': '',
          'fields': [{'id': 'q1',
                      'label': '1. Dado o esquema R(A, B, C, D) e o conjunto de dependências funcionais F = '
                               '{A -> B, B -> C, C -> D}, qual é o fechamento {A}+ e a classificação de A?',
                      'options': ['{A}+ = {A, B}; logo A não é superchave nem chave candidata mínima de R',
                                  '{A}+ = {A, B, C, D}; A é superchave e chave candidata mínima de R',
                                  '{A}+ = {A, B, C}; logo A é apenas chave parcial dependente de D em R',
                                  '{A}+ = {B, C, D}; logo A atua como chave estrangeira transitiva em R'],
                      'answer': '{A}+ = {A, B, C, D}; A é superchave e chave candidata mínima de R',
                      'explanation': 'Inicia com X+ = {A}. Aplicando o Algoritmo 14.1 (ibd-parte6.pdf): A -> '
                                     'B inclui B; B -> C inclui C; C -> D inclui D. Logo {A}+ = {A, B, C, '
                                     'D}, cobrindo toda a relação R.'},
                     {'id': 'q2',
                      'label': '2. Dado R(A, B, C, D) com F = {A -> B, C -> D}, qual é o fechamento {A}+ e '
                               'qual conjunto forma a única chave candidata de R?',
                      'options': ['{A}+ = {A, B, C, D}; a única chave candidata de R é {A}',
                                  '{A}+ = {A, C}; a única chave candidata de R é {B, D}',
                                  '{A}+ = {A, B}; a única chave candidata de R é {A, B, C}',
                                  '{A}+ = {A, B}; a única chave candidata de R é {A, C}'],
                      'answer': '{A}+ = {A, B}; a única chave candidata de R é {A, C}',
                      'explanation': '{A}+ alcança apenas {A, B}. Como A e C nunca aparecem no lado direito '
                                     'de nenhuma DF, ambos devem fazer parte de qualquer chave candidata. '
                                     'Calculando {A, C}+ obtemos {A, B, C, D}.'}]},
 'T8.2': {'title': 'Diagnóstico de Violações de 2FN e 3FN (Slides ibd-parte6)',
          'type': 'treino',
          'mode': 'structured',
          'setup': '',
          'fields': [{'id': 'q1',
                      'label': '1. A relação `EMP_PROJ(SSN, PNumber, Hours, EName, PName, PLocation)` com PK '
                               'composta `{SSN, PNumber}` e DFs `{SSN, PNumber} -> Hours`, `SSN -> EName`, '
                               '`PNumber -> {PName, PLocation}` viola a 2FN por quê?',
                      'options': ['Porque EName, PName e PLocation dependem parcialmente de subconjuntos '
                                  'próprios da chave primária {SSN, PNumber}',
                                  'Porque Hours depende totalmente da chave composta {SSN, PNumber} em vez '
                                  'de depender apenas de SSN',
                                  'Porque EName depende de PName através de uma dependência funcional '
                                  'transitiva entre atributos não-primos',
                                  'Porque a tabela possui chave primária composta por dois atributos, o que '
                                  'é proibido pela Primeira Forma Normal'],
                      'answer': 'Porque EName, PName e PLocation dependem parcialmente de subconjuntos '
                                'próprios da chave primária {SSN, PNumber}',
                      'explanation': 'Slide 21 de ibd-parte6.pdf: A 2FN exige que todo atributo não-primo '
                                     'seja totalmente dependente da chave candidata inteira (não pode '
                                     'depender apenas de parte da chave composta).'},
                     {'id': 'q2',
                      'label': '2. A relação `EMP_DEPT(SSN, EName, BDate, Address, DNumber, DName, DMgrSSN)` '
                               'com PK simples `SSN` e DFs `SSN -> {EName, BDate, Address, DNumber}` e '
                               '`DNumber -> {DName, DMgrSSN}` está na 2FN, mas viola a 3FN por quê?',
                      'options': ['Porque DName e DMgrSSN dependem parcialmente de uma fração própria da '
                                  'chave primária SSN',
                                  'Porque DNumber é uma chave candidata alternativa que determina o atributo '
                                  'principal SSN',
                                  'Porque DName e DMgrSSN dependem transitivamente da chave SSN via atributo '
                                  'não-chave DNumber',
                                  'Porque os atributos BDate e Address são multivalorados e violam a '
                                  'atomicidade da 1FN em R'],
                      'answer': 'Porque DName e DMgrSSN dependem transitivamente da chave SSN via atributo '
                                'não-chave DNumber',
                      'explanation': 'Slide 24 de ibd-parte6.pdf: Como a PK `SSN` é simples (1 atributo), a '
                                     'relação está automaticamente na 2FN. Porém, `SSN -> DNumber` e '
                                     '`DNumber -> {DName, DMgrSSN}` configura dependência transitiva (viola '
                                     'a 3FN).'}]},
 'T8.3': {'title': 'Axiomas de Armstrong e Conjunto Minimal de Dependências',
          'type': 'treino',
          'mode': 'structured',
          'setup': '',
          'fields': [{'id': 'q1',
                      'label': '1. Dadas as dependências funcionais F = {X -> Y, WY -> Z}, qual regra de '
                               'inferência (slide 18 de ibd-parte6.pdf) permite deduzir diretamente que WX '
                               '-> Z?',
                      'options': ['Regra da Decomposição (RI4)',
                                  'Regra da União / Aditiva (RI5)',
                                  'Regra do Aumento (RI2)',
                                  'Regra Pseudotransitiva (RI6)'],
                      'answer': 'Regra Pseudotransitiva (RI6)',
                      'explanation': 'Slide 18 de ibd-parte6.pdf: A Regra Pseudotransitiva (RI6) estabelece '
                                     'que de {X -> Y, WY -> Z} infere-se WX -> Z.'},
                     {'id': 'q2',
                      'label': '2. Segundo o slide 19 de ibd-parte6.pdf, quais são as 3 condições '
                               'obrigatórias para que um conjunto F de dependências funcionais seja MINIMAL '
                               '(cobertura canônica)?',
                      'options': ['Ter lado esquerdo sempre unitário, possuir no máximo 3 dependências e '
                                  'conter apenas atributos primos no lado direito',
                                  'Ter um único atributo no lado direito de cada DF, não ter atributos '
                                  'redundantes no lado esquerdo e não ter nenhuma DF redundante',
                                  'Ter todos os atributos da chave primária no lado esquerdo de todas as DFs '
                                  'e nenhum atributo estrangeiro no lado direito',
                                  'Estar decomposto em relações binárias onde cada relação possui exatamente '
                                  'uma chave candidata simples e nenhuma transitividade'],
                      'answer': 'Ter um único atributo no lado direito de cada DF, não ter atributos '
                                'redundantes no lado esquerdo e não ter nenhuma DF redundante',
                      'explanation': 'Slide 19 de ibd-parte6.pdf: As 3 condições de um conjunto minimal F '
                                     'são: (1) lado direito com um único atributo; (2) nenhum atributo '
                                     'estranho/redundante no lado esquerdo; (3) nenhuma dependência '
                                     'funcional redundante.'}]},
 'E8.1': {'title': '[Oficial Lista Normalização Q1] Chaves Candidatas em R(A, B, C, D, E)',
          'type': 'oficial',
          'mode': 'structured',
          'setup': '',
          'fields': [{'id': 'q1',
                      'label': '1. (Questão 1 da Lista Oficial) Considere R(A, B, C, D, E) com as '
                               'dependências funcionais AB -> C e CD -> E. AB é chave candidata dessa '
                               'relação? Se não, ABD é?',
                      'options': ['Sim, AB é chave candidata porque {AB}+ = {A, B, C, D, E}; logo ABD é '
                                  'apenas uma superchave não-mínima',
                                  'Não, AB não é chave ({AB}+ = {A, B, C}), e ABD também não é chave porque '
                                  '{AD}+ já determina todos os atributos',
                                  'Não, AB não é chave ({AB}+ = {A, B, C}); já ABD É chave candidata mínima '
                                  'pois {ABD}+ = {A, B, C, D, E}',
                                  'Sim, tanto AB quanto ABD são chaves candidatas mínimas equivalentes para '
                                  'o esquema R(A, B, C, D, E)'],
                      'answer': 'Não, AB não é chave ({AB}+ = {A, B, C}); já ABD É chave candidata mínima '
                                'pois {ABD}+ = {A, B, C, D, E}',
                      'explanation': 'Calculando o fechamento: {AB}+ = {A, B, C} (não alcança D nem E). Como '
                                     'A, B e D nunca aparecem no lado direito de nenhuma DF, toda chave '
                                     'candidata deve conter {A, B, D}. E {ABD}+ = {A, B, C, D, E}, sendo '
                                     'mínima!'}]},
 'E8.2': {'title': '[Oficial Lista Normalização Q2] Decomposição em 2FN e 3FN de R(A..J)',
          'type': 'oficial',
          'mode': 'structured',
          'setup': '',
          'fields': [{'id': 'q1',
                      'label': '1. (Questão 2 da Lista Oficial) Dada R(A, B, C, D, E, F, G, H, I, J) com F = '
                               '{AB -> C, A -> DE, B -> F, F -> GH, D -> IJ}, qual é a chave candidata de R?',
                      'options': ['{A, B}, pois {AB}+ = {A, B, C, D, E, F, G, H, I, J} e nem {A}+ nem {B}+ '
                                  'cobrem R',
                                  '{A, B, D, F}, pois todos os determinantes devem compor a chave primária',
                                  '{A, B, C}, pois C depende diretamente do par inicial {A, B} na primeira '
                                  'dependência',
                                  '{D, F}, pois D determina {I, J} e F determina {G, H} por transitividade'],
                      'answer': '{A, B}, pois {AB}+ = {A, B, C, D, E, F, G, H, I, J} e nem {A}+ nem {B}+ '
                                'cobrem R',
                      'explanation': 'A e B são os únicos atributos que nunca aparecem no lado direito de '
                                     'nenhuma DF em F. Calculando {AB}+: AB->C, A->DE, D->IJ, B->F, F->GH => '
                                     '{AB}+ cobre todos os 10 atributos!'},
                     {'id': 'q2',
                      'label': '2. Na Questão 2, qual é a decomposição correta de R para a Segunda Forma '
                               'Normal (2FN), eliminando apenas as dependências parciais em relação à chave '
                               '{A, B}?',
                      'options': ['R1(A, B, C, D, E) com PK {A, B}  e  R2(B, F, G, H, I, J) com PK simples '
                                  '{B}',
                                  'R1(A, B, C) com PK {A, B},  R2(A, D, E, F) com PK {A}  e  R3(B, G, H, I, '
                                  'J) com PK {B}',
                                  'R1(A, B, C) com PK {A, B},  R2(A, D, E, I, J) com PK {A}  e  R3(B, F, G, '
                                  'H) com PK {B}',
                                  'R1(A, B, C) com PK {A, B},  R2(D, E, I, J) com PK {D}  e  R3(F, G, H) com '
                                  'PK simples {F}'],
                      'answer': 'R1(A, B, C) com PK {A, B},  R2(A, D, E, I, J) com PK {A}  e  R3(B, F, G, H) '
                                'com PK {B}',
                      'explanation': 'Para passar da 1FN para a 2FN, extraímos o fechamento de cada '
                                     'subconjunto próprio da chave {A, B}: de A saem {D, E, I, J} formando '
                                     'R2(A, D, E, I, J); de B saem {F, G, H} formando R3(B, F, G, H); e em '
                                     'R1 resta (A, B, C).'},
                     {'id': 'q3',
                      'label': '3. Ainda na Questão 2, decompondo as relações da 2FN para a Terceira Forma '
                               'Normal (3FN) para eliminar as dependências transitivas D -> IJ e F -> GH, '
                               'obtemos:',
                      'options': ['R1(A, B, C),  R21(A, D, E),  R22(D, I, J),  R31(B, F),  R32(F, G, H) — '
                                  'mantendo FKs D em R21 e F em R31',
                                  'R1(A, B, C),  R21(A, E),  R22(D, I, J),  R31(B),  R32(F, G, H) — '
                                  'eliminando as colunas D de R21 e F de R31',
                                  'R1(A, B, C),  R21(A, D, I),  R22(E, J),  R31(B, G),  R32(F, H) — '
                                  'dividindo os atributos não-primos igualmente',
                                  'R1(A, B, C, D, F),  R2(D, E, I, J),  R3(F, G, H) — migrando os '
                                  'determinantes transitivos D e F para a tabela R1'],
                      'answer': 'R1(A, B, C),  R21(A, D, E),  R22(D, I, J),  R31(B, F),  R32(F, G, H) — '
                                'mantendo FKs D em R21 e F em R31',
                      'explanation': 'Em R2(A, D, E, I, J), D -> IJ é transitiva: separamos R22(D, I, J) com '
                                     'PK D e mantemos D como FK em R21(A, D, E). Em R3(B, F, G, H), F -> GH '
                                     'é transitiva: separamos R32(F, G, H) com PK F e mantemos F como FK em '
                                     'R31(B, F).'}]},
 'E8.3': {'title': '[Oficial Lista Normalização Q3] Sistema Acadêmico de Cursos e Turmas',
          'type': 'oficial',
          'mode': 'structured',
          'setup': '',
          'fields': [{'id': 'q1',
                      'label': '1. (Questão 3 da Lista Oficial) Dada R(CourseNo, SecNo, OfferDept, '
                               'CredHours, CourseLevel, ISSN, Sem, Year, Days_Hours, RoomNo, NoOfStuds) com '
                               'DF1: {CourseNo} -> {OfferDept, CredHours, CourseLevel}, DF2: {CourseNo, '
                               'SecNo, Sem, Year} -> {Days_Hours, RoomNo, NoOfStuds, ISSN}, e DF3: {RoomNo, '
                               'Days_Hours, Sem, Year} -> {ISSN, CourseNo, SecNo}. Quais são as chaves '
                               'candidatas de R?',
                      'options': ['Apenas uma chave candidata: K1 = {CourseNo, SecNo, Sem, Year}',
                                  'Apenas uma chave candidata: K2 = {CourseNo, RoomNo, Days_Hours}',
                                  'Três chaves candidatas: {CourseNo}, {CourseNo, SecNo, Sem, Year} e '
                                  '{RoomNo, Days_Hours, Sem, Year}',
                                  'Duas chaves candidatas: K1 = {CourseNo, SecNo, Sem, Year} e K2 = {RoomNo, '
                                  'Days_Hours, Sem, Year}'],
                      'answer': 'Duas chaves candidatas: K1 = {CourseNo, SecNo, Sem, Year} e K2 = {RoomNo, '
                                'Days_Hours, Sem, Year}',
                      'explanation': '{CourseNo, SecNo, Sem, Year}+ fecha nos 11 atributos (via DF2 e DF1). '
                                     'Além disso, {RoomNo, Days_Hours, Sem, Year}+ determina {ISSN, '
                                     'CourseNo, SecNo} via DF3, e a partir daí determina todos os demais via '
                                     'DF1 e DF2! Logo ambas são chaves candidatas mínimas.'},
                     {'id': 'q2',
                      'label': '2. Decompondo a relação R da Questão 3 para 2FN e 3FN, como ficam as '
                               'relações resultantes?',
                      'options': ['R1(CourseNo, SecNo, OfferDept, CredHours, CourseLevel) com PK (CourseNo, '
                                  'SecNo), e R2(CourseNo, Sem, Year, ISSN, Days_Hours, RoomNo, NoOfStuds) '
                                  'com PK (CourseNo, Sem, Year) e chave alternativa (RoomNo, Days_Hours, '
                                  'Sem, Year)',
                                  'R1(CourseNo, OfferDept, CredHours, CourseLevel) com PK CourseNo, e '
                                  'R2(CourseNo, SecNo, Sem, Year, ISSN, Days_Hours, RoomNo, NoOfStuds) com '
                                  'PK (CourseNo, SecNo, Sem, Year) e chave alternativa (RoomNo, Days_Hours, '
                                  'Sem, Year)',
                                  'R1(CourseNo, OfferDept, ISSN, CredHours) com PK CourseNo, R2(CourseLevel, '
                                  'NoOfStuds) com PK CourseLevel, e R3(CourseNo, SecNo, Sem, Year, '
                                  'Days_Hours, RoomNo) com PK composta (CourseNo, SecNo, Sem, Year) e FK '
                                  'para R1',
                                  'R1(OfferDept, CredHours, CourseLevel) com PK OfferDept, e R2(CourseNo, '
                                  'SecNo, Sem, Year, ISSN, Days_Hours, RoomNo, NoOfStuds) com PK (RoomNo, '
                                  'Days_Hours, Sem, Year) e chave alternativa composta (CourseNo, SecNo, '
                                  'Sem, Year)'],
                      'answer': 'R1(CourseNo, OfferDept, CredHours, CourseLevel) com PK CourseNo, e '
                                'R2(CourseNo, SecNo, Sem, Year, ISSN, Days_Hours, RoomNo, NoOfStuds) com PK '
                                '(CourseNo, SecNo, Sem, Year) e chave alternativa (RoomNo, Days_Hours, Sem, '
                                'Year)',
                      'explanation': '{CourseNo} -> {OfferDept, CredHours, CourseLevel} é dependência '
                                     'parcial da chave K1 (e transitiva em relação a K2). Ao decompor em '
                                     'R1(CourseNo, OfferDept, CredHours, CourseLevel) e R2(CourseNo, SecNo, '
                                     'Sem, Year, ISSN, Days_Hours, RoomNo, NoOfStuds), ambas as relações '
                                     'ficam na 2FN e na 3FN!'}]}}

from round1_exercises import ROUND1_EXERCISES
EXERCISES_DATA.update(ROUND1_EXERCISES)

from round2_exercises import ROUND2_EXERCISES
EXERCISES_DATA.update(ROUND2_EXERCISES)

from round3_exercises import ROUND3_EXERCISES
EXERCISES_DATA.update(ROUND3_EXERCISES)

from round4_exercises import ROUND4_EXERCISES
EXERCISES_DATA.update(ROUND4_EXERCISES)


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

