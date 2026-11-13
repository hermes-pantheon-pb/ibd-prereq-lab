# 🏛️ IBD Exam Mastery — Multi-Round Question Bank Roadmap (Módulos 7 & 8)

Este documento registra as diretrizes pedagógicas, padrões técnicos de qualidade e o planejamento em rodadas (10 questões por rodada) para a prova final de **Projeto Lógico (Módulo 7)** e **Projeto Relacional & Normalização (Módulo 8)** da disciplina **DCC011 / DCC222 (UFMG — Prof. Marcos André Gonçalves)**.

---

## 📌 Diretrizes Obrigatórias para Todas as Rodadas (Quality Invariants)

1. **Ritmo de 10 Exercícios por Rodada:**
   - Cada rodada adiciona exatamente **10 exercícios de alta profundidade** (`R1.1`–`R1.10`, `R2.1`–`R2.10`, `R3.1`–`R3.10`, etc.), divididos equilibradamente entre **Módulo 7 (Projeto Lógico: Mapeamento ER/EER $\to$ Relacional)** e **Módulo 8 (Normalização: DFs, Fecho $X^+$, Cobertura Mínima, 1FN/2FN/3FN/BCNF)**.
2. **Diversificação de Métodos de Avaliação:**
   - **Diagramas ER/EER Reais (SVG nativo no enunciado):** Questões de mapeamento exibem diagramas ER/EER reais (baseados em bancos de questões acadêmicos: *Elmasri & Navathe*, *Silberschatz*, provas da UFMG/USP/UNICAMP) usando a notação exata dos slides (`(min, max)` ou `1:N`, retângulos duplos para entidades fracas, sublinhado tracejado para chave parcial, elipses duplas/ramificadas, círculos `d`/`o` com linha simples/dupla).
   - **Caderno de Resolução Discursiva (Scratchpad) + Folha de Gabarito Oficial (`answer_sheet_html`):** Para problemas abertos ou de múltiplas etapas (como escrever todo o esquema lógico `R(A(nn), B)` com `RIRs` `-b-> / -p-> / -n->`, desenhar/ler transformações ou decompor passo a passo 1FN $\to$ 2FN $\to$ 3FN), o aluno dispõe de um **Caderno de Rascunho** persistente e de um botão **"🔑 Ver Folha de Gabarito Completa (Answer Sheet)"** com a resolução comentada passo a passo.
   - **Execução SQL DDL com Injeção de Falhas (`sql_ddl`):** Tradução direta de esquemas ER/EER para `CREATE TABLE` validada por testes automatizados de integridade.
   - **Auditoria de Instâncias com SQL (`sql_query`):** Detecção prática de tuplas violadoras de Dependências Funcionais $X \to Y$ sobre extensões reais de tabelas.
   - **Checkpoints Estruturados Balanceados (`structured`):**
     - **Posição da resposta correta:** Distribuída de forma estritamente uniforme entre os índices `{0, 1, 2, 3}` (25% em cada opção).
     - **Paridade visual e formal dos distratores:** Todas as 4 alternativas devem possuir a mesma estrutura gramatical, mesma notação formal (`(nn)`, `-b->`, `-p->`, `-n->`, `PK`, `X+`) e comprimentos de caracteres equivalentes (diferença máxima $\le 5$ caracteres em relação ao maior distrator).
3. **Ficha de Estudo / Cheat Sheet Dedicada com Exemplo Análogo (`study_guide` + `study_guides/*.md`):**
   - Cada questão ou grupo coeso de questões possui uma **Ficha de Estudo** vinculada contendo:
     1. **Referência Exata ao Material da Disciplina:** Qual arquivo PDF (`ibd-parte5.pdf`, `ExercicioProjetoLogico.pdf`, `ibd-parte6.pdf`, `ExerciciosNormalizacaoSemResposta.pdf`) e qual seção/regra fundamenta a questão.
     2. **Resumo das Regras Formais:** Tabela ou algoritmo direto ao ponto.
     3. **Exemplo Resolvido Passo a Passo com Objetos de Domínio Diferente:** Demonstra a aplicação exata da regra em um mini-mundo diferente daquele cobrado no exercício.

