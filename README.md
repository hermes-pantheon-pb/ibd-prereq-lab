# IBD Prerequisite Studio & Exam Mastery 🏛️
> Laboratório Interativo, Visual e Prático para **Modelagem Conceitual (ER/EER), Mapeamento Relacional e Normalização de Banco de Dados** (DCC222 / DCC011 - UFMG - Prof. Marcos André Gonçalves).

Este repositório cobre todo o conteúdo curricular exigido até o exame de **Projeto Lógico e Normalização**, integrando:
1. **Simbologia Visual Completa do Esquema ER/EER** e suas regras formais de transformação para esquemas relacionais.
2. **Resoluções e Testes Interativos das Listas Oficiais** (`exercicios_modelo_relacional.pdf`, `ExercERRequisitos600.pdf`, `consultas_ProfMarcosG.pdf`, `ExercicioProjetoLogico.pdf` e `ExerciciosNormalizacaoSemResposta.pdf`).
3. **Motor de Injeção de Falhas em DDL** e **Transpilador ANSI SQL-92 `CREATE ASSERTION`**.
4. **Algoritmo de Fechamento de Atributos ($X^+$) e Decomposição em 1FN, 2FN e 3FN**.

---

## 🗺️ Guia de Simbologia ER e Mapeamento para Relações

### 1. Entidades e Atributos

| Símbolo Gráfico no ER | Conceito Semântico | Exemplo nos Slides | Como Mapeia para Relações |
|:---|:---|:---|:---|
| **Retângulo Simples** | **Tipo de Entidade Forte** (independente) | `Empregado`, `Departamento`, `Voo` | Vira uma **relação própria**: $R(A_1, \dots, A_n)$ com $PK$ igual à chave da entidade. |
| **Retângulo Duplo** | **Tipo de Entidade Fraca** (sem chave própria) | `Dependente` (dono `Empregado`), `Trecho_Voo` (dono `Voo`) | Vira relação cuja $PK$ é composta: **$(PK_{dono}, ChaveParcial)$**, com $RIR: W[PK_{dono}] \xrightarrow{p} E[PK_{dono}]$ (**política $p$ / CASCADE**). |
| **Elipse Simples** | **Atributo Simples / Atômico** | `NomeEmp`, `Salario`, `Numero` | Vira uma **coluna** na tabela. |
| **Elipse Sublinhada (Linha Contínua)** | **Chave Primária da Entidade** | `SSN`, `DNumber`, `Codigo_aeroporto` | Vira a **`PRIMARY KEY`** da tabela. |
| **Elipse Sublinhada (Tracejada)** | **Chave Parcial (Discriminador)** | `Dependent_Name` em Dependente, `Trecho_num` em Trecho_Voo | Vira parte da chave primária composta da entidade fraca. |
| **Elipse com Ramificações** | **Atributo Composto** | `Endereço` ($\rightarrow$ Rua, Número, Bairro, CEP) | Apenas os **atributos folha simples** viram colunas na tabela. O pai não vira coluna. |
| **Elipse de Linha Dupla** | **Atributo Multivalorado** | `Localizações` de Depto, múltiplos telefones | **Vira uma NOVA relação**: $R_{multi}(PK_{dono}, Atributo)$ com $PK$ composta e política $p$ (CASCADE). |
| **Elipse Tracejada** | **Atributo Derivado** | `Idade` (de DataNasc), `NumEmpregados` | **Não vira coluna** (é calculado via `SELECT COUNT` ou view). |

---

### 2. Relacionamentos e Cardinalidades

| Símbolo Gráfico | Conceito Semântico | Notação Tradicional vs. $(min, max)$ | Como Mapeia para Relações |
|:---|:---|:---|:---|
| **Losango Simples** | **Relacionamento Comum** entre entidades fortes | `Trabalha_para`, `Gerencia` | Depende da cardinalidade ($1:1$, $N:1$ ou $M:N$). |
| **Losango Duplo** | **Relacionamento Identificador** | `Possui` (liga Empregado a Dependente), `Trechos` (Voo a Trecho_Voo) | Conecta a entidade fraca ao seu dono (sempre participação total / $min=1$ da fraca). |
| **Linha Simples** | **Participação Parcial** | $min = 0$ ao lado da entidade | A chave estrangeira pode assumir `NULL`. |
| **Linha Dupla** | **Participação Total** (Existência Obrigatória) | $min \ge 1$ ao lado da entidade | A chave estrangeira deve ser `NOT NULL` (ou restrição estrutural de igualdade). |
| **Cardinalidade $N:1$** | **Muitos para Um** | $N$ em Empregado, $1$ em Depto (ou Empregado com $(1,1)$, Depto com $(1,N)$) | **Mapeamento Otimizado**: a $PK$ do lado 1 migra como $FK$ para a relação do lado N. |
| **Cardinalidade $M:N$** | **Muitos para Muitos** | $M$ em Empregado, $N$ em Projeto (`WORKS_ON`) | **Vira uma NOVA relação**: $R_{rel}(PK_1, PK_2, AtributosRel)$ com $PK = (PK_1, PK_2)$ e políticas $p$ em ambas as FKs. |
| **Linha com Papéis (Recursivo)** | **Auto-Relacionamento** | Papel 1 (Supervisor), Papel 2 (Supervisionado) | Migra como $FK$ na mesma tabela referenciando a si própria (`SUPERSSN REFERENCES EMPLOYEE(SSN) ON DELETE SET NULL`). |

