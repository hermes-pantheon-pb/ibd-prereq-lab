# -*- coding: utf-8 -*-
"""
Banco de Exercícios Oficial / Estilo Prova — Rodada 2 (Módulos 7 e 8)
R2.1–R2.5: Módulo 7 (Recursividade, Cadeias Fracas, Subclasses Compartilhadas & Agregação, Engenharia Reversa, CREATE ASSERTION)
R2.6–R2.10: Módulo 8 (Tuplas Espúrias em SQL, Junção Sem Perda & Preservação de DFs, BCNF vs 3FN, Síntese 3FN com Fc, Auditoria ER→3FN)
"""

# ---------------------------------------------------------------------------
# Fichas de Estudo (Study Guides G5..G8 — domínios paralelos aos exercícios)
# ---------------------------------------------------------------------------

STUDY_GUIDE_G5 = {
    "id": "G5",
    "title": "G5 — Recursividade, Cadeias Fracas & Agregação EER",
    "file_path": "study_guides/G5_Recursividade_CadeiasFracas_e_AgregacaoEER.md",
    "coursework_ref": "ibd-parte5.pdf — Etapa 1 (Forte + M:N/1:N), Etapa 2 (Fraca em cadeia) e Slide 40 (Agregação EER & Reticulado)",
    "quick_rules_html": """
<div class="sg-rules-box">
  <h4>Resumo Operacional — Rodada 2 (Grupo G5)</h4>
  <ul>
    <li><strong>Relacionamento Recursivo (Auto-relacionamento):</strong>
      <ul>
        <li><code>1:N</code> recursivo (ex.: chefia/hierarquia): sem tabela nova; adicione a FK apontando para a <strong>PK da própria tabela</strong>, renomeada pelo papel (<code>IdSuperior NULL</code> para permitir a raiz).</li>
        <li><code>M:N</code> recursivo (ex.: composição/pré-requisito): crie tabela associativa com <strong>duas FKs apontando para a mesma tabela</strong>, com nomes distintos pelos papéis; a PK é o par composto <code>(<u>FK_Papel1</u>, <u>FK_Papel2</u>)</code>.</li>
      </ul>
    </li>
    <li><strong>Cadeia de Entidades Fracas (Forte &rarr; Fraca1 &rarr; Fraca2):</strong> Cada elo propaga toda a PK acumulada da proprietária anterior e soma sua chave parcial com <code>ON DELETE CASCADE</code>.</li>
    <li><strong>Subclasse Compartilhada (Herança Múltipla / Reticulado EER):</strong> Quando duas subclasses de uma mesma raiz superclasse convergem em uma subclasse comum, a PK herdada permanece única (a da raiz comum), evitando duplicidade de chave.</li>
    <li><strong>Agregação EER (Slide 40):</strong> Mapeie primeiro o relacionamento agregado como uma tabela associativa (com PK composta das entidades participantes) e faça o segundo relacionamento referenciar essa <strong>PK composta como FK</strong>.</li>
  </ul>
</div>
""",
    "example_html": """
<div class="sg-example-box">
  <h4>Exemplos Análogos (Domínios Diferentes da Tarefa)</h4>
  <p><strong>1. Grade Curricular Recursiva (M:N):</strong> Uma <code>DISCIPLINA(<u>CodDisc</u>, Nome, Creditos)</code> exige pré-requisitos entre si.</p>
  <pre class="sql-code">DISCIPLINA(<u>CodDisc</u>, Nome, Creditos)
PRE_REQUISITO(<u>CodDisc</u>, <u>CodPreReq</u>, NotaMinima)
  -- FK1: CodDisc &rarr; DISCIPLINA(CodDisc)
  -- FK2: CodPreReq &rarr; DISCIPLINA(CodDisc)</pre>
  <p><strong>2. Copa Esportiva em Cadeia Fraca (3 níveis):</strong> <code>TORNEIO(<u>CodTorneio</u>)</code> &rarr; <code>FASE(<u>NumFase</u>)</code> &rarr; <code>PARTIDA(<u>SeqPartida</u>)</code>:</p>
  <pre class="sql-code">TORNEIO(<u>CodTorneio</u>, Ano, Nome)
FASE(<u>CodTorneio</u>, <u>NumFase</u>, NomeFase)           -- FK: CodTorneio (CASCADE)
PARTIDA(<u>CodTorneio</u>, <u>NumFase</u>, <u>SeqPartida</u>, Placar) -- FK: (CodTorneio, NumFase) (CASCADE)</pre>
  <p><strong>3. Consultoria com Agregação EER:</strong> O relacionamento <code>(CONSULTOR — ATUA_EM — CLIENTE)</code> possui <code>APONTAMENTO(<u>IdApont</u>, Horas)</code>:</p>
  <pre class="sql-code">ATUA_EM(<u>CPF_Consultor</u>, <u>CNPJ_Cliente</u>, Funcao)
APONTAMENTO(<u>IdApont</u>, CPF_Consultor, CNPJ_Cliente, Horas)
  -- FK composta (CPF_Consultor, CNPJ_Cliente) &rarr; ATUA_EM(CPF_Consultor, CNPJ_Cliente)</pre>
</div>
"""
}

STUDY_GUIDE_G6 = {
    "id": "G6",
    "title": "G6 — Engenharia Reversa (DDL &rarr; ER) &amp; Assertions EER",
    "file_path": "study_guides/G6_EngenhariaReversa_e_Assertions_EER.md",
    "coursework_ref": "ibd-parte5.pdf — Leitura bidirecional Relacional &harr; ER/EER e Restrições de Disjunção/Totalidade (SQL-92 ASSERTION)",
    "quick_rules_html": """
<div class="sg-rules-box">
  <h4>Resumo Operacional — Rodada 2 (Grupo G6)</h4>
  <ul>
    <li><strong>Sinais de Engenharia Reversa (SQL &rarr; ER):</strong>
      <ul>
        <li><code>FK NOT NULL</code> em tabela forte &rarr; relacionamento <code>1:N</code> com participação <strong>total</strong> <code>(1,1)</code> no lado da FK.</li>
        <li><code>PK = (FK_Pai, ColunaParcial)</code> com <code>ON DELETE CASCADE</code> &rarr; <strong>Entidade Fraca</strong> ligada por losango identificador duplo.</li>
        <li>Tabela só de 2+ FKs compósitas na PK (+ atributos simples) &rarr; relacionamento <code>M:N</code>.</li>
        <li>Tabela filha cuja <strong>PK é exatamente uma FK</strong> para outra tabela &rarr; <strong>Especialização EER</strong> (Opção 8A) ou relação <code>1:1</code>.</li>
      </ul>
    </li>
    <li><strong><code>CREATE ASSERTION</code> para Disjunção &amp; Totalidade:</strong> Na Opção 8A (superclasse + subclasses em tabelas separadas), FKs garantem existência no pai, mas não impedem sobreposição nem ausência de subclasse: use <code>CHECK (NOT EXISTS (...))</code> global.</li>
  </ul>
</div>
""",
    "example_html": """
<div class="sg-example-box">
  <h4>Exemplo Análogo: Banco &amp; Cartões (Leitura Reversa + Invariante {d, total})</h4>
  <pre class="sql-code">-- Se uma conta NÃO pode ser Corrente e Poupança ao mesmo tempo (disjunção):
CREATE ASSERTION CONTA_DISJUNTA CHECK (
  NOT EXISTS (
    SELECT 1 FROM CONTA_CORRENTE c
    JOIN CONTA_POUPANCA p ON c.NumConta = p.NumConta
  )
);
-- Se toda CONTA_BANCARIA precisa estar em pelo menos uma subclasse (totalidade):
CREATE ASSERTION CONTA_TOTAL CHECK (
  NOT EXISTS (
    SELECT 1 FROM CONTA_BANCARIA cb
    WHERE cb.NumConta NOT IN (SELECT NumConta FROM CONTA_CORRENTE)
      AND cb.NumConta NOT IN (SELECT NumConta FROM CONTA_POUPANCA)
  )
);</pre>
  <p><strong>Leitura Reversa:</strong> se existir <code>CARTAO(<u>NumConta</u>, <u>SeqCartao</u>, Bandeira)</code> com FK <code>NumConta REFERENCES CONTA_BANCARIA ON DELETE CASCADE</code>, então <code>CARTAO</code> é uma <strong>Entidade Fraca</strong> (duplo retângulo) dependente de <code>CONTA_BANCARIA</code>.</p>
</div>
"""
}

STUDY_GUIDE_G7 = {
    "id": "G7",
    "title": "G7 — Junção Sem Perda, Tuplas Espúrias &amp; Preservação de DFs",
    "file_path": "study_guides/G7_JuncaoSemPerda_TuplasEspurias_e_PreservacaoDFs.md",
    "coursework_ref": "ibd-parte6.pdf — Diretriz 4 (Tuplas Espúrias), Propriedade de Junção Sem Perda (NJP) e Preservação de Dependências",
    "quick_rules_html": """
<div class="sg-rules-box">
  <h4>Resumo Operacional — Rodada 2 (Grupo G7)</h4>
  <ul>
    <li><strong>Diretriz 4 (Evitar Tuplas Espúrias):</strong> Decompor e depois recombinar com <code>NATURAL JOIN</code> sobre um atributo que <strong>não é superchave</strong> de nenhuma das partições gera tuplas falsas inexistentes no estado original.</li>
    <li><strong>Teste Binário de Junção Sem Perda (Lossless Join):</strong> Uma decomposição binária <code>D = {R1, R2}</code> de <code>R</code> tem junção sem perda sse a interseção <code>R1 &cap; R2</code> for superchave de <code>R1</code> <strong>OU</strong> superchave de <code>R2</code> sob <code>F+</code>:
      <br><code>(R1 &cap; R2) &rarr; R1 &isin; F+</code> &nbsp;ou&nbsp; <code>(R1 &cap; R2) &rarr; R2 &isin; F+</code>.
    </li>
    <li><strong>Preservação de Dependências:</strong> <code>D = {R1, R2}</code> preserva <code>F</code> quando todas as DFs de <code>F</code> podem ser verificadas individualmente dentro de <code>R1</code> ou <code>R2</code> (isto é, <code>(&pi;<sub>R1</sub>(F) &cup; &pi;<sub>R2</sub>(F))+ = F+</code>) sem precisar de <code>JOIN</code> entre tabelas.</li>
  </ul>
</div>
""",
    "example_html": """
<div class="sg-example-box">
  <h4>Exemplo Análogo: Transporte de Encomendas <code>ENTREGA(Envio, PlacaVan, Cidade)</code></h4>
  <p>Suponha <code>F = { Envio &rarr; PlacaVan, Cidade }</code>. Considere decompor em <code>D_ruim = { R1(Envio, Cidade), R2(PlacaVan, Cidade) }</code>:</p>
  <ul>
    <li><strong>Interseção:</strong> <code>R1 &cap; R2 = {Cidade}</code>.</li>
    <li><strong>Fecho:</strong> <code>{Cidade}+ = {Cidade}</code>. Não determina <code>Envio</code> nem <code>PlacaVan</code>!</li>
    <li><strong>Efeito no SQL:</strong> Se duas vans diferentes entregam em <code>'Belo Horizonte'</code> (Envio 10 com Van X; Envio 20 com Van Y), <code>R1 NATURAL JOIN R2</code> inventa <code>(10, Van Y, 'BH')</code> e <code>(20, Van X, 'BH')</code> &mdash; <strong>tuplas espúrias</strong>!</li>
    <li><strong>Correto:</strong> Decompor mantendo interseção como superchave (ex.: se houvesse <code>PlacaVan &rarr; Garagem</code>, então <code>PlacaVan</code> é superchave em <code>VANS(<u>PlacaVan</u>, Garagem)</code>).</li>
  </ul>
</div>
"""
}