---

## ✅ Rodada 1 (`R1.1` a `R1.10`) — Status: CONCLUÍDA

### Grupo 1 (`R1.1` – `R1.3`): Mapeamento ER Básico, Entidades Fracas e Políticas de RIR (`b, p, n`)
- **Arquivo de Estudo:** `study_guides/G1_Mapeamento_ER_Basico_e_RIRs.md`
  - *Base nos Slides:* `ibd-parte5.pdf` (Etapa 1: Regras 1 a 6 e Políticas de Remoção `b`, `p`, `n`).
  - *Exemplo Análogo na Ficha:* **Rede Bancária (`BANCO`, `AGENCIA` fraca, `CLIENTE`, `CONTA`, `EMPRESTIMO`)** (Elmasri Cap. 7/9).
- **Domínio dos Exercícios (`R1.1`–`R1.3`):** **Sistema Hospitalar & Prontuário Clínico (`ALA_HOSPITALAR`, `MEDICO`, `PACIENTE`, `EXAME_LABORATORIAL`)** com Diagrama ER SVG completo.
  - **`R1.1` (`structured` + Scratchpad + Answer Sheet):** Mapeamento de entidades fortes, atributo composto (`Endereco`), atributo multivalorado (`Especialidades`) e entidade fraca (`EXAME_LABORATORIAL` com chave parcial `NumSeqExame`).
  - **`R1.2` (`structured` + Scratchpad + Answer Sheet):** Mapeamento de relacionamentos `1:1` (`CHEFIADA_POR`), `1:N` (`INTERNADO_EM`) e `M:N` (`PRESCRICAO`) e escolha de políticas de remoção `-b->`, `-p->`, `-n->`.
  - **`R1.3` (`sql_ddl` + Answer Sheet):** Implementação prática em SQL DDL do núcleo hospitalar com `PRIMARY KEY` composta e `ON DELETE RESTRICT / CASCADE` validada por bateria de injeção de falhas.

### Grupo 2 (`R1.4` – `R1.5`): Mapeamento EER — Hierarquias (`d`/`o`, Total/Parcial) e Relacionamentos Ternários
- **Arquivo de Estudo:** `study_guides/G2_Mapeamento_EER_Hierarquias_e_Ternarios.md`
  - *Base nos Slides:* `ibd-parte5.pdf` (Etapa 2: Opções 1, 2 e 3 para Hierarquias de Especialização/Generalização, Cláusula `CHECK` e Relacionamentos de Grau $\ge 3$).
  - *Exemplo Análogo na Ficha:* **Frota Marítima (`EMBARCACAO` $\to$ `{PETROLEIRO, PORTA_CONTENTOR}` e Ternário `ATRACACAO`)**.
- **Domínio dos Exercícios (`R1.4`–`R1.5`):** **Pós-Graduação & Pesquisa Universitária (`PESSOA` $\to$ `{DOCENTE, ALUNO_POS}`, `BOLSA_PESQUISA` $\to$ `{MESTRADO, DOUTORADO}`, Ternário `BANCA_DEFESA`)** com Diagrama EER SVG completo.
  - **`R1.4` (`structured` + Scratchpad + Answer Sheet):** Comparação e aplicação das Opções 1, 2 e 3 nas duas hierarquias EER e mapeamento do relacionamento ternário `BANCA_DEFESA`.
  - **`R1.5` (`sql_ddl` + Answer Sheet):** Implementação SQL DDL da Opção 1 (Tabela Única `BOLSA_PESQUISA`) com cláusula `CHECK` garantindo disjunção (`d`) e totalidade entre bolsas de Mestrado e Doutorado.