---

### 3. Especialização / Generalização (EER)

| Símbolo Gráfico | Conceito | Condição em Álgebra Relacional | Mapeamento em SQL |
|:---|:---|:---|:---|
| **Círculo com 'd' (Disjunta)** | Subclasses mutuamente exclusivas | $\pi_{PK}(S_1) \cap \pi_{PK}(S_2) = \emptyset$ | Em tabela única: `CHECK (NOT (A IS NOT NULL AND B IS NOT NULL))` |
| **Círculo com 'o' (Sobreposta)** | Pode pertencer a múltiplas subclasses | Interseção pode ser não-vazia | Em tabela única: colunas independentes sem exclusão mútua |
| **Linha Dupla (Total)** | Toda tupla da superclasse é subclasse | $\bigcup \pi_{PK}(S_i) = \pi_{PK}(Super)$ | `CHECK (A IS NOT NULL OR B IS NOT NULL)` ou `CREATE ASSERTION` |
| **Linha Simples (Parcial)** | Pode não ser nenhuma subclasse | $\bigcup \pi_{PK}(S_i) \subset \pi_{PK}(Super)$ | Atributos específicos aceitam nulos sem obrigatoriedade |

---

## 📚 Estrutura Completa dos 8 Módulos do Curso

| Módulo | Tema Curricular | Tipo de Exercícios | Arquivos Oficiais Cobertos |
|:---|:---|:---|:---|
| **1. Arquitetura e Independência** | 3 Níveis ANSI/SPARC, Esquema (*Intensão*) vs. Instância (*Extensão*), Independência Lógica vs. Física | Diagnóstico Estruturado | `01-introducao.pdf` |
| **2. Modelo ER e Cardinalidades** | Atributos, Pegadinha $1:N$ vs. $(min, max)$, Entidades Fracas e Chave Parcial | Comparativo Estruturado | `ibd-parte2.pdf` (Esquema COMPANY) |
| **3. Modelo EER e Notação UML** | Hierarquias ($d/o$, Total/Parcial), Lattices, Ternários vs. 3 Binários, Qualificadores UML | Diagnóstico + Caso Real | `ibd-parte2.pdf` + `ExercERRequisitos600.pdf` (Georgia Tech Library) |
| **4. Modelo Relacional e RIR** | Superchaves, Chaves Candidatas, Integridade de Entidade, RIR formal e Políticas ($b, p, n$) | Formalismo Relacional | `ibd-parte3.pdf` + `exercicios_modelo_relacional.pdf` |
| **5. Álgebra Relacional Avançada** | União-Compatibilidade, Divisão Relacional ($\div$), Fórmulas Algébricas de Restrições Estruturais | Consultas SQL + AR | `ibd-parte3.pdf` + `consultas_ProfMarcosG.pdf` |
| **6. SQL para Projeto Lógico** | DDL Completo (`ON DELETE`), `CHECK` de Tupla, Visões (Modificação de Consulta), Asserções Gerais | Injeção de Falhas + Asserções | `ibd-parte4_without_obs.pdf` + `consultas_ProfMarcosG.pdf` |
| **7. Mapeamento ER/EER $\rightarrow$ Relacional** | 7 Regras de Mapeamento, Migração de FKs, Agregações e Mapeamento de Hierarquias | Mapeamento Formal | `ibd-parte5.pdf` + `ExercicioProjetoLogico.pdf` (Sistema Aéreo) |
| **8. Normalização de Dados** | Anomalias de Atualização, Fechamento de Atributos ($X^+$), Chaves Candidatas, 1FN, 2FN e 3FN | Decomposição Algébrica | `ibd-parte6.pdf` + `ExerciciosNormalizacaoSemResposta.pdf` (Q1, Q2, Q3) |

---

## 🚀 Como Executar Localmente

O estúdio não possui dependências de terceiros (utiliza apenas Python 3 nativo):

```bash
# 1. Entrar na pasta do projeto
cd ibd-prereq-lab

# 2. Iniciar o servidor local na porta 8080 (ou PORT=8081 python3 web_server.py)
python3 web_server.py
```

Acesse em seu navegador:
👉 **`http://localhost:8080`**

---

## 🛠️ CLI de Teste Rápido

Você também pode inspecionar e testar consultas e esquemas via linha de comando:

```bash
# Listar todos os 34 exercícios do currículo
python3 db_engine.py list

# Inspecionar esquemas e dados de teste
python3 db_engine.py schema T5.1
```
