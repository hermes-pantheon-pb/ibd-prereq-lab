# 📘 Ficha de Estudo G1 — Mapeamento ER Básico, Entidades Fracas e Políticas de RIR (`b`, `p`, `n`)

> **Exercícios Vinculados na Rodada 1:** `R1.1`, `R1.2`, `R1.3` (Domínio do Problema: *Sistema Hospitalar & Prontuário Clínico*)  
> **Base Direta no Material da Disciplina:** `ibd-parte5.pdf` (*Projeto Lógico de BDs — Etapa 1: Mapeamento do Modelo ER Básico, Regras 1 a 6, e Especificação de Políticas de Remoção em Restrições de Integridade Referencial*) e `ExercicioProjetoLogico.pdf`.

---

## 1. Resumo Sistemático das 6 Regras da Etapa 1 (`ibd-parte5.pdf`)

| Construção no Esquema ER | Regra de Mapeamento Relacional (`ibd-parte5.pdf`) | Política de Remoção RIR Padrão |
| :--- | :--- | :--- |
| **1. Tipo de Entidade Forte $E$** | Cria-se uma relação $E$ com os atributos simples. A chave de $E$ torna-se a PK com restrição `(nn)`. | — |
| **2a. Atributo Composto** | **Achatamento (Flattening):** Incluem-se apenas os sub-atributos componentes atômicos na relação da entidade dona. O nome do grupo composto desaparece. | — |
| **2b. Atributo Multivalorado $\{M\}$** | Cria-se uma **nova relação** $R_M(\underline{PK_E(nn), M(nn)})$. A chave primária é composta por ambos os atributos! | `R_M[PK_E] -p-> E[PK_E]` (**Propagação / CASCADE**) |
| **3. Entidade Fraca $W$ (Dona $E$)** | Cria-se a relação $W$ incluindo a PK da entidade dona $E$ como FK `(nn)`. A PK de $W$ é composta: $(\underline{PK_E(nn), ChaveParcial_W(nn)})$. | `W[PK_E] -p-> E[PK_E]` (**Propagação / CASCADE**) |
| **4. Relacionamento Binário `1:1`** | • **Ambos `(1,1)` total:** Fusão em relação única.<br>• **Um lado `(1,1)` total e outro `(0,1)` parcial:** A relação do lado **total `(1,1)`** recebe a PK do lado parcial como FK `(nn)` + atributos do relacionamento.<br>• **Ambos `(0,1)` parciais:** FK anulável em um dos lados (ou nova tabela se pouquíssimas instâncias participam). | `-b->` (**Bloqueio**) se vínculo obrigatório, ou `-n->` (**Nulos**) se opcional |
| **5. Relacionamento Binário `1:N`** | A relação do lado **`N`** (que tem cardinalidade máxima `1` na notação `(min,max)`, isto é, `(0,1)` ou `(1,1)`) absorve a PK do lado **`1`** como FK + atributos próprios do relacionamento. | `-b->` se participação total `(1,1)` (FK é `nn`), ou `-n->` / `-b->` se parcial `(0,1)` |
| **6. Relacionamento Binário `M:N`** | Cria-se obrigatoriamente uma **nova relação** $R_{MN}(\underline{PK_A(nn), PK_B(nn)}, \text{AtributosRel})$. PK composta pelas duas FKs. | Duas RIRs com política `-p->` (**Propagação**) ou `-b->` conforme regra do negócio |

---

## 2. Exemplo Análogo Resolvido Passo a Passo (Domínio Diferente: *Rede Bancária*)

> **Atenção:** Este exemplo usa objetos do domínio bancário (`BANCO`, `AGENCIA`, `CLIENTE`, `CONTA`, `GERENTE`) para demonstrar exatamente a mecânica exigida nos exercícios `R1.1` a `R1.3` (que tratam de um *Hospital*).

