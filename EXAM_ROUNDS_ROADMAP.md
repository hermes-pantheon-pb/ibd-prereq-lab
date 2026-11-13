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

## 📋 Planejamento Salvo para a Próxima Rodada

### Rodada 3 (`R3.1` a `R3.10`) — Simulados Integrados de Prova Final:
- 2 provas completas estilo UFMG divididas em 5 etapas cada (Leitura de Requisitos -> Modelagem ER/EER -> Mapeamento Lógico + RIRs -> SQL DDL/Assertions -> Normalização até 3FN/BCNF).

