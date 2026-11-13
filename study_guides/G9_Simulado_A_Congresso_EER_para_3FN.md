# Ficha de Estudo G9 — Simulado A: Da Análise de Requisitos & EER até SQL DDL e 3FN

> **Exercícios Vinculados na Rodada 3:** `R3.1`, `R3.2`, `R3.3`, `R3.4`, `R3.5` (Simulado A — 5 Etapas)  
> **Base no Material da Disciplina:** `ibd-parte5.pdf` (Etapas 1–2, EER `o`/`d`, Ternários, Políticas RIR `-b->`, `-p->`, `-n->`) e `ibd-parte6.pdf` (Normalização 1FN -> 2FN -> 3FN)

---

## 1. Fluxo Completo de uma Prova de Projeto de BD

| Etapa da Prova | Foco Técnico | Checklist de Pontuação Máxima |
| :--- | :--- | :--- |
| **1. Requisitos -> EER** | Entidades fortes/fracas, especialização `d`/`o`, ternários | Identificar fracas (linha dupla + chave parcial), multivalorados (elipse dupla) e relações de grau 3 |
| **2. Leitura EER** | Cardinalidade `(min, max)` & Opções `8A`/`8B`/`8C` | Usar `8A` para sobreposição (`o`) ou quando subclasses participam de relações próprias |
| **3. Lógico + RIRs** | PKs, FKs, `-b->`, `-p->`, `-n->` | Multivalorado e fraca usam `-p->` (`CASCADE`); relação `1:N` usa `-b->` (`RESTRICT`) ou `-n->` |
| **4. SQL DDL + CHECK** | Tradução literal para `CREATE TABLE` | Declarar `PRIMARY KEY (...)` composta, `FOREIGN KEY ... ON DELETE ...` e `CHECK (...)` |
| **5. Normalização Legada** | Auditar tabelas vindas de planilhas | Separar parciais (2FN) e transitivas (3FN) mesmo sobre dados que pareciam já modelados |

---

## 2. Exemplo Resolvido Análogo: Mostra de Cinema (Domínio Diferente)

> **Atenção:** Este guia usa **Mostra de Cinema (`MOSTRA`, `SALA_EXIBICAO`, `FILME`, `JURADO_CINEASTA`)**, domínio distinto do **Congresso Científico (`R3.1`–`R3.5`)**.

1. **Hierarquia `{o, parcial}`:** `PESSOA(<u>CPF</u>, Nome)` especializa-se em `CURADOR(RegCurador)` e `CINEASTA(DRT)` com sobreposição (`o`). Pela **Opção 8A**:
   - `PESSOA(<u>CPF</u>, Nome)`
   - `CURADOR(<u>CPF</u>, RegCurador)` com `CURADOR[CPF] -p-> PESSOA[CPF]`
   - `CINEASTA(<u>CPF</u>, DRT)` com `CINEASTA[CPF] -p-> PESSOA[CPF]`
2. **Entidade Fraca + Ternário:** `MOSTRA(<u>CodMostra</u>)` possui a fraca `SALA_EXIBICAO(<u>CodMostra</u>, <u>NumSala</u>, Lotacao)` (`-p->`), e `PREMIACAO(<u>CPF_Curador</u>, <u>CodFilme</u>, <u>CodCateg</u>, Pontos)` valida `CHECK (Pontos BETWEEN 0 AND 100)`.
3. **Normalização de Planilha Legada de Ingressos:**
   - Planilha inicial: `VENDA_BRUTA(<u>NumBilhete</u>, <u>CodSecao</u>, HoraSessao, CPFComprador, NomeComp, CodCupom, PercentualDesc)`
   - Parcial em `{NumBilhete, CodSecao}` -> `NumBilhete -> {CPFComprador, NomeComp, CodCupom, PercentualDesc}` e `CodSecao -> HoraSessao` (viola **2FN**).
   - Transitiva remanescente -> `CodCupom -> PercentualDesc` e `CPFComprador -> NomeComp` (viola **3FN**).
   - Final 3FN: `COMPRADOR(CPF, NomeComp)`, `CUPOM(CodCupom, PercentualDesc)`, `SECAO(CodSecao, HoraSessao)`, `BILHETE(NumBilhete, CPF, CodCupom)`, `INGRESSO_SECAO(NumBilhete, CodSecao)`.