### Enunciado do Exemplo Análogo (Rede Bancária — Elmasri & Navathe Cap. 7/9):
Considere o seguinte esquema ER de um sistema bancário:
1. **`BANCO`** (Entidade Forte): `CodBanco` (PK), `NomeBanco`, atributo composto `Sede(Logradouro, Cidade, UF)` e atributo multivalorado `{TelefonesSAC}`.
2. **`AGENCIA`** (Entidade Fraca identificada por `BANCO` via relacionamento identificador `POSSUI_AGENCIA` `1:N` com participação total de `AGENCIA`): chave parcial `NumAgencia` (sublinhado tracejado) e `Bairro`.
3. **`FUNCIONARIO`** (Entidade Forte): `CPF` (PK), `NomeFunc`, `Salario`.
4. **Relacionamento `GERENCIA` (`1:1`):** Entre `AGENCIA` com `(1,1)` (toda agência tem exatamente 1 gerente) e `FUNCIONARIO` com `(0,1)` (nem todo funcionário é gerente), com atributo `DataInicioGerencia`.
5. **Relacionamento `LOTADO_EM` (`1:N`):** Uma `AGENCIA` emprega `(0,N)` funcionários, e cada `FUNCIONARIO` está lotado em `(0,1)` agência, com atributo `RamalInterno`.
6. **Relacionamento `OPERACAO_CAIXA` (`M:N`):** Entre `FUNCIONARIO` `(0,N)` e `CLIENTE(CPFCli, NomeCli)` `(0,N)`, com atributo `ValorMovimentado`.

### Resolução Completa do Exemplo Análogo no Padrão da Prova (UFMG):

#### Passo A: Entidades Fortes, Atributo Composto e Multivalorado
- O atributo composto `Sede` é **achatado** em `Logradouro`, `Cidade`, `UF`.
- O atributo multivalorado `{TelefonesSAC}` vira uma **nova relação** com PK composta e RIR de propagação (`p`):
```text
BANCO(CodBanco(nn), NomeBanco(nn), Logradouro, Cidade, UF)
  PK: CodBanco

BANCO_TELEFONES(CodBanco(nn), TelefoneSAC(nn))
  PK: (CodBanco, TelefoneSAC)
  RIR: BANCO_TELEFONES[CodBanco] -p-> BANCO[CodBanco]
```

#### Passo B: Entidade Fraca (`AGENCIA`) e Relacionamento `1:1` (`GERENCIA`)
- Como `AGENCIA` é fraca de `BANCO`, sua PK concatena `CodBanco(nn)` + `NumAgencia(nn)`.
- Como `AGENCIA` tem participação **total `(1,1)`** em `GERENCIA` e `FUNCIONARIO` tem participação **parcial `(0,1)`**, a FK `CPFGerente(nn)` e o atributo `DataInicioGerencia` são absorvidos por `AGENCIA` (evitando nulos!):
```text
FUNCIONARIO(CPF(nn), NomeFunc(nn), Salario, CodBancoLotacao, NumAgenciaLotacao, RamalInterno)
  PK: CPF

AGENCIA(CodBanco(nn), NumAgencia(nn), Bairro, CPFGerente(nn), DataInicioGerencia)
  PK: (CodBanco, NumAgencia)
  Chave Alternativa (UNIQUE): CPFGerente
  RIR 1: AGENCIA[CodBanco] -p-> BANCO[CodBanco]
  RIR 2: AGENCIA[CPFGerente] -b-> FUNCIONARIO[CPF]
```

#### Passo C: Relacionamento `1:N` (`LOTADO_EM`) e `M:N` (`OPERACAO_CAIXA`)
- Em `LOTADO_EM`, o lado `N` é `FUNCIONARIO` (que aponta para no máximo 1 agência). Como a chave de `AGENCIA` é composta, a FK em `FUNCIONARIO` precisa das **duas colunas** `(CodBancoLotacao, NumAgenciaLotacao)`! E como a participação de `FUNCIONARIO` é parcial `(0,1)`, usamos política `n` (substituição por nulos) ou `b` (bloqueio):
```text
  RIR em FUNCIONARIO: FUNCIONARIO[CodBancoLotacao, NumAgenciaLotacao] -n-> AGENCIA[CodBanco, NumAgencia]

OPERACAO_CAIXA(CPFFunc(nn), CPFCli(nn), ValorMovimentado)
  PK: (CPFFunc, CPFCli)
  RIR 1: OPERACAO_CAIXA[CPFFunc] -p-> FUNCIONARIO[CPF]
  RIR 2: OPERACAO_CAIXA[CPFCli] -p-> CLIENTE[CPFCli]
```