### Grupo 3 (`R1.6` – `R1.7`): Dependências Funcionais em Instâncias, Axiomas de Armstrong e Fecho $X^+$
- **Arquivo de Estudo:** `study_guides/G3_Dependencias_Funcionais_Instancias_e_Fecho.md`
  - *Base nos Slides:* `ibd-parte6.pdf` (Seções 1, 2 e 3: Semântica de DFs, Satisfação/Refutação em Extensões $r(R)$, Regras de Inferência e Algoritmo de Fecho $X^+$ para Múltiplas Chaves Candidatas).
  - *Exemplo Análogo na Ficha:* **Circulação de Biblioteca (`EMPRESTIMO_ACERVO`) e Método de Particionamento de Atributos (Esquerda / Meio / Direita)**.
- **Domínio dos Exercícios (`R1.6`–`R1.7`):** **Escala de Navios (`ESCALA_NAVIO`) e Esquema Formal Multicandidato $R(A,B,C,D,E,G)$**.
  - **`R1.6` (`sql_query` + Answer Sheet):** Detetive de DFs em instância populada `ESCALA_NAVIO` — consulta SQL para encontrar pares de tuplas que refutam uma DF proposta (`NomeNavio -> Comandante`) + análise completa na Folha de Gabarito.
  - **`R1.7` (`structured` + Scratchpad + Answer Sheet):** Cálculo de Fecho $X^+$, descoberta de todas as chaves candidatas ($\{A,B\}, \{B,C\}, \{B,D\}$) e classificação de atributos primos vs. não-primos em $R(A,B,C,D,E,G)$.

### Grupo 4 (`R1.8` – `R1.10`): Cobertura Mínima (Irredutível) e Normalização 1FN $\to$ 2FN $\to$ 3FN
- **Arquivo de Estudo:** `study_guides/G4_Cobertura_Minima_e_Normalizacao_1FN_2FN_3FN.md`
  - *Base nos Slides:* `ibd-parte6.pdf` (Seção 3.4: Cobertura Mínima em 3 Passos; Seção 4: 1FN, 2FN, 3FN — Definição Básica e Definição Geral) e `ExerciciosNormalizacaoSemResposta.pdf`.
  - *Exemplo Análogo na Ficha:* **Festival de Música (`SHOW_PALCO`)** — cálculo completo de cobertura mínima e decomposição passo a passo até 3FN.
- **Domínio dos Exercícios (`R1.8`–`R1.10`):**
  - **`R1.8` (`structured` + Scratchpad + Answer Sheet):** Derivação algorítmica da Cobertura Mínima $F_c$ nos 3 passos formais (Lado direito simples, Remoção de atributo estranho no lado esquerdo via fecho, Remoção de DF redundante via fecho em $F - \{f\}$).
  - **`R1.9` (`structured` + Scratchpad + Answer Sheet):** Estudo de caso clássico Elmasri (`CAR_SALE` & `PEDIDO_COMPRA`) — eliminação de atributos multivalorados/aninhados (1FN), dependências parciais (2FN) e transitivas (3FN).
  - **`R1.10` (`structured` + Scratchpad + Answer Sheet):** Decomposição completa 1FN $\to$ 2FN $\to$ 3FN pela **Definição Geral** (múltiplas chaves candidatas) no esquema `SESSAO_CONGRESSO(CodTrilha, NumSessao, Sala, Horario, CPFPalestrante, NomePalestrante, FilialPatrocinador, OrcamentoTrilha, CapacidadeSala)`.

---

## ✅ Rodada 2 (`R2.1` a `R2.10`) — CONCLUÍDA E INTEGRADA AO LAB

### Grupo 5 (`R2.1` – `R2.3`): Recursividade, Cadeias de Entidades Fracas & Agregação/Reticulado EER
- **Arquivo de Estudo:** `study_guides/G5_Recursividade_CadeiasFracas_e_AgregacaoEER.md`
  - *Base nos Slides:* `ibd-parte5.pdf` (Etapa 1/4/5 auto-relacionamentos, Etapa 2 entidades fracas em cadeia, Slide 40 Agregação EER & Subclasses Compartilhadas).
  - *Exemplos Análogos na Ficha:* **Grade Curricular (`DISCIPLINA`)**, **Copa Esportiva (`TORNEIO` -> `FASE` -> `PARTIDA`)** e **Consultoria (`ATUA_EM` -> `APONTAMENTO`)**.
