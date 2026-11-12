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

## 📋 Planejamento Salvo para as Próximas Rodadas (Não Executar Agora!)

### Rodada 2 (`R2.1` a `R2.10`) — Tópicos Planejados:
1. **`R2.1` (Módulo 7):** Relacionamentos Recursivos (Auto-relacionamentos `1:1`, `1:N` e `M:N` com papéis/roles explícitos, ex: `PECA_COMPOSTA` / Bill of Materials e `CASAMENTO`).
2. **`R2.2` (Módulo 7):** Entidades Fracas em Cadeia (2 e 3 níveis: ex: `CONDOMINIO` $\to$ `BLOCO` $\to$ `APARTAMENTO` $\to$ `VAGA_GARAGEM`) e propagação de chaves e RIRs `-p->`.
3. **`R2.3` (Módulo 7):** Subclasses Compartilhadas (Herança Múltipla / Reticulado EER) e Categorias (`UNION types` do Elmasri).
4. **`R2.4` (Módulo 7):** Engenharia Reversa Completa: Dado um script SQL DDL com 6 tabelas, `UNIQUE`, `CHECK` e `FOREIGN KEY`, reconstruir o Diagrama ER/EER original e suas cardinalidades `(min, max)`.
5. **`R2.5` (Módulo 7 — `sql_assertion`):** Mapeamento de restrições inter-tabelas de hierarquias EER (Opções 2 e 3) via `CREATE ASSERTION` em SQL-92.
6. **`R2.6` (Módulo 8):** Propriedade da Junção Sem Perda (Lossless-Join Decomposition) — Teste formal $R_1 \cap R_2 \to R_1$ ou $R_1 \cap R_2 \to R_2$ e demonstração em SQL de tuplas espúrias em decomposições com perda.
7. **`R2.7` (Módulo 8):** Preservação de Dependências Funcionais — Quando uma decomposição perde uma DF e como projetar $F$ sobre $R_i$.
8. **`R2.8` (Módulo 8):** Forma Normal de Boyce-Codd (BCNF) vs. 3FN — O caso clássico onde $X \to A$ viola BCNF mas está em 3FN porque $A$ é atributo primo (ex: `ENDERECO_CEP` ou `ORIENTACAO_TCC`).
9. **`R2.9` (Módulo 8):** Algoritmo de Síntese para 3FN a partir da Cobertura Mínima $F_c$ (garantindo Junção Sem Perda + Preservação de DFs).
10. **`R2.10` (Integrado M7 + M8):** Auditoria de Normalização sobre um Esquema Mapeado de um Diagrama ER com atributos mal posicionados no relacionamento.

### Rodada 3 (`R3.1` a `R3.10`) — Simulados Integrados de Prova Final:
- 2 provas completas estilo UFMG divididas em 5 etapas cada (Leitura de Requisitos $\to$ Modelagem ER/EER $\to$ Mapeamento Lógico + RIRs $\to$ SQL DDL/Assertions $\to$ Normalização até 3FN/BCNF).
