# -*- coding: utf-8 -*-
"""
Banco de Exercícios Oficial / Estilo Prova — Rodada 5 (A Orquestra Final — Módulos 7 e 8)
Reforço cirúrgico 100% alinhado a ibd-parte5.pdf, ibd-parte6.pdf e listas oficiais:
  - Grupo 13 (R5.1–R5.5): Leitura Inversa (Lógico+RIRs -> ER), 1:1 Assimétrico + Multivalorado Composto,
    Cadeia Hospitalar 3 níveis em SQL DDL, Mini-Simulado Completo de Papel (Agência Espacial) e ASSERTION Ferroviária.
  - Grupo 14 (R5.6–R5.10): Cobertura Mínima em cascata (2 estranhos LHS), Auditoria DF em Vendas SQL,
    Ciclo de 4 Chaves Candidatas R(A..G) (3FN vs BCNF), Discursiva E8.3-style 1FN->3FN e Checklist Pré-Prova.
"""

# ---------------------------------------------------------------------------
# Fichas de Estudo (Study Guides G13 & G14 — domínios paralelos)
# ---------------------------------------------------------------------------

STUDY_GUIDE_G13 = {
    "id": "G13",
    "title": "G13 — Leitura Inversa, 1:1 Assimétrico &amp; Cadeias/Redes em SQL",
    "file_path": "study_guides/G13_M7_LeituraInversa_1a1_e_ChecklistFinal.md",
    "coursework_ref": "ibd-parte5.pdf (Mapeamento Bidirecional Lógico &harr; ER, 1:1 Total/Parcial, Multivalorado Composto e RIRs)",
    "quick_rules_html": """
<div class="sg-rules-box">
  <h4>Resumo Operacional — Rodada 5 (Grupo G13)</h4>
  <ul>
    <li><strong>Leitura Inversa (Lógico &rarr; ER):</strong>
      <ul>
        <li><code>T(<u>PK</u>, FK(unique, nn))</code> &rArr; Relação <strong><code>1:1</code></strong> com participação <strong>total</strong> <code>(1,1)</code> em <code>T</code> e parcial <code>(0,1)</code> no pai.</li>
        <li><code>T(<u>PK_pai</u>, <u>Parcial</u>, ...)</code> com <code>-p-&gt;</code> &rArr; <strong>Entidade Fraca</strong> (retângulo/losango duplos).</li>
        <li><code>T(<u>PK</u>, FK(nn))</code> com <code>-b-&gt;</code> &rArr; Relação <code>1:N</code> com lado <strong>total <code>(1,1)</code></strong> em <code>T</code>.</li>
      </ul>
    </li>
    <li><strong>Composto + Multivalorado Composto:</strong> Composto simples achata colunas; multivalorado composto gera nova tabela com <strong>todos os subatributos na PK</strong> ou identificador parcial + <code>-p-&gt;</code>.</li>
    <li><strong><code>1:1</code> Assimétrico (<code>(1,1)</code> vs <code>(0,1)</code>):</strong> Migre a FK com <code>UNIQUE NOT NULL</code> para o lado <strong>total <code>(1,1)</code></strong> para zerar <code>NULL</code>s.</li>
  </ul>
</div>
""",
    "example_html": """
<div class="sg-example-box">
  <h4>Exemplos Análogos (Domínios Diferentes das Tarefas)</h4>
  <p><strong>1. <code>1:1</code> Assimétrico (<code>COFRE (1,1)</code> vs <code>GERENTE (0,1)</code>):</strong> Como todo cofre tem 1 gerente, mas nem todo gerente cuida de um cofre, adicione <code>CPF_Gerente UNIQUE NOT NULL</code> em <code>COFRE</code> (zero nulos!).</p>
  <p><strong>2. Multivalorado Composto (<code>FORNECEDOR</code>):</strong> Composto <code>End(Logr, CEP)</code> achata direto em <code>FORNECEDOR(..., Logr, CEP)</code>; multivalorado composto <code>{Contatos(Nome, Ramal)}</code> gera <code>FORN_CONTATO(<u>CNPJ</u>, <u>Nome</u>, <u>Ramal</u>)</code> com <code>-p-&gt; FORNECEDOR</code>.</p>
  <p><strong>3. Rede sem auto-laço (Porto/Rodovia):</strong> <code>CREATE ASSERTION SEM_LACO CHECK (NOT EXISTS (SELECT 1 FROM ROTA WHERE Origem = Destino));</code>.</p>
</div>
"""
}

STUDY_GUIDE_G14 = {
    "id": "G14",
    "title": "G14 — Cobertura Mínima (Fc), Ciclos de 4 Chaves &amp; Checklist Final M8",
    "file_path": "study_guides/G14_M8_CoberturaMinima_CiclosChaves_e_ChecklistFinal.md",
    "coursework_ref": "ibd-parte6.pdf (Algoritmo Fc em 3 Passos, Ciclos de Equivalência, 1FN–3FN vs BCNF e NJP Sequencial)",
    "quick_rules_html": """
<div class="sg-rules-box">
  <h4>Resumo Operacional — Rodada 5 (Grupo G14)</h4>
  <ul>
    <li><strong>Cobertura Mínima <code>Fc</code> (Ordem Exata):</strong> (1) RHS unitário; (2) Remova atributos estranhos no LHS testando <code>(LHS - {B})+</code>; (3) Só depois remova DFs redundantes testando <code>X+</code> em <code>F - {f}</code>.</li>
    <li><strong>Armadilha do Ciclo + Atributo Isolado (<code>A &rarr; B &rarr; C &rarr; D &rarr; A</code> + <code>E</code>):</strong> Todas as combinações com <code>E</code> viram chaves candidatas (<code>{AE, BE, CE, DE}</code>)! Logo <code>A &rarr; B</code> tem RHS <strong>primo</strong>: satisfaz 2FN e 3FN, violando apenas a BCNF.</li>
    <li><strong>Checklist de Junção Sem Perda em 3+ Tabelas:</strong> Uma cadeia <code>R &rarr; R1, R2</code> e depois <code>R2 &rarr; R2a, R2b</code> é sem perda se cada passo binário satisfizer <code>(Ri &cap; Rj) &rarr; Ri</code> ou <code>Rj</code>.</li>
  </ul>
</div>
""",
    "example_html": """
<div class="sg-example-box">
  <h4>Exemplos Análogos (Domínios Diferentes das Tarefas)</h4>
  <p><strong>1. <code>Fc</code> em 3 Passos:</strong> Em <code>{ P &rarr; Q, Q &rarr; R, PQ &rarr; T, P &rarr; T }</code>: no Passo 2, <code>P &rarr; Q</code> torna <code>Q</code> estranho em <code>PQ &rarr; T</code> (vira <code>P &rarr; T</code>); no Passo 3 remove-se a cópia duplicada de <code>P &rarr; T</code>.</p>
  <p><strong>2. Esquema Cíclico <code>X(P, Q, R, S, T)</code> com <code>F = { P &rarr; Q, Q &rarr; R, R &rarr; P, PS &rarr; T }</code>:</strong> Chaves = <code>{PS, QS, RS}</code>; Primos = <code>{P, Q, R, S}</code>; Não-primo = <code>{T}</code>. Resultado: está em <strong>3FN</strong> (não em BCNF).</p>
</div>
"""
}


# ---------------------------------------------------------------------------
# Dicionário Principal de Exercícios da Rodada 5 (R5.1 .. R5.10)
# ---------------------------------------------------------------------------