- **Domínio dos Exercícios (`R2.1`–`R2.3`):**
  - **`R2.1` (`structured` + Diagrama SVG):** Recursividade `M:N` (`PECA` / `COMPOE`) e `1:N` (`ENGENHEIRO` / `SUPERVISIONA`) com renomeação por papéis.
  - **`R2.2` (`sql_ddl` + Diagrama SVG):** Implementação SQLite DDL com `ON DELETE CASCADE` em cadeia de 3 níveis (`RESORT` -> `BLOCO` -> `APARTAMENTO`).
  - **`R2.3` (`structured` + Diagrama EER SVG):** Subclasse compartilhada (`VEICULO` -> `TERRESTRE` & `CARGA_PESADA` -> `CAMINHAO_FROTA`) e agregação (`EXECUTA` -> `AUTO_FISCAL`).

### Grupo 6 (`R2.4` – `R2.5`): Engenharia Reversa (DDL -> ER) & Assertions SQL-92
- **Arquivo de Estudo:** `study_guides/G6_EngenhariaReversa_e_Assertions_EER.md`
  - *Base nos Slides:* `ibd-parte5.pdf` (Leitura bidirecional Relacional <-> ER/EER e `CREATE ASSERTION`).
  - *Exemplo Análogo na Ficha:* **Banco & Cartões (`CONTA_BANCARIA` -> `CONTA_CORRENTE`, `CONTA_POUPANCA`, `CARTAO`)**.
- **Domínio dos Exercícios (`R2.4`–`R2.5`):**
  - **`R2.4` (`open_design` + Gabarito Visual SVG):** Engenharia reversa completa do script SQL DDL da plataforma de streaming (`PLANO`, `ASSINANTE`, subclasses `INDIVIDUAL`/`FAMILIA`, fraca `PERFIL_USO`, `FAVORITA`, `MUSICA`) para desenho ER/EER no caderno com verificação visual.
  - **`R2.5` (`sql_assertion` + Diagrama EER SVG):** Declaração em SQL-92 de `CREATE ASSERTION` garantindo disjunção (`d`) e totalidade entre `PROFISSIONAL`, `MEDICO` e `DENTISTA`.

### Grupo 7 (`R2.6` – `R2.7`): Tuplas Espúrias, Junção Sem Perda & Preservação de DFs
- **Arquivo de Estudo:** `study_guides/G7_JuncaoSemPerda_TuplasEspurias_e_PreservacaoDFs.md`
  - *Base nos Slides:* `ibd-parte6.pdf` (Diretriz 4, Teste Binário NJP `(R1 ∩ R2)+`, Preservação de Dependências).
  - *Exemplo Análogo na Ficha:* **Transporte de Encomendas (`ENTREGA(Envio, PlacaVan, Cidade)`)**.
- **Domínio dos Exercícios (`R2.6`–`R2.7`):**
  - **`R2.6` (`sql_query`):** Demonstração prática no SQLite de tuplas espúrias geradas ao recompor `EMP_LOCS NATURAL JOIN EMP_PROJ_BAD` sobre atributo não-superchave (`PLocation`).
  - **`R2.7` (`structured`):** Análise formal do esquema universitário `R(A,B,C,D,E)` sob `F = {A->BC, CD->E, B->D, E->A}` nas decomposições `D1` e `D2`.

### Grupo 8 (`R2.8` – `R2.10`): BCNF vs 3FN, Síntese 3FN (Fc) & Auditoria Integrada
- **Arquivo de Estudo:** `study_guides/G8_BCNF_vs_3FN_Sintese_e_Auditoria.md`
  - *Base nos Slides:* `ibd-parte6.pdf` (BCNF vs 3FN com atributo primo, Algoritmo de Síntese 3FN).
  - *Exemplos Análogos na Ficha:* **Revisão de Artigos (`REVISAO`)** e síntese abstrata **`W(P, Q, R, S, U)`**.