STUDY_GUIDE_G8 = {
    "id": "G8",
    "title": "G8 — BCNF vs 3FN, Algoritmo de Síntese (Fc) &amp; Auditoria",
    "file_path": "study_guides/G8_BCNF_vs_3FN_Sintese_e_Auditoria.md",
    "coursework_ref": "ibd-parte6.pdf — 3FN (Exceção de Atributo Primo), Forma Normal de Boyce-Codd (BCNF) e Síntese 3FN a partir de Fc",
    "quick_rules_html": """
<div class="sg-rules-box">
  <h4>Resumo Operacional — Rodada 2 (Grupo G8)</h4>
  <ul>
    <li><strong>BCNF vs 3FN:</strong> Para toda DF não-trivial <code>X &rarr; A</code>:
      <ul>
        <li><strong>BCNF</strong> exige que <code>X</code> seja <strong>superchave</strong> (sem exceções).</li>
        <li><strong>3FN</strong> permite que <code>X</code> não seja superchave <em>se</em> <code>A</code> for <strong>atributo primo</strong> (pertencer a alguma chave candidata).</li>
      </ul>
    </li>
    <li><strong>Dilema Clássico:</strong> Toda relação tem decomposição BCNF sem perda, mas às vezes <strong>sacrifica a preservação de DFs</strong> (caso 3FN mas não BCNF). A 3FN sempre alcança <strong>ambas</strong> (sem perda + preservação).</li>
    <li><strong>Algoritmo de Síntese 3FN em 4 Passos:</strong> (1) Calcule a cobertura mínima <code>Fc</code> (RHS unitário, remova atributos estranhos no LHS, remova DFs redundantes); (2) Agrupe DFs de mesmo LHS <code>X &rarr; Y1..Yk</code> em <code>R_i(X, Y1..Yk)</code>; (3) Se nenhuma tabela contiver uma chave candidata de <code>R</code>, crie uma relação extra só com uma chave candidata; (4) Remova subconjuntos redundantes.</li>
  </ul>
</div>
""",
    "example_html": """
<div class="sg-example-box">
  <h4>Exemplos Análogos: Revisão de Artigos &amp; Síntese <code>W(P, Q, R, S, U)</code></h4>
  <p><strong>Caso 3FN mas NÃO BCNF:</strong> <code>REVISAO(Artigo, Area, Revisor)</code> com <code>F = { (Artigo, Area) &rarr; Revisor ; Revisor &rarr; Area }</code>.</p>
  <ul>
    <li>Chaves candidatas: <code>{Artigo, Area}</code> e <code>{Artigo, Revisor}</code>.</li>
    <li>Todos os 3 atributos são <strong>primos</strong>! Logo <code>Revisor &rarr; Area</code> é tolerada pela <strong>3FN</strong>, porém viola <strong>BCNF</strong> (<code>Revisor</code> não é superchave).</li>
    <li>Se decompusermos em BCNF <code>R1(<u>Revisor</u>, Area)</code> e <code>R2(<u>Artigo</u>, <u>Revisor</u>)</code>, eliminamos a redundância, mas perdemos a verificação local da DF <code>(Artigo, Area) &rarr; Revisor</code>.</li>
  </ul>
  <p><strong>Síntese 3FN com atributo ausente:</strong> Em <code>W(P, Q, R, S, U)</code> com <code>Fc = { P &rarr; Q, Q &rarr; R, P &rarr; S }</code>, note que <code>U</code> nunca aparece em <code>Fc</code>. Assim, a chave candidata é <code>{P, U}</code>! O passo 2 gera <code>R1(<u>P</u>, Q, S)</code> e <code>R2(<u>Q</u>, R)</code>; o passo 3 exige adicionar <code>R3(<u>P</u>, <u>U</u>)</code> para manter a junção sem perda.</p>
</div>
"""
}


# ---------------------------------------------------------------------------
# Dicionário Principal de Exercícios da Rodada 2 (R2.1 .. R2.10)
# ---------------------------------------------------------------------------

