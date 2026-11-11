"""
Module Generator for IBD Studio:
Expands curriculum.json and db_engine.py with:
- Módulo 7: Mapeamento ER para Esquema Relacional e Restrições Estruturais
- Módulo 8: Normalização de Bancos de Dados: DF, Fechamento (Closure), 1FN, 2FN e 3FN
And embeds the official exercises from:
- ExerciciosNormalizacaoSemResposta.pdf (Q1, Q2, Q3)
- ExercicioProjetoLogico.pdf (Voo/Trecho/Aeroporto)
"""

import json

NEW_MODULES = [
    {
        "id": 7,
        "badge": "Módulo 7",
        "title": "Módulo 7: Mapeamento ER/EER para Esquema Relacional (Transformação)",
        "summary": "Domine as 7 regras fundamentais de transformação de diagramas ER e EER em tabelas relacionais com PKs, FKs, políticas de remoção (b, p, n) e restrições estruturais formais em álgebra relacional e SQL.",
        "concepts": [
            {
                "title": "Regra 1 e 2: Entidades Fortes e Atributos Multivalorados",
                "content": "- **Entidade Forte:** Cria-se uma relação $R$ contendo todos os atributos simples e as folhas de atributos compostos. A chave primária $PK$ é a chave da entidade.\n- **Atributos Multivalorados (Elipse Dupla):** Cria-se uma **nova relação** $R_{multi}(PK, Atributo)$, onde a chave primária composta é $(PK, Atributo)$ e $R_{multi}[PK] \\xrightarrow{p} R[PK]$ (política $p$ / CASCADE obrigatória)."
            },
            {
                "title": "Regra 3: Entidades Fracas (Retângulo Duplo)",
                "content": "Para cada tipo de entidade fraca $W$ com entidade dona $E$:\n- Cria-se uma relação $W$.\n- A chave primária de $W$ é a combinação da chave primária do dono com a chave parcial (discriminador) da fraca: $PK(W) = (PK(E), ChaveParcial)$.\n- A chave estrangeira $W[PK(E)] \\xrightarrow{p} E[PK(E)]$ possui **obrigatoriamente política $p$ (propagação / ON DELETE CASCADE)**."
            },
            {
                "title": "Regra 4 e 5: Relacionamentos 1:1, N:1 e M:N",
                "content": "- **Relacionamento N:1:** Mapeamento otimizado: inclui-se a chave primária do lado '1' como chave estrangeira $FK$ na relação do lado 'N' ($R_N[FK] \\rightarrow R_1[PK]$).\n- **Relacionamento 1:1:** Escolhe-se o lado com participação total para receber a $FK$ do outro lado (com restrição `UNIQUE`).\n- **Relacionamento M:N (Losango com M e N):** Cria-se uma **nova relação de relacionamento** $R_{rel}(PK_1, PK_2, AtributosRel)$ onde a chave primária é composta pelas duas chaves estrangeiras: $PK = (PK_1, PK_2)$, ambas com política $p$ (CASCADE)."
            },
            {
                "title": "Regra 6 e 7: Hierarquias EER (Mapeamento 1-1 vs. Otimizado)",
                "content": "- **Mapeamento 1-1 (Tabelas Separadas):** Cria-se a superclasse e uma relação para cada subclasse com $PK$ igual à da superclasse ($Sub[PK] \\xrightarrow{p} Super[PK]$).\n- **Mapeamento Otimizado (Tabela Única):** Colapsa-se a superclasse e todas as subclasses em uma única tabela com atributos específicos anuláveis, controlados por restrições `CHECK` de tupla.\n- **Restrições Estruturais em Álgebra Relacional:**\n  - Disjunção ('d'): $\\pi_{PK}(S_1) \\cap \\pi_{PK}(S_2) = \\emptyset$\n  - Totalidade (Linha Dupla): $\\bigcup \\pi_{PK}(S_i) = \\pi_{PK}(Super)$"
            }
        ],
        "exercises": ["T7.1", "T7.2", "E7.1"]
    },
    {
        "id": 8,
        "badge": "Módulo 8",
        "title": "Módulo 8: Normalização de Dados — DF, Fechamento (Closure), 1FN, 2FN e 3FN",
        "summary": "Meça formalmente a qualidade do projeto relacional: anomalias de atualização, algoritmo de Fechamento de Atributos (X+), identificação de chaves candidatas e decomposição passo a passo em 1FN, 2FN e 3FN.",
        "concepts": [
            {
                "title": "As 3 Anomalias de Atualização e Valores Nulos",
                "content": "Quando um esquema mistura múltiplos conceitos em uma relação (ex: `Emp_Dept` agrupando dados de empregado e departamento):\n\n1. **Anomalia de Inserção:** Não é possível inserir um departamento novo antes que ele possua pelo menos um empregado cadastrado (pois a PK da tabela é o SSN do empregado).\n2. **Anomalia de Remoção:** Se removermos o último empregado de um departamento, os dados do departamento (nome, gerente) são perdidos para sempre.\n3. **Anomalia de Modificação:** Se o gerente do departamento mudar, centenas de linhas de empregados precisam ser atualizadas; se uma linha falhar, o banco fica inconsistente."
            },
            {
                "title": "Algoritmo de Fechamento de Atributos (X+) e Determinação de Chaves",
                "content": "Para encontrar o fechamento $X^+$ de um conjunto de atributos $X$ sob dependências funcionais $F$:\n1. Inicialize $X^+ = X$.\n2. Repita: para cada dependência $Y \\rightarrow Z$ em $F$, se $Y \\subseteq X^+$, então $X^+ = X^+ \\cup Z$.\n3. Pare quando $X^+$ não crescer mais.\n\n**Teste de Chave Candidata:**\n- $X$ é uma **Superchave** se $X^+$ contiver todos os atributos da relação.\n- $X$ é uma **Chave Candidata** se for superchave e nenhum subconjunto próprio de $X$ for superchave (minimalidade)."
            },
            {
                "title": "1FN, 2FN e 3FN: Critérios de Decomposição",
                "content": "- **Primeira Forma Normal (1FN):** Todos os valores de atributos devem ser atômicos (proibido valores multivalorados ou relações aninhadas).\n- **Segunda Forma Normal (2FN):** Está na 1FN e **nenhum atributo não-chave depende parcialmente de qualquer chave candidata composta**. Se $AB$ é chave e $A \\rightarrow C$, a relação viola 2FN e deve ser decomposta em $R_1(A, C)$ e $R_2(A, B, \\dots)$.\n- **Terceira Forma Normal (3FN):** Está na 2FN e **nenhum atributo não-chave depende transitivamente da chave primária** (ou seja, não pode haver $X \\rightarrow Y$ onde $X$ não seja superchave e $Y$ não seja atributo primo). Se $SSN \\rightarrow DNum$ e $DNum \\rightarrow DName$, decompõe-se em $R_1(SSN, \\dots, DNum)$ e $R_2(DNum, DName)$."
            }
        ],
        "exercises": ["T8.1", "T8.2", "E8.1", "E8.2", "E8.3"]
    }
]

# Update generate_curriculum.py with the 8 modules
with open("generate_curriculum.py", "r", encoding="utf-8") as f:
    code = f.read()

# Read curriculum.json, add modules, save
with open("curriculum.json", "r", encoding="utf-8") as f:
    curr = json.load(f)

# Keep first 6 modules, append module 7 and 8
curr["modules"] = [m for m in curr["modules"] if m["id"] <= 6] + NEW_MODULES

with open("curriculum.json", "w", encoding="utf-8") as f:
    json.dump(curr, f, indent=2, ensure_ascii=False)

print("Curriculum updated with Modules 7 & 8!")
