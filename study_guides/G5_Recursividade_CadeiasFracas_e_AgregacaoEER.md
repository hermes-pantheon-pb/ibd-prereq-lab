# 📘 Ficha de Estudo G5 — Relacionamentos Recursivos, Cadeias de Entidades Fracas e Reticulados / Agregação EER

> **Exercícios Vinculados na Rodada 2:** `R2.1`, `R2.2`, `R2.3`  
> **Base Direta no Material da Disciplina:** `ibd-parte5.pdf` (*Etapa 1: Auto-relacionamentos 1:1 / 1:N / M:N com papéis explícitos e RIRs; Regra 3 em Cadeias de Entidades Fracas; Etapa 2 slide 40: Agregação EER e Subclasses Compartilhadas*) + `ExercicioProjetoLogico.pdf`.

---

## 1. Mapeamento de Relacionamentos Recursivos (Auto-Relacionamentos)

Quando uma entidade `E(K, a1, ...)` se relaciona consigo mesma, **a regra de mapeamento depende da cardinalidade máxima**, exatamente como em relacionamentos binários comuns — porém **exige renomeação de papéis (roles)** para evitar colunas com o mesmo nome na mesma relação:

| Tipo do Auto-Relacionamento | Regra de Mapeamento Relacional (`ibd-parte5.pdf`) | Política RIR (`b`, `n`, `p`) e `CHECK` |
| :--- | :--- | :--- |
| **1:1 Recursivo**<br>*(ex: Cônjuge / Sucessor)* | Adiciona-se uma `FK` dentro da **própria relação `E`** referenciando `E[K]`, com restrição **`UNIQUE`** (garantindo 1:1). | `-n->` (`SET NULL` se opcional) ou `-b->` (`RESTRICT`).<br>`CHECK (K <> K_Papel)` evita auto-referência circular trivial quando proibido. |
| **1:N Recursivo**<br>*(ex: Supervisor → Subordinados)* | Adiciona-se uma `FK` no **lado N** (ou seja, dentro da **própria relação `E`**!), sem criar nova tabela! | `-n->` (`ON DELETE SET NULL`, ex: demitir gerente deixa subordinados sem chefe) ou `-b->` (`RESTRICT`). |
| **M:N Recursivo**<br>*(ex: Pré-Requisito / Composição)* | **Cria-se uma nova relação associativa `R_REC(K_Papel1(nn), K_Papel2(nn), Atrib)`** com **`PK = (K_Papel1, K_Papel2)`**! | Ambas as FKs apontam para `E[K]` com política **`-p->` (`ON DELETE CASCADE`)**. |

---

## 2. Cadeias de Entidades Fracas (Múltiplos Níveis)

Quando uma entidade forte $A$ identifica uma fraca $B$ (discriminador $k_B$), e $B$ identifica uma fraca $C$ (discriminador $k_C$):
1. **$A(\underline{K_A}, \dots)$** $\to$ `PK: (K_A)`
2. **$B(\underline{K_A(nn), k_B(nn)}, \dots)$** $\to$ `PK: (K_A, k_B)` | RIR: `B[K_A] -p-> A[K_A]`
3. **$C(\underline{K_A(nn), k_B(nn), k_C(nn)}, \dots)$** $\to$ **`PK: (K_A, k_B, k_C)`** | RIR: `C[K_A, k_B] -p-> B[K_A, k_B]` (`ON DELETE CASCADE`!)

> **Armadilha clássica de prova:** Nunca coloque apenas `(k_B, k_C)` como chave primária do nível 3! Como `k_B` só é único dentro de um $A$, e `k_C` só é único dentro de um $B$, a chave primária precisa carregar **toda a cadeia ancestral desde a entidade forte raiz**.

---

## 3. Subclasses Compartilhadas (Reticulado EER) e Agregação EER (Slide 40)

- **Subclasse Compartilhada (Herança Múltipla):** Uma subclasse `Sub` que herda simultaneamente de `Pai1(K, ...)` e `Pai2(K, ...)` (ambas pertencentes à mesma hierarquia de chave raiz `K`). No modelo relacional pela **Opção 3**, `Sub(K(nn), atribs_Sub)` herda a mesma PK `K` e possui **duas RIRs** com política `-p->` para ambos os pais (`Sub[K] -p-> Pai1[K]` e `Sub[K] -p-> Pai2[K]`).
- **Agregação EER (`ibd-parte5.pdf`, slide 40):** Quando um relacionamento $R(E_1, E_2)$ é encapsulado como uma agregação para participar de outro relacionamento com $E_3$:
  - A agregação $R$ já foi mapeada como relação própria com chave `(PK_E1, PK_E2)`.
  - Se $E_3$ possui participação N:1 com a agregação $R$, então **$E_3$ importa a chave composta `(PK_E1, PK_E2)` como chave estrangeira** referenciando $R$! Se for M:N, a nova tabela associativa une `(PK_E1, PK_E2, PK_E3)`.

