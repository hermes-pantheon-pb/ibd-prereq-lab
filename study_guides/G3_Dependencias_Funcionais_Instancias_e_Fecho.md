# 📘 Ficha de Estudo G3 — Dependências Funcionais em Instâncias, Axiomas de Armstrong e Fecho $X^+$

> **Exercícios Vinculados na Rodada 1:** `R1.6`, `R1.7` (Domínio do Problema: *Escala de Navios & Esquema Multicandidato $R(A,B,C,D,E,G)$*)  
> **Base Direta no Material da Disciplina:** `ibd-parte6.pdf` (*Seção 1: Diretrizes Informais e Anomalias; Seção 2: Definição Formal de Dependência Funcional $X \to Y$; Seção 3: Regras de Inferência de Armstrong, Algoritmo de Fecho $X^+$ e Chaves Candidatas*) e `ExerciciosNormalizacaoSemResposta.pdf`.

---

## 1. Semântica vs. Instância de uma Dependência Funcional (`ibd-parte6.pdf`, Seção 2)

Uma Dependência Funcional $X \to Y$ é uma restrição sobre **todos os estados possíveis** $r(R)$:
$$\forall t_1, t_2 \in r(R): \quad t_1[X] = t_2[X] \implies t_1[Y] = t_2[Y]$$

- **Regra de Ouro para Provas:**
  1. **Não se pode provar** que $X \to Y$ é verdadeira olhando apenas para uma tabela populada $r(R)$ (pois pode ser coincidência daquele estado específico).
  2. **PODE-SE REFUTAR (provar que é FALSA)** $X \to Y$ encontrando **um único par de tuplas** $(t_1, t_2)$ na instância tal que $t_1[X] = t_2[X]$ e $t_1[Y] \neq t_2[Y]$!
  3. **Em SQL:** Para encontrar todas as tuplas que violam $X \to Y$ na tabela `T`:
     ```sql
     SELECT DISTINCT t1.*
     FROM T t1
     JOIN T t2 ON t1.X = t2.X AND t1.Y <> t2.Y;
     ```

---

## 2. Método Rápido para Encontrar TODAS as Chaves Candidatas via Fecho $X^+$ (`ibd-parte6.pdf`, Seção 3)

Dado um esquema $R$ e um conjunto de DFs $F$, classifique os atributos de $R$ em **3 conjuntos**:

1. **Conjunto $L$ (Essenciais / Somente à Esquerda ou Ausentes):** Atributos que **NUNCA aparecem no lado direito (RHS)** de nenhuma DF em $F$.
   - *Teorema:* Todo atributo de $L$ **obrigatoriamente faz parte de TODA chave candidata** de $R$!
2. **Conjunto $D$ (Inúteis para Chave / Somente à Direita):** Atributos que aparecem **apenas no lado direito (RHS)** e nunca no lado esquerdo (LHS).
   - *Teorema:* Nenhum atributo de $D$ jamais pertencerá a uma chave candidata mínima.
3. **Conjunto $M$ (Intermediários / Ambos os Lados):** Atributos que aparecem tanto no LHS quanto no RHS.

### Algoritmo Prático:
- **Passo 1:** Calcule o fecho $L^+$ do conjunto essencial $L$. Se $L^+ = R$, então $L$ é a **única** chave candidata de $R$!
- **Passo 2:** Se $L^+ \neq R$, combine $L$ com 1 atributo de $M$ por vez ($L \cup \{m_i\}$) e calcule $(L \cup \{m_i\})^+$. Todo conjunto que fechar $R$ é chave candidata!
- **Passo 3:** Todo atributo que pertence a **pelo menos uma** chave candidata é chamado de **Atributo Primo** (`ibd-parte6.pdf`). Os demais são **Atributos Não-Primos**.

---

## 3. Exemplo Análogo Resolvido Passo a Passo (Domínio Diferente: *Esquema $S(P, Q, R, T, U)$*)

> **Atenção:** Este exemplo usa o esquema $S(P, Q, R, T, U)$ com $F = \{PQ \to R,\; R \to P,\; QR \to T,\; T \to U\}$ para demonstrar como encontrar múltiplas chaves candidatas antes de você resolver `R1.7`.

### Resolução Passo a Passo:
1. **Particionamento dos atributos de $S = \{P, Q, R, T, U\}$:**
   - Lados direitos (RHS) presentes em $F$: $\{R, P, T, U\}$.
   - **$L$ (Nunca aparecem no RHS):** $\{Q\}$ (logo $Q$ está em **todas** as chaves candidatas!).
   - **$D$ (Apenas no RHS):** $\{U\}$ (nunca fará parte de chave candidata).
   - **$M$ (Ambos os lados):** $\{P, R, T\}$.
2. **Teste de Fecho de $L = \{Q\}$:**
   - $\{Q\}^+ = \{Q\} \neq S$. Precisamos combinar $Q$ com elementos de $M = \{P, R, T\}$:
3. **Testando pares com $Q$:**
   - **$\{P, Q\}^+$:**
     - Base: $\{P, Q\}$
     - Usa $PQ \to R \implies \{P, Q, R\}$
     - Usa $QR \to T \implies \{P, Q, R, T\}$
     - Usa $T \to U \implies \{P, Q, R, T, U\} = S$. **Logo $\{P, Q\}$ é Chave Candidata ($CK_1$)!**
   - **$\{Q, R\}^+$:**
     - Base: $\{Q, R\}$
     - Usa $R \to P \implies \{P, Q, R\}$
     - Usa $QR \to T \implies \{P, Q, R, T\}$
     - Usa $T \to U \implies \{P, Q, R, T, U\} = S$. **Logo $\{Q, R\}$ é Chave Candidata ($CK_2$)!**
   - **$\{Q, T\}^+$:**
     - Base: $\{Q, T\}$
     - Usa $T \to U \implies \{Q, T, U\} \neq S$ (não é superchave).
4. **Conclusão:**
   - **Chaves Candidatas:** $\{P, Q\}$ e $\{Q, R\}$.
   - **Atributos Primos:** $\{P, Q, R\}$.
   - **Atributos Não-Primos:** $\{T, U\}$.
