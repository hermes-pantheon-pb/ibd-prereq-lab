# Ficha de Estudo G13 — Leitura Inversa, Relacionamento 1:1 Assimétrico & Mini-Simulado M7

> **Exercícios Vinculados na Rodada 5:** `R5.1`, `R5.2`, `R5.3`, `R5.4`, `R5.5` (Orquestra Final — Módulo 7)  
> **Base no Material da Disciplina:** `ibd-parte5.pdf` (Etapas 1–2, RIRs `-b->`/`-p->`/`-n->`, Mapeamento Bidirecional, `1:1` Assimétrico) & `ExercicioProjetoLogico.pdf`

---

## 1. Como Ler Cardinalidades a Partir do Esquema Lógico (Leitura Inversa)

| Padrão no Esquema Lógico | Significado no Diagrama ER Original |
| :--- | :--- |
| `T_filha(<u>PK_pai</u>, <u>Parcial</u>, ...)` + `T_filha[PK_pai] -p-> T_pai[PK_pai]` | **Entidade Fraca** ligada por relacionamento identificador (`(1,1)` no filho, `(1,N)` ou `(0,N)` no pai) |
| `T_N(<u>PK</u>, FK_pai(nn))` + `-b-> T_1[PK]` | Relação `1:N` com **participação total `(1,1)`** no lado de `T_N` (`NOT NULL`) |
| `T_A(<u>PK</u>, FK_B(unique, nn))` | Relação **`1:1` com participação total `(1,1)`** no lado de `T_A` (FK com `UNIQUE NOT NULL` impede múltiplos em `T_B`) |
| `T_A(<u>PK</u>, FK_B(unique))` + `-n-> T_B` | Relação **`1:1` parcial `(0,1)`** no lado de `T_A` (`UNIQUE` aceitando `NULL`) |

---

## 2. Exemplos Análogos (Domínios Diferentes das Tarefas)

> **Atenção:** Este guia usa **Museu & Exposições**, **Porto Marítimo** e **Hotelaria**, distintos de *Secretaria Acadêmica*, *Seguradora*, *Rede Hospitalar*, *Agência Espacial* e *Rede Ferroviária* (`R5.1`–`R5.5`).

1. **`1:1` Assimétrico (`COFRE (1,1)` vs `GERENTE (0,1)`):**
   - Todo cofre tem exatamente 1 gerente responsável, mas nem todo gerente cuida de um cofre.
   - **Regra:** Coloque `CPF_Gerente UNIQUE NOT NULL` dentro de `COFRE` (lado `(1,1)` total), eliminando `NULL`s na FK!
2. **Composto + Multivalorado Composto (`FORNECEDOR`):**
   - Composto simples `End(Logr, CEP)` achata como colunas normais em `FORNECEDOR(..., Logr, CEP)`.
   - Multivalorado composto `{Contatos(Nome, Ramal)}` vira tabela própria `FORN_CONTATO(<u>CNPJ</u>, <u>Nome</u>, <u>Ramal</u>)` com `FORN_CONTATO[CNPJ] -p-> FORNECEDOR[CNPJ]`.
3. **Invariante de Rede (`TRECHO` em Porto/Rodovia via `CREATE ASSERTION`):**
   - Proibir auto-laço na tabela de trechos: `NOT EXISTS (SELECT 1 FROM ROTA r WHERE r.Origem = r.Destino)`.