- **Domínio dos Exercícios (`R2.8`–`R2.10`):**
  - **`R2.8` (`structured`):** Diagnóstico BCNF vs 3FN em `BANCA_TCC(Matricula, Area, Professor)` e `FORNECEDOR_CEP(IdForn, CEP, Cidade, Estado)`.
  - **`R2.9` (`structured`):** Algoritmo completo de Síntese 3FN em `T(A,B,C,D,E,G)` com atributo estranho no LHS, DFs redundantes e inclusão da tabela extra da chave `{A,G}`.
  - **`R2.10` (`structured` + Diagrama ER SVG):** Auditoria ER -> 2FN -> 3FN/BCNF refatorando `PEDIDO_BRUTO` de E-Commerce.

---

## ✅ Rodada 3 (`R3.1` a `R3.10`) — CONCLUÍDA E INTEGRADA AO LAB

### Grupo 9 (`R3.1` – `R3.5`): Simulado A — Congresso Científico (5 Etapas: Requisitos -> EER -> RIRs -> DDL -> 3FN)
- **Arquivo de Estudo:** `study_guides/G9_Simulado_A_Congresso_EER_para_3FN.md`
  - *Base nos Slides:* `ibd-parte5.pdf` (Etapas 1–2, EER `{o, parcial}`, Ternários, RIRs `b/p/n`) & `ibd-parte6.pdf` (2FN/3FN).
  - *Exemplo Análogo na Ficha:* **Mostra de Cinema (`PESSOA` -> `{CURADOR, CINEASTA}`, `MOSTRA -> EXIBICAO`, `VENDA_BRUTA`)**.
- **As 5 Etapas do Simulado A:**
  - **`R3.1` (`open_design` + Gabarito Visual SVG):** Leitura de requisitos do Congresso Científico -> desenho EER no caderno (`PESSOA {o, parcial}`, multivalorado `Emails`, fraca `SESSAO`, `M:N ESCREVE`, ternário `PARECER`).
  - **`R3.2` (`structured` + SVG EER):** Decisões 8A vs 8C, chave parcial de `SESSAO` e não-redutibilidade do ternário `PARECER`.
  - **`R3.3` (`structured`):** Mapeamento lógico completo e RIRs (`-p->` em `PESSOA_EMAILS`/`SESSAO`, `-b->` em `ARTIGO[CodTrilha]`).
  - **`R3.4` (`sql_ddl`):** SQLite DDL completo de `TRILHA`, `SESSAO`, `ARTIGO` e `PARECER` (`CHECK (Nota >= 0 AND Nota <= 10)`) com 5 testes automatizados.
  - **`R3.5` (`structured`):** Normalização da planilha legada `INSC_BRUTA` até 3FN (5 tabelas).

### Grupo 10 (`R3.6` – `R3.10`): Simulado B — Plataforma de Leilões Online & Logística (5 Etapas)
- **Arquivo de Estudo:** `study_guides/G10_Simulado_B_Auditoria_SQL_BCNF_e_Chaves.md`
  - *Base nos Slides:* `ibd-parte5.pdf` (`CREATE ASSERTION`) & `ibd-parte6.pdf` (Detecção de DFs em SQL, NJP, 3FN vs BCNF, Definição Geral).
  - *Exemplos Análogos na Ficha:* **Galeria de Arte** (`PROIBE_AUTO_AVALIACAO`) & esquema abstrato **`K(U, V, W, X, Y)`**.
- **As 5 Etapas do Simulado B:**
  - **`R3.6` (`structured` + SVG EER):** Auditoria de armadilhas EER em Leilões Online (`USUARIO {o, total}`, fraca `LANCE`).
  - **`R3.7` (`sql_assertion`):** SQL-92 `CREATE ASSERTION` bloqueando auto-lance (`IdComprador = IdVendedor`) e lance em leilão fechado (`Status <> 'ABERTO'`).
  - **`R3.8` (`sql_query`):** Auditoria SQL na instância `LANCE_AUDIT` provando violação de `CEPVendedor -> CPFVendedor`.
  - **`R3.9` (`structured`):** Rigor formal em `R(M, N, P, Q, S)` (`F = {MN->P, NP->Q, Q->S, S->M}`): 4 chaves candidatas, 3FN vs BCNF, NJP e perda de preservação de DFs.
  - **`R3.10` (`structured`):** Normalização pela Definição Geral em `ENTREGA_DRONE` (chaves `{IdEntrega}` e `{CodDrone, DataHora}`) até BCNF.

