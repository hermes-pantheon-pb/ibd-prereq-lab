# Ficha de Estudo G11 — Mestrado EER (Opções 1/2/3, AR, Ternário M:N:1 & RIRs)

> **Exercícios Vinculados na Rodada 4:** `R4.1`, `R4.2`, `R4.3`, `R4.4`, `R4.5` (Módulo 7 — Alta Incidência em Provas)  
> **Base no Material da Disciplina:** `ibd-parte5.pdf` (Etapas 1–2: Opções de Hierarquias, Fórmulas de Álgebra Relacional, Ternário com cardinalidade `1` e RIRs `b, p, n`) & `ExercicioProjetoLogico.pdf`

---

## 1. Quando Usar Cada Opção de Especialização (`ibd-parte5.pdf`)

| Opção | Estrutura de Tabelas | Restrições Exigidas | Ponto Forte & Risco |
| :--- | :--- | :--- | :--- |
| **Opção 1 (1-1 / 8A)** | Superclasse `C(PK, ...)` + `Si(PK, ...)` | `π_PK(S1) ∩ π_PK(S2) = ∅` (disj.)<br>`π_PK(S1) ∪ π_PK(S2) = π_PK(C)` (total) | Funciona para qualquer `{d/o, total/parcial}`; exige `JOIN` para dados completos |
| **Opção 2 (Tabela Única / 8C)** | Apenas `C(PK, ..., AtribsS1, AtribsS2)` | `CHECK ((AtribS1 IS NOT NULL AND AtribS2 IS NULL) OR ...)` (para `{d, total}`) | Evita `JOIN`; gera muitos `NULL`s se as subclasses tiverem vários atributos próprios |
| **Opção 3 (Somente Subclasses / 8B)** | Apenas `S1(PK_C, ...)` e `S2(PK_C, ...)` | Só vale se especialização for **Total** (se for `{d, total}`, evita redundância e `NULL`) | **Proibida** em especialização parcial (perderia instâncias só da superclasse) |

---

## 2. Ternário com Lado `1` vs `M:N:P` & Políticas RIR

- **Regra do Ternário com lado `1` (`M:N:1`):** Se um par fixado dos lados `M` e `N` (ex.: `Projeto` e `Peca`) está ligado a no máximo **1** elemento do terceiro lado (ex.: `Fornecedor`), a `PRIMARY KEY` da tabela do relacionamento é composta **apenas pelas PKs dos lados `M` e `N`**: `FORNECE(<u>CodProj</u>, <u>CodPeca</u>, CodForn)`.
- **Políticas de Deleção (`RIR`):**
  - `-p->` (`CASCADE`): Entidade fraca, atributo multivalorado, tabela associativa `M:N` ou subclasse (`8A`).
  - `-n->` (`SET NULL`): Relação `N:1` com participação **parcial** `(0,1)` no lado da FK (coluna aceita `NULL`).
  - `-b->` (`RESTRICT`): Relação `N:1` com participação **total** `(1,1)` (`NOT NULL`), protegendo o pai enquanto houver dependentes.

---

## 3. Exemplos Análogos (Domínios Diferentes das Tarefas)

> **Atenção:** Este guia usa **Viajante Rodoviário**, **Clínica Veterinária** e **Rede de Farmácias**, distintos de *Cinemateca*, *Locadora de Veículos*, *Estágio Universitário*, *Cooperativa Bancária* e *Biblioteca* (`R4.1`–`R4.5`).

1. **Hierarquia `{d, total}` com Opção Tabela Única (`PASSAGEM` -> `CONVENCIONAL` / `LEITO`):**
   ```sql
   CREATE TABLE PASSAGEM (
     CodBilhete INTEGER PRIMARY KEY,
     NumPoltrona TEXT,      -- preenchido se CONVENCIONAL
     TaxaLencol REAL,       -- preenchido se LEITO
     CHECK ((NumPoltrona IS NOT NULL AND TaxaLencol IS NULL)
         OR (NumPoltrona IS NULL AND TaxaLencol IS NOT NULL))
   );
   ```
2. **Ternário `CONSULTA_MEDICA(Tutor, Pet, Veterinario)` com lado `1`:** Se cada par `(Pet, Especialidade)` é atendido por apenas **1** `Veterinario` fixo, a PK é `(IdPet, CodEsp)`, enquanto `CRM_Vet` entra como atributo não-chave com FK `CRM_Vet -> VETERINARIO`.
3. **Equações AR -> `CREATE ASSERTION` (`CLINICA` -> `{INTERNADO, AMBULATORIAL}`):**
   - `π_Id(INTERNADO) ∩ π_Id(AMBULATORIAL) = ∅` vira `NOT EXISTS (SELECT 1 FROM INTERNADO i JOIN AMBULATORIAL a ON i.Id = a.Id)`.
