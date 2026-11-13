# Ficha de Estudo G14 — Orquestra Final M8: Cobertura Mínima em Cascata, Ciclos & Checklist

> **Exercícios Vinculados na Rodada 5:** `R5.6`, `R5.7`, `R5.8`, `R5.9`, `R5.10` (Orquestra Final — Módulo 8 & Revisão Geral)  
> **Base no Material da Disciplina:** `ibd-parte6.pdf` (Cobertura Mínima 3 Passos, Ciclos de Chaves, 1FN -> 2FN -> 3FN vs BCNF, NJP) & `ExerciciosNormalizacaoSemResposta.pdf`

---

## 1. Roteiro Infalível de Cobertura Mínima (`Fc`) & Chaves Cíclicas

1. **Ordem Obrigatória na Cobertura Mínima (3 Passos):**
   - **Passo 1:** Quebre o lado direito (`X → YZ` vira `X → Y`, `X → Z`).
   - **Passo 2 (Atributo estranho no LHS):** Em toda DF composta `XB → Y`, teste `X+` (com as DFs atuais). Se `B ∈ X+` (ou `Y ∈ X+`), **remova `B` imediatamente** antes de passar para o Passo 3!
   - **Passo 3 (DF redundante):** Para cada `f: X → Y` restante, calcule `X+` **sem usar `f`**. Se `Y ∈ X+`, remova `f`.
2. **Quando Existe Um Ciclo (`P → Q, Q → R, R → P`) Combinado a Um Isolado (`S`):**
   - Se `P, Q, R` se equivalem em fechamento e existe `S` fora do RHS, as chaves candidatas multiplicam-se em **`{PS, QS, RS}`**!
   - **Armadilha clássica:** Uma DF como `P → Q` parece parcial sobre `{PS}`, porém **não viola 2FN nem 3FN** porque `Q` é **atributo primo** (faz parte de `{QS}`)! Só viola **BCNF**.

---

## 2. Exemplos Análogos (Domínios Diferentes das Tarefas)

> **Atenção:** Este guia usa o esquema abstrato **`X(P, Q, R, S, T)`** e **Fatura de Supermercado (`CUPOM_SUPERMERCADO`)**, distintos dos objetos em `R5.6`–`R5.10`.

1. **Exemplo de Passo 2 + Passo 3 (`Fc`):** Em `{ P → Q, Q → R, PQ → T, P → T }`:
   - Passo 2: Em `PQ → T`, `P → Q` remove `Q`, ficando `P → T`.
   - Passo 3: Não há redundância se só sobrar uma cópia; se houver `Q → U` e `P → U`, `P → U` cai por ser derivável via `P → Q → U`.
2. **Ciclo `P → Q → R → P` com `PS → T` em `X(P, Q, R, S, T)`:**
   - Chaves candidatas: `{PS, QS, RS}`. Primos: `{P, Q, R, S}`. Não-primo: `{T}`.
   - Maior forma normal: **3FN** (viola BCNF em `P → Q`, `Q → R`, `R → P`).
