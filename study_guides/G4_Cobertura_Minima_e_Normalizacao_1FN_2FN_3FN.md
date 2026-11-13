# 📘 Ficha de Estudo G4 — Cobertura Mínima (Irredutível) e Decomposição 1FN $\to$ 2FN $\to$ 3FN

> **Exercícios Vinculados na Rodada 1:** `R1.8`, `R1.9`, `R1.10` (Domínio do Problema: *Cobertura Mínima, Concessionária `CAR_SALE` e Congresso Científico `SESSAO_CONGRESSO`*)  
> **Base Direta no Material da Disciplina:** `ibd-parte6.pdf` (*Seção 3.4: Cobertura Mínima de um Conjunto de DFs; Seção 4: Formas Normais Baseadas em Chaves Primárias e Definição Geral de 2FN e 3FN*) e `ExerciciosNormalizacaoSemResposta.pdf`.

---

## 1. Algoritmo Formal de Cobertura Mínima $F_c$ em 3 Passos (`ibd-parte6.pdf`, Seção 3.4)

Para transformar qualquer conjunto de DFs $F$ em sua **Cobertura Mínima (Conjunto Canônico Irredutível)** $F_c$:

1. **Passo 1 (Decomposição do Lado Direito / RHS Único):**
   - Substitua cada DF com mais de um atributo no lado direito $X \to \{A_1, A_2, \dots, A_k\}$ por $k$ dependências simples: $X \to A_1$, $X \to A_2$, ..., $X \to A_k$.
2. **Passo 2 (Remoção de Atributos Estranhos no Lado Esquerdo / LHS Mínimo):**
   - Para cada DF com lado esquerdo composto (ex: $XY \to Z$), teste se $X$ ou $Y$ é redundante no LHS:
     - Calcule $\{X\}^+$ em $F$. Se $Y \in \{X\}^+$ (ou $Z \in \{X\}^+$), então $Y$ é **estranho (redundante)** em $XY \to Z$, reduzindo-a para $X \to Z$!
3. **Passo 3 (Remoção de DFs Redundantes):**
   - Para cada DF restante $f: X \to A$, remova-a temporariamente formando $F' = F - \{f\}$ e calcule o fecho $\{X\}^+$ usando apenas $F'$.
   - Se $A \in \{X\}_{F'}^+$, então a dependência $X \to A$ é **derivável das outras (transitiva/redundante)** e deve ser eliminada!

---

## 2. Definição Geral de 1FN, 2FN e 3FN (`ibd-parte6.pdf`, Seção 4)

| Forma Normal | Regra Formal (`ibd-parte6.pdf`) | Como Decompor quando Violada |
| :--- | :--- | :--- |
| **1FN** | Todos os atributos possuem domínios **atômicos** (sem atributos multivalorados nem relações aninhadas). | Extraia o grupo repetitivo para uma nova relação com a PK da relação original + a chave do grupo repetitivo. |
| **2FN (Geral)** | Nenhum atributo **não-primo** depende **parcialmente** de qualquer chave candidata (isto é, não pode depender de um subconjunto próprio $X \subsetneq CK$). | Para cada determinante parcial $X \subsetneq CK$, crie uma nova relação $R_i(\underline{X}, \text{dependentes de } X)$ e remova os dependentes da relação original (mantendo $X$ como FK). |
| **3FN (Geral)** | Para toda DF não-trivial $X \to A$ em $R$: **ou (a)** $X$ é uma **superchave** de $R$, **ou (b)** $A$ é um **atributo primo** (pertence a alguma chave candidata). | Para cada determinante transitivo não-chave $Y \to Z$, crie uma nova relação $R_j(\underline{Y}, Z)$ e remova $Z$ da relação original (mantendo $Y$ como FK em $R$). |

---

## 3. Exemplo Análogo Resolvido Passo a Passo (Domínio Diferente: *Festival de Música*)

> **Atenção:** Este exemplo usa o esquema `SHOW_FESTIVAL` (com duas chaves candidatas!) para demonstrar o mesmo raciocínio cobrado em `R1.9` e `R1.10`.

### Enunciado do Exemplo Análogo:
Considere a relação `SHOW_FESTIVAL`:
$$\text{SHOW\_FESTIVAL}(\underline{\text{CodFestival}, \text{OrdemShow}}, \text{CodPalco}, \text{Horario}, \text{IdBanda}, \text{NomeBanda}, \text{CidadeFestival}, \text{CapacidadePalco}, \text{CacheShow})$$

Com as seguintes Dependências Funcionais $F$:
- **DF1:** $\{\text{CodFestival}, \text{OrdemShow}\} \to \{\text{CodPalco}, \text{Horario}, \text{IdBanda}, \text{CacheShow}\}$
- **DF2:** $\{\text{CodPalco}, \text{Horario}\} \to \{\text{CodFestival}, \text{OrdemShow}\}$ *(Um palco num horário só recebe um show de um festival)*
- **DF3:** $\text{CodFestival} \to \text{CidadeFestival}$
- **DF4:** $\text{CodPalco} \to \text{CapacidadePalco}$
- **DF5:** $\text{IdBanda} \to \text{NomeBanda}$

### Resolução Completa do Exemplo Análogo:
1. **Chaves Candidatas e Atributos Primos:**
   - $CK_1 = \{\text{CodFestival}, \text{OrdemShow}\}$ (PK escolhida)
   - $CK_2 = \{\text{CodPalco}, \text{Horario}\}$ (Chave Candidata Alternativa — `UNIQUE`)
   - **Atributos Primos:** `CodFestival`, `OrdemShow`, `CodPalco`, `Horario`.
   - **Atributos Não-Primos:** `IdBanda`, `NomeBanda`, `CidadeFestival`, `CapacidadePalco`, `CacheShow`.
2. **Decomposição para 2FN (Eliminando Dependências Parciais de $CK_1$ e $CK_2$):**
   - **DF3 ($\text{CodFestival} \to \text{CidadeFestival}$):** `CidadeFestival` (não-primo) depende apenas de `CodFestival` (parte de $CK_1$) $\implies$ **Viola 2FN!**
   - **DF4 ($\text{CodPalco} \to \text{CapacidadePalco}$):** `CapacidadePalco` (não-primo) depende apenas de `CodPalco` (parte de $CK_2$) $\implies$ **Viola a Definição Geral de 2FN!**
   - Extraímos `FESTIVAL` e `PALCO`:
     - `FESTIVAL(CodFestival(nn), CidadeFestival)` — PK: `CodFestival`
     - `PALCO(CodPalco(nn), CapacidadePalco)` — PK: `CodPalco`
     - `SHOW_2FN(CodFestival(nn), OrdemShow(nn), CodPalco(nn), Horario(nn), IdBanda(nn), NomeBanda, CacheShow)`
3. **Decomposição para 3FN (Eliminando Dependência Transitiva em `SHOW_2FN`):**
   - **DF5 ($\text{IdBanda} \to \text{NomeBanda}$):** `IdBanda` não é superchave e `NomeBanda` não é atributo primo $\implies$ **Viola 3FN!**
   - Extraímos `BANDA` e mantemos `IdBanda` como FK em `SHOW`:
     - `BANDA(IdBanda(nn), NomeBanda)` — PK: `IdBanda`
     - `SHOW(CodFestival(nn), OrdemShow(nn), CodPalco(nn), Horario(nn), IdBanda(nn), CacheShow)`
       - PK: `(CodFestival, OrdemShow)` | Chave Alternativa: `(CodPalco, Horario)`
       - FKs: `CodFestival -> FESTIVAL`, `CodPalco -> PALCO`, `IdBanda -> BANDA`.

