# 📘 Ficha de Estudo G2 — Mapeamento EER: Hierarquias (`d`/`o`, Total/Parcial), `CHECK` e Relacionamentos Ternários

> **Exercícios Vinculados na Rodada 1:** `R1.4`, `R1.5` (Domínio do Problema: *Pós-Graduação & Pesquisa Universitária*)  
> **Base Direta no Material da Disciplina:** `ibd-parte5.pdf` (*Projeto Lógico de BDs — Etapa 2: Mapeamento de Construções do Modelo EER: Hierarquias de Especialização/Generalização — Opções 1, 2 e 3, Cláusula `CHECK` de Tupla, e Relacionamentos de Grau $\ge 3$*).

---

## 1. As 3 Opções de Mapeamento de Hierarquias EER (`ibd-parte5.pdf`)

Considere uma superclasse $S(\underline{K}, a_1, a_2)$ com subclasses $S_1(b_1)$ e $S_2(c_1)$:

| Opção (`ibd-parte5.pdf`) | Esquema Relacional Gerado | Quando é Recomendada / Limitações |
| :--- | :--- | :--- |
| **Opção 1: Relação Única (Superclasse absorve tudo)** | $S(\underline{K(nn)}, a_1, a_2, \text{Tipo}, b_1, c_1)$ | • Excelente quando há poucos atributos específicos nas subclasses e deseja-se evitar `JOIN`s.<br>• Exige cláusula **`CHECK`** na tupla para impor disjunção (`d`) e/ou totalidade! |
| **Opção 2: Apenas Relações das Subclasses (Sem tabela da superclasse)** | $S_1(\underline{K(nn)}, a_1, a_2, b_1)$<br>$S_2(\underline{K(nn)}, a_1, a_2, c_1)$ | • **SÓ É VÁLIDA** se a cobertura for **TOTAL** (linha dupla)! (Se fosse parcial, instâncias que não pertencem a nenhuma subclasse desapareceriam do banco).<br>• Se for sobreposta (`o`), gera redundância dos atributos herdados $a_1, a_2$. |
| **Opção 3: Relação da Superclasse + Relações das Subclasses** | $S(\underline{K(nn)}, a_1, a_2)$<br>$S_1(\underline{K(nn)}, b_1)$ com `S1[K] -p-> S[K]`<br>$S_2(\underline{K(nn)}, c_1)$ com `S2[K] -p-> S[K]` | • **Opção Universal:** Funciona para qualquer combinação (`d` ou `o`, Total ou Parcial).<br>• As chaves primárias das subclasses são também FKs para a superclasse com política **`p` (propagação / CASCADE)**. |

---

## 2. Padrões Exatos de Cláusula `CHECK` na Opção 1 (`ibd-parte5.pdf`)

Quando mapeamos na **Opção 1** (tabela única) com um atributo específico $b_1$ da Subclasse 1 e $c_1$ da Subclasse 2:

1. **Hierarquia Disjunta e Total (`d`, Linha Dupla — OU-Exclusivo / XOR):**
   Exatamente um dos dois conjuntos de atributos deve ser não-nulo:
   ```sql
   CHECK (
       (b1 IS NOT NULL AND c1 IS NULL)
       OR
       (b1 IS NULL AND c1 IS NOT NULL)
   )
   ```
2. **Hierarquia Disjunta e Parcial (`d`, Linha Simples — No máximo um):**
   Não podem ser ambos não-nulos ao mesmo tempo (mas ambos podem ser `NULL`):
   ```sql
   CHECK (
       (b1 IS NULL) OR (c1 IS NULL)
   )
   ```
3. **Hierarquia Sobreposta e Total (`o`, Linha Dupla — Pelo menos um):**
   Pelo menos um dos dois deve ser preenchido (e ambos podem ser preenchidos simultaneamente):
   ```sql
   CHECK (
       (b1 IS NOT NULL) OR (c1 IS NOT NULL)
   )
   ```

---

## 3. Exemplo Análogo Resolvido Passo a Passo (Domínio Diferente: *Frota Marítima*)

> **Atenção:** Este exemplo usa objetos do domínio marítimo (`EMBARCACAO`, `PETROLEIRO`, `PORTA_CONTENTOR`, `ATRACACAO`) para ilustrar o mesmo raciocínio cobrado em `R1.4` e `R1.5` (que tratam de uma *Universidade*).

### Enunciado do Exemplo Análogo:
1. **`EMBARCACAO` (`CodIMO`, `NomeNavio`, `Tonelagem`)** possui duas subclasses em uma especialização **Disjunta e Total (`d`, linha dupla)**:
   - **`PETROLEIRO`** com atributo específico `CapacidadeBarris(nn)`.
   - **`PORTA_CONTENTOR`** com atributo específico `MaximoTEUs(nn)`.
2. Relacionamento ternário **`ATRACACAO` (`M:N:P`)** conectando `EMBARCACAO`, `PORTO(CodPorto, NomePorto)` e `AGENTE_MARITIMO(CNPJAgente, RazaoSocial)`, com atributo `TaxaPortuaria`.

### Resolução Completa do Exemplo Análogo:
- **Mapeamento da Hierarquia `EMBARCACAO` pela Opção 1 (Tabela Única + `CHECK`):**
  ```sql
  CREATE TABLE EMBARCACAO (
      CodIMO VARCHAR(15) NOT NULL,
      NomeNavio VARCHAR(80) NOT NULL,
      Tonelagem NUMERIC(10,2) NOT NULL,
      CapacidadeBarris INTEGER,
      MaximoTEUs INTEGER,
      PRIMARY KEY (CodIMO),
      CHECK (
          (CapacidadeBarris IS NOT NULL AND MaximoTEUs IS NULL)
          OR
          (CapacidadeBarris IS NULL AND MaximoTEUs IS NOT NULL)
      )
  );
  ```
- **Mapeamento do Relacionamento Ternário `ATRACACAO`:**
  Relacionamentos de grau 3 (`M:N:P`) geram uma nova relação cuja chave primária é a concatenação das chaves primárias das 3 entidades participantes (a menos que uma das pontas tenha cardinalidade máxima 1):
  ```text
  ATRACACAO(CodIMO(nn), CodPorto(nn), CNPJAgente(nn), TaxaPortuaria)
    PK: (CodIMO, CodPorto, CNPJAgente)
    RIR 1: ATRACACAO[CodIMO] -p-> EMBARCACAO[CodIMO]
    RIR 2: ATRACACAO[CodPorto] -p-> PORTO[CodPorto]
    RIR 3: ATRACACAO[CNPJAgente] -p-> AGENTE_MARITIMO[CNPJAgente]
  ```