ROUND2_EXERCISES = {
    "R2.1": {
        "title": "R2.1 (Oficial/Estendido) — Mapeamento de Recursividade M:N e 1:N (Manufatura)",
        "type": "oficial",
        "mode": "structured",
        "study_guide": STUDY_GUIDE_G5,
        "context_html": """
<p><strong>Cenário Industrial (Padrão UFMG / Elmasri):</strong> O departamento de engenharia de uma fábrica modelou seus componentes mecânicos e sua estrutura de supervisão técnica no diagrama ER abaixo.</p>
<div style="text-align:center; margin: 14px 0;">
<svg viewBox="0 0 760 290" width="100%" style="max-width:740px; background:#0d1117; border:1px solid #30363d; border-radius:8px;">
  <defs>
    <marker id="arr21" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,1 L10,5 L0,9 z" fill="#8b949e"/></marker>
  </defs>
  <!-- PECA Entity -->
  <rect x="45" y="105" width="160" height="58" rx="4" fill="#161b22" stroke="#58a6ff" stroke-width="2.2"/>
  <text x="125" y="139" text-anchor="middle" fill="#f0f6fc" font-size="15" font-weight="700">PECA</text>
  <!-- Attributes PECA -->
  <ellipse cx="75" cy="48" rx="48" ry="20" fill="#161b22" stroke="#8b949e" stroke-width="1.5"/>
  <text x="75" y="53" text-anchor="middle" fill="#e6edf3" font-size="12" text-decoration="underline" font-weight="700">IdPeca</text>
  <line x1="85" y1="68" x2="105" y2="105" stroke="#8b949e" stroke-width="1.5"/>

  <ellipse cx="180" cy="48" rx="46" ry="20" fill="#161b22" stroke="#8b949e" stroke-width="1.5"/>
  <text x="180" y="53" text-anchor="middle" fill="#e6edf3" font-size="12">Peso</text>
  <line x1="168" y1="68" x2="145" y2="105" stroke="#8b949e" stroke-width="1.5"/>

  <!-- Recursive Diamond COMPOE -->
  <polygon points="315,134 365,98 415,134 365,170" fill="#1f2937" stroke="#d2a8ff" stroke-width="2"/>
  <text x="365" y="138" text-anchor="middle" fill="#d2a8ff" font-size="12" font-weight="700">COMPOE</text>
  <!-- Role top: [composto] (0,N) -->
  <path d="M 160,105 L 160,82 L 365,82 L 365,98" fill="none" stroke="#8b949e" stroke-width="1.6"/>
  <text x="260" y="76" text-anchor="middle" fill="#79c0ff" font-size="11">[composto] (0, N)</text>
  <!-- Role bottom: [componente] (0,N) -->
  <path d="M 160,163 L 160,192 L 365,192 L 365,170" fill="none" stroke="#8b949e" stroke-width="1.6"/>
  <text x="260" y="208" text-anchor="middle" fill="#79c0ff" font-size="11">[componente] (0, N)</text>
  <!-- Attr Qtd on COMPOE -->
  <ellipse cx="365" cy="240" rx="42" ry="18" fill="#161b22" stroke="#8b949e" stroke-width="1.5"/>
  <text x="365" y="244" text-anchor="middle" fill="#e6edf3" font-size="12">Qtd</text>
  <line x1="365" y1="170" x2="365" y2="222" stroke="#8b949e" stroke-width="1.5"/>

  <!-- Divider -->
  <line x1="445" y1="20" x2="445" y2="270" stroke="#30363d" stroke-dasharray="5,5"/>

  <!-- ENGENHEIRO Entity -->
  <rect x="485" y="105" width="175" height="58" rx="4" fill="#161b22" stroke="#3fb950" stroke-width="2.2"/>
  <text x="572" y="139" text-anchor="middle" fill="#f0f6fc" font-size="14" font-weight="700">ENGENHEIRO</text>
  <ellipse cx="520" cy="48" rx="48" ry="20" fill="#161b22" stroke="#8b949e" stroke-width="1.5"/>
  <text x="520" y="53" text-anchor="middle" fill="#e6edf3" font-size="12" text-decoration="underline" font-weight="700">CREA</text>
  <line x1="530" y1="68" x2="548" y2="105" stroke="#8b949e" stroke-width="1.5"/>
  <ellipse cx="630" cy="48" rx="48" ry="20" fill="#161b22" stroke="#8b949e" stroke-width="1.5"/>
  <text x="630" y="53" text-anchor="middle" fill="#e6edf3" font-size="12">NomeEng</text>
  <line x1="615" y1="68" x2="598" y2="105" stroke="#8b949e" stroke-width="1.5"/>

  <!-- Recursive Diamond SUPERVISIONA -->
  <polygon points="572,202 627,232 572,262 517,232" fill="#1f2937" stroke="#f2cc60" stroke-width="2"/>
  <text x="572" y="236" text-anchor="middle" fill="#f2cc60" font-size="11" font-weight="700">SUPERVISIONA</text>
  <!-- Role left: [subordinado] (0,1) -->
  <path d="M 510,163 L 510,232 L 517,232" fill="none" stroke="#8b949e" stroke-width="1.6"/>
  <text x="480" y="210" text-anchor="middle" fill="#ffa657" font-size="11">[subord.]</text>
  <text x="480" y="224" text-anchor="middle" fill="#ffa657" font-size="11">(0, 1)</text>
  <!-- Role right: [supervisor] (0,N) -->
  <path d="M 635,163 L 635,232 L 627,232" fill="none" stroke="#8b949e" stroke-width="1.6"/>
  <text x="692" y="210" text-anchor="middle" fill="#ffa657" font-size="11">[supervisor]</text>
  <text x="692" y="224" text-anchor="middle" fill="#ffa657" font-size="11">(0, N)</text>
</svg>
</div>
<p>Transforme os dois auto-relacionamentos (<code>COMPOE</code> e <code>SUPERVISIONA</code>) para o modelo relacional aplicando as regras das Etapas 4 e 5 de <code>ibd-parte5.pdf</code>.</p>
""",
        "answer_sheet_html": """
<div class="answer-sheet-box">
  <h4>Gabarito Explicado — R2.1 (Recursividade no Projeto Lógico)</h4>
  <ul>
    <li><strong>Relacionamento M:N recursivo (<code>COMPOE</code>):</strong> Cria-se uma nova relação com duas chaves estrangeiras apontando para <code>PECA(IdPeca)</code>, obrigatoriamente renomeadas segundo os papéis para não haver conflito de nomes de colunas:<br>
    <code>PECA(<u>IdPeca</u>, Peso)</code><br>
    <code>COMPOE(<u>IdPecaComposto</u>, <u>IdPecaComponente</u>, Qtd)</code>, onde ambas referenciam <code>PECA(IdPeca)</code>.</li>
    <li><strong>Relacionamento 1:N recursivo (<code>SUPERVISIONA</code>):</strong> Como cada subordinado tem no máximo 1 supervisor <code>(0, 1)</code>, aplica-se a regra de propagação 1:N (sem tabela extra), inserindo a auto-FK na própria tabela <code>ENGENHEIRO</code>:<br>
    <code>ENGENHEIRO(<u>CREA</u>, NomeEng, CREA_Supervisor)</code>, onde <code>CREA_Supervisor</code> referencia <code>ENGENHEIRO(CREA)</code> e aceita <code>NULL</code> (para diretores sem supervisor).</li>
  </ul>
</div>
""",
        "fields": [
            {
                "id": "f1",
                "label": "1) Mapeamento relacional correto para a entidade PECA e o relacionamento recursivo M:N COMPOE:",
                "options": [
                    "Manter apenas PECA(IdPeca, Peso, IdPecaComponente, Qtd), permitindo NULL em IdPecaComponente.",
                    "Criar PECA(IdPeca, Peso) e COMPOE(IdPecaComposto, IdPecaComponente, Qtd) com PK composta e duas FKs para PECA(IdPeca).",
                    "Criar PECA(IdPeca, Peso) e COMPOE(IdCompoe, IdPeca, Qtd) com apenas uma FK referenciando PECA(IdPeca).",
                    "Criar duas tabelas idênticas PECA_COMPOSTO(IdPeca, Peso) e PECA_COMPONENTE(IdPeca, Qtd) separadas."
                ],
                "answer": "Criar PECA(IdPeca, Peso) e COMPOE(IdPecaComposto, IdPecaComponente, Qtd) com PK composta e duas FKs para PECA(IdPeca).",
                "explanation": "Em relacionamentos M:N recursivos, cada ocorrência une duas peças distintas (ou subpeças) em papéis diferentes. Por isso cria-se uma tabela associativa cuja chave primária combina as duas FKs renomeadas pelos papéis."
            },
            {
                "id": "f2",
                "label": "2) Qual esquema relacional mapeia corretamente o auto-relacionamento 1:N SUPERVISIONA sem criar tabelas desnecessárias?",
                "options": [
                    "SUPERVISIONA(CREA_Supervisor, CREA_Subordinado) com chave primária obrigatória (CREA_Supervisor, CREA_Subordinado).",
                    "ENGENHEIRO(CREA, NomeEng, CREA_Subordinado) onde cada linha armazena toda a lista de subordinados diretos.",
                    "ENGENHEIRO(CREA, NomeEng, CREA_Supervisor) onde CREA_Supervisor é auto-FK para ENGENHEIRO(CREA) aceitando NULL.",
                    "ENGENHEIRO(CREA, NomeEng) junto de SUPERVISOR(CREA_Supervisor) contendo apenas a chave primária repetida."
                ],
                "answer": "ENGENHEIRO(CREA, NomeEng, CREA_Supervisor) onde CREA_Supervisor é auto-FK para ENGENHEIRO(CREA) aceitando NULL.",
                "explanation": "Na regra 1:N, a chave estrangeira migra sempre para o lado de cardinalidade máxima igual a 1 — neste caso, cada engenheiro no papel [subordinado] possui (0,1) supervisor, recebendo a auto-FK CREA_Supervisor anulável."
            },
            {
                "id": "f3",
                "label": "3) Por que é obrigatório renomear as duas colunas da FK na tabela associativa COMPOE e quais valores são admitidos?",
                "options": [
                    "Uma tabela relacional não pode ter dois atributos com o mesmo nome (IdPeca); os papéis distinguem o pai do componente na PK composta.",
                    "O SGBD exige que auto-relacionamentos M:N não possuam chaves estrangeiras declaradas, mantendo apenas índices textuais comuns.",
                    "Para que a coluna Qtd faça parte integrante da chave primária composta de COMPOE caso duas peças distintas sejam combinadas.",
                    "Para impedir que uma mesma peça seja componente de mais de uma peça composta diferente ao longo da lista de materiais."
                ],
                "answer": "Uma tabela relacional não pode ter dois atributos com o mesmo nome (IdPeca); os papéis distinguem o pai do componente na PK composta.",
                "explanation": "Pela definição formal do modelo relacional, nomes de atributos numa mesma relação devem ser únicos. Renomear para os papéis [composto] e [componente] evita colisão semântica e identifica cada arco da árvore de peças."
            }
        ]
    },

    "R2.2": {
        "title": "R2.2 (Lab SQL DDL) — Cadeia de Entidades Fracas em 3 Níveis (Resort)",
        "type": "oficial",
        "mode": "sql_ddl",
        "study_guide": STUDY_GUIDE_G5,
        "setup": "",
        "context_html": """
<p><strong>Modelagem em Cadeia de Dependência Existencial:</strong> Implemente em SQL DDL (<code>CREATE TABLE</code> no dialeto SQLite, com chaves estrangeiras ativas) o diagrama ER abaixo de uma rede de condomínios/resorts de 3 níveis:</p>
<div style="text-align:center; margin: 12px 0;">
<svg viewBox="0 0 760 215" width="100%" style="max-width:740px; background:#0d1117; border:1px solid #30363d; border-radius:8px;">
  <!-- RESORT (Forte) -->
  <rect x="28" y="88" width="120" height="50" rx="4" fill="#161b22" stroke="#58a6ff" stroke-width="2.2"/>
  <text x="88" y="118" text-anchor="middle" fill="#f0f6fc" font-size="14" font-weight="700">RESORT</text>
  <ellipse cx="62" cy="36" rx="46" ry="18" fill="#161b22" stroke="#8b949e" stroke-width="1.5"/>
  <text x="62" y="40" text-anchor="middle" fill="#e6edf3" font-size="11" text-decoration="underline" font-weight="700">CodResort</text>
  <line x1="68" y1="54" x2="78" y2="88" stroke="#8b949e" stroke-width="1.4"/>
  <ellipse cx="138" cy="36" rx="34" ry="18" fill="#161b22" stroke="#8b949e" stroke-width="1.5"/>
  <text x="138" y="40" text-anchor="middle" fill="#e6edf3" font-size="11">Nome</text>
  <line x1="130" y1="54" x2="110" y2="88" stroke="#8b949e" stroke-width="1.4"/>

  <!-- TEM (Identifying) -->
  <line x1="148" y1="113" x2="205" y2="113" stroke="#8b949e" stroke-width="1.6"/>
  <text x="174" y="103" text-anchor="middle" fill="#79c0ff" font-size="11">(1, N)</text>
  <polygon points="205,113 245,86 285,113 245,140" fill="#1f2937" stroke="#f0883e" stroke-width="2"/>
  <polygon points="212,113 245,91 278,113 245,135" fill="none" stroke="#f0883e" stroke-width="1.3"/>
  <text x="245" y="117" text-anchor="middle" fill="#f0883e" font-size="11" font-weight="700">TEM</text>
  <!-- Total double line -->
  <line x1="285" y1="110" x2="340" y2="110" stroke="#f0883e" stroke-width="1.6"/>
  <line x1="285" y1="116" x2="340" y2="116" stroke="#f0883e" stroke-width="1.6"/>
  <text x="312" y="102" text-anchor="middle" fill="#ffa657" font-size="11">(1, 1)</text>

  <!-- BLOCO (Fraca 1) -->
  <rect x="340" y="85" width="122" height="56" rx="4" fill="#161b22" stroke="#f0883e" stroke-width="2"/>
  <rect x="345" y="90" width="112" height="46" rx="2" fill="none" stroke="#f0883e" stroke-width="1.3"/>
  <text x="401" y="118" text-anchor="middle" fill="#f0f6fc" font-size="14" font-weight="700">BLOCO</text>
  <ellipse cx="401" cy="36" rx="48" ry="18" fill="#161b22" stroke="#8b949e" stroke-width="1.5"/>
  <text x="401" y="40" text-anchor="middle" fill="#e6edf3" font-size="11" stroke-dasharray="3,2" font-weight="700">CodBloco</text>
  <line x1="372" y1="44" x2="430" y2="44" stroke="#f0883e" stroke-width="1.3" stroke-dasharray="3,2"/>
  <line x1="401" y1="54" x2="401" y2="85" stroke="#8b949e" stroke-width="1.4"/>

  <!-- POSSUI (Identifying) -->
  <line x1="462" y1="113" x2="515" y2="113" stroke="#8b949e" stroke-width="1.6"/>
  <text x="488" y="103" text-anchor="middle" fill="#79c0ff" font-size="11">(1, N)</text>
  <polygon points="515,113 555,86 595,113 555,140" fill="#1f2937" stroke="#f0883e" stroke-width="2"/>
  <polygon points="522,113 555,91 588,113 555,135" fill="none" stroke="#f0883e" stroke-width="1.3"/>
  <text x="555" y="117" text-anchor="middle" fill="#f0883e" font-size="10" font-weight="700">POSSUI</text>
  <!-- Total double line -->
  <line x1="595" y1="110" x2="635" y2="110" stroke="#f0883e" stroke-width="1.6"/>
  <line x1="595" y1="116" x2="635" y2="116" stroke="#f0883e" stroke-width="1.6"/>
  <text x="615" y="102" text-anchor="middle" fill="#ffa657" font-size="11">(1, 1)</text>

  <!-- APARTAMENTO (Fraca 2) -->
  <rect x="635" y="85" width="112" height="56" rx="4" fill="#161b22" stroke="#f0883e" stroke-width="2"/>
  <rect x="640" y="90" width="102" height="46" rx="2" fill="none" stroke="#f0883e" stroke-width="1.3"/>
  <text x="691" y="118" text-anchor="middle" fill="#f0f6fc" font-size="12" font-weight="700">APARTAMENTO</text>
  <ellipse cx="660" cy="36" rx="42" ry="18" fill="#161b22" stroke="#8b949e" stroke-width="1.5"/>
  <text x="660" y="40" text-anchor="middle" fill="#e6edf3" font-size="11" font-weight="700">NumApto</text>
  <line x1="634" y1="44" x2="686" y2="44" stroke="#f0883e" stroke-width="1.3" stroke-dasharray="3,2"/>
  <line x1="665" y1="54" x2="675" y2="85" stroke="#8b949e" stroke-width="1.4"/>
  <ellipse cx="725" cy="178" rx="30" ry="16" fill="#161b22" stroke="#8b949e" stroke-width="1.5"/>
  <text x="725" y="182" text-anchor="middle" fill="#e6edf3" font-size="11">AreaM2</text>
  <line x1="712" y1="163" x2="700" y2="141" stroke="#8b949e" stroke-width="1.4"/>
</svg>
</div>
<p><strong>Requisitos exatos de nomenclatura e integridade para validação automática:</strong></p>
<ul>
  <li>Tabelas: <code>RESORT</code> (<code>CodResort</code> INT, <code>Nome</code> TEXT), <code>BLOCO</code> (<code>CodResort</code>, <code>CodBloco</code> TEXT), <code>APARTAMENTO</code> (<code>CodResort</code>, <code>CodBloco</code>, <code>NumApto</code> INT, <code>AreaM2</code> REAL).</li>
  <li>Cada entidade fraca deve herdar a <strong>PK completa</strong> da sua proprietária em sua própria <code>PRIMARY KEY</code> e declarar a <code>FOREIGN KEY ... ON DELETE CASCADE</code> composta correspondente.</li>
</ul>
""",
        "answer_sheet_html": """
<div class="answer-sheet-box">
  <h4>Gabarito DDL de Referência — R2.2</h4>
  <pre class="sql-code">CREATE TABLE RESORT (
  CodResort INTEGER PRIMARY KEY,
  Nome      TEXT NOT NULL
);

CREATE TABLE BLOCO (
  CodResort INTEGER NOT NULL,
  CodBloco  TEXT NOT NULL,
  PRIMARY KEY (CodResort, CodBloco),
  FOREIGN KEY (CodResort) REFERENCES RESORT(CodResort) ON DELETE CASCADE
);

CREATE TABLE APARTAMENTO (
  CodResort INTEGER NOT NULL,
  CodBloco  TEXT NOT NULL,
  NumApto   INTEGER NOT NULL,
  AreaM2    REAL,
  PRIMARY KEY (CodResort, CodBloco, NumApto),
  FOREIGN KEY (CodResort, CodBloco) REFERENCES BLOCO(CodResort, CodBloco) ON DELETE CASCADE
);</pre>
</div>
""",
        "ddl_tests": [
            {
                "name": "Existência das tabelas RESORT, BLOCO e APARTAMENTO",
                "type": "tables_exist",
                "tables": ["RESORT", "BLOCO", "APARTAMENTO"],
                "hint": "Crie exatamente as tabelas RESORT, BLOCO e APARTAMENTO."
            },
            {
                "name": "Permitir blocos e aptos homônimos em resorts distintos",
                "type": "must_succeed",
                "sql": """
                    INSERT INTO RESORT (CodResort, Nome) VALUES (1, 'Atlântico'), (2, 'Serra Azul');
                    INSERT INTO BLOCO (CodResort, CodBloco) VALUES (1, 'A'), (2, 'A');
                    INSERT INTO APARTAMENTO (CodResort, CodBloco, NumApto, AreaM2) VALUES (1, 'A', 101, 65.5), (2, 'A', 101, 72.0);
                """,
                "hint": "CodBloco='A' e NumApto=101 precisam poder coexistir em Resorts 1 e 2: a PK de BLOCO é (CodResort, CodBloco) e a de APARTAMENTO é (CodResort, CodBloco, NumApto)."
            },
            {
                "name": "Rejeitar APARTAMENTO sem BLOCO pai (FK composta ausente)",
                "type": "must_fail",
                "sql": """
                    INSERT INTO RESORT (CodResort, Nome) VALUES (10, 'Brisa');
                    INSERT INTO APARTAMENTO (CodResort, CodBloco, NumApto, AreaM2) VALUES (10, 'Z', 202, 50.0);
                """,
                "hint": "APARTAMENTO deve declarar FOREIGN KEY (CodResort, CodBloco) REFERENCES BLOCO(CodResort, CodBloco)."
            },
            {
                "name": "Rejeitar duplicata na PK tripla de APARTAMENTO",
                "type": "must_fail",
                "sql": """
                    INSERT INTO RESORT (CodResort, Nome) VALUES (1, 'Atlântico');
                    INSERT INTO BLOCO (CodResort, CodBloco) VALUES (1, 'A');
                    INSERT INTO APARTAMENTO (CodResort, CodBloco, NumApto, AreaM2) VALUES (1, 'A', 101, 60.0);
                    INSERT INTO APARTAMENTO (CodResort, CodBloco, NumApto, AreaM2) VALUES (1, 'A', 101, 80.0);
                """,
                "hint": "A chave primária composta (CodResort, CodBloco, NumApto) não pode admitir duplicatas."
            },
            {
                "name": "Exclusão em cascata ao remover RESORT (ON DELETE CASCADE em cadeia)",
                "type": "cascade_check",
                "sql_setup": """
                    INSERT INTO RESORT (CodResort, Nome) VALUES (1, 'Atlântico'), (2, 'Serra');
                    INSERT INTO BLOCO (CodResort, CodBloco) VALUES (1, 'A'), (2, 'A');
                    INSERT INTO APARTAMENTO (CodResort, CodBloco, NumApto, AreaM2) VALUES (1, 'A', 101, 65.5), (2, 'A', 101, 70.0);
                    DELETE FROM RESORT WHERE CodResort = 1;
                """,
                "verify_query": "SELECT COUNT(*) FROM APARTAMENTO WHERE CodResort = 1;",
                "expected_scalar": 0,
                "hint": "Declare ON DELETE CASCADE tanto na FK de BLOCO quanto na FK composta de APARTAMENTO."
            }
        ]
    },

    "R2.3": {
        "title": "R2.3 (Oficial/EER) — Subclasse Compartilhada (Herança Múltipla) & Agregação EER",
        "type": "oficial",
        "mode": "structured",
        "study_guide": STUDY_GUIDE_G5,
        "context_html": """
<p><strong>Diagrama EER (Padrão Slide 40 de <code>ibd-parte5.pdf</code>):</strong> Uma transportadora possui uma hierarquia com <strong>subclasse compartilhada</strong> (<code>CAMINHAO_FROTA</code> herdando simultaneamente de <code>TERRESTRE</code> e <code>CARGA_PESADA</code>) e uma <strong>agregação</strong> envolvendo <code>CAMINHAO_FROTA</code> e <code>ROTA</code> que é auditada por <code>AUTO_FISCAL</code>.</p>
<div style="text-align:center; margin: 12px 0;">
<svg viewBox="0 0 760 320" width="100%" style="max-width:740px; background:#0d1117; border:1px solid #30363d; border-radius:8px;">
  <!-- VEICULO -->
  <rect x="135" y="18" width="130" height="42" rx="4" fill="#161b22" stroke="#58a6ff" stroke-width="2"/>
  <text x="200" y="44" text-anchor="middle" fill="#f0f6fc" font-size="13" font-weight="700">VEICULO (<u>Placa</u>)</text>
  <!-- Circle (d) total -->
  <line x1="200" y1="60" x2="200" y2="78" stroke="#8b949e" stroke-width="1.8"/>
  <circle cx="200" cy="92" r="14" fill="#161b22" stroke="#d2a8ff" stroke-width="2"/>
  <text x="200" y="96" text-anchor="middle" fill="#d2a8ff" font-size="12" font-weight="700">o</text>
  <!-- Branches to TERRESTRE and CARGA_PESADA -->
  <line x1="188" y1="100" x2="110" y2="128" stroke="#8b949e" stroke-width="1.6"/>
  <line x1="212" y1="100" x2="290" y2="128" stroke="#8b949e" stroke-width="1.6"/>
  <rect x="40" y="128" width="140" height="40" rx="4" fill="#161b22" stroke="#79c0ff" stroke-width="1.8"/>
  <text x="110" y="152" text-anchor="middle" fill="#e6edf3" font-size="12" font-weight="700">TERRESTRE (Eixos)</text>
  <rect x="220" y="128" width="150" height="40" rx="4" fill="#161b22" stroke="#79c0ff" stroke-width="1.8"/>
  <text x="295" y="152" text-anchor="middle" fill="#e6edf3" font-size="12" font-weight="700">CARGA_PESADA (Ton)</text>

  <!-- Convergence into Shared Subclass CAMINHAO_FROTA -->
  <line x1="110" y1="168" x2="170" y2="215" stroke="#3fb950" stroke-width="1.8"/>
  <line x1="295" y1="168" x2="230" y2="215" stroke="#3fb950" stroke-width="1.8"/>
  <!-- Aggregation dashed container around (CAMINHAO_FROTA -- EXECUTA -- ROTA) -->
  <rect x="92" y="205" width="468" height="92" rx="8" fill="none" stroke="#f2cc60" stroke-width="1.8" stroke-dasharray="6,4"/>
  <text x="326" y="290" text-anchor="middle" fill="#f2cc60" font-size="10">Agregação: Execução de Rota</text>

  <rect x="110" y="218" width="145" height="44" rx="4" fill="#161b22" stroke="#3fb950" stroke-width="2"/>
  <text x="182" y="237" text-anchor="middle" fill="#f0f6fc" font-size="11" font-weight="700">CAMINHAO_FROTA</text>
  <text x="182" y="253" text-anchor="middle" fill="#8b949e" font-size="10">(LicencaEsp)</text>

  <line x1="255" y1="240" x2="295" y2="240" stroke="#8b949e" stroke-width="1.6"/>
  <text x="275" y="232" text-anchor="middle" fill="#79c0ff" font-size="10">(0,N)</text>
  <polygon points="295,240 340,214 385,240 340,266" fill="#1f2937" stroke="#d2a8ff" stroke-width="2"/>
  <text x="340" y="244" text-anchor="middle" fill="#d2a8ff" font-size="10" font-weight="700">EXECUTA</text>
  <text x="340" y="276" text-anchor="middle" fill="#e6edf3" font-size="9">Attr: KmRodado</text>

  <line x1="385" y1="240" x2="430" y2="240" stroke="#8b949e" stroke-width="1.6"/>
  <text x="407" y="232" text-anchor="middle" fill="#79c0ff" font-size="10">(0,N)</text>
  <rect x="430" y="218" width="116" height="44" rx="4" fill="#161b22" stroke="#58a6ff" stroke-width="2"/>
  <text x="488" y="237" text-anchor="middle" fill="#f0f6fc" font-size="11" font-weight="700">ROTA</text>
  <text x="488" y="253" text-anchor="middle" fill="#8b949e" font-size="10">(<u>IdRota</u>, Origem)</text>

  <!-- Relationship from Aggregation to AUTO_FISCAL -->
  <line x1="560" y1="248" x2="600" y2="155" stroke="#f2cc60" stroke-width="1.8"/>
  <text x="564" y="195" text-anchor="middle" fill="#ffa657" font-size="10">(0,N)</text>
  <polygon points="600,155 645,130 690,155 645,180" fill="#1f2937" stroke="#f2cc60" stroke-width="2"/>
  <text x="645" y="159" text-anchor="middle" fill="#f2cc60" font-size="10" font-weight="700">GERA</text>
  <line x1="645" y1="130" x2="645" y2="82" stroke="#8b949e" stroke-width="1.6"/>
  <text x="665" y="110" text-anchor="middle" fill="#ffa657" font-size="10">(1,1)</text>
  <rect x="580" y="34" width="138" height="48" rx="4" fill="#161b22" stroke="#f0883e" stroke-width="2"/>
  <text x="649" y="54" text-anchor="middle" fill="#f0f6fc" font-size="11" font-weight="700">AUTO_FISCAL</text>
  <text x="649" y="70" text-anchor="middle" fill="#8b949e" font-size="10">(<u>NumAuto</u>, Valor)</text>
</svg>
</div>
<p>Considere o mapeamento da hierarquia pela <strong>Opção 8A</strong> e da agregação conforme o Slide 40 de <code>ibd-parte5.pdf</code>.</p>
""",
        "answer_sheet_html": """
<div class="answer-sheet-box">
  <h4>Gabarito Explicado — R2.3 (Herança Múltipla &amp; Agregação EER)</h4>
  <ul>
    <li><strong>Subclasse Compartilhada (<code>CAMINHAO_FROTA</code>):</strong> Como ambas as superclasses diretas (<code>TERRESTRE</code> e <code>CARGA_PESADA</code>) descendem da mesma superclasse raiz <code>VEICULO</code>, a chave primária propagada é única: <code>Placa</code>. Não se cria <code>(Placa1, Placa2)</code> nem se duplica a coluna; porém, pode-se declarar duas FKs sobre <code>Placa</code> apontando para <code>TERRESTRE</code> e <code>CARGA_PESADA</code> para garantir que o caminhão pertença às duas especializações.</li>
    <li><strong>Agregação EER:</strong> Mapeia-se <code>EXECUTA(<u>Placa</u>, <u>IdRota</u>, KmRodado)</code> como tabela associativa. Em seguida, como um <code>AUTO_FISCAL</code> participa como <code>(1,1)</code> na relação <code>GERA</code> com a agregação, adiciona-se a chave estrangeira composta <code>(Placa, IdRota)</code> em <code>AUTO_FISCAL(<u>NumAuto</u>, Valor, Placa, IdRota)</code> referenciando <code>EXECUTA(Placa, IdRota)</code>.</li>
  </ul>
</div>
""",
        "fields": [
            {
                "id": "f1",
                "label": "1) Na Opção 8A, qual deve ser a chave primária de CAMINHAO_FROTA (subclasse compartilhada)?",
                "options": [
                    "Um novo código artificial IdCaminhao acompanhado de Eixos e Ton repetidos na tabela filha.",
                    "A chave composta (Placa_Terrestre, Placa_CargaPesada) formando duas colunas distintas na PK.",
                    "A chave simples Placa (herdada da raiz comum VEICULO), servindo de PK e FK simultânea para os dois pais.",
                    "Apenas o atributo específico LicencaEsp convertido diretamente em chave primária da subclasse."
                ],
                "answer": "A chave simples Placa (herdada da raiz comum VEICULO), servindo de PK e FK simultânea para os dois pais.",
                "explanation": "Em reticulados EER com superclasse raiz única, todas as subclasses herdam o mesmo identificador (Placa). Mantém-se Placa como PK única, referenciando TERRESTRE(Placa) e CARGA_PESADA(Placa)."
            },
            {
                "id": "f2",
                "label": "2) Por que usar a Opção 8C (tabela única com discriminadores) nessa hierarquia de sobreposição 'o' gera inconvenientes?",
                "options": [
                    "Porque a Opção 8C exige obrigatoriamente que as subclasses possuam tipos distintos incompatíveis com SQL.",
                    "Porque impede qualquer consulta SQL sobre atributos específicos de VEICULO sem junções múltiplas.",
                    "Porque uma tabela única não consegue armazenar mais de uma chave primária ao mesmo tempo.",
                    "Porque gera muitos NULLs em veículos que não pertencem às subclasses e exige múltiplos flags booleanos para sobreposição 'o'."
                ],
                "answer": "Porque gera muitos NULLs em veículos que não pertencem às subclasses e exige múltiplos flags booleanos para sobreposição 'o'.",
                "explanation": "Em especializações com sobreposição ('o'), um único discriminador simples não basta (são necessários múltiplos booleanos t_terrestre, t_carga, etc.), além de desperdiçar espaço com NULLs."
            },
            {
                "id": "f3",
                "label": "3) Como a agregação (EXECUTA) e o relacionamento GERA (1,1 no lado de AUTO_FISCAL) são representados no relacional?",
                "options": [
                    "Adicionando apenas IdRota em AUTO_FISCAL, pois a placa pode ser descoberta por consulta indireta.",
                    "Criando EXECUTA(Placa, IdRota, KmRodado) e propagando a FK composta (Placa, IdRota) para dentro de AUTO_FISCAL.",
                    "Inserindo NumAuto diretamente dentro da tabela VEICULO para evitar propagar chave composta da agregação.",
                    "Eliminando EXECUTA e ligando AUTO_FISCAL com duas FKs independentes para VEICULO e ROTA separadamente."
                ],
                "answer": "Criando EXECUTA(Placa, IdRota, KmRodado) e propagando a FK composta (Placa, IdRota) para dentro de AUTO_FISCAL.",
                "explanation": "Ligar AUTO_FISCAL independentemente a VEICULO e ROTA não garantiria que o veículo realmente executou aquela rota. Propagar a FK composta (Placa, IdRota) -> EXECUTA(Placa, IdRota) preserva a semântica exata da agregação."
            }
        ]
    },

    "R2.4": {
        "title": "R2.4 (Desenho / Engenharia Reversa) — Do Esquema SQL DDL ao Diagrama ER/EER",
        "type": "oficial",
        "mode": "open_design",
        "study_guide": STUDY_GUIDE_G6,
        "context_html": """
<p><strong>Exercício Aberto de Modelagem (Sem Checagem Automática &mdash; Gabarito Visual Completo Disponível):</strong><br>
Leia atentamente o script DDL abaixo de uma plataforma de streaming musical e <strong>desenhe em seu caderno o Diagrama ER/EER completo</strong> que originou essas tabelas, indicando: retângulos fortes/fracos, losangos (simples/identificadores), atributos chave, chaves parciais, cardinalidades <code>(min, max)</code> e especializações EER.</p>
<pre class="sql-code">CREATE TABLE PLANO (
  CodPlano INTEGER PRIMARY KEY,
  NomePlano TEXT NOT NULL,
  PrecoMensal REAL NOT NULL
);

CREATE TABLE ASSINANTE (
  IdAssinante INTEGER PRIMARY KEY,
  Email TEXT UNIQUE NOT NULL,
  CodPlano INTEGER NOT NULL REFERENCES PLANO(CodPlano)
);

CREATE TABLE ASSINANTE_INDIVIDUAL (
  IdAssinante INTEGER PRIMARY KEY REFERENCES ASSINANTE(IdAssinante),
  CPF TEXT UNIQUE NOT NULL
);

CREATE TABLE ASSINANTE_FAMILIA (
  IdAssinante INTEGER PRIMARY KEY REFERENCES ASSINANTE(IdAssinante),
  MaxTelas INTEGER NOT NULL
);

CREATE TABLE PERFIL_USO (
  IdAssinante INTEGER NOT NULL,
  Apelido TEXT NOT NULL,
  FaixaEtaria TEXT,
  PRIMARY KEY (IdAssinante, Apelido),
  FOREIGN KEY (IdAssinante) REFERENCES ASSINANTE(IdAssinante) ON DELETE CASCADE
);

CREATE TABLE MUSICA (
  ISRC TEXT PRIMARY KEY,
  Titulo TEXT NOT NULL
);

CREATE TABLE FAVORITA (
  IdAssinante INTEGER NOT NULL,
  Apelido TEXT NOT NULL,
  ISRC TEXT NOT NULL,
  DataMarcacao DATE,
  PRIMARY KEY (IdAssinante, Apelido, ISRC),
  FOREIGN KEY (IdAssinante, Apelido) REFERENCES PERFIL_USO(IdAssinante, Apelido),
  FOREIGN KEY (ISRC) REFERENCES MUSICA(ISRC)
);</pre>
<p><em>Dica:</em> Observe cada coluna <code>NOT NULL</code>, cada <code>PRIMARY KEY</code> que também é <code>FOREIGN KEY</code> e o <code>ON DELETE CASCADE</code> antes de abrir o gabarito visual.</p>
""",
        "answer_sheet_html": """
<div class="answer-sheet-box">
  <h4>Gabarito Visual (Diagrama ER/EER Reconstruído) — R2.4</h4>
  <div style="text-align:center; margin: 10px 0;">
  <svg viewBox="0 0 760 330" width="100%" style="max-width:740px; background:#0d1117; border:1px solid #30363d; border-radius:8px;">
    <!-- PLANO -->
    <rect x="28" y="34" width="130" height="44" rx="4" fill="#161b22" stroke="#58a6ff" stroke-width="2"/>
    <text x="93" y="53" text-anchor="middle" fill="#f0f6fc" font-size="12" font-weight="700">PLANO</text>
    <text x="93" y="69" text-anchor="middle" fill="#8b949e" font-size="10">(<u>CodPlano</u>, Nome, Preco)</text>

    <!-- CONTRATA (1:N total in ASSINANTE) -->
    <line x1="158" y1="56" x2="215" y2="56" stroke="#8b949e" stroke-width="1.6"/>
    <text x="186" y="47" text-anchor="middle" fill="#79c0ff" font-size="10">(0, N)</text>
    <polygon points="215,56 260,32 305,56 260,80" fill="#1f2937" stroke="#d2a8ff" stroke-width="1.8"/>
    <text x="260" y="60" text-anchor="middle" fill="#d2a8ff" font-size="10" font-weight="700">CONTRATA</text>
    <!-- Double line total -->
    <line x1="305" y1="53" x2="365" y2="53" stroke="#58a6ff" stroke-width="1.5"/>
    <line x1="305" y1="59" x2="365" y2="59" stroke="#58a6ff" stroke-width="1.5"/>
    <text x="335" y="44" text-anchor="middle" fill="#79c0ff" font-size="10">(1, 1)</text>

    <!-- ASSINANTE -->
    <rect x="365" y="34" width="155" height="44" rx="4" fill="#161b22" stroke="#58a6ff" stroke-width="2.2"/>
    <text x="442" y="53" text-anchor="middle" fill="#f0f6fc" font-size="12" font-weight="700">ASSINANTE</text>
    <text x="442" y="69" text-anchor="middle" fill="#8b949e" font-size="10">(<u>IdAssinante</u>, Email*)</text>

    <!-- EER Specialization -->
    <line x1="442" y1="78" x2="442" y2="105" stroke="#8b949e" stroke-width="1.6"/>
    <circle cx="442" cy="120" r="14" fill="#161b22" stroke="#3fb950" stroke-width="2"/>
    <text x="442" y="124" text-anchor="middle" fill="#3fb950" font-size="12" font-weight="700">d</text>
    <line x1="430" y1="128" x2="355" y2="160" stroke="#8b949e" stroke-width="1.6"/>
    <line x1="454" y1="128" x2="530" y2="160" stroke="#8b949e" stroke-width="1.6"/>
    <rect x="275" y="160" width="155" height="40" rx="4" fill="#161b22" stroke="#3fb950" stroke-width="1.8"/>
    <text x="352" y="178" text-anchor="middle" fill="#f0f6fc" font-size="11" font-weight="700">ASSINANTE_INDIVIDUAL</text>
    <text x="352" y="192" text-anchor="middle" fill="#8b949e" font-size="10">(CPF*)</text>
    <rect x="465" y="160" width="155" height="40" rx="4" fill="#161b22" stroke="#3fb950" stroke-width="1.8"/>
    <text x="542" y="178" text-anchor="middle" fill="#f0f6fc" font-size="11" font-weight="700">ASSINANTE_FAMILIA</text>
    <text x="542" y="192" text-anchor="middle" fill="#8b949e" font-size="10">(MaxTelas)</text>

    <!-- Identifying TEM_PERFIL -->
    <line x1="520" y1="56" x2="585" y2="56" stroke="#8b949e" stroke-width="1.6"/>
    <text x="552" y="46" text-anchor="middle" fill="#79c0ff" font-size="10">(1, N)</text>
    <polygon points="585,56 625,30 665,56 625,82" fill="#1f2937" stroke="#f0883e" stroke-width="2"/>
    <polygon points="592,56 625,35 658,56 625,77" fill="none" stroke="#f0883e" stroke-width="1.2"/>
    <text x="625" y="59" text-anchor="middle" fill="#f0883e" font-size="10" font-weight="700">CRIA</text>
    <!-- Total to PERFIL_USO -->
    <line x1="622" y1="82" x2="622" y2="122" stroke="#f0883e" stroke-width="1.5"/>
    <line x1="628" y1="82" x2="628" y2="122" stroke="#f0883e" stroke-width="1.5"/>
    <text x="650" y="106" text-anchor="middle" fill="#ffa657" font-size="10">(1, 1)</text>

    <!-- PERFIL_USO (Weak) -->
    <rect x="630" y="122" width="118" height="48" rx="4" fill="#161b22" stroke="#f0883e" stroke-width="2"/>
    <rect x="635" y="127" width="108" height="38" rx="2" fill="none" stroke="#f0883e" stroke-width="1.2"/>
    <text x="689" y="144" text-anchor="middle" fill="#f0f6fc" font-size="11" font-weight="700">PERFIL_USO</text>
    <text x="689" y="159" text-anchor="middle" fill="#ffa657" font-size="9">({Apelido}, Faixa)</text>

    <!-- M:N FAVORITA to MUSICA -->
    <line x1="689" y1="170" x2="689" y2="215" stroke="#8b949e" stroke-width="1.6"/>
    <text x="712" y="196" text-anchor="middle" fill="#79c0ff" font-size="10">(0, N)</text>
    <polygon points="642,240 689,215 736,240 689,265" fill="#1f2937" stroke="#d2a8ff" stroke-width="1.8"/>
    <text x="689" y="244" text-anchor="middle" fill="#d2a8ff" font-size="10" font-weight="700">FAVORITA</text>
    <text x="689" y="278" text-anchor="middle" fill="#8b949e" font-size="9">(DataMarcacao)</text>
    <line x1="642" y1="240" x2="545" y2="240" stroke="#8b949e" stroke-width="1.6"/>
    <text x="593" y="232" text-anchor="middle" fill="#79c0ff" font-size="10">(0, N)</text>

    <!-- MUSICA -->
    <rect x="405" y="220" width="140" height="42" rx="4" fill="#161b22" stroke="#58a6ff" stroke-width="2"/>
    <text x="475" y="238" text-anchor="middle" fill="#f0f6fc" font-size="11" font-weight="700">MUSICA</text>
    <text x="475" y="253" text-anchor="middle" fill="#8b949e" font-size="10">(<u>ISRC</u>, Titulo)</text>
  </svg>
  </div>
  <ul>
    <li><strong>Checklist de Autoavaliação:</strong> (1) <code>ASSINANTE</code> tem participação total <code>(1,1)</code> com <code>PLANO</code> devido ao <code>CodPlano NOT NULL</code>; (2) <code>ASSINANTE_INDIVIDUAL</code> e <code>ASSINANTE_FAMILIA</code> são subclasses (Opção 8A) porque sua PK é apenas FK para <code>ASSINANTE</code>; (3) <code>PERFIL_USO</code> é Entidade Fraca com chave parcial <code>Apelido</code> por herdar <code>IdAssinante</code> na PK e ter <code>ON DELETE CASCADE</code>; (4) <code>FAVORITA</code> é um relacionamento <code>M:N</code> com atributo <code>DataMarcacao</code>.</li>
  </ul>
</div>
""",
        "fields": []
    },

    "R2.5": {
        "title": "R2.5 (Lab Assertions SQL-92) — Disjunção e Totalidade EER na Clínica Médica",
        "type": "oficial",
        "mode": "sql_assertion",
        "study_guide": STUDY_GUIDE_G6,
        "setup": """
CREATE TABLE PROFISSIONAL (
  RegConselho TEXT PRIMARY KEY,
  Nome TEXT NOT NULL
);
CREATE TABLE MEDICO (
  RegConselho TEXT PRIMARY KEY REFERENCES PROFISSIONAL(RegConselho),
  CRM_Especialidade TEXT NOT NULL
);
CREATE TABLE DENTISTA (
  RegConselho TEXT PRIMARY KEY REFERENCES PROFISSIONAL(RegConselho),
  CRO_UF TEXT NOT NULL
);
INSERT INTO PROFISSIONAL VALUES ('REG-01', 'Dra. Helena'), ('REG-02', 'Dr. Tiago');
INSERT INTO MEDICO VALUES ('REG-01', 'Cardiologia');
INSERT INTO DENTISTA VALUES ('REG-02', 'MG');
""",
        "context_html": """
<p><strong>Restrições Semânticas {d, total} via SQL-92 <code>CREATE ASSERTION</code>:</strong> A especialização abaixo foi mapeada pela <strong>Opção 8A</strong> em três tabelas já carregadas no banco (<code>PROFISSIONAL</code>, <code>MEDICO</code> e <code>DENTISTA</code>).</p>
<div style="text-align:center; margin: 10px 0;">
<svg viewBox="0 0 460 155" width="100%" style="max-width:440px; background:#0d1117; border:1px solid #30363d; border-radius:8px;">
  <rect x="145" y="12" width="170" height="36" rx="4" fill="#161b22" stroke="#58a6ff" stroke-width="2"/>
  <text x="230" y="34" text-anchor="middle" fill="#f0f6fc" font-size="12" font-weight="700">PROFISSIONAL (<u>RegConselho</u>)</text>
  <!-- Double line = total -->
  <line x1="227" y1="48" x2="227" y2="70" stroke="#f2cc60" stroke-width="1.8"/>
  <line x1="233" y1="48" x2="233" y2="70" stroke="#f2cc60" stroke-width="1.8"/>
  <circle cx="230" cy="84" r="14" fill="#161b22" stroke="#f2cc60" stroke-width="2"/>
  <text x="230" y="88" text-anchor="middle" fill="#f2cc60" font-size="12" font-weight="700">d</text>
  <line x1="218" y1="92" x2="120" y2="112" stroke="#8b949e" stroke-width="1.6"/>
  <line x1="242" y1="92" x2="340" y2="112" stroke="#8b949e" stroke-width="1.6"/>
  <rect x="40" y="112" width="150" height="34" rx="4" fill="#161b22" stroke="#3fb950" stroke-width="1.8"/>
  <text x="115" y="133" text-anchor="middle" fill="#f0f6fc" font-size="11" font-weight="700">MEDICO (CRM_Esp.)</text>
  <rect x="270" y="112" width="150" height="34" rx="4" fill="#161b22" stroke="#3fb950" stroke-width="1.8"/>
  <text x="345" y="133" text-anchor="middle" fill="#f0f6fc" font-size="11" font-weight="700">DENTISTA (CRO_UF)</text>
</svg>
</div>
<p>As chaves estrangeiras padrão não garantem nem a <strong>disjunção (<code>d</code>)</strong> nem a <strong>totalidade (linha dupla)</strong>. Escreva <strong>duas declarações <code>CREATE ASSERTION ... CHECK (NOT EXISTS (...));</code></strong> separadas por ponto-e-vírgula:</p>
<ol>
  <li><strong>Disjunção:</strong> nenhum <code>RegConselho</code> pode existir ao mesmo tempo em <code>MEDICO</code> e <code>DENTISTA</code>.</li>
  <li><strong>Totalidade:</strong> todo <code>RegConselho</code> cadastrado em <code>PROFISSIONAL</code> deve pertencer a <code>MEDICO</code> ou a <code>DENTISTA</code>.</li>
</ol>
""",
        "answer_sheet_html": """
<div class="answer-sheet-box">
  <h4>Gabarito de Referência — R2.5 (Assertions EER)</h4>
  <pre class="sql-code">CREATE ASSERTION ESP_DISJUNTA CHECK (
  NOT EXISTS (
    SELECT 1 FROM MEDICO m
    JOIN DENTISTA d ON m.RegConselho = d.RegConselho
  )
);

CREATE ASSERTION ESP_TOTAL CHECK (
  NOT EXISTS (
    SELECT 1 FROM PROFISSIONAL p
    WHERE p.RegConselho NOT IN (SELECT RegConselho FROM MEDICO)
      AND p.RegConselho NOT IN (SELECT RegConselho FROM DENTISTA)
  )
);</pre>
</div>
""",
        "assertion_tests": [
            {
                "name": "Estado inicial consistente (1 Médico, 1 Dentista, ambos em PROFISSIONAL)",
                "violation_sql": None,
                "should_pass": True,
                "hint": "O estado inicial é válido {d, total}: nenhuma das asserções deve falhar."
            },
            {
                "name": "Inserir novo Médico válido (PROFISSIONAL + MEDICO)",
                "violation_sql": "INSERT INTO PROFISSIONAL VALUES ('REG-03', 'Dr. Lucas'); INSERT INTO MEDICO VALUES ('REG-03', 'Ortopedia');",
                "should_pass": True,
                "hint": "Inserir em PROFISSIONAL e em apenas uma subclasse (MEDICO) satisfaz {d, total}."
            },
            {
                "name": "Bloquear sobreposição (mesmo RegConselho em MEDICO e DENTISTA)",
                "violation_sql": "INSERT INTO DENTISTA VALUES ('REG-01', 'SP');",
                "should_pass": False,
                "hint": "REG-01 já é MEDICO; sua asserção de disjunção precisa detectar a interseção entre MEDICO e DENTISTA."
            },
            {
                "name": "Bloquear profissional órfão de subclasse (violação da totalidade)",
                "violation_sql": "INSERT INTO PROFISSIONAL VALUES ('REG-99', 'Sem Subclasse');",
                "should_pass": False,
                "hint": "Todo registro de PROFISSIONAL precisa aparecer em MEDICO ou em DENTISTA."
            }
        ]
    },

    "R2.6": {
        "title": "R2.6 (Lab SQL) — Detectando Tuplas Espúrias na Prática (Elmasri EMP_PROJ1)",
        "type": "oficial",
        "mode": "sql_query",
        "study_guide": STUDY_GUIDE_G7,
        "setup": """
CREATE TABLE EMP_PROJ_ORIG (
  Ssn TEXT,
  PNumber INTEGER,
  Hours REAL,
  EName TEXT,
  PName TEXT,
  PLocation TEXT,
  PRIMARY KEY (Ssn, PNumber)
);
INSERT INTO EMP_PROJ_ORIG VALUES
  ('111', 10, 20.0, 'Smith',   'Computerization', 'Stafford'),
  ('222', 20, 15.0, 'Wong',    'Reorganization',  'Houston'),
  ('333', 30, 10.0, 'English', 'Newbenefits',     'Stafford'),
  ('444', 40, 25.0, 'Narayan', 'ProductZ',        'Houston');

-- Decomposição defeituosa pelo atributo não-superchave PLocation (Guideline 4):
CREATE TABLE EMP_LOCS AS SELECT DISTINCT EName, PLocation FROM EMP_PROJ_ORIG;
CREATE TABLE EMP_PROJ_BAD AS SELECT Ssn, PNumber, Hours, PName, PLocation FROM EMP_PROJ_ORIG;
""",
        "context_html": """
<p><strong>Diretriz 4 de Projeto Relacional (<code>ibd-parte6.pdf</code> / Elmasri):</strong> O esquema original <code>EMP_PROJ_ORIG(Ssn, PNumber, Hours, EName, PName, PLocation)</code> foi decomposto de forma inadequada em:</p>
<ul>
  <li><code>EMP_LOCS(EName, PLocation)</code></li>
  <li><code>EMP_PROJ_BAD(Ssn, PNumber, Hours, PName, PLocation)</code></li>
</ul>
<p>Ao tentar reconstruir os dados com um <code>JOIN</code> sobre <code>PLocation</code> (que <strong>não é superchave</strong>), surgem <strong>tuplas espúrias</strong> (combinações falsas de empregados com projetos onde eles nunca trabalharam!).</p>
<p><strong>Sua Tarefa SQL:</strong> Escreva uma consulta que realize a junção natural entre <code>EMP_LOCS</code> e <code>EMP_PROJ_BAD</code> (via <code>PLocation</code>) e retorne <strong>apenas as tuplas espúrias</strong> &mdash; isto é, aquelas cujo par <code>(EName, Ssn, PNumber, PLocation)</code> <strong>não existe</strong> em <code>EMP_PROJ_ORIG</code>.</p>
<p><strong>Colunas esperadas:</strong> <code>EName</code>, <code>Ssn</code>, <code>PNumber</code>, <code>PLocation</code>.</p>
""",
        "answer_sheet_html": """
<div class="answer-sheet-box">
  <h4>Gabarito SQL — R2.6 (Comprovando Tuplas Espúrias)</h4>
  <pre class="sql-code">SELECT l.EName, p.Ssn, p.PNumber, l.PLocation
FROM EMP_LOCS l
JOIN EMP_PROJ_BAD p ON l.PLocation = p.PLocation
WHERE NOT EXISTS (
  SELECT 1 FROM EMP_PROJ_ORIG o
  WHERE o.Ssn = p.Ssn AND o.PNumber = p.PNumber AND o.EName = l.EName
);</pre>
  <p>Resultado: os 2 projetos de <code>'Stafford'</code> e os 2 de <code>'Houston'</code> cruzam entre si gerando <strong>4 tuplas espúrias</strong> falsas além das 4 originais!</p>
</div>
""",
        "expected_columns": ["EName", "Ssn", "PNumber", "PLocation"],
        "expected_rows": [
            ["Smith",   "333", 30, "Stafford"],
            ["English", "111", 10, "Stafford"],
            ["Wong",    "444", 40, "Houston"],
            ["Narayan", "222", 20, "Houston"]
        ]
    },

    "R2.7": {
        "title": "R2.7 (Oficial/Teórico) — Teste Binário de Junção Sem Perda &amp; Preservação de DFs",
        "type": "oficial",
        "mode": "structured",
        "study_guide": STUDY_GUIDE_G7,
        "context_html": """
<p><strong>Problema Clássico de Banco de Provas Universitárias:</strong> Seja a relação <code>R(A, B, C, D, E)</code> submetida ao seguinte conjunto de dependências funcionais:</p>
<pre class="sql-code">F = { A → BC,  CD → E,  B → D,  E → A }</pre>
<p>Avalie duas propostas de decomposição binária de <code>R</code>:</p>
<ul>
  <li><strong>Decomposição D1:</strong> <code>R1(A, B, C)</code> e <code>R2(A, D, E)</code></li>
  <li><strong>Decomposição D2:</strong> <code>R1(A, B, C)</code> e <code>R2(C, D, E)</code></li>
</ul>
""",
        "answer_sheet_html": """
<div class="answer-sheet-box">
  <h4>Gabarito Passo a Passo — R2.7</h4>
  <ul>
    <li><strong>D1 (<code>R1(A,B,C)</code>, <code>R2(A,D,E)</code>):</strong> Interseção = <code>{A}</code>. Como <code>A → BC</code> e <code>B → D</code> e <code>CD → E</code>, temos <code>A+ = {A,B,C,D,E}</code>! Logo <code>A</code> é superchave de <code>R1</code> (e também de <code>R2</code>), garantindo <strong>Junção Sem Perda</strong>.</li>
    <li><strong>D2 (<code>R1(A,B,C)</code>, <code>R2(C,D,E)</code>):</strong> Interseção = <code>{C}</code>. Sob <code>F</code>, <code>C+ = {C}</code>, que não determina nem <code>R1</code> nem <code>R2</code> → <strong>COM perda de informação</strong>.</li>
    <li><strong>Preservação em D1:</strong> Projetando <code>F</code> em <code>R1</code> obtém-se <code>A → BC</code>; projetando em <code>R2</code> obtém-se <code>A → DE</code> e <code>E → AD</code>. Porém, nem <code>B → D</code> nem <code>CD → E</code> podem ser derivados a partir dessas projeções locais (<code>B+</code> local é só <code>{B}</code>!) → D1 <strong>NÃO preserva dependências</strong>.</li>
  </ul>
</div>
""",
        "fields": [
            {
                "id": "f1",
                "label": "1) Aplicando o teste binário de junção sem perda à decomposição D1 = { R1(A,B,C), R2(A,D,E) }:",
                "options": [
                    "Tem junção sem perda, pois R1 ∩ R2 = {A} e A+ = {A,B,C,D,E} torna {A} superchave de R1 e de R2.",
                    "Tem perda de informação, pois nenhum atributo de F determina sozinho os atributos de R2.",
                    "Tem junção sem perda somente se B e D forem replicados em ambas as tabelas de D1.",
                    "Tem perda de informação, pois B → D cruza da primeira partição para a segunda partição."
                ],
                "answer": "Tem junção sem perda, pois R1 ∩ R2 = {A} e A+ = {A,B,C,D,E} torna {A} superchave de R1 e de R2.",
                "explanation": "A+ = {A,B,C,D,E} (via A->BC, B->D, CD->E). Como R1 ∩ R2 = {A} é superchave de R1 (e de R2), D1 satisfaz o teorema de junção sem perda."
            },
            {
                "id": "f2",
                "label": "2) Quanto à propriedade de junção sem perda na decomposição D2 = { R1(A,B,C), R2(C,D,E) }:",
                "options": [
                    "Tem junção sem perda, porque E → A permite recuperar R1 diretamente a partir de R2.",
                    "Tem junção sem perda, pois C aparece tanto em A → BC quanto no determinante de CD → E.",
                    "Tem perda apenas sobre B, mantendo intactos todos os pares válidos entre A, C e E.",
                    "Tem perda de informação, pois R1 ∩ R2 = {C} e C+ = {C} não é superchave de R1 nem R2."
                ],
                "answer": "Tem perda de informação, pois R1 ∩ R2 = {C} e C+ = {C} não é superchave de R1 nem R2.",
                "explanation": "C não aparece sozinho do lado esquerdo de nenhuma DF não-trivial em F; logo C+ = {C}, falhando o critério binário de superchave."
            },
            {
                "id": "f3",
                "label": "3) Sobre a preservação de dependências funcionais na decomposição D1 = { R1(A,B,C), R2(A,D,E) }:",
                "options": [
                    "Preserva todas as DFs de F, porque o conjunto {A → BC, E → A} já implica B → D por transitividade.",
                    "Preserva B → D, mas perde exclusivamente a dependência E → A pelo fato de E estar em R2.",
                    "NÃO preserva F, pois as projeções locais em R1 e R2 perdem B → D e CD → E.",
                    "Preserva F integralmente sempre que a decomposição possuir a propriedade de junção sem perda."
                ],
                "answer": "NÃO preserva F, pois as projeções locais em R1 e R2 perdem B → D e CD → E.",
                "explanation": "Em R1 só valem DFs deriváveis dentro de {A,B,C} (como A->BC), e em R2 dentro de {A,D,E} (A->DE, E->AD). Nelas, (B)+ = {B} (perde B->D) e (CD)+ = {CD} (perde CD->E)."
            }
        ]
    },

    "R2.8": {
        "title": "R2.8 (Oficial/Clássico) — Diagnóstico BCNF vs 3FN &amp; Exceção de Atributo Primo",
        "type": "oficial",
        "mode": "structured",
        "study_guide": STUDY_GUIDE_G8,
        "context_html": """
<p><strong>Análise Comparativa de Formas Normais (<code>ibd-parte6.pdf</code>):</strong> Analise atentamente duas relações extraídas de sistemas acadêmicos e logísticos reais:</p>
<ul>
  <li><strong>Relação 1:</strong> <code>BANCA_TCC(Matricula, Area, Professor)</code><br>
      com <code>F1 = { (Matricula, Area) → Professor ;  Professor → Area }</code></li>
  <li><strong>Relação 2:</strong> <code>FORNECEDOR_CEP(IdForn, CEP, Cidade, Estado)</code><br>
      com <code>F2 = { IdForn → CEP, Cidade, Estado ;  CEP → Cidade, Estado }</code></li>
</ul>
""",
        "answer_sheet_html": """
<div class="answer-sheet-box">
  <h4>Gabarito Explicado — R2.8 (BCNF vs 3FN)</h4>
  <ul>
    <li><strong><code>BANCA_TCC</code>:</strong> Chaves candidatas = <code>{Matricula, Area}</code> e <code>{Matricula, Professor}</code>. Assim, os 3 atributos são <strong>primos</strong>! Na DF <code>Professor → Area</code>, o determinante não é superchave (viola <strong>BCNF</strong>), mas o lado direito <code>Area</code> é atributo primo (satisfeita pela <strong>3FN</strong>).</li>
    <li><strong>Decomposição BCNF de <code>BANCA_TCC</code>:</strong> <code>DOCENTE_AREA(<u>Professor</u>, Area)</code> e <code>ALUNO_ORIENTACAO(<u>Matricula</u>, <u>Professor</u>)</code> eliminam a redundância, porém não preservam localmente <code>(Matricula, Area) → Professor</code>.</li>
    <li><strong><code>FORNECEDOR_CEP</code>:</strong> Chave única = <code>{IdForn}</code> (não há dependência parcial → está em 2FN). Como <code>CEP → Cidade, Estado</code> liga um não-primo a outros não-primos, viola <strong>3FN e BCNF</strong>.</li>
  </ul>
</div>
""",
        "fields": [
            {
                "id": "f1",
                "label": "1) Qual é exatamente a maior forma normal satisfeita por BANCA_TCC(Matricula, Area, Professor)?",
                "options": [
                    "Está em 2FN, mas viola a 3FN porque Professor determina Area de maneira transitiva.",
                    "Está em 3FN (pois Area é atributo primo), mas viola a BCNF (Professor não é superchave).",
                    "Está em BCNF plena, porque todo professor está vinculado a apenas uma única Area.",
                    "Não está sequer em 2FN, porque Professor determina parcialmente a chave (Matricula, Area)."
                ],
                "answer": "Está em 3FN (pois Area é atributo primo), mas viola a BCNF (Professor não é superchave).",
                "explanation": "{Matricula, Area} e {Matricula, Professor} são chaves candidatas, tornando Area atributo primo. Logo Professor->Area passa na 3FN, mas reprova na BCNF."
            },
            {
                "id": "f2",
                "label": "2) Ao decompor BANCA_TCC para alcançar BCNF via Professor → Area, qual efeito colateral ocorre?",
                "options": [
                    "Obtém-se DOCENTE_AREA(Professor, Area) e ALUNO_BANCA(Matricula, Professor) com junção sem perda, mas sem preservar (Matricula, Area) → Professor.",
                    "Obtém-se decomposição sem perda e preservando todas as dependências, eliminando qualquer anomalia de inserção.",
                    "Perde-se a junção sem perda ao tentar recombinar Matricula e Area pelo atributo comum Professor.",
                    "Exige que Matricula e Area permaneçam juntas em DOCENTE_AREA(Professor, Matricula, Area)."
                ],
                "answer": "Obtém-se DOCENTE_AREA(Professor, Area) e ALUNO_BANCA(Matricula, Professor) com junção sem perda, mas sem preservar (Matricula, Area) → Professor.",
                "explanation": "A interseção das duas novas tabelas é {Professor}, que é chave de DOCENTE_AREA (logo junção sem perda), mas nenhum esquema contém juntos {Matricula, Area, Professor} para checar a DF original localmente."
            },
            {
                "id": "f3",
                "label": "3) Qual é a maior forma normal satisfeita por FORNECEDOR_CEP e qual é sua correção mínima?",
                "options": [
                    "Está em 3FN e BCNF, não exigindo nenhuma decomposição estrutural adicional.",
                    "Está apenas em 1FN, sendo preciso decompor CEP em chave primária composta com IdForn.",
                    "Está em 3FN, pois Cidade e Estado pertencem a alguma chave candidata secundária da relação.",
                    "Está em 2FN (viola 3FN por CEP → Cidade, Estado), devendo separar FORN(IdForn, CEP) e END_CEP(CEP, Cidade, Estado)."
                ],
                "answer": "Está em 2FN (viola 3FN por CEP → Cidade, Estado), devendo separar FORN(IdForn, CEP) e END_CEP(CEP, Cidade, Estado).",
                "explanation": "Chave única {IdForn} evita dependência parcial (logo está em 2FN), mas CEP -> Cidade, Estado é dependência transitiva entre não-primos, violando a 3FN."
            }
        ]
    },

    "R2.9": {
        "title": "R2.9 (Oficial/Algorítmico) — Algoritmo de Síntese 3FN &amp; Cobertura Mínima Fc",
        "type": "oficial",
        "mode": "structured",
        "study_guide": STUDY_GUIDE_G8,
        "context_html": """
<p><strong>Execução Rigorosa do Algoritmo de Síntese para 3FN:</strong> Dada a relação <code>T(A, B, C, D, E, G)</code> e o conjunto de dependências funcionais não-mínimo:</p>
<pre class="sql-code">F = { A → BC,  B → C,  AB → D,  D → E,  A → E }</pre>
<p>Aplique os 4 passos da síntese para 3FN: (1) encontre a cobertura mínima <code>Fc</code>, (2) construa as relações agrupadas por determinante, (3) verifique se alguma chave candidata de <code>T</code> está contida em alguma relação gerada, e (4) identifique as propriedades garantidas.</p>
""",
        "answer_sheet_html": """
<div class="answer-sheet-box">
  <h4>Gabarito Detalhado — R2.9 (Síntese 3FN)</h4>
  <ol>
    <li><strong>Decomposição do RHS:</strong> <code>A → B</code>, <code>A → C</code>, <code>B → C</code>, <code>AB → D</code>, <code>D → E</code>, <code>A → E</code>.</li>
    <li><strong>Atributo estranho no LHS:</strong> Em <code>AB → D</code>, como <code>A → B</code>, <code>B</code> é redundante no LHS → simplifica para <code>A → D</code>.</li>
    <li><strong>DFs redundantes:</strong> <code>A → C</code> segue de <code>A → B</code> + <code>B → C</code>; e <code>A → E</code> segue de <code>A → D</code> + <code>D → E</code>. Logo <code>Fc = { A → BD, B → C, D → E }</code>.</li>
    <li><strong>Chave Candidata &amp; Tabela Extra:</strong> Note que <code>G</code> não aparece em nenhuma DF; logo a única chave candidata é <code>{A, G}</code>. Como nenhuma tabela do passo 2 contém <code>{A, G}</code>, o algoritmo adiciona <code>R4(<u>A</u>, <u>G</u>)</code>!</li>
  </ol>
</div>
""",
        "fields": [
            {
                "id": "f1",
                "label": "1) Qual é a cobertura mínima Fc obtida após simplificar LHS e remover DFs redundantes em F?",
                "options": [
                    "Fc = { A → B, A → C, AB → D, D → E }",
                    "Fc = { A → B, B → C, D → E, A → E }",
                    "Fc = { A → B, C → B, A → D, D → E }",
                    "Fc = { A → B, B → C, A → D, D → E }"
                ],
                "answer": "Fc = { A → B, B → C, A → D, D → E }",
                "explanation": "Em AB -> D, B é estranho pois A -> B; depois A -> C é redundante via (A -> B, B -> C) e A -> E é redundante via (A -> D, D -> E)."
            },
            {
                "id": "f2",
                "label": "2) Quais relações finais (com chaves primárias) são produzidas pelo algoritmo completo de síntese 3FN?",
                "options": [
                    "R1(A, B, D), R2(B, C), R3(D, E), sem nenhuma tabela extra porque {A} já é superchave de R1.",
                    "R1(A, B, D), R2(B, C), R3(D, E) e uma tabela adicional R4(A, G) para conter a chave candidata {A, G}.",
                    "R1(A, B, C, D), R2(D, E) e R3(A, G), fundindo A -> B e B -> C em uma única tabela.",
                    "R1(A, B, D, G), R2(B, C) e R3(D, E), inserindo G diretamente em R1 após remover B."
                ],
                "answer": "R1(A, B, D), R2(B, C), R3(D, E) e uma tabela adicional R4(A, G) para conter a chave candidata {A, G}.",
                "explanation": "Como G não aparece em Fc, (A,G)+ = {A,B,C,D,E,G} e nenhuma relação de Fc contém {A,G}; logo o Passo 3 exige criar R4(A, G)!"
            },
            {
                "id": "f3",
                "label": "3) Quais garantias matemáticas o conjunto {R1, R2, R3, R4} gerado por essa síntese assegura sempre?",
                "options": [
                    "Garante 3FN e preservação de DFs, mas não garante necessariamente junção sem perda quando há tabela extra.",
                    "Garante BCNF, preservação de todas as dependências funcionais e junção sem perda em todos os casos.",
                    "Garante todas as tabelas em 3FN, preservação de todas as dependências de F e junção sem perda.",
                    "Garante BCNF apenas quando F possui pelo menos uma chave candidata composta como {A, G}."
                ],
                "answer": "Garante todas as tabelas em 3FN, preservação de todas as dependências de F e junção sem perda.",
                "explanation": "O teorema do Algoritmo de Síntese 3FN garante simultaneamente os 3 pilares: 3FN em cada relação, preservação de dependências e junção sem perda (garantida pela inclusão de R4)."
            }
        ]
    },

    "R2.10": {
        "title": "R2.10 (Auditoria Integrada ER → 3FN) — Refatorando E-Commerce Malformado",
        "type": "oficial",
        "mode": "structured",
        "study_guide": STUDY_GUIDE_G8,
        "context_html": """
<p><strong>Integração Módulos 7 + 8:</strong> Um desenvolvedor implementou o diagrama ER de E-Commerce abaixo de forma apressada em apenas uma grande tabela desnormalizada chamada <code>PEDIDO_BRUTO</code>.</p>
<div style="text-align:center; margin: 12px 0;">
<svg viewBox="0 0 760 155" width="100%" style="max-width:740px; background:#0d1117; border:1px solid #30363d; border-radius:8px;">
  <rect x="16" y="45" width="128" height="46" rx="4" fill="#161b22" stroke="#58a6ff" stroke-width="2"/>
  <text x="80" y="64" text-anchor="middle" fill="#f0f6fc" font-size="11" font-weight="700">CLIENTE</text>
  <text x="80" y="79" text-anchor="middle" fill="#8b949e" font-size="9">(<u>IdCli</u>, Nome, UF)</text>

  <line x1="144" y1="68" x2="176" y2="68" stroke="#8b949e" stroke-width="1.5"/>
  <text x="160" y="59" text-anchor="middle" fill="#79c0ff" font-size="9">(0,N)</text>
  <polygon points="176,68 206,48 236,68 206,88" fill="#1f2937" stroke="#d2a8ff" stroke-width="1.6"/>
  <text x="206" y="71" text-anchor="middle" fill="#d2a8ff" font-size="9" font-weight="700">FAZ</text>
  <line x1="236" y1="65" x2="270" y2="65" stroke="#58a6ff" stroke-width="1.5"/>
  <line x1="236" y1="71" x2="270" y2="71" stroke="#58a6ff" stroke-width="1.5"/>
  <text x="253" y="57" text-anchor="middle" fill="#79c0ff" font-size="9">(1,1)</text>

  <rect x="270" y="45" width="118" height="46" rx="4" fill="#161b22" stroke="#58a6ff" stroke-width="2"/>
  <text x="329" y="64" text-anchor="middle" fill="#f0f6fc" font-size="11" font-weight="700">PEDIDO</text>
  <text x="329" y="79" text-anchor="middle" fill="#8b949e" font-size="9">(<u>IdPed</u>, DataPed)</text>

  <line x1="388" y1="68" x2="418" y2="68" stroke="#8b949e" stroke-width="1.5"/>
  <text x="403" y="59" text-anchor="middle" fill="#79c0ff" font-size="9">(1,N)</text>
  <polygon points="418,68 455,44 492,68 455,92" fill="#1f2937" stroke="#f2cc60" stroke-width="1.6"/>
  <text x="455" y="71" text-anchor="middle" fill="#f2cc60" font-size="9" font-weight="700">CONTEM</text>
  <text x="455" y="108" text-anchor="middle" fill="#8b949e" font-size="9">(Qtd, PrecoUnit)</text>
  <line x1="492" y1="68" x2="522" y2="68" stroke="#8b949e" stroke-width="1.5"/>
  <text x="507" y="59" text-anchor="middle" fill="#79c0ff" font-size="9">(0,N)</text>

  <rect x="522" y="45" width="128" height="46" rx="4" fill="#161b22" stroke="#58a6ff" stroke-width="2"/>
  <text x="586" y="64" text-anchor="middle" fill="#f0f6fc" font-size="11" font-weight="700">PRODUTO</text>
  <text x="586" y="79" text-anchor="middle" fill="#8b949e" font-size="9">(<u>CodProd</u>, Titulo)</text>

  <line x1="650" y1="68" x2="672" y2="68" stroke="#8b949e" stroke-width="1.5"/>
  <text x="685" y="58" text-anchor="middle" fill="#79c0ff" font-size="9">1:N</text>
  <rect x="672" y="45" width="76" height="46" rx="4" fill="#161b22" stroke="#3fb950" stroke-width="1.8"/>
  <text x="710" y="64" text-anchor="middle" fill="#f0f6fc" font-size="10" font-weight="700">CATEG</text>
  <text x="710" y="79" text-anchor="middle" fill="#8b949e" font-size="9">(<u>CodCat</u>)</text>
</svg>
</div>
<pre class="sql-code">PEDIDO_BRUTO(<u>IdPed</u>, <u>CodProd</u>, DataPed, IdCli, Nome, UF, Qtd, PrecoUnit, Titulo, CodCat)</pre>
<p><em>Nota de negócio:</em> <code>PrecoUnit</code> em <code>CONTEM</code> é o preço histórico praticado no item do pedido.</p>
""",
        "answer_sheet_html": """
<div class="answer-sheet-box">
  <h4>Gabarito Integrado — R2.10 (Auditoria ER → 3FN)</h4>
  <ul>
    <li><strong>Violação de 2FN em <code>PEDIDO_BRUTO</code>:</strong> <code>DataPed, IdCli, Nome, UF</code> dependem apenas de <code>IdPed</code> (parcial), enquanto <code>Titulo, CodCat</code> dependem apenas de <code>CodProd</code> (parcial).</li>
    <li><strong>Violação de 3FN após decomposição 2FN:</strong> A tabela extraída <code>PEDIDO_2FN(<u>IdPed</u>, DataPed, IdCli, Nome, UF)</code> contém a transitiva <code>IdPed → IdCli → {Nome, UF}</code>, exigindo separar <code>CLIENTE</code>.</li>
    <li><strong>Esquema 3FN / BCNF Final fiel ao ER:</strong><br>
    <code>CATEG(<u>CodCat</u>, ...)</code> &bull; <code>CLIENTE(<u>IdCli</u>, Nome, UF)</code> &bull; <code>PEDIDO(<u>IdPed</u>, DataPed, IdCli)</code> &bull; <code>PRODUTO(<u>CodProd</u>, Titulo, CodCat)</code> &bull; <code>CONTEM(<u>IdPed</u>, <u>CodProd</u>, Qtd, PrecoUnit)</code>.</li>
  </ul>
</div>
""",
        "fields": [
            {
                "id": "f1",
                "label": "1) Qual anomalia de dependência funcional faz PEDIDO_BRUTO violar imediatamente a 2FN?",
                "options": [
                    "Dependências parciais sobre a PK composta {IdPed, CodProd}, como IdPed → DataPed, IdCli e CodProd → Titulo.",
                    "Existência do atributo histórico PrecoUnit na tabela de itens de venda em vez da tabela de produtos.",
                    "O fato de IdCli poder comprar vários pedidos diferentes ao longo do tempo no diagrama ER.",
                    "A repetição de valores atômicos simples como UF na mesma tupla do cliente."
                ],
                "answer": "Dependências parciais sobre a PK composta {IdPed, CodProd}, como IdPed → DataPed, IdCli e CodProd → Titulo.",
                "explanation": "Na PK {IdPed, CodProd}, atributos que dependem apenas de IdPed ou apenas de CodProd são dependências parciais, ferindo a 2FN."
            },
            {
                "id": "f2",
                "label": "2) Ao colocar PEDIDO_BRUTO em 2FN, cria-se PEDIDO_2FN(IdPed, DataPed, IdCli, Nome, UF). Por que ela ainda viola a 3FN?",
                "options": [
                    "Porque DataPed depende parcialmente de IdCli e não da chave primária IdPed.",
                    "Porque cada cliente faz mais de um pedido, exigindo mover IdPed para dentro de CLIENTE.",
                    "Porque possui dependência transitiva de um atributo não-primo para outros não-primos: IdCli → Nome, UF.",
                    "Porque Nome e UF pertencem diretamente ao produto e não ao comprador."
                ],
                "answer": "Porque possui dependência transitiva de um atributo não-primo para outros não-primos: IdCli → Nome, UF.",
                "explanation": "Em PEDIDO_2FN, IdPed -> IdCli e IdCli -> {Nome, UF}; logo Nome e UF dependem transitivamente da chave via o atributo não-primo IdCli."
            },
            {
                "id": "f3",
                "label": "3) Qual conjunto final de tabelas é simultaneamente fiel ao diagrama ER e normalizado em 3FN/BCNF?",
                "options": [
                    "CLIENTE(IdCli, Nome, UF), PEDIDO(IdPed, DataPed, IdCli), PRODUTO(CodProd, Titulo) e CATEG(CodCat, CodProd).",
                    "CLIENTE(IdCli, Nome, UF), PEDIDO(IdPed, DataPed, IdCli), PRODUTO(CodProd, Titulo, CodCat), CATEG(CodCat) e CONTEM(IdPed, CodProd, Qtd, PrecoUnit).",
                    "PEDIDO_CLI(IdPed, IdCli, Nome, UF, DataPed) e ITEM_PROD(IdPed, CodProd, Titulo, CodCat, Qtd, PrecoUnit).",
                    "CLIENTE(IdCli, Nome, UF), PEDIDO(IdPed, DataPed, CodProd, Qtd, PrecoUnit) e PRODUTO(CodProd, Titulo, CodCat)."
                ],
                "answer": "CLIENTE(IdCli, Nome, UF), PEDIDO(IdPed, DataPed, IdCli), PRODUTO(CodProd, Titulo, CodCat), CATEG(CodCat) e CONTEM(IdPed, CodProd, Qtd, PrecoUnit).",
                "explanation": "Reflete exatamente 1:N total (IdCli NOT NULL em PEDIDO), 1:N (CodCat em PRODUTO) e M:N (CONTEM com PK composta e atributos do relacionamento Qtd, PrecoUnit)."
            }
        ]
    }
}