---

## ✅ Rodada 4 (`R4.1` a `R4.10`) — CONCLUÍDA E INTEGRADA AO LAB

### Grupo 11 (`R4.1` – `R4.5`): Alta Incidência Módulo 7 — Opções 1/2/3 + AR, DDL (`CHECK` + `-n->`), Ternário `M:N:1` & Lista Oficial
- **Arquivo de Estudo:** `study_guides/G11_M7_Hierarquias8B_TernarioMN1_e_RIRs.md`
  - *Base nos Slides:* `ibd-parte5.pdf` (Opções 1/2/3, Fórmulas AR, Ternário com lado `1`, RIRs `-b->`, `-p->`, `-n->`) & `ExercicioProjetoLogico.pdf`.
  - *Exemplos Análogos na Ficha:* **Passagem Rodoviária** (`CHECK` XOR `{d, total}`), **Clínica Veterinária** (`CONSULTA_VET`) e **`CLINICA`** (Equações AR -> `ASSERTION`).
- **Exercícios (`R4.1`–`R4.5`):**
  - **`R4.1` (`structured` + SVG EER):** Comparação Opções 1/2/3 e equações em Álgebra Relacional em `MIDIA` (`{d, total}`) vs `COLABORADOR` (`{o, parcial}`).
  - **`R4.2` (`sql_ddl`):** Tabela única `VEICULO` `{d, total}` com `CHECK` XOR + relação parcial `N:1` com `INSPETOR` usando `-n->` (`ON DELETE SET NULL`).
  - **`R4.3` (`structured` + SVG ER):** Ternário `ESTAGIO(ALUNO: N, EMPRESA: M, ORIENTADOR: 1)` com PK dupla `(Matr, CNPJ)` + RIR `-n->` em `ORIENTADOR[IdLab]`.
  - **`R4.4` (`open_design` + SVG EER):** Mapeamento lógico formal completo no caderno (PKs, `(nn)` e setas RIR) do sistema de Cooperativa Bancária com gabarito completo.
  - **`R4.5` (`sql_assertion`):** Tradução direta das equações AR de disjunção (`∩ = ∅`) e totalidade (`∪ = π_PK(ACERVO)`) da Opção 1 em Biblioteca (`ACERVO`, `LIVRO_FISICO`, `PERIODICO`).

### Grupo 12 (`R4.6` – `R4.10`): Alta Incidência Módulo 8 — DFs em SQL, Armstrong/Equivalência, Particionamento L/M/R & 1FN–3FN
- **Arquivo de Estudo:** `study_guides/G12_M8_Armstrong_Equivalencia_Particionamento_1a3FN.md`
  - *Base nos Slides:* `ibd-parte6.pdf` (Anomalias, DFs em instâncias, Armstrong, `F ≡ G`, Particionamento de chaves, 1FN->2FN->3FN) & `ExerciciosNormalizacaoSemResposta.pdf`.
  - *Exemplos Análogos na Ficha:* Esquema abstrato **`S(P, Q, R, T, U, W)`** e comparação `F1` vs `F2`.
- **Exercícios (`R4.6`–`R4.10`):**
  - **`R4.6` (`sql_query`):** Auditoria SQL em `MATRICULA_HIST` refutando `Sala -> CPFProf`.
  - **`R4.7` (`structured`):** Derivação via Armstrong (Pseudotransitividade) e testes bidirecionais de cobertura / equivalência `F ≡ G` vs `P ≢ Q`.
  - **`R4.8` (`structured`):** Método dos 3 conjuntos (`L / M / R`) em `R(A,B,C,D,E,G)` descobrindo `{AB, AC, AE}` e diagnosticando violação de 2FN (Def. Geral) em `C -> D`.
  - **`R4.9` (`open_design`):** Questão discursiva completa passo a passo (`1FN -> 2FN -> 3FN`) sobre `BOLETIM_ANUAL` com gabarito detalhado.
  - **`R4.10` (`structured`):** Bateria mista sobre Anomalia de Inserção (`PLANTAO_MEDICO`), 3FN (`OS_OFICINA`) e perda de informação + tuplas espúrias (`EMP`).

