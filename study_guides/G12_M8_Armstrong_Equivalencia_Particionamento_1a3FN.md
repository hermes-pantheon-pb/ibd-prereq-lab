# Ficha de Estudo G12 — Inferência (Armstrong), Equivalência F ≡ G, Chaves & 1FN–3FN

> **Exercícios Vinculados na Rodada 4:** `R4.6`, `R4.7`, `R4.8`, `R4.9`, `R4.10` (Módulo 8 — Alta Incidência em Provas)  
> **Base no Material da Disciplina:** `ibd-parte6.pdf` (Anomalias, DFs em Instâncias, Axiomas de Armstrong, Equivalência `F ≡ G`, Método de Particionamento para Chaves, 1FN -> 2FN -> 3FN) & `ExerciciosNormalizacaoSemResposta.pdf`

---

## 1. Resumo Prático dos Algoritmos Mais Cobrados

1. **Equivalência de Conjuntos de DFs (`F ≡ G`):**
   - `F` **cobre** `G` (`F ⊇ G`) se, para toda `X → Y ∈ G`, o fecho `X+` calculado **usando apenas as regras de `F`** contém `Y`.
   - `F ≡ G` ocorre **se e somente se** `F` cobre `G` **E** `G` cobre `F`.
2. **Método dos 3 Conjuntos para Chaves Candidatas (Particionamento):**
   - **Somente Esquerda (`L`):** atributos que só aparecem do lado esquerdo (ou em nenhuma DF). **Estão obrigatoriamente em TODA chave candidata.**
   - **Somente Direita (`R`):** atributos que só aparecem do lado direito. **Nunca entram em nenhuma chave candidata mínima.**
   - **Ambos / Meio (`M`):** aparecem nos dois lados. Teste primeiro `L+`; se não cobrir toda a tabela, combine `L` com subconjuntos crescentes de `M` (1 atributo de `M`, depois 2, etc., pulando superconjuntos de chaves já achadas).
3. **1FN -> 2FN -> 3FN com Anomalias:**
   - **1FN:** Elimine grupos repetitivos / atributos multivalorados criando tabela filha com PK composta `(PK_pai, item)`.
   - **2FN:** Remova dependências parciais sobre *qualquer* chave candidata composta (para não-primos).
   - **3FN:** Remova dependências transitivas entre não-primos (`Chave -> X -> Y`).

---

## 2. Exemplos Análogos (Domínios Diferentes das Tarefas)

> **Atenção:** Este guia usa o esquema abstrato **`S(P, Q, R, T, U, W)`** e **Folha de Pagamento de Hotel (`HOSPEDAGEM`)**, distintos de `MATRICULA_HISTORICO`, `F/G` (`R4.7`), `R(A,B,C,D,E,G)` (`R4.8`), `BOLETIM_ANUAL` (`R4.9`) e `OS_OFICINA` (`R4.10`).

### Exemplo A — Equivalência `F1` vs `F2`
- `F1 = { P → Q, Q → R, P → R }` e `F2 = { P → QR }`.
- `F1` cobre `F2` porque `P+` sob `F1` é `{P, Q, R}` (`⊇ QR`).
- `F2` **não** cobre `F1` porque `Q+` sob `F2` é `{Q}` (não contém `R`, falhando em `Q → R`). Logo `F1 ≢ F2`!

### Exemplo B — Chaves por Particionamento em `S(P, Q, R, T, U, W)`
Suponha `F = { PQ → R, R → T, T → Q, T → U, U → W }`:
- `Somente Esquerda (L)` = `{P}` (`P` nunca aparece no RHS)
- `Somente Direita (R)` = `{W}` (`W` nunca aparece no LHS)
- `Meio (M)` = `{Q, R, T, U}`
- Testando `P` + 1 de `M`: `(PQ)+ = {P,Q,R,T,U,W}`, `(PR)+ = {P,R,T,Q,U,W}`, `(PT)+ = {P,T,Q,U,W,R}` -> 3 chaves binárias `{PQ, PR, PT}`! Note `(PU)+ = {P,U,W}` (não é chave!).
- Como `R → U` usa `R` (subconjunto próprio da chave `{PR}`) para determinar o não-primo `U`, `S` viola a **2FN**!
