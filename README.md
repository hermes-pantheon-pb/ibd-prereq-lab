# IBD Prerequisite Studio & Exam Mastery 🏛️
> Laboratório Interativo, Visual e Prático para **Modelagem Conceitual (ER/EER), Mapeamento Relacional e Normalização de Banco de Dados** (DCC222 / DCC011 - UFMG - Prof. Marcos André Gonçalves).

---

## ⚡ Guia Rápido de Execução (Computador Pessoal ou Laboratório Universitário)

Este laboratório foi construído especificamente para rodar em computadores de **laboratórios de faculdade (Linux, Windows ou macOS) sem privilégios de administrador (sem `root` / sem `sudo`)** e sem necessidade de conexão com a internet após o download:

- ❌ **Sem `pip install`:** Não precisa instalar nenhuma biblioteca externa (utiliza 100% a biblioteca padrão do Python 3).
- ❌ **Sem permissão de `root` / `sudo`:** Roda inteiramente no espaço de usuário (`/home/aluno` ou Desktop).
- ❌ **Sem banco externo instalado:** O SQLite roda em memória e no próprio processo padrão do Python.
- ⚡ **Detecção Automática de Porta Livre:** Se a porta padrão `8080` estiver ocupada por outro aluno ou bloqueada por firewall local, o servidor detecta automaticamente e sobe na próxima porta livre (`8081`, `8082`, etc.).

---

### Opção A: Executar via Terminal (Linux / macOS / Windows PowerShell)

```bash
# 1. Clonar o repositório (ou descompactar o arquivo .zip)
git clone https://github.com/hermes-pantheon-pb/ibd-prereq-lab.git
cd ibd-prereq-lab

# 2. Iniciar o servidor (qualquer Python 3.8+ serve)
python3 web_server.py
```

No Windows (PowerShell / Prompt):
```powershell
python web_server.py
```

O terminal exibirá a URL pronta:
```text
=================================================================
 🏛️  IBD Prerequisite & Exam Studio (DCC222 / DCC011 - UFMG)
=================================================================
 ✔ Modo de execução: Usuário Comum / Laboratório Universitário
 ✔ Interface Web ativa em: http://localhost:8080
 ✔ Pressione Ctrl + C para encerrar o servidor.
=================================================================
```

Abra o navegador e acesse:
👉 **`http://localhost:8080`**

---

### Opção B: Caso você não tenha `git` no laboratório (Download Direto)

Se a máquina do laboratório não tiver `git` instalado ou bloquear conexões SSH/Git:
1. Baixe o código como ZIP:
   👉 Clique em **Code $\rightarrow$ Download ZIP** em [https://github.com/hermes-pantheon-pb/ibd-prereq-lab](https://github.com/hermes-pantheon-pb/ibd-prereq-lab)
2. Extraia a pasta em qualquer diretório local.
3. Dê dois cliques em `web_server.py` ou execute `python3 web_server.py` no terminal.

---

### Opção C: Uso Direto pelo Terminal / Modo CLI (Sem abrir navegador)

Se você preferir praticar ou debugar direto no shell do Linux da universidade:

```bash
# Listar todos os 34 exercícios do currículo e seus modos
python3 db_engine.py list

# Inspecionar esquemas de tabelas e tuplas de teste
python3 db_engine.py schema T5.1
```

---

## 🗺️ Guia de Simbologia ER e Transformação em Relações

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