ROUND5_EXERCISES = {
    "R5.1": {
        "title": "R5.1 (Leitura Inversa) — Do Esquema Lógico com RIRs às Cardinalidades ER (Secretaria)",
        "type": "oficial",
        "mode": "structured",
        "study_guide": STUDY_GUIDE_G13,
        "context_html": """
<p><strong>Leitura Bidirecional (Esquema Lógico &rarr; Diagrama ER):</strong> Analise o esquema lógico abaixo já mapeado por um professor da UFMG e deduza exatamente as restrições originais do Diagrama ER:</p>
<pre class="sql-code">FACULDADE(<u>CodFac</u>, NomeFac)
COLEGIADO(<u>CodFac</u>, <u>NumCol</u>, Sala)
  COLEGIADO[CodFac] -p-&gt; FACULDADE[CodFac]

DIRETOR(<u>SIAPE</u>, NomeDir)
GERENCIA_FAC(<u>CodFac</u>, SIAPE(unique, nn))
  -- Ou diretamente em FACULDADE: FACULDADE(<u>CodFac</u>, NomeFac, SIAPE_Dir(unique, nn))
  FACULDADE[SIAPE_Dir] -b-&gt; DIRETOR[SIAPE]

ALUNO(<u>Matr</u>, NomeAluno, CodFac(nn), NumCol(nn), CodTutor)
  ALUNO[CodFac, NumCol] -b-&gt; COLEGIADO[CodFac, NumCol]
  ALUNO[CodTutor] -n-&gt; ALUNO[Matr]

PROJETO(<u>IdProj</u>, Titulo)
PARTICIPA(<u>Matr</u>, <u>IdProj</u>, Horas)
  PARTICIPA[Matr] -p-&gt; ALUNO[Matr]
  PARTICIPA[IdProj] -p-&gt; PROJETO[IdProj]</pre>
""",
        "answer_sheet_html": """
<div class="answer-sheet-box">
  <h4>Gabarito Explicado — R5.1 (Leitura Inversa)</h4>
  <ul>
    <li><strong><code>COLEGIADO</code>:</strong> PK composta herdando <code>CodFac</code> + política <code>-p-&gt;</code> &rArr; <strong>Entidade Fraca</strong> identificada por <code>FACULDADE</code> (<code>NumCol</code> é chave parcial).</li>
    <li><strong><code>FACULDADE[SIAPE_Dir(unique, nn)]</code>:</strong> FK com <code>UNIQUE</code> e <code>NOT NULL</code> &rArr; relacionamento <strong><code>1:1</code></strong> com participação <strong>total <code>(1,1)</code></strong> em <code>FACULDADE</code> e parcial <code>(0,1)</code> em <code>DIRETOR</code> (um diretor pode não dirigir faculdade alguma).</li>
    <li><strong><code>ALUNO[CodFac(nn), NumCol(nn)] -b-&gt;</code> e <code>ALUNO[CodTutor] -n-&gt;</code>:</strong> Todo aluno está matriculado em exatamente 1 colegiado <code>(1,1)</code> (impedindo excluir colegiado com alunos via <code>-b-&gt;</code>), e possui <strong>auto-relacionamento <code>1:N</code></strong> opcional <code>(0,1)</code> com um aluno tutor (se o tutor sair, <code>CodTutor</code> vira <code>NULL</code> via <code>-n-&gt;</code>).</li>
  </ul>
</div>
""",
        "fields": [
            {
                "id": "f1",
                "label": "1) Olhando apenas para FACULDADE(CodFac, NomeFac, SIAPE_Dir(unique, nn)) -b-> DIRETOR[SIAPE], qual é o relacionamento ER original?",
                "options": [
                    "Relacionamento M:N entre FACULDADE e DIRETOR, pois uma faculdade pode possuir vários diretores ao mesmo tempo.",
                    "Relacionamento 1:N onde um único diretor dirige várias faculdades simultaneamente sem exclusividade.",
                    "Relacionamento 1:1 com participação total (1,1) de FACULDADE e parcial (0,1) de DIRETOR.",
                    "Entidade fraca DIRETOR dependente existencialmente da chave primária composta de FACULDADE."
                ],
                "answer": "Relacionamento 1:1 com participação total (1,1) de FACULDADE e parcial (0,1) de DIRETOR.",
                "explanation": "UNIQUE na FK garante no máximo 1 faculdade por SIAPE_Dir; NOT NULL garante que toda faculdade tem 1 diretor (1,1); e estar em FACULDADE deixa DIRETOR como (0,1)."
            },
            {
                "id": "f2",
                "label": "2) O que indicam simultaneamente a PK de COLEGIADO(CodFac, NumCol) e a RIR -p-> FACULDADE[CodFac]?",
                "options": [
                    "COLEGIADO é uma Entidade Fraca subordinada a FACULDADE com chave parcial NumCol e propagação CASCADE.",
                    "COLEGIADO é uma entidade forte independente ligada por um relacionamento M:N simples a FACULDADE.",
                    "COLEGIADO representa um atributo multivalorado de apenas um campo textual de FACULDADE.",
                    "NumCol é uma chave primária global única, podendo COLEGIADO existir com CodFac igual a NULL."
                ],
                "answer": "COLEGIADO é uma Entidade Fraca subordinada a FACULDADE com chave parcial NumCol e propagação CASCADE.",
                "explanation": "Herdar a PK do pai na própria PK composta somada à política -p-> caracteriza uma Entidade Fraca clássica."
            },
            {
                "id": "f3",
                "label": "3) O que significa a dupla de políticas ALUNO[CodFac, NumCol] -b-> COLEGIADO e ALUNO[CodTutor] -n-> ALUNO[Matr]?",
                "options": [
                    "O aluno pode ficar sem colegiado caso o curso feche (-n->), mas jamais pode ficar sem aluno tutor.",
                    "Apagar um colegiado exclui em cascata todos os alunos nele matriculados e os projetos deles.",
                    "Ambos os relacionamentos são M:N com participação opcional nos dois extremos do diagrama ER.",
                    "Todo aluno pertence obrigatoriamente a 1 colegiado (bloqueia exclusão do pai), e tem tutor opcional (vira NULL se removido)."
                ],
                "answer": "Todo aluno pertence obrigatoriamente a 1 colegiado (bloqueia exclusão do pai), e tem tutor opcional (vira NULL se removido).",
                "explanation": "CodFac e NumCol são NOT NULL com -b-> (RESTRICT); já CodTutor é anulável (auto-FK 1:N parcial) e aceita -n-> (SET NULL)."
            }
        ]
    },

    "R5.2": {
        "title": "R5.2 (Oficial/ER) — 1:1 Assimétrico + Atributo Composto &amp; Multivalorado Composto (Seguradora)",
        "type": "oficial",
        "mode": "structured",
        "study_guide": STUDY_GUIDE_G13,
        "context_html": """
<p><strong>Modelagem Detalhada de Atributos &amp; 1:1 (<code>ibd-parte5.pdf</code> — Regras 1, 2 e 4):</strong> Analise o diagrama ER de uma seguradora veicular abaixo:</p>
<div style="text-align:center; margin: 12px 0;">
<svg viewBox="0 0 760 215" width="100%" style="max-width:740px; background:#0d1117; border:1px solid #30363d; border-radius:8px;">
  <!-- SEGURADO -->
  <rect x="26" y="75" width="146" height="46" rx="4" fill="#161b22" stroke="#58a6ff" stroke-width="2.2"/>
  <text x="99" y="94" text-anchor="middle" fill="#f0f6fc" font-size="11" font-weight="700">SEGURADO</text>
  <text x="99" y="109" text-anchor="middle" fill="#8b949e" font-size="9">(<tspan text-decoration="underline">CPF</tspan>, Nome)</text>
  <!-- Composite Endereco(Rua, Cidade) -->
  <ellipse cx="75" cy="30" rx="52" ry="16" fill="#161b22" stroke="#8b949e" stroke-width="1.3"/>
  <text x="75" y="34" text-anchor="middle" fill="#e6edf3" font-size="9">End(Rua, Cidade)</text>
  <line x1="80" y1="46" x2="90" y2="75" stroke="#8b949e" stroke-width="1.3"/>
  <!-- Composite Multivalued {{Benef(NomeBen, Grau)}} -->
  <ellipse cx="105" cy="172" rx="76" ry="21" fill="#161b22" stroke="#79c0ff" stroke-width="1.4"/>
  <ellipse cx="105" cy="172" rx="70" ry="16" fill="none" stroke="#79c0ff" stroke-width="1.2"/>
  <text x="105" y="175" text-anchor="middle" fill="#e6edf3" font-size="9">Benef(NomeBen, Grau)</text>
  <line x1="102" y1="121" x2="104" y2="151" stroke="#8b949e" stroke-width="1.3"/>

  <!-- POSSUI 1:N -> VEICULO -->
  <line x1="172" y1="98" x2="218" y2="98" stroke="#8b949e" stroke-width="1.5"/>
  <text x="195" y="89" text-anchor="middle" fill="#79c0ff" font-size="9">(1,N)</text>
  <polygon points="218,98 250,76 282,98 250,120" fill="#1f2937" stroke="#d2a8ff" stroke-width="1.6"/>
  <text x="250" y="101" text-anchor="middle" fill="#d2a8ff" font-size="9" font-weight="700">TEM</text>
  <line x1="282" y1="95" x2="322" y2="95" stroke="#58a6ff" stroke-width="1.5"/>
  <line x1="282" y1="101" x2="322" y2="101" stroke="#58a6ff" stroke-width="1.5"/>
  <text x="302" y="86" text-anchor="middle" fill="#79c0ff" font-size="9">(1,1)</text>

  <!-- VEICULO -->
  <rect x="322" y="75" width="136" height="46" rx="4" fill="#161b22" stroke="#58a6ff" stroke-width="2.2"/>
  <text x="390" y="94" text-anchor="middle" fill="#f0f6fc" font-size="11" font-weight="700">VEICULO</text>
  <text x="390" y="109" text-anchor="middle" fill="#8b949e" font-size="9">(<tspan text-decoration="underline">Placa</tspan>, Ano)</text>

  <!-- 1:1 Asymmetrical EQUIPADO -> RASTREADOR -->
  <!-- Double line on VEICULO side (1,1), single line on RASTREADOR side (0,1) -->
  <line x1="458" y1="95" x2="500" y2="95" stroke="#f2cc60" stroke-width="1.6"/>
  <line x1="458" y1="101" x2="500" y2="101" stroke="#f2cc60" stroke-width="1.6"/>
  <text x="479" y="86" text-anchor="middle" fill="#ffa657" font-size="9">(1,1)</text>
  <polygon points="500,98 542,74 584,98 542,122" fill="#1f2937" stroke="#f2cc60" stroke-width="1.8"/>
  <text x="542" y="101" text-anchor="middle" fill="#f2cc60" font-size="9" font-weight="700">USA_GPS</text>
  <line x1="584" y1="98" x2="625" y2="98" stroke="#8b949e" stroke-width="1.5"/>
  <text x="604" y="89" text-anchor="middle" fill="#79c0ff" font-size="9">(0,1)</text>

  <!-- RASTREADOR -->
  <rect x="625" y="75" width="120" height="46" rx="4" fill="#161b22" stroke="#3fb950" stroke-width="2"/>
  <text x="685" y="94" text-anchor="middle" fill="#f0f6fc" font-size="11" font-weight="700">RASTREADOR</text>
  <text x="685" y="109" text-anchor="middle" fill="#8b949e" font-size="9">(<tspan text-decoration="underline">NumSerie</tspan>, Lote)</text>
</svg>
</div>
<p>Realize o mapeamento lógico exato seguindo as regras da Etapa 1 de <code>ibd-parte5.pdf</code>.</p>
""",
        "answer_sheet_html": """
<div class="answer-sheet-box">
  <h4>Gabarito Explicado — R5.2</h4>
  <ul>
    <li><strong>Atributo Composto Simples (<code>End(Rua, Cidade)</code>):</strong> Achata-se apenas nas folhas simples dentro de <code>SEGURADO(<u>CPF</u>, Nome, Rua, Cidade)</code> (<code>Endereco</code> em si não vira coluna).</li>
    <li><strong>Atributo Multivalorado Composto (<code>Benef(NomeBen, Grau)</code>):</strong> Gera tabela separada <code>BENEFICIARIO(<u>CPF</u>, <u>NomeBen</u>, <u>Grau</u>)</code> (ou incluindo todos os subcomponentes simples na PK para permitir dois beneficiários homônimos de graus distintos se necessário, com <code>-p-&gt; SEGURADO[CPF]</code>).</li>
    <li><strong>Relacionamento <code>1:1</code> Assimétrico (<code>VEICULO (1,1)</code> vs <code>RASTREADOR (0,1)</code>):</strong> Como todo veículo tem <code>(1,1)</code> rastreador, mas um rastreador em estoque tem <code>(0,1)</code> veículo, deve-se incluir <code>NumSerie UNIQUE NOT NULL</code> em <strong><code>VEICULO</code></strong> (zerando valores <code>NULL</code> nessa coluna!).</li>
  </ul>
</div>
""",
        "fields": [
            {
                "id": "f1",
                "label": "1) Para o relacionamento 1:1 entre VEICULO (1,1) e RASTREADOR (0,1), qual é o melhor posicionamento da chave estrangeira sem NULLs?",
                "options": [
                    "Colocar Placa_Veic dentro de RASTREADOR aceitando NULL para rastreadores no estoque.",
                    "Colocar NumSerie (UNIQUE, NOT NULL) dentro de VEICULO, pois todo veículo possui exatamente 1 rastreador.",
                    "Criar obrigatoriamente uma terceira tabela associativa USA_GPS(Placa, NumSerie) com duas FKs opcionais.",
                    "Fundir RASTREADOR e SEGURADO em uma única relação por causa do endereço composto."
                ],
                "answer": "Colocar NumSerie (UNIQUE, NOT NULL) dentro de VEICULO, pois todo veículo possui exatamente 1 rastreador.",
                "explanation": "A Regra 4 orienta migrar a FK com UNIQUE para o lado de participação TOTAL (1,1) — aqui VEICULO — evitando os valores NULL que surgiriam em RASTREADOR(0,1)."
            },
            {
                "id": "f2",
                "label": "2) Como devem ser mapeados o atributo composto simples End(Rua, Cidade) e o multivalorado composto {{Benef(NomeBen, Grau)}} de SEGURADO?",
                "options": [
                    "Criar tabelas separadas tanto para Endereco quanto para Beneficiario ligadas por -b->.",
                    "Colocar Endereco, NomeBen e Grau juntos em SEGURADO como colunas textuais concatenadas.",
                    "Achatar apenas NomeBen dentro de SEGURADO e manter Endereco em uma nova tabela auxiliar.",
                    "Achatar Rua e Cidade direto em SEGURADO; criar BENEF(CPF, NomeBen, Grau) com -p-> SEGURADO."
                ],
                "answer": "Achatar Rua e Cidade direto em SEGURADO; criar BENEF(CPF, NomeBen, Grau) com -p-> SEGURADO.",
                "explanation": "Compostos simples sempre viram suas colunas folha na tabela dona; multivalorados (mesmo compostos) viram nova relação contendo a PK do dono e os subatributos com política -p->."
            },
            {
                "id": "f3",
                "label": "3) Supondo que SEGURADO também receba a FK em VEICULO(Placa, Ano, CPF_Seg(nn), NumSerie(unique, nn)), qual é a RIR correta para CPF_Seg se não desejarmos apagar acidentalmente um segurado que possui veículos ativos?",
                "options": [
                    "VEICULO[CPF_Seg] -n-> SEGURADO[CPF] definindo o CPF como NULL ao excluir o titular.",
                    "VEICULO[CPF_Seg] -p-> SEGURADO[CPF] forçando a remoção do histórico de todos os carros.",
                    "VEICULO[CPF_Seg] -b-> SEGURADO[CPF] (RESTRICT / bloqueia a exclusão do dono enquanto houver veículo).",
                    "SEGURADO[CPF] -b-> VEICULO[Placa] apontando a chave estrangeira do pai para o filho."
                ],
                "answer": "VEICULO[CPF_Seg] -b-> SEGURADO[CPF] (RESTRICT / bloqueia a exclusão do dono enquanto houver veículo).",
                "explanation": "Como CPF_Seg é NOT NULL (-n-> inválido) e queremos impedir remoção acidental do titular enquanto houver veículo vinculado, aplica-se -b-> (RESTRICT)."
            }
        ]
    },

    "R5.3": {
        "title": "R5.3 (Lab SQL DDL) — Cadeia Hospitalar 3 Níveis + Ocupação &amp; CHECK (SQLite)",
        "type": "oficial",
        "mode": "sql_ddl",
        "study_guide": STUDY_GUIDE_G13,
        "setup": "",
        "context_html": """
<p><strong>Simulado Prático DDL (Cadeia de Entidades Fracas + Restrições de Domínio e RIRs):</strong> Construa em SQLite DDL o esquema completo abaixo:</p>
<ul>
  <li><code>UNIDADE(CodUnid INTEGER PK, Nome TEXT NOT NULL)</code></li>
  <li><code>SETOR(CodUnid INTEGER, CodSetor TEXT, Andar INTEGER NOT NULL)</code> &mdash; Fraca de <code>UNIDADE</code> com <code>ON DELETE CASCADE</code>.</li>
  <li><code>LEITO(CodUnid INTEGER, CodSetor TEXT, NumLeito INTEGER, Status TEXT NOT NULL)</code> &mdash; Fraca de <code>SETOR</code> com PK tripla <code>(CodUnid, CodSetor, NumLeito)</code>, FK composta com <code>ON DELETE CASCADE</code> e <code>CHECK (Status IN ('LIVRE', 'OCUPADO', 'MANUTENCAO'))</code>.</li>
  <li><code>INTERNACAO(IdInt INTEGER PK, PacCPF TEXT NOT NULL, CodUnid INTEGER NOT NULL, CodSetor TEXT NOT NULL, NumLeito INTEGER NOT NULL)</code> &mdash; FK composta para <code>LEITO</code> com <code>ON DELETE RESTRICT</code> (impedir apagar leito enquanto houver internação registrada!).</li>
</ul>
""",
        "answer_sheet_html": """
<div class="answer-sheet-box">
  <h4>Gabarito DDL de Referência — R5.3</h4>
  <pre class="sql-code">CREATE TABLE UNIDADE (
  CodUnid INTEGER PRIMARY KEY,
  Nome    TEXT NOT NULL
);

CREATE TABLE SETOR (
  CodUnid  INTEGER NOT NULL,
  CodSetor TEXT NOT NULL,
  Andar    INTEGER NOT NULL,
  PRIMARY KEY (CodUnid, CodSetor),
  FOREIGN KEY (CodUnid) REFERENCES UNIDADE(CodUnid) ON DELETE CASCADE
);

CREATE TABLE LEITO (
  CodUnid  INTEGER NOT NULL,
  CodSetor TEXT NOT NULL,
  NumLeito INTEGER NOT NULL,
  Status   TEXT NOT NULL CHECK (Status IN ('LIVRE', 'OCUPADO', 'MANUTENCAO')),
  PRIMARY KEY (CodUnid, CodSetor, NumLeito),
  FOREIGN KEY (CodUnid, CodSetor) REFERENCES SETOR(CodUnid, CodSetor) ON DELETE CASCADE
);

CREATE TABLE INTERNACAO (
  IdInt    INTEGER PRIMARY KEY,
  PacCPF   TEXT NOT NULL,
  CodUnid  INTEGER NOT NULL,
  CodSetor TEXT NOT NULL,
  NumLeito INTEGER NOT NULL,
  FOREIGN KEY (CodUnid, CodSetor, NumLeito)
    REFERENCES LEITO(CodUnid, CodSetor, NumLeito) ON DELETE RESTRICT
);</pre>
</div>
""",
        "ddl_tests": [
            {
                "name": "Existência das 4 tabelas (UNIDADE, SETOR, LEITO, INTERNACAO)",
                "type": "tables_exist",
                "tables": ["UNIDADE", "SETOR", "LEITO", "INTERNACAO"],
                "hint": "Verifique os 4 nomes exatos: UNIDADE, SETOR, LEITO e INTERNACAO."
            },
            {
                "name": "Aceitar leitos homônimos em setores/unidades distintos e internação válida",
                "type": "must_succeed",
                "sql": """
                    INSERT INTO UNIDADE VALUES (1, 'HC-UFMG'), (2, 'Pronto Socorro');
                    INSERT INTO SETOR VALUES (1, 'UTI', 3), (2, 'UTI', 1);
                    INSERT INTO LEITO VALUES (1, 'UTI', 10, 'OCUPADO'), (2, 'UTI', 10, 'LIVRE'), (1, 'UTI', 11, 'LIVRE');
                    INSERT INTO INTERNACAO VALUES (500, '111.222.333-44', 1, 'UTI', 10);
                """,
                "hint": "Leito (1,'UTI',10) e (2,'UTI',10) precisam coexistir."
            },
            {
                "name": "Bloquear Status inválido em LEITO via CHECK",
                "type": "must_fail",
                "sql": """
                    INSERT INTO UNIDADE VALUES (1, 'HC');
                    INSERT INTO SETOR VALUES (1, 'UTI', 2);
                    INSERT INTO LEITO VALUES (1, 'UTI', 5, 'RESERVADO');
                """,
                "hint": "Status deve restringir a ('LIVRE', 'OCUPADO', 'MANUTENCAO') via CHECK."
            },
            {
                "name": "Bloquear remoção de UNIDADE quando existe INTERNACAO ativa em algum leito (-b->)",
                "type": "must_fail",
                "sql": """
                    INSERT INTO UNIDADE VALUES (1, 'HC');
                    INSERT INTO SETOR VALUES (1, 'UTI', 2);
                    INSERT INTO LEITO VALUES (1, 'UTI', 10, 'OCUPADO');
                    INSERT INTO INTERNACAO VALUES (1, '999', 1, 'UTI', 10);
                    DELETE FROM UNIDADE WHERE CodUnid = 1;
                """,
                "hint": "INTERNACAO deve referenciar LEITO com ON DELETE RESTRICT para bloquear exclusões com paciente internado."
            },
            {
                "name": "Propagar exclusão em cascata quando o leito não tem internações",
                "type": "cascade_check",
                "sql_setup": """
                    INSERT INTO UNIDADE VALUES (1, 'HC'), (2, 'Anexo');
                    INSERT INTO SETOR VALUES (1, 'UTI', 2), (2, 'UTI', 1);
                    INSERT INTO LEITO VALUES (1, 'UTI', 11, 'LIVRE'), (2, 'UTI', 11, 'LIVRE');
                    DELETE FROM UNIDADE WHERE CodUnid = 1;
                """,
                "verify_query": "SELECT COUNT(*) FROM LEITO WHERE CodUnid = 1;",
                "expected_scalar": 0,
                "hint": "SETOR e LEITO precisam declarar ON DELETE CASCADE em cadeia."
            }
        ]
    },

    "R5.4": {
        "title": "R5.4 (Prova Completa de Papel) — Mini-Simulado Agência Espacial (EER + Lógico + RIRs)",
        "type": "oficial",
        "mode": "open_design",
        "study_guide": STUDY_GUIDE_G13,
        "context_html": """
<p><strong>Questão Aberta Completa Estilo Prova Final (Sem Checagem Automática &mdash; Gabarito Duplo SVG + Esquema Lógico):</strong><br>
Com base nos requisitos abaixo, faça em seu caderno <strong>(A) o Diagrama EER completo</strong> e <strong>(B) o Esquema Lógico Relacional com todas as RIRs (<code>-b-&gt;</code>, <code>-p-&gt;</code>, <code>-n-&gt;</code>)</strong>:</p>
<div class="sg-rules-box">
  <ol>
    <li>Uma agência espacial cadastra <strong>Tripulantes</strong> (<code><u>CodTrip</u></code>, <code>Nome</code>, atributo composto <code>Passaporte(Numero, Pais)</code>). Todo tripulante atua obrigatoriamente como <strong>Comandante</strong> (<code>HorasVoo</code>) e/ou <strong>Especialista</strong> (<code>AreaCientifica</code>), podendo acumular ambos os papéis (<code>{o, total}</code>).</li>
    <li>Existem <strong>Bases de Lançamento</strong> (<code><u>CodBase</u></code>, <code>Local</code>), cada qual mantendo várias <strong>Plataformas</strong> numeradas a partir de 1 dentro da base (<code>NumPlat</code>, <code>CapacidadeKg</code>).</li>
    <li>Cada <strong>Missão</strong> (<code><u>CodMissao</u></code>, <code>DataPrevista</code>) é liderada obrigatoriamente por um único <code>Comandante</code>, decola de uma única <code>Plataforma</code> específica (<code>(1,1)</code>) e conta com uma equipe de <code>Especialistas</code> (<code>M:N</code>, com atributo <code>FuncaoBordo</code>).</li>
  </ol>
</div>
""",
        "answer_sheet_html": """
<div class="answer-sheet-box">
  <h4>Gabarito Duplo Oficial — R5.4 (EER Visual + Esquema Lógico)</h4>
  <div style="text-align:center; margin: 10px 0;">
  <svg viewBox="0 0 820 340" width="100%" style="max-width:800px; background:#0d1117; border:1px solid #30363d; border-radius:8px;">
    <!-- TRIPULANTE {o, total} -> COMANDANTE, ESPECIALISTA -->
    <rect x="18" y="16" width="214" height="44" rx="4" fill="#161b22" stroke="#58a6ff" stroke-width="2"/>
    <text x="125" y="34" text-anchor="middle" fill="#f0f6fc" font-size="11" font-weight="700">TRIPULANTE</text>
    <text x="125" y="49" text-anchor="middle" fill="#8b949e" font-size="9">(<tspan text-decoration="underline">CodTrip</tspan>, Nome, Pass(Num,Pais))</text>
    <line x1="122" y1="60" x2="122" y2="80" stroke="#f2cc60" stroke-width="1.5"/>
    <line x1="128" y1="60" x2="128" y2="80" stroke="#f2cc60" stroke-width="1.5"/>
    <circle cx="125" cy="93" r="12" fill="#161b22" stroke="#f2cc60" stroke-width="1.8"/>
    <text x="125" y="97" text-anchor="middle" fill="#f2cc60" font-size="11" font-weight="700">o</text>
    <line x1="114" y1="101" x2="67" y2="126" stroke="#8b949e" stroke-width="1.4"/>
    <line x1="136" y1="101" x2="186" y2="126" stroke="#8b949e" stroke-width="1.4"/>
    <rect x="16" y="126" width="102" height="40" rx="4" fill="#161b22" stroke="#3fb950" stroke-width="1.6"/>
    <text x="67" y="144" text-anchor="middle" fill="#f0f6fc" font-size="10" font-weight="700">COMANDANTE</text>
    <text x="67" y="158" text-anchor="middle" fill="#8b949e" font-size="9">(HorasVoo)</text>
    <rect x="130" y="126" width="112" height="40" rx="4" fill="#161b22" stroke="#3fb950" stroke-width="1.6"/>
    <text x="186" y="144" text-anchor="middle" fill="#f0f6fc" font-size="10" font-weight="700">ESPECIALISTA</text>
    <text x="186" y="158" text-anchor="middle" fill="#8b949e" font-size="9">(AreaCient.)</text>

    <!-- BASE -> TEM -> PLATAFORMA -->
    <rect x="365" y="16" width="128" height="42" rx="4" fill="#161b22" stroke="#58a6ff" stroke-width="2"/>
    <text x="429" y="34" text-anchor="middle" fill="#f0f6fc" font-size="11" font-weight="700">BASE</text>
    <text x="429" y="48" text-anchor="middle" fill="#8b949e" font-size="9">(<tspan text-decoration="underline">CodBase</tspan>, Local)</text>
    <line x1="493" y1="37" x2="535" y2="37" stroke="#8b949e" stroke-width="1.4"/>
    <text x="514" y="29" text-anchor="middle" fill="#79c0ff" font-size="9">(1,N)</text>
    <polygon points="535,37 570,15 605,37 570,59" fill="#1f2937" stroke="#f0883e" stroke-width="1.8"/>
    <polygon points="541,37 570,20 599,37 570,54" fill="none" stroke="#f0883e" stroke-width="1.2"/>
    <text x="570" y="41" text-anchor="middle" fill="#f0883e" font-size="9" font-weight="700">TEM</text>
    <line x1="605" y1="34" x2="645" y2="34" stroke="#f0883e" stroke-width="1.5"/>
    <line x1="605" y1="40" x2="645" y2="40" stroke="#f0883e" stroke-width="1.5"/>
    <text x="625" y="26" text-anchor="middle" fill="#ffa657" font-size="9">(1,1)</text>
    <rect x="645" y="14" width="152" height="46" rx="4" fill="#161b22" stroke="#f0883e" stroke-width="2"/>
    <rect x="650" y="19" width="142" height="36" rx="2" fill="none" stroke="#f0883e" stroke-width="1.2"/>
    <text x="721" y="34" text-anchor="middle" fill="#f0f6fc" font-size="10" font-weight="700">PLATAFORMA</text>
    <text x="721" y="48" text-anchor="middle" fill="#ffa657" font-size="9">({NumPlat}, CapKg)</text>

    <!-- MISSAO in middle-bottom -->
    <rect x="370" y="205" width="160" height="46" rx="4" fill="#161b22" stroke="#58a6ff" stroke-width="2.2"/>
    <text x="450" y="224" text-anchor="middle" fill="#f0f6fc" font-size="11" font-weight="700">MISSAO</text>
    <text x="450" y="239" text-anchor="middle" fill="#8b949e" font-size="9">(<tspan text-decoration="underline">CodMissao</tspan>, DataPrev)</text>

    <!-- EQUIPE M:N [FuncaoBordo] between ESPECIALISTA and MISSAO -->
    <path d="M 186,166 L 186,228 L 245,228" fill="none" stroke="#8b949e" stroke-width="1.4"/>
    <text x="215" y="220" text-anchor="middle" fill="#79c0ff" font-size="9">(0,N)</text>
    <polygon points="245,228 288,204 331,228 288,252" fill="#1f2937" stroke="#d2a8ff" stroke-width="1.8"/>
    <text x="288" y="232" text-anchor="middle" fill="#d2a8ff" font-size="9" font-weight="700">EQUIPE</text>
    <text x="288" y="264" text-anchor="middle" fill="#d2a8ff" font-size="9">[FuncaoBordo]</text>
    <line x1="331" y1="228" x2="370" y2="228" stroke="#8b949e" stroke-width="1.4"/>
    <text x="350" y="220" text-anchor="middle" fill="#79c0ff" font-size="9">(0,N)</text>

    <!-- LIDERA 1:N total in MISSAO from COMANDANTE -->
    <path d="M 67,166 L 67,298 L 195,298" fill="none" stroke="#8b949e" stroke-width="1.4"/>
    <text x="130" y="290" text-anchor="middle" fill="#79c0ff" font-size="9">(0,N)</text>
    <polygon points="195,298 240,274 285,298 240,322" fill="#1f2937" stroke="#58a6ff" stroke-width="1.8"/>
    <text x="240" y="302" text-anchor="middle" fill="#79c0ff" font-size="9" font-weight="700">LIDERA</text>
    <path d="M 285,295 L 447,295 L 447,251" fill="none" stroke="#58a6ff" stroke-width="1.5"/>
    <path d="M 285,301 L 453,301 L 453,251" fill="none" stroke="#58a6ff" stroke-width="1.5"/>
    <text x="366" y="287" text-anchor="middle" fill="#79c0ff" font-size="9">(1,1)</text>

    <!-- DECOLA 1:N total in MISSAO from PLATAFORMA -->
    <line x1="721" y1="60" x2="721" y2="118" stroke="#8b949e" stroke-width="1.4"/>
    <text x="742" y="92" text-anchor="middle" fill="#79c0ff" font-size="9">(0,N)</text>
    <polygon points="676,142 721,118 766,142 721,166" fill="#1f2937" stroke="#58a6ff" stroke-width="1.8"/>
    <text x="721" y="146" text-anchor="middle" fill="#79c0ff" font-size="9" font-weight="700">DECOLA</text>
    <path d="M 676,139 L 582,139 L 582,225 L 530,225" fill="none" stroke="#58a6ff" stroke-width="1.5"/>
    <path d="M 676,145 L 588,145 L 588,231 L 530,231" fill="none" stroke="#58a6ff" stroke-width="1.5"/>
    <text x="630" y="131" text-anchor="middle" fill="#79c0ff" font-size="9">(1,1)</text>
  </svg>
  </div>
  <pre class="sql-code">TRIPULANTE(<u>CodTrip</u>, Nome, PassNumero, PassPais)
COMANDANTE(<u>CodTrip</u>, HorasVoo(nn))
  COMANDANTE[CodTrip] -p-&gt; TRIPULANTE[CodTrip]
ESPECIALISTA(<u>CodTrip</u>, AreaCientifica(nn))
  ESPECIALISTA[CodTrip] -p-&gt; TRIPULANTE[CodTrip]

BASE(<u>CodBase</u>, Local)
PLATAFORMA(<u>CodBase</u>, <u>NumPlat</u>, CapacidadeKg)
  PLATAFORMA[CodBase] -p-&gt; BASE[CodBase]

MISSAO(<u>CodMissao</u>, DataPrevista, CodComandante(nn), CodBase(nn), NumPlat(nn))
  MISSAO[CodComandante] -b-&gt; COMANDANTE[CodTrip]
  MISSAO[CodBase, NumPlat] -b-&gt; PLATAFORMA[CodBase, NumPlat]

EQUIPE(<u>CodMissao</u>, <u>CodEsp</u>, FuncaoBordo)
  EQUIPE[CodMissao] -p-&gt; MISSAO[CodMissao]
  EQUIPE[CodEsp] -p-&gt; ESPECIALISTA[CodTrip]</pre>
</div>
""",
        "fields": []
    },

    "R5.5": {
        "title": "R5.5 (Lab Assertions SQL-92) — Invariantes de Rede Ferroviária (Auto-laço &amp; Expressa)",
        "type": "oficial",
        "mode": "sql_assertion",
        "study_guide": STUDY_GUIDE_G13,
        "setup": """
CREATE TABLE ESTACAO (
  CodEst TEXT PRIMARY KEY,
  Cidade TEXT NOT NULL
);
CREATE TABLE TREM (
  CodTrem TEXT PRIMARY KEY,
  CapMin INTEGER NOT NULL
);
CREATE TABLE TRECHO (
  IdTrecho INTEGER PRIMARY KEY,
  CodOrig TEXT NOT NULL REFERENCES ESTACAO(CodEst),
  CodDest TEXT NOT NULL REFERENCES ESTACAO(CodEst),
  TipoLinha TEXT NOT NULL,
  CodTrem TEXT NOT NULL REFERENCES TREM(CodTrem)
);
INSERT INTO ESTACAO VALUES ('BH', 'Belo Horizonte'), ('SP', 'São Paulo'), ('RJ', 'Rio de Janeiro');
INSERT INTO TREM VALUES ('T-EXP', 420), ('T-REG', 180);
INSERT INTO TRECHO VALUES (1, 'BH', 'SP', 'EXPRESSA', 'T-EXP'), (2, 'BH', 'RJ', 'REGIONAL', 'T-REG');
""",
        "context_html": """
<p><strong>Regras de Negócio em Rede Ferroviária via SQL-92 <code>CREATE ASSERTION</code>:</strong> As tabelas <code>ESTACAO</code>, <code>TREM(CodTrem, CapMin)</code> e <code>TRECHO(IdTrecho, CodOrig, CodDest, TipoLinha, CodTrem)</code> já estão carregadas.</p>
<p>Escreva <strong>duas declarações <code>CREATE ASSERTION ... CHECK (NOT EXISTS (...));</code></strong> separadas por ponto-e-vírgula:</p>
<ol>
  <li><strong>Proibir Auto-laço:</strong> nenhum <code>TRECHO</code> pode ter <code>CodOrig = CodDest</code>.</li>
  <li><strong>Capacidade Mínima Expressa:</strong> todo <code>TRECHO</code> com <code>TipoLinha = 'EXPRESSA'</code> precisa usar um <code>TREM</code> cuja capacidade <code>CapMin &gt;= 300</code>.</li>
</ol>
""",
        "answer_sheet_html": """
<div class="answer-sheet-box">
  <h4>Gabarito de Referência — R5.5 (Assertions de Rede)</h4>
  <pre class="sql-code">CREATE ASSERTION SEM_AUTOLACO CHECK (
  NOT EXISTS (
    SELECT 1 FROM TRECHO t
    WHERE t.CodOrig = t.CodDest
  )
);

CREATE ASSERTION EXPRESSA_CAPACIDADE CHECK (
  NOT EXISTS (
    SELECT 1 FROM TRECHO t
    JOIN TREM tr ON t.CodTrem = tr.CodTrem
    WHERE t.TipoLinha = 'EXPRESSA' AND tr.CapMin &lt; 300
  )
);</pre>
</div>
""",
        "assertion_tests": [
            {
                "name": "Estado inicial válido (BH->SP com T-EXP de 420 lug., BH->RJ regional)",
                "violation_sql": None,
                "should_pass": True,
                "hint": "O estado inicial respeita ambas as regras."
            },
            {
                "name": "Permitir trecho regional SP->RJ com T-REG (180 lugares)",
                "violation_sql": "INSERT INTO TRECHO VALUES (3, 'SP', 'RJ', 'REGIONAL', 'T-REG');",
                "should_pass": True,
                "hint": "A exigência >= 300 lugares aplica-se apenas a TipoLinha = 'EXPRESSA'."
            },
            {
                "name": "Bloquear auto-laço (trecho BH -> BH)",
                "violation_sql": "INSERT INTO TRECHO VALUES (4, 'BH', 'BH', 'REGIONAL', 'T-REG');",
                "should_pass": False,
                "hint": "Sua primeira asserção precisa detectar CodOrig = CodDest em TRECHO."
            },
            {
                "name": "Bloquear linha EXPRESSA alocando trem pequeno (T-REG com 180 lugares)",
                "violation_sql": "INSERT INTO TRECHO VALUES (5, 'SP', 'RJ', 'EXPRESSA', 'T-REG');",
                "should_pass": False,
                "hint": "Verifique JOIN TRECHO com TREM onde TipoLinha = 'EXPRESSA' AND CapMin < 300."
            }
        ]
    },

    "R5.6": {
        "title": "R5.6 (Oficial/Algoritmo) — Cobertura Mínima Fc em Cascata (2 Estranhos LHS)",
        "type": "oficial",
        "mode": "structured",
        "study_guide": STUDY_GUIDE_G14,
        "context_html": """
<p><strong>Algoritmo Exato de Cobertura Mínima (<code>ibd-parte6.pdf</code> — Seção 3.4):</strong> Dado o esquema <code>R(A, B, C, D, E)</code> e o conjunto não-mínimo de dependências funcionais:</p>
<pre class="sql-code">F = { A &rarr; B,  B &rarr; C,  AB &rarr; D,  BC &rarr; E,  A &rarr; E }</pre>
<p>Execute rigorosamente os <strong>3 passos formais</strong> (Passo 1: RHS simples &bull; Passo 2: eliminação de atributo estranho no LHS &bull; Passo 3: eliminação de DF redundante) e verifique as propriedades de <code>Fc</code>.</p>
""",
        "answer_sheet_html": """
<div class="answer-sheet-box">
  <h4>Gabarito Passo a Passo — R5.6 (Cobertura Mínima Fc)</h4>
  <ol>
    <li><strong>Passo 1 (RHS simples):</strong> Já está unitário: <code>{ A &rarr; B, B &rarr; C, AB &rarr; D, BC &rarr; E, A &rarr; E }</code>.</li>
    <li><strong>Passo 2 (Atributos estranhos no LHS):</strong>
      <ul>
        <li>Em <code>AB &rarr; D</code>: testando sem <code>B</code>, <code>A+ = {A, B, ...}</code> já contém <code>B</code> (via <code>A &rarr; B</code>)! Logo <code>B</code> é estranho &rArr; simplifica para <strong><code>A &rarr; D</code></strong>.</li>
        <li>Em <code>BC &rarr; E</code>: testando sem <code>C</code>, <code>B+ = {B, C, ...}</code> já contém <code>C</code> (via <code>B &rarr; C</code>)! Logo <code>C</code> é estranho &rArr; simplifica para <strong><code>B &rarr; E</code></strong>.</li>
      </ul>
      Conjunto intermediário: <code>{ A &rarr; B, B &rarr; C, A &rarr; D, B &rarr; E, A &rarr; E }</code>.
    </li>
    <li><strong>Passo 3 (DFs redundantes):</strong> Testando <code>A &rarr; E</code> sem ela mesma: <code>A+ = {A, B, D, C, E}</code> (pois <code>A &rarr; B</code> e <code>B &rarr; E</code>!). Logo <code>A &rarr; E</code> é redundante e é removida!</li>
    <li><strong>Resultado Final:</strong> <code>Fc = { A &rarr; B, B &rarr; C, A &rarr; D, B &rarr; E }</code> (ou agrupado: <code>A &rarr; BD</code>, <code>B &rarr; CE</code>).</li>
  </ol>
</div>
""",
        "fields": [
            {
                "id": "f1",
                "label": "1) No Passo 2 (remoção de atributos estranhos do lado esquerdo), como ficam simplificadas AB → D e BC → E?",
                "options": [
                    "AB → D vira A → D (pois A → B elimina B) e BC → E vira B → E (pois B → C elimina C).",
                    "AB → D vira B → D (pois A → B elimina A) e BC → E vira C → E (pois B → C elimina B).",
                    "Nenhuma das duas se altera, pois todos os determinantes compostos precisam permanecer intactos.",
                    "Apenas AB → D reduz para A → D, enquanto BC → E só se reduz após remover A → E no Passo 3."
                ],
                "answer": "AB → D vira A → D (pois A → B elimina B) e BC → E vira B → E (pois B → C elimina C).",
                "explanation": "Em AB -> D, como B ∈ A+, B é estranho; em BC -> E, como C ∈ B+, C é estranho."
            },
            {
                "id": "f2",
                "label": "2) No Passo 3 (após simplificar LHS), qual dependência funcional restante é eliminada por ser redundante?",
                "options": [
                    "B → C, porque pode ser deduzida diretamente a partir da combinação de A → B com A → D.",
                    "A → D, pois a dependência B → E implica transitivamente que A determina D.",
                    "A → E, pois o fecho de A sem ela (via A → B e B → E) já deriva E.",
                    "B → E, pois A → E junto de A → B garante automaticamente que B determine E."
                ],
                "answer": "A → E, pois o fecho de A sem ela (via A → B e B → E) já deriva E.",
                "explanation": "Sem A -> E, o conjunto {A -> B, B -> C, A -> D, B -> E} produz A+ = {A, B, C, D, E}, contendo E! Logo A -> E é redundante."
            },
            {
                "id": "f3",
                "label": "3) Qual afirmação está CORRETA sobre a cobertura mínima final Fc = { A → B, B → C, A → D, B → E } e chaves de R(A,B,C,D,E)?",
                "options": [
                    "Fc possui duas chaves candidatas {A} e {B}, e nenhuma delas consegue determinar D.",
                    "Fc ≡ F, possui chave candidata única {A}, e nenhuma DF restante em Fc é redundante.",
                    "Fc tem menos poder expressivo que F porque eliminou a dependência explícita A → E.",
                    "A tabela sintetizada a partir de Fc exigirá criar uma relação extra para conter a chave {A, E}."
                ],
                "answer": "Fc ≡ F, possui chave candidata única {A}, e nenhuma DF restante em Fc é redundante.",
                "explanation": "A só aparece no LHS e A+ = ABCDE, logo {A} é a chave única; remover uma DF redundante preserva integralmente o fechamento F+ = Fc+."
            }
        ]
    },

    "R5.7": {
        "title": "R5.7 (Lab SQL) — Auditoria de Vendas Fiscais: Qual DF Vale na Extensão?",
        "type": "oficial",
        "mode": "sql_query",
        "study_guide": STUDY_GUIDE_G14,
        "setup": """
CREATE TABLE VENDAS_FISCAL (
  IdItem INTEGER PRIMARY KEY,
  NumNF INTEGER NOT NULL,
  CPFCliente TEXT NOT NULL,
  NomeCliente TEXT NOT NULL,
  CodVendedor TEXT NOT NULL,
  CodProd TEXT NOT NULL,
  Qtd INTEGER NOT NULL
);
INSERT INTO VENDAS_FISCAL VALUES
  (1, 1001, '111', 'Lucas Silva', 'V1', 'P10', 2),
  (2, 1001, '111', 'Lucas Silva', 'V1', 'P20', 1),
  (3, 1002, '222', 'Maria Souza', 'V2', 'P10', 3),
  (4, 1003, '111', 'Lucas Silva', 'V2', 'P30', 1),
  (5, 1004, '333', 'Pedro Lima',  'V3', 'P10', 4),
  (6, 1005, '222', 'Maria Souza', 'V1', 'P40', 2);
""",
        "context_html": """
<p><strong>Auditoria de Regras de Negócio em Vendas (<code>ibd-parte6.pdf</code>):</strong> Analise a tabela populada <code>VENDAS_FISCAL(IdItem, NumNF, CPFCliente, NomeCliente, CodVendedor, CodProd, Qtd)</code>.</p>
<ul>
  <li>Note que <code>NumNF &rarr; CodVendedor</code> e <code>CPFCliente &rarr; NomeCliente</code> valem em todas as linhas.</li>
  <li>Já um gerente supôs que <strong>todo cliente compra sempre com um vendedor fixo</strong> (<code>CPFCliente &rarr; CodVendedor</code>).</li>
</ul>
<p><strong>Sua Tarefa SQL:</strong> Escreva uma consulta que retorne todos os pares distintos (<code>a.IdItem &lt; b.IdItem</code>) provando que <strong><code>CPFCliente &rarr; CodVendedor</code> NÃO vale</strong> na tabela.</p>
<p><strong>Colunas esperadas:</strong> <code>Id1</code>, <code>Id2</code>, <code>CPFCliente</code>, <code>Vend1</code>, <code>Vend2</code>.</p>
""",
        "answer_sheet_html": """
<div class="answer-sheet-box">
  <h4>Gabarito SQL — R5.7</h4>
  <pre class="sql-code">SELECT a.IdItem AS Id1,
       b.IdItem AS Id2,
       a.CPFCliente,
       a.CodVendedor AS Vend1,
       b.CodVendedor AS Vend2
FROM VENDAS_FISCAL a
JOIN VENDAS_FISCAL b
  ON a.CPFCliente = b.CPFCliente
 AND a.CodVendedor &lt;&gt; b.CodVendedor
 AND a.IdItem &lt; b.IdItem;</pre>
  <p>Encontra exatamente os 3 contra-exemplos: Lucas (<code>'111'</code>) em <code>(1, 4)</code> e <code>(2, 4)</code> (comprando com <code>V1</code> e <code>V2</code>), e Maria (<code>'222'</code>) em <code>(3, 6)</code> (comprando com <code>V2</code> e <code>V1</code>).</p>
</div>
""",
        "expected_columns": ["Id1", "Id2", "CPFCliente", "Vend1", "Vend2"],
        "expected_rows": [
            [1, 4, "111", "V1", "V2"],
            [2, 4, "111", "V1", "V2"],
            [3, 6, "222", "V2", "V1"]
        ]
    },

    "R5.8": {
        "title": "R5.8 (Oficial/Clássico) — Ciclo de 4 Chaves Candidatas &amp; Armadilha 2FN/3FN vs BCNF",
        "type": "oficial",
        "mode": "structured",
        "study_guide": STUDY_GUIDE_G14,
        "context_html": """
<p><strong>Problema Clássico de Provas Multicandidatas:</strong> Considere o esquema <code>R(A, B, C, D, E, G)</code> com um ciclo de equivalência funcional combinado a um atributo isolado:</p>
<pre class="sql-code">F = { A &rarr; B,  B &rarr; C,  C &rarr; D,  D &rarr; A,  AE &rarr; G }</pre>
<p>Encontre todas as chaves candidatas e classifique exatamente a maior forma normal satisfeita por <code>R</code> (1FN, 2FN, 3FN ou BCNF), justificando com base na definição de atributo primo.</p>
""",
        "answer_sheet_html": """
<div class="answer-sheet-box">
  <h4>Gabarito Explicado — R5.8 (Ciclo de 4 Chaves)</h4>
  <ul>
    <li><strong>Chaves Candidatas:</strong> Como <code>E</code> nunca aparece no RHS, está em TODA chave. Além disso, <code>A+ = {A, B, C, D}</code>, <code>B+ = {A, B, C, D}</code>, <code>C+ = {A, B, C, D}</code> e <code>D+ = {A, B, C, D}</code>! Logo, qualquer um deles junto com <code>E</code> fecha todos os 6 atributos via <code>AE &rarr; G</code>:<br>
    Chaves Candidatas = <strong><code>{AE, BE, CE, DE}</code></strong> (4 chaves!).</li>
    <li><strong>Primos vs Não-Primos:</strong> Primos = <code>{A, B, C, D, E}</code>; único Não-Primo = <code>{G}</code>.</li>
    <li><strong>Armadilha da Prova:</strong> <code>A &rarr; B</code> (e as demais do ciclo) tem <code>A</code> sendo apenas metade da chave <code>{AE}</code>, <strong>PORÉM <code>B</code> É PRIMO</strong>! Logo <strong>NÃO viola a 2FN nem a 3FN</strong>! O único não-primo (<code>G</code>) depende integralmente da superchave <code>AE</code>. Assim, <code>R</code> já está em <strong>3FN</strong>, violando apenas a <strong>BCNF</strong> (pois <code>A, B, C, D</code> não são superchaves).</li>
  </ul>
</div>
""",
        "fields": [
            {
                "id": "f1",
                "label": "1) Quais são exatamente todas as chaves candidatas de R(A, B, C, D, E, G) sob F?",
                "options": [
                    "Apenas {AE}, pois somente A aparece explicitamente ao lado de E em AE → G.",
                    "Apenas {AE} e {BE}, pois C e D não possuem acesso direto para determinar G.",
                    "{ABCD} e {AE}, porque E só consegue fechar os atributos A, B, C e D por união completa.",
                    "{AE}, {BE}, {CE} e {DE}, pois E é obrigatório e {A, B, C, D} formam um ciclo fechado equivalente."
                ],
                "answer": "{AE}, {BE}, {CE} e {DE}, pois E é obrigatório e {A, B, C, D} formam um ciclo fechado equivalente.",
                "explanation": "A -> B -> C -> D -> A faz A, B, C e D terem exatamente o mesmo fechamento {A,B,C,D}; somando E (que nunca vem no RHS), fecha G via AE -> G."
            },
            {
                "id": "f2",
                "label": "2) Qual é a maior forma normal satisfeita pela relação R(A, B, C, D, E, G)?",
                "options": [
                    "Viola a 2FN (Definição Geral), porque A → B depende apenas de parte da chave {AE}.",
                    "Está em 3FN (viola apenas a BCNF), pois todo atributo à direita nas DFs do ciclo é primo e G depende da chave inteira AE.",
                    "Está em BCNF plena, visto que A, B, C e D pertencem cada um a uma chave candidata distinta.",
                    "Está apenas em 1FN porque o ciclo A → B → C → D → A gera dependência transitiva para o não-primo G."
                ],
                "answer": "Está em 3FN (viola apenas a BCNF), pois todo atributo à direita nas DFs do ciclo é primo e G depende da chave inteira AE.",
                "explanation": "Na 2FN e na 3FN, dependências cujo lado direito é atributo PRIMO (A, B, C, D) são permitidas! Somente a BCNF exige superchave no LHS sem exceções."
            },
            {
                "id": "f3",
                "label": "3) Quantos e quais atributos de R são classificados como NÃO-PRIMOS?",
                "options": [
                    "Apenas 1 atributo não-primo: {G}, visto que A, B, C, D e E participam das 4 chaves candidatas.",
                    "3 atributos não-primos: {B, C, D}, porque são derivados transitivamente de A.",
                    "4 atributos não-primos: {B, C, D, G}, considerando apenas {AE} como chave principal escolhida.",
                    "Nenhum atributo é não-primo, pois todos os 6 atributos pertencem a pelo menos uma chave."
                ],
                "answer": "Apenas 1 atributo não-primo: {G}, visto que A, B, C, D e E participam das 4 chaves candidatas.",
                "explanation": "Atributo primo é qualquer atributo que pertença a AO MENOS UMA chave candidata: {AE} ∪ {BE} ∪ {CE} ∪ {DE} = {A, B, C, D, E}."
            }
        ]
    },

    "R5.9": {
        "title": "R5.9 (Aberta Estilo E8.3) — Decomposição Completa 1FN &rarr; 3FN (Clínica de Exames)",
        "type": "oficial",
        "mode": "open_design",
        "study_guide": STUDY_GUIDE_G14,
        "context_html": """
<p><strong>Questão Discursiva Completa Estilo <code>E8.3</code> (<code>ExerciciosNormalizacaoSemResposta.pdf</code>):</strong><br>
Normalize em seu caderno passo a passo (<strong>1FN &rarr; 2FN &rarr; 3FN</strong>) a ficha bruta de atendimento diagnóstico abaixo, destacando <strong>PKs, FKs e as DFs causadoras de cada violação</strong>:</p>
<pre class="sql-code">GUIA_EXAMES(<u>NumGuia</u>, DataGuia, CPFPac, NomePac, CodConv, NomeConv,
  { ExamesSolicitados(<u>CodExame</u>, NomeExame, CodSetor, NomeSetor, PrepJejumHoras, Resultado) })</pre>
<p><strong>Regras de domínio:</strong> Uma guia lista vários exames distintos (grupo repetitivo); cada guia pertence a um paciente (<code>NumGuia &rarr; DataGuia, CPFPac</code>) e cada paciente possui um convênio principal (<code>CPFPac &rarr; NomePac, CodConv</code>, onde <code>CodConv &rarr; NomeConv</code>); cada <code>CodExame</code> pertence a um setor fixo (<code>CodExame &rarr; NomeExame, PrepJejumHoras, CodSetor</code> e <code>CodSetor &rarr; NomeSetor</code>); o <code>Resultado</code> depende de <code>(NumGuia, CodExame)</code>.</p>
""",
        "answer_sheet_html": """
<div class="answer-sheet-box">
  <h4>Gabarito Passo a Passo (1FN &rarr; 2FN &rarr; 3FN) — R5.9</h4>
  <ol>
    <li><strong>1FN (Desaninhamento do grupo repetitivo <code>ExamesSolicitados</code>):</strong><br>
    <code>GUIA_1FN(<u>NumGuia</u>, DataGuia, CPFPac, NomePac, CodConv, NomeConv)</code><br>
    <code>ITEM_GUIA_1FN(<u>NumGuia</u>, <u>CodExame</u>, NomeExame, CodSetor, NomeSetor, PrepJejumHoras, Resultado)</code></li>
    <li><strong>2FN (Eliminar parcial <code>CodExame &rarr; NomeExame, CodSetor, NomeSetor, PrepJejumHoras</code> em <code>ITEM_GUIA_1FN</code>):</strong><br>
    <code>GUIA_2FN(<u>NumGuia</u>, DataGuia, CPFPac, NomePac, CodConv, NomeConv)</code><br>
    <code>ITEM_2FN(<u>NumGuia</u>, <u>CodExame</u>, Resultado)</code> (já em 3FN/BCNF!)<br>
    <code>EXAME_2FN(<u>CodExame</u>, NomeExame, PrepJejumHoras, CodSetor, NomeSetor)</code></li>
    <li><strong>3FN (Eliminar transitivas <code>NumGuia &rarr; CPFPac &rarr; NomePac, CodConv &rarr; NomeConv</code> e <code>CodExame &rarr; CodSetor &rarr; NomeSetor</code>):</strong><br>
    <code>CONVENIO(<u>CodConv</u>, NomeConv)</code><br>
    <code>PACIENTE(<u>CPFPac</u>, NomePac, CodConv)</code> [FK: CodConv]<br>
    <code>GUIA(<u>NumGuia</u>, DataGuia, CPFPac)</code> [FK: CPFPac]<br>
    <code>SETOR(<u>CodSetor</u>, NomeSetor)</code><br>
    <code>EXAME(<u>CodExame</u>, NomeExame, PrepJejumHoras, CodSetor)</code> [FK: CodSetor]<br>
    <code>ITEM_GUIA(<u>NumGuia</u>, <u>CodExame</u>, Resultado)</code> [FKs: NumGuia, CodExame]</li>
  </ol>
  <p>Todas as 6 tabelas finais possuem junção sem perda, preservam todas as DFs e satisfazem <strong>3FN e BCNF</strong>!</p>
</div>
""",
        "fields": []
    },

    "R5.10": {
        "title": "R5.10 (Orquestra Final) — Checklist Cirúrgico Pré-Prova (Módulos 7 &amp; 8)",
        "type": "oficial",
        "mode": "structured",
        "study_guide": STUDY_GUIDE_G14,
        "context_html": """
<p><strong>Revisão Final Consolidada (Armadilhas Clássicas dos Módulos 7 e 8):</strong> Antes de fechar sua preparação para a prova, valide os três pontos de decisão mais críticos cobrados pela banca da UFMG.</p>
""",
        "answer_sheet_html": """
<div class="answer-sheet-box">
  <h4>Gabarito Final Consolidado — R5.10</h4>
  <ul>
    <li><strong>Ponto 1 (M7 — RIR <code>-n-&gt;</code>):</strong> Só pode existir quando a coluna FK admite <code>NULL</code> (participação parcial). Jamais pode ser usada em PK composta (entidade fraca, multivalorado, <code>M:N</code>) ou em FK <code>NOT NULL</code> de participação total <code>(1,1)</code>.</li>
    <li><strong>Ponto 2 (M8 — 3FN vs BCNF):</strong> Toda relação pode ser decomposta sem perda em <strong>BCNF</strong> e sem perda em <strong>3FN</strong>; porém a <strong>3FN garante preservação de dependências</strong> enquanto a <strong>BCNF às vezes sacrifica a preservação</strong> (ex.: quando existe <code>X &rarr; A</code> com <code>X</code> não-superchave e <code>A</code> primo).</li>
    <li><strong>Ponto 3 (M8 — NJP em 3+ Tabelas):</strong> Para uma decomposição sequencial <code>R &rarr; {R1, R2}</code> e depois <code>R2 &rarr; {R2a, R2b}</code> ser sem perda, <strong>ambas as divisões binárias</strong> devem satisfazer o critério de superchave na interseção!</li>
  </ul>
</div>
""",
        "fields": [
            {
                "id": "f1",
                "label": "1) Em qual das situações abaixo a política de integridade referencial -n-> (ON DELETE SET NULL) é TECNICAMENTE IMPOSSÍVEL?",
                "options": [
                    "Num relacionamento 1:N onde a entidade filha participa com cardinalidade mínima zero (0,1) do lado N.",
                    "Na FK herdada por uma Entidade Fraca ou tabela associativa M:N onde a FK compõe a chave primária.",
                    "Num auto-relacionamento 1:N onde o atributo SupervisorCPF aceita NULL para o presidente da empresa.",
                    "Num relacionamento 1:1 onde o lado parcial guarda opcionalmente a chave alternativa UNIQUE anulável."
                ],
                "answer": "Na FK herdada por uma Entidade Fraca ou tabela associativa M:N onde a FK compõe a chave primária.",
                "explanation": "Chaves primárias (inclusive parciais/compostas em fracas e M:N) têm restrição NOT NULL obrigatória; logo -n-> (SET NULL) é proibido e deve-se usar -p-> ou -b->."
            },
            {
                "id": "f2",
                "label": "2) Qual afirmação resume com precisão rigorosa a diferença entre 3FN e BCNF no projeto relacional?",
                "options": [
                    "A 3FN sempre permite atingir junção sem perda e preservação de DFs; a BCNF elimina toda redundância de DF, mas pode perder preservação.",
                    "A BCNF é menos restritiva que a 3FN porque aceita que atributos não-primos determinem atributos primos.",
                    "A 3FN nunca garante junção sem perda quando se usa o algoritmo de síntese a partir da cobertura mínima.",
                    "Toda relação em 3FN já está automaticamente em BCNF sempre que possuir pelo menos uma chave candidata composta."
                ],
                "answer": "A 3FN sempre permite atingir junção sem perda e preservação de DFs; a BCNF elimina toda redundância de DF, mas pode perder preservação.",
                "explanation": "O algoritmo de Síntese 3FN sempre alcança Sem Perda + Preservação de DFs + 3FN. Já decomposições BCNF sempre alcançam Sem Perda + BCNF, podendo sacrificar a preservação."
            },
            {
                "id": "f3",
                "label": "3) Para auditar rapidamente uma decomposição em etapas R → {R1, R2} seguida de R2 → {R2a, R2b}, o que garante Junção Sem Perda global?",
                "options": [
                    "Basta que R1 e R2a compartilhem ao menos um atributo qualquer em comum, mesmo não sendo superchave.",
                    "Basta que a soma de todos os atributos das três tabelas contenha os atributos da relação original R.",
                    "Cada divisão binária na árvore (R1 ∩ R2 e R2a ∩ R2b) precisa ser superchave de pelo menos um dos dois lados divididos.",
                    "É necessário que todas as três tabelas finais R1, R2a e R2b compartilhem exatamente a mesma chave primária."
                ],
                "answer": "Cada divisão binária na árvore (R1 ∩ R2 e R2a ∩ R2b) precisa ser superchave de pelo menos um dos dois lados divididos.",
                "explanation": "A propriedade de junção sem perda (NJP) é associativa em árvore de decomposição binária: se cada passo (R -> R1, R2 e R2 -> R2a, R2b) for sem perda, a junção total R1 ⋈ R2a ⋈ R2b recupera R sem tuplas espúrias."
            }
        ]
    }
}
