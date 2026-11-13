# 📘 Ficha de Estudo G8 — BCNF vs. 3FN, Algoritmo de Síntese 3FN e Auditoria Completa

> **Exercícios Vinculados na Rodada 2:** `R2.8`, `R2.9`, `R2.10`  
> **Base Direta no Material da Disciplina:** `ibd-parte6.pdf` (Forma Normal de Boyce-Codd / BCNF; Diferença crítica 3FN vs. BCNF quando $A$ é atributo primo; Algoritmo de Síntese 3FN garantindo Junção Sem Perda e Preservação de DFs).

---

## 1. Terceira Forma Normal (3FN) vs. Boyce-Codd (BCNF)

Considere qualquer dependência funcional **não-trivial** $X \to A$ ($A \notin X$) válida em $R$:

| Forma Normal | Regra Formal (`ibd-parte6.pdf`) | O que acontece na prática? |
| :--- | :--- | :--- |
| **3FN (Geral)** | Para toda $X \to A$ não-trivial:<br>**(a)** $X$ é **superchave**, **OU**<br>**(b)** $A$ é **atributo primo** *(pertence a alguma CK)*. | Toda relação tem **sempre** uma decomposição em 3FN que garante simultaneamente **Junção Sem Perda** e **Preservação de DFs**! |
| **BCNF** | Para toda $X \to A$ não-trivial:<br>**(a)** $X$ **OBRIGATORIAMENTE é superchave**.<br>*(Remove a exceção "(b) $A$ é primo"!)* | Elimina **toda** redundância causada por DFs, porém **nem sempre** existe uma decomposição em BCNF que preserve todas as dependências funcionais! |

> **Resumo de Ouro:** Toda relação em **BCNF está automaticamente na 3FN**, mas uma relação em **3FN pode NÃO estar em BCNF**! Isso ocorre exatamente quando há uma DF $X \to A$ onde $X$ **não** é superchave, mas $A$ **é primo** (parte de outra chave candidata composta).

---

## 2. Algoritmo de Síntese 3FN (`ibd-parte6.pdf`) — Passo a Passo

Dado um esquema universal $R$ e um conjunto $F$ de DFs, queremos gerar uma decomposição $\{R_1, \dots, R_k\}$ em **3FN com Junção Sem Perda e Preservação de DFs**:

1. **Passo 1 — Cobertura Mínima ($F_c$):** Encontre uma cobertura mínima $F_c$ para $F$ (lado direito único, sem atributo estranho no LHS, sem DF redundante).
2. **Passo 2 — Criação das Relações por Determinante ($X \to A \in F_c$):**
   - Agrupe as DFs de $F_c$ que possuem o **mesmo lado esquerdo $X$** (ex: $X \to A_1, X \to A_2 \implies X \to A_1 A_2$) e crie uma relação $R_i = (X \cup \{A_1, A_2, \dots\})$ com PK $X$.
3. **Passo 3 — Garantia da Junção Sem Perda (Teste da Chave Candidata):**
   - Verifique se **pelo menos uma** das relações $R_i$ geradas no Passo 2 **contém uma chave candidata $K$ de $R$**!
   - Se nenhuma relação contiver uma chave candidata de $R$, **adicione uma nova relação extra $R_{chave}(K)$** formada pelos atributos de uma chave candidata $K$ de $R$! *(Se já contiver, não adicione nada!)*
4. **Passo 4 — Remoção de Esquemas Redundantes:**
   - Se alguma relação $R_i$ for subconjunto próprio de outra relação $R_j$ ($R_i \subseteq R_j$), elimine $R_i$.

---

## 3. Exemplo Análogo Resolvido (Domínio Diferente: *Revisão de Artigos Científicos*)

> **Atenção:** Este exemplo usa **Artigos, Tópicos e Revisor** e o esquema abstrato $W(P, Q, R, S)$, domínios distintos de `LOTACAO_DOCENTE` / `ENDERECO` (`R2.8`), `T(A,B,C,D,E)` (`R2.9`) e E-Commerce (`R2.10`).

### Exemplo A (3FN que viola BCNF — *Comitê Científico*):
Considere `REVISAO(IdArtigo, AreaTematica, CPFRevisor)` com:
- `DF1: {IdArtigo, AreaTematica} -> CPFRevisor`
- `DF2: CPFRevisor -> AreaTematica` *(Cada revisor só atua em uma única área temática)*
1. **Chaves Candidatas:** $CK_1 = \{\text{IdArtigo}, \text{AreaTematica}\}$ e $CK_2 = \{\text{IdArtigo}, \text{CPFRevisor}\}$.
2. **Todos os atributos são primos?** SIM! (`IdArtigo`, `AreaTematica`, `CPFRevisor`).
3. **Está na 3FN?** **SIM!** Em `DF2`, `AreaTematica` é atributo primo, logo satisfaz a cláusula (b) da 3FN.
4. **Está na BCNF?** **NÃO!** Em `DF2`, `CPFRevisor` **não é superchave** (pois `CPFRevisor` não determina `IdArtigo`).
5. **Consequência se forçarmos BCNF:** Decompor em `R1(CPFRevisor, AreaTematica)` e `R2(IdArtigo, CPFRevisor)` alcança BCNF e é sem perda (`CPFRevisor -> R1`), **mas perde a preservação de `{IdArtigo, AreaTematica} -> CPFRevisor`**!

### Exemplo B (Algoritmo de Síntese 3FN quando falta a Chave Candidata):
Dado $W(P, Q, R, S)$ com $F_c = \{ Q \to R, \; R \to S \}$:
- **Passo 2:** Cria $R_1(\underline{Q}, R)$ e $R_2(\underline{R}, S)$.
- **Passo 3:** Qual é a chave candidata de $W$? Como $P$ não aparece em nenhuma DF e $Q$ nunca está no RHS, temos $K = \{P, Q\}$ ($ \{P, Q\}^+ = \{P, Q, R, S\}$). Nenhuma relação ($R_1$ ou $R_2$) contém $\{P, Q\}$! Portanto, **é obrigatório adicionar $R_3(\underline{P, Q})$** para garantir Junção Sem Perda!
- **Esquema Final (Síntese 3FN):** $\{ (\underline{Q}, R), \; (\underline{R}, S), \; (\underline{P, Q}) \}$.
