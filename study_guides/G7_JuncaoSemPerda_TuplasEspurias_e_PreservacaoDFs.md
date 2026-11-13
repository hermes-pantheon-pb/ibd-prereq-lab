# 📘 Ficha de Estudo G7 — Junção Sem Perda (Não-Aditiva), Tuplas Espúrias e Preservação de DFs

> **Exercícios Vinculados na Rodada 2:** `R2.6`, `R2.7`  
> **Base Direta no Material da Disciplina:** `ibd-parte6.pdf` (Guideline 4: Proibição de Tuplas Espúrias; Propriedade da Junção Sem Perda / Não-Aditiva `NJ`; Preservação de Dependências Funcionais na Decomposição).

---

## 1. Guideline 4 e o Fenômeno das Tuplas Espúrias (*Spurious Tuples*)

Ao decompor uma relação $R$ em sub-esquemas $\{R_1, R_2, \dots, R_m\}$, precisamos conseguir **reconstruir exatamente a extensão original $r(R)$** através do operador de **Junção Natural (`NATURAL JOIN` / $\bowtie$)**:
$$R_1 \bowtie R_2 \bowtie \dots \bowtie R_m = r(R)$$

- Se o conjunto de atributos em comum entre duas tabelas **não identificar unicamente as tuplas de pelo menos uma delas**, o `JOIN` cruza linhas que não pertenciam umas às outras no mundo real — gerando **tuplas espúrias (falsas)**! Isso é chamado de **Decomposição com Perda (Lossy-Join)**.

---

## 2. Teste Formal de Junção Sem Perda para Decomposição Binária $\{R_1, R_2\}$

Uma decomposição de $R$ em **duas** relações $R_1$ e $R_2$ (onde $R_1 \cup R_2 = R$) possui a propriedade da **Junção Sem Perda (Lossless / Não-Aditiva)** com respeito a $F$ **se e somente se** ao menos uma das seguintes dependências pertencer a $F^+$:

1. **$(R_1 \cap R_2) \to R_1$** *(a interseção é superchave de $R_1$)*, **OU**
2. **$(R_1 \cap R_2) \to R_2$** *(a interseção é superchave de $R_2$)*.

> **Como testar em 10 segundos na prova:**
> Calcule o fechamento **$(R_1 \cap R_2)^+$** usando $F$.
> Se $(R_1 \cap R_2)^+$ contiver todos os atributos de $R_1$ **OU** todos os atributos de $R_2$, a decomposição é **SEM PERDA**. Caso contrário, **TEM PERDA (gera tuplas espúrias)**!

---

## 3. Preservação de Dependências Funcionais

Uma decomposição $D = \{R_1, R_2, \dots, R_m\}$ **preserva dependências** se, ao projetar $F^+$ sobre cada sub-relação $R_i$ (formando $\pi_{R_i}(F)$ com as DFs cujos atributos estão todos contidos dentro de $R_i$), a união dessas projeções ainda implicar logicamente todas as DFs originais:
$$(\pi_{R_1}(F) \cup \pi_{R_2}(F) \cup \dots \cup \pi_{R_m}(F))^+ = F^+$$

- **Por que isso importa?** Se uma DF $X \to Y$ não for preservada em nenhuma tabela individual, o SGBD não consegue checá-la com uma simples chave `PRIMARY KEY`/`UNIQUE` local — exigiria `JOIN` caro ou `CREATE ASSERTION`!

---

## 4. Exemplo Análogo Resolvido (Domínio Diferente: *Transporte de Encomendas*)

> **Atenção:** Este exemplo usa **Entregas e Centros de Distribuição** (`ENTREGA`), domínio distinto de `EMP_PROJ_LOC` (`R2.6`) e do esquema abstrato $R(A,B,C,D,E)$ (`R2.7`).

Considere $R(\text{CodEnvio}, \text{PlacaVan}, \text{CidadeDestino})$ com $F = \{ \text{CodEnvio} \to \text{PlacaVan}, \text{CodEnvio} \to \text{CidadeDestino}, \text{PlacaVan} \to \text{CidadeDestino} \}$.

- **Tentativa ERRADA (Decomposição por atributo em comum não-chave):**
  $R_1(\text{CodEnvio}, \text{CidadeDestino})$ e $R_2(\text{PlacaVan}, \text{CidadeDestino})$.
  - **Interseção:** $R_1 \cap R_2 = \{\text{CidadeDestino}\}$.
  - **Fecho da interseção:** $\{\text{CidadeDestino}\}^+ = \{\text{CidadeDestino}\}$, que **não contém** $\text{CodEnvio}$ (não cobre $R_1$) nem $\text{PlacaVan}$ (não cobre $R_2$)!
  - **Consequência:** Se a Van `ABC-1` e a Van `XYZ-9` ambas entregam em `'Belo Horizonte'`, ao fazer $R_1 \bowtie R_2$ (`ON R1.CidadeDestino = R2.CidadeDestino`), um envio da Van `ABC-1` será pareado falsamente com a Van `XYZ-9` (**tupla espúria**)! Além disso, a DF `CodEnvio -> PlacaVan` **foi perdida**!

- **Tentativa CORRETA (Junção Sem Perda + Preservação de todas as DFs):**
  $R_1(\text{CodEnvio}, \text{PlacaVan})$ e $R_2(\text{PlacaVan}, \text{CidadeDestino})$.
  - **Interseção:** $R_1 \cap R_2 = \{\text{PlacaVan}\}$.
  - **Teste:** Como $\text{PlacaVan} \to \text{CidadeDestino}$, temos $\{\text{PlacaVan}\}^+ \supseteq R_2$ $\implies$ **Junção Sem Perda!**
  - **Preservação:** `CodEnvio -> PlacaVan` fica em $R_1$, `PlacaVan -> CidadeDestino` fica em $R_2$, e por transitividade `CodEnvio -> CidadeDestino` continua derivável!