---

## 4. Exemplos Análogos Resolvidos (Domínios Diferentes das Questões)

> Estes exemplos usam **Disciplinas Acadêmicas**, **Copa Esportiva** e **Academia Corporativa** (objetos distintos de Manufatura, Resort/Vagas e Frota Logística cobrados em `R2.1`–`R2.3`).

### Exemplo A (Recursividade `1:N` e `M:N` — *Grade Curricular*):
- `DISCIPLINA(CodDisc, Nome)` possui:
  - Auto-relacionamento `M:N` **`PRE_REQUISITO(Obrigatoriedade)`** (papéis `DiscPrincipal` e `DiscRequisito`).
  - Auto-relacionamento `1:N` **`EQUIVALE_A`** (`CodDiscEquivalente`: cada disciplina optativa pode apontar para no máximo 1 equivalente matriz).
- **Mapeamento Relacional Exato:**
  ```text
  DISCIPLINA(CodDisc(nn), Nome(nn), CodDiscEquivalente)
    PK: CodDisc
    RIR: DISCIPLINA[CodDiscEquivalente] -n-> DISCIPLINA[CodDisc]   -- (1:N absorvido!)

  PRE_REQUISITO(CodDiscPrincipal(nn), CodDiscRequisito(nn), Obrigatoriedade)
    PK: (CodDiscPrincipal, CodDiscRequisito)
    RIR 1: PRE_REQUISITO[CodDiscPrincipal] -p-> DISCIPLINA[CodDisc]
    RIR 2: PRE_REQUISITO[CodDiscRequisito] -p-> DISCIPLINA[CodDisc]
  ```

### Exemplo B (Cadeia de Entidades Fracas — *Copa Esportiva*):
- `TORNEIO(CodTorneio, Ano)` $\to$ `FASE(NumFase, Descricao)` [Fraca Nível 1] $\to$ `JOGO(NumJogo, Placar)` [Fraca Nível 2].
  ```sql
  CREATE TABLE TORNEIO (
      CodTorneio VARCHAR(10) PRIMARY KEY,
      Ano INTEGER NOT NULL
  );
  CREATE TABLE FASE (
      CodTorneio VARCHAR(10) NOT NULL,
      NumFase INTEGER NOT NULL,
      Descricao VARCHAR(50),
      PRIMARY KEY (CodTorneio, NumFase),
      FOREIGN KEY (CodTorneio) REFERENCES TORNEIO(CodTorneio) ON DELETE CASCADE
  );
  CREATE TABLE JOGO (
      CodTorneio VARCHAR(10) NOT NULL,
      NumFase INTEGER NOT NULL,
      NumJogo INTEGER NOT NULL,
      Placar VARCHAR(15),
      PRIMARY KEY (CodTorneio, NumFase, NumJogo),
      FOREIGN KEY (CodTorneio, NumFase) REFERENCES FASE(CodTorneio, NumFase) ON DELETE CASCADE
  );
  ```

### Exemplo C (Agregação EER — *Consultoria de Cursos*):
- `ATUA_EM(CPFConsultor, CodProjeto, Funcao)` (agregação `M:N`) conecta-se `1:N` à entidade fraca/associada `APONTAMENTO_HORAS(NumSeq, Horas)` (`(1,1)` do lado de `APONTAMENTO_HORAS`):
  ```text
  ATUA_EM(CPFConsultor(nn), CodProjeto(nn), Funcao)  -- PK: (CPFConsultor, CodProjeto)
  APONTAMENTO_HORAS(CPFConsultor(nn), CodProjeto(nn), NumSeq(nn), Horas(nn))
    PK: (CPFConsultor, CodProjeto, NumSeq)
    RIR: APONTAMENTO_HORAS[CPFConsultor, CodProjeto] -p-> ATUA_EM[CPFConsultor, CodProjeto]
  ```
