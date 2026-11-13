# 📘 Ficha de Estudo G6 — Engenharia Reversa (SQL DDL → Diagrama ER/EER) e `CREATE ASSERTION` para Hierarquias

> **Exercícios Vinculados na Rodada 2:** `R2.4`, `R2.5`  
> **Base Direta no Material da Disciplina:** `ibd-parte5.pdf` (Leitura bidirecional ER/EER $\leftrightarrow$ Esquema Relacional; Álgebra Relacional e `CREATE ASSERTION` SQL-92 para impor Totalidade e Disjunção em mapeamentos pela Opção 3).

---

## 1. Dicionário de Engenharia Reversa: O que cada Construto SQL DDL revela sobre o ER/EER?

Para reconstruir o Diagrama ER/EER original a partir de um script `CREATE TABLE`:

| Evidência no SQL DDL | Significado no Diagrama ER / EER Original (`ibd-parte5.pdf`) |
| :--- | :--- |
| **`PRIMARY KEY (K_Dono, K_Parcial)`** onde `K_Dono` é `FOREIGN KEY ... ON DELETE CASCADE` e só aponta para **1 tabela pai** | **Entidade Fraca** (retângulo duplo) subordinada ao dono via **Relacionamento Identificador** (losango duplo, cardinalidade `(1,1)` no lado fraco com linha dupla)! *(Ou atributo multivalorado se não tiver outros atributos não-chave nem relacionamentos próprios.)* |
| **`PRIMARY KEY (K_A, K_B)`** onde `K_A` é FK para `A` e `K_B` é FK para `B` (ambas `ON DELETE CASCADE`) | **Relacionamento `M:N`** entre `A` (`(0,N)`) e `B` (`(0,N)`), com eventuais atributos próprios da tabela associativa no losango! |
| **`FK_X NOT NULL UNIQUE REFERENCES X(PK_X)`** dentro da tabela `Y` | **Relacionamento `1:1`** entre `Y` e `X`! Como `Y` recebeu a `FK` com `NOT NULL`, **`Y` tinha participação TOTAL `(1,1)`** no relacionamento e **`X` tinha participação `(0,1)`**! |
| **`FK_X NOT NULL REFERENCES X(PK_X)`** (sem `UNIQUE`) dentro da tabela `Y` | **Relacionamento `1:N`**! **`Y` está do lado `N` (`(1,1)` em `(min,max)`, pois `NOT NULL` indica `min=1`)**, enquanto `X` está do lado `1` (`(0,N)` em `(min,max)`)! Se `FK_X` aceitasse `NULL`, seria `(0,1)` em `Y`. |
| **Tabela `Sub(PK)` onde `PK` é simultaneamente `PRIMARY KEY` e `FOREIGN KEY REFERENCES Super(PK) ON DELETE CASCADE`** | **Hierarquia EER mapeada pela Opção 3 (1-1)**! `Sub` é subclasse da superclasse `Super`. |
| **Tabela única `Super` com atributos anuláveis `Atrib1, Atrib2` + `CHECK XOR`** | **Hierarquia EER mapeada pela Opção 1** (`(Atrib1 IS NOT NULL AND Atrib2 IS NULL) OR (Atrib1 IS NULL AND Atrib2 IS NOT NULL)` $\implies$ **Disjunta `d` e Total**)! |

---

## 2. Traduzindo Restrições EER (Opção 3) para `CREATE ASSERTION` SQL-92

Quando mapeamos uma hierarquia EER pela **Opção 3 (Superclasse + Subclasses separadas)**, chaves estrangeiras isoladas garantem apenas que toda instância de uma subclasse existe na superclasse (`Sub ⊆ Super`), mas **não garantem sozinhas**:
1. **Totalidade (Linha Dupla):** Todo elemento de `Super` precisa estar em pelo menos uma subclasse (`π(S1) ∪ π(S2) = π(Super)`).
   - Em `CREATE ASSERTION CHECK (NOT EXISTS (...))`, buscamos a **tupla violadora** — ou seja, um registro de `Super` que não aparece em nenhuma subclasse:
   ```sql
   CREATE ASSERTION VERIFICA_TOTALIDADE
   CHECK (NOT EXISTS (
       SELECT * FROM Super S
       WHERE S.PK NOT IN (SELECT PK FROM Sub1 UNION SELECT PK FROM Sub2)
   ));
   ```
2. **Disjunção (`'d'`):** Nenhuma instância pode pertencer a duas subclasses ao mesmo tempo (`π(S1) ∩ π(S2) = ∅`):
   ```sql
   CREATE ASSERTION VERIFICA_DISJUNCAO
   CHECK (NOT EXISTS (
       SELECT * FROM Sub1 S1, Sub2 S2
       WHERE S1.PK = S2.PK
   ));
   ```

> **Dica de Ouro:** No SQL-92 (`ibd-parte5.pdf`), você pode escrever duas asserções separadas OU unificar ambas as violações dentro de um único `NOT EXISTS ( SELECT PK FROM ... WHERE condição_violação_total UNION SELECT ... WHERE condição_violação_disjunção )`!

---

## 3. Exemplo Análogo Resolvido (Domínio Diferente: *Banco & Cartões Digitais*)

> **Atenção:** Este exemplo usa **Correntistas e Cartões Bancários** (`CORRENTISTA`, `CORRENTE`, `POUPANCA`, `CARTAO`), domínio distinto da Plataforma de Streaming (`R2.4`) e da Clínica Médica (`R2.5`).

### Exemplo de Engenharia Reversa + `CREATE ASSERTION` para Totalidade e Disjunção:
Dadas as tabelas:
```sql
CREATE TABLE CONTA_BANCARIA (
    NumConta INT PRIMARY KEY,
    Saldo NUMERIC(10,2) NOT NULL
);
CREATE TABLE CONTA_CORRENTE (
    NumConta INT PRIMARY KEY,
    LimiteCheque NUMERIC(8,2) NOT NULL,
    FOREIGN KEY (NumConta) REFERENCES CONTA_BANCARIA(NumConta) ON DELETE CASCADE
);
CREATE TABLE CONTA_POUPANCA (
    NumConta INT PRIMARY KEY,
    DiaAniversario INT NOT NULL,
    FOREIGN KEY (NumConta) REFERENCES CONTA_BANCARIA(NumConta) ON DELETE CASCADE
);
```
1. **Reconstrução EER:** Como `NumConta` em `CONTA_CORRENTE` e `CONTA_POUPANCA` é **ao mesmo tempo `PRIMARY KEY` e `FK` em cascata para `CONTA_BANCARIA`**, tratam-se de duas subclasses de `CONTA_BANCARIA` mapeadas pela **Opção 3**!
2. **Asserção Unificada para impor Hierarquia Disjunta (`d`) e Total (Linha Dupla):**
```sql
CREATE ASSERTION CONTA_DISJUNTA_TOTAL
CHECK (NOT EXISTS (
    -- Viola Totalidade: existe conta que não é nem Corrente nem Poupança
    SELECT C.NumConta FROM CONTA_BANCARIA C
    WHERE C.NumConta NOT IN (
        SELECT NumConta FROM CONTA_CORRENTE
        UNION
        SELECT NumConta FROM CONTA_POUPANCA
    )
    UNION
    -- Viola Disjunção: existe conta que está nas duas subclasses ao mesmo tempo
    SELECT CC.NumConta FROM CONTA_CORRENTE CC
    INNER JOIN CONTA_POUPANCA CP ON CC.NumConta = CP.NumConta
));
```