---

## ✅ Rodada 5 (`R5.1` a `R5.10`) — A ORQUESTRA FINAL (CONCLUÍDA E INTEGRADA AO LAB)

> **Banco Completo Consolidado:** 5 Rodadas × 10 exercícios (`R1.1`–`R5.10`) + 38 exercícios base/oficiais = **88 exercícios** cobrindo integralmente `ibd-parte5.pdf`, `ibd-parte6.pdf`, `ExercicioProjetoLogico.pdf` e `ExerciciosNormalizacaoSemResposta.pdf`.

### Grupo 13 (`R5.1` – `R5.5`): Orquestra Final Módulo 7 — Leitura Inversa, `1:1` Assimétrico, Cadeia DDL & Mini-Simulado
- **Arquivo de Estudo:** `study_guides/G13_M7_LeituraInversa_1a1_e_ChecklistFinal.md`
  - *Exemplos Análogos na Ficha:* **`COFRE` vs `GERENTE` (`1:1`)**, **`FORNECEDOR` (multivalorado composto)** e **Porto/Rodovia (`SEM_LACO`)**.
- **Exercícios (`R5.1`–`R5.5`):**
  - **`R5.1` (`structured`):** Leitura inversa (Esquema Lógico + RIRs -> Cardinalidades ER) em Secretaria Acadêmica.
  - **`R5.2` (`structured` + SVG ER):** `1:1` assimétrico `VEICULO(1,1)` vs `RASTREADOR(0,1)` + composto simples e multivalorado composto em Seguradora.
  - **`R5.3` (`sql_ddl`):** Cadeia Hospitalar 3 níveis (`UNIDADE -> SETOR -> LEITO`) com `ON DELETE CASCADE`, `CHECK` de Status e `INTERNACAO` com `ON DELETE RESTRICT`.
  - **`R5.4` (`open_design` + Gabarito Duplo SVG + Esquema Lógico):** Prova completa de papel — Agência Espacial (`TRIPULANTE {o, total}`, `BASE -> PLATAFORMA`, `MISSAO`).
  - **`R5.5` (`sql_assertion`):** SQL-92 `CREATE ASSERTION` para Rede Ferroviária (`SEM_AUTOLACO` e `EXPRESSA_CAPACIDADE`).

### Grupo 14 (`R5.6` – `R5.10`): Orquestra Final Módulo 8 — `Fc` em Cascata, Ciclos de 4 Chaves & Checklist Pré-Prova
- **Arquivo de Estudo:** `study_guides/G14_M8_CoberturaMinima_CiclosChaves_e_ChecklistFinal.md`
  - *Exemplos Análogos na Ficha:* **`Fc` passo 2+3** e **Esquema Cíclico `X(P, Q, R, S, T)`**.
- **Exercícios (`R5.6`–`R5.10`):**
  - **`R5.6` (`structured`):** Cobertura mínima `Fc` passo a passo com 2 atributos estranhos no LHS (`AB -> D`, `BC -> E`) e eliminação de `A -> E`.
  - **`R5.7` (`sql_query`):** Auditoria SQL em `VENDAS_FISCAL` refutando `CPFCliente -> CodVendedor`.
  - **`R5.8` (`structured`):** Esquema cíclico com 4 chaves candidatas `{AE, BE, CE, DE}` (3FN vs BCNF sem cair na falsa violação de 2FN).
  - **`R5.9` (`open_design`):** Estudo de caso aberto `1FN -> 2FN -> 3FN` (`GUIA_EXAMES`) com gabarito completo em 6 tabelas.
  - **`R5.10` (`structured`):** Checklist cirúrgico final cobrindo impossibilidades de `-n->`, 3FN vs BCNF e NJP sequencial.

