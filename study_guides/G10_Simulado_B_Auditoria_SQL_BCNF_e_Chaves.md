# Ficha de Estudo G10 — Simulado B: Auditoria SQL, ASSERTION, 3FN vs BCNF & Definição Geral

> **Exercícios Vinculados na Rodada 3:** `R3.6`, `R3.7`, `R3.8`, `R3.9`, `R3.10` (Simulado B — 5 Etapas)  
> **Base no Material da Disciplina:** `ibd-parte5.pdf` (`CREATE ASSERTION` SQL-92) e `ibd-parte6.pdf` (Auditoria de DFs em Instâncias, Chaves Múltiplas, 2FN Geral, 3FN vs BCNF e NJP)

---

## 1. Pontos Críticos de Prova em Normalização Avançada & Auditoria

1. **Testar BCNF vs 3FN em Esquemas com Múltiplas Chaves Candidatas:**
   - **Passo A:** Encontre **todas** as chaves candidatas calculando os fechos `X+`.
   - **Passo B:** Liste o conjunto de **atributos primos** (união de todas as chaves candidatas).
   - **Passo C (2FN Geral):** Verifique se algum atributo **não-primo** depende parcialmente de **qualquer** chave candidata composta (não apenas da chave primária escolhida!).
   - **Passo D (3FN vs BCNF):** Se uma DF não-trivial `X → A` tem `X` não-superchave e `A` **primo**, ela **passa na 3FN**, mas **viola a BCNF**.
2. **Decomposição Binária Sem Perda (`D = {R1, R2}`):** Tem junção sem perda se e só se `(R1 ∩ R2)+` contém todo `R1` **ou** todo `R2`.
3. **Detecção Empírica de Violação de DF `X → Y` em SQL:** Use auto-junção `t1 JOIN t2 ON t1.X = t2.X AND t1.Y <> t2.Y` (com `t1.PK < t2.PK` para evitar pares espelhados).

---

## 2. Exemplos Resolvidos Análogos (Domínios Diferentes da Tarefa)

> **Atenção:** Este guia usa **Mercado de Arte** e o esquema abstrato **`K(U, V, W, X, Y)`**, distintos de **Leilões Online (`R3.6`–`R3.8`)**, **`R(M, N, P, Q, S)` (`R3.9`)** e **`ENTREGA_DRONE` (`R3.10`)**.

### Exemplo A — Invariante EER via `CREATE ASSERTION` (Galeria de Arte)
Um curador não pode avaliar sua própria obra:
```sql
CREATE ASSERTION PROIBE_AUTO_AVALIACAO CHECK (
  NOT EXISTS (
    SELECT 1 FROM AVALIACAO_OBRA a
    JOIN OBRA o ON a.IdObra = o.IdObra
    WHERE a.CPFAvaliador = o.CPFArtista
  )
);
```

### Exemplo B — Detecção de Violação de DF em Instância SQL
Para testar se `CEPArtista → CPFArtista` falha em `OBRAS_AUDITORIA`:
```sql
SELECT a.IdObra AS Obra1, b.IdObra AS Obra2, a.CEPArtista,
       a.CPFArtista AS CPF1, b.CPFArtista AS CPF2
FROM OBRAS_AUDITORIA a
JOIN OBRAS_AUDITORIA b
  ON a.CEPArtista = b.CEPArtista
 AND a.CPFArtista <> b.CPFArtista
 AND a.IdObra < b.IdObra;
```

### Exemplo C — Esquema `K(U, V, W, X, Y)` com `F = { UV → W, VW → X, X → Y, Y → U }`
- **Chaves candidatas:** `{UV}`, `{VW}`, `{VX}`, `{VY}` (todas binárias; **todos os 5 atributos são primos**!).
- **Forma Normal:** Está em **3FN** (porque `X → Y` e `Y → U` têm RHS primo), mas viola **BCNF**.
- **Teste Binário NJP:** Em `D1 = { K1(U, V, W, X), K2(X, Y) }`, `K1 ∩ K2 = {X}` e `X+ = {X, Y, U}`, determinando todo `K2(X, Y)` -> **Junção Sem Perda**!
