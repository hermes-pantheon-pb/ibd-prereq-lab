# -*- coding: utf-8 -*-
"""
Banco de Exercícios Oficial / Estilo Prova — Rodada 4 (Módulos 7 e 8)
Foco de alta incidência nas provas da UFMG (ibd-parte5.pdf e ibd-parte6.pdf):
  - Grupo 11 (R4.1–R4.5): Opções 1/2/3 de Hierarquias & AR, SQL DDL com CHECK + SET NULL (-n->),
    Ternário M:N:1, Esquema Lógico Completo estilo Lista Oficial (open_design) e ASSERTION de Equações AR.
  - Grupo 12 (R4.6–R4.10): Auditoria SQL de DFs em instância, Axiomas de Armstrong & Equivalência F ≡ G,
    Particionamento Esquerda/Meio/Direita para Chaves, 1FN->2FN->3FN Completo (open_design) e Bateria de Anomalias.
"""

# ---------------------------------------------------------------------------
# Fichas de Estudo (Study Guides G11 & G12 — domínios paralelos aos exercícios)
# ---------------------------------------------------------------------------

STUDY_GUIDE_G11 = {
    "id": "G11",
    "title": "G11 — Opções EER (1/2/3 & AR), Ternário M:N:1 e RIRs (-n- / -b- / -p-)",
    "file_path": "study_guides/G11_M7_Hierarquias8B_TernarioMN1_e_RIRs.md",
    "coursework_ref": "ibd-parte5.pdf (Etapas 1–2: Opções de Hierarquias, Fórmulas AR, Ternário com lado 1 e RIRs b/p/n)",
    "quick_rules_html": """
<div class="sg-rules-box">
  <h4>Resumo Operacional — Rodada 4 (Grupo G11)</h4>
  <ul>
    <li><strong>Comparação das 3 Opções de Hierarquia (<code>ibd-parte5.pdf</code>):</strong>
      <ul>
        <li><strong>Opção 1 (1-1):</strong> Superclasse + Subclasses; aceita qualquer <code>{d/o, total/parcial}</code>.</li>
        <li><strong>Opção 2 (Tabela Única):</strong> Colapsa tudo numa tabela; exige <code>CHECK</code> XOR para <code>{d, total}</code> e gera <code>NULL</code>s.</li>
        <li><strong>Opção 3 (Somente Subclasses / 8B):</strong> Só é válida quando a especialização for <strong>total</strong> (e idealmente disjunta <code>d</code>).</li>
      </ul>
    </li>
    <li><strong>Ternário com Lado 1 (<code>M:N:1</code>):</strong> Quando um par <code>(A, B)</code> se liga a no máximo <code>1</code> elemento de <code>C</code>, a PK da tabela do relacionamento é formada apenas pelos lados muitos: <code>(<u>PK_A</u>, <u>PK_B</u>, FK_C)</code>!</li>
    <li><strong>Política <code>-n-&gt;</code> (<code>SET NULL</code>):</strong> Só pode ser usada quando a FK pertence a relacionamento com participação <strong>parcial</strong> (<code>(0,1)</code> ou <code>(0,N)</code>), pois a coluna da FK precisa aceitar <code>NULL</code>.</li>
  </ul>
</div>
""",
    "example_html": """
<div class="sg-example-box">
  <h4>Exemplos Análogos (Domínios Diferentes da Tarefa)</h4>
  <p><strong>1. Hierarquia <code>{d, total}</code> em Tabela Única (Passagem Rodoviária):</strong></p>
  <pre class="sql-code">CREATE TABLE PASSAGEM (
  CodBilhete INTEGER PRIMARY KEY,
  Poltrona   TEXT,    -- apenas CONVENCIONAL
  TaxaLencol REAL,    -- apenas LEITO
  CHECK ((Poltrona IS NOT NULL AND TaxaLencol IS NULL)
      OR (Poltrona IS NULL AND TaxaLencol IS NOT NULL))
);</pre>
  <p><strong>2. Ternário <code>CONSULTA_VET(Pet, Especialidade, Veterinario)</code> com lado 1:</strong> Se todo par <code>(Pet, Especialidade)</code> é atendido por um único <code>Veterinario</code> fixo, mapeia-se <code>CONSULTA_VET(<u>IdPet</u>, <u>CodEsp</u>, CRM_Vet)</code>.</p>
  <p><strong>3. Equação AR &rarr; <code>CREATE ASSERTION</code> (<code>CLINICA</code> &rarr; <code>INTERNADO</code>/<code>AMBULATORIAL</code>):</strong> <code>&pi;_PK(INTERNADO) &cap; &pi;_PK(AMBULATORIAL) = &empty;</code> traduz para <code>NOT EXISTS (SELECT 1 FROM INTERNADO i JOIN AMBULATORIAL a ON i.Id = a.Id)</code>.</p>
</div>
"""
}

STUDY_GUIDE_G12 = {
    "id": "G12",
    "title": "G12 — Armstrong, Equivalência F ≡ G, Particionamento de Chaves &amp; 1FN–3FN",
    "file_path": "study_guides/G12_M8_Armstrong_Equivalencia_Particionamento_1a3FN.md",
    "coursework_ref": "ibd-parte6.pdf (Anomalias, DFs em Instâncias, Armstrong, Equivalência, Método de Particionamento e 1FN–3FN)",
    "quick_rules_html": """
<div class="sg-rules-box">
  <h4>Resumo Operacional — Rodada 4 (Grupo G12)</h4>
  <ul>
    <li><strong>Equivalência <code>F &equiv; G</code>:</strong> Teste se cada <code>X &rarr; Y &isin; G</code> pertence a <code>(X)+</code> sob <code>F</code> (<code>F</code> cobre <code>G</code>) <strong>E</strong> se cada <code>U &rarr; V &isin; F</code> pertence a <code>(U)+</code> sob <code>G</code> (<code>G</code> cobre <code>F</code>).</li>
    <li><strong>Particionamento em 3 Conjuntos para Chaves Candidatas:</strong>
      <ul>
        <li><code>Somente Esquerda (L)</code>: Obrigatório em <strong>toda</strong> chave candidata.</li>
        <li><code>Somente Direita (R)</code>: <strong>Nunca</strong> participa de nenhuma chave candidata mínima.</li>
        <li><code>Meio (M)</code>: Combine com <code>L</code> apenas se <code>L+ &ne; TodosAtributos</code>.</li>
      </ul>
    </li>
    <li><strong>As 3 Anomalias de Projeto:</strong> Inserção (não cadastrar fato independente sem o dependente), Remoção (apagar último filho apaga dados do pai) e Modificação (atualização parcial gera inconsistência).</li>
  </ul>
</div>
""",
    "example_html": """
<div class="sg-example-box">
  <h4>Exemplos Análogos: Equivalência &amp; Esquema Abstrato <code>S(P, Q, R, T, U, W)</code></h4>
  <p><strong>Equivalência (direção única):</strong> Para <code>F1 = { P &rarr; Q, Q &rarr; R }</code> e <code>F2 = { P &rarr; QR }</code>, temos <code>P+<sub>F1</sub> = {P,Q,R}</code> (<code>F1</code> cobre <code>F2</code>), porém <code>Q+<sub>F2</sub> = {Q}</code> (<code>F2</code> NÃO cobre <code>Q &rarr; R</code>). Logo <code>F1 &nequiv; F2</code>!</p>
  <p><strong>Chaves por Particionamento em <code>S(P, Q, R, T, U, W)</code> com <code>{ PQ &rarr; R, R &rarr; T, T &rarr; Q, T &rarr; U, U &rarr; W }</code>:</strong></p>
  <ul>
    <li><code>L = {P}</code> (obrigatório), <code>R = {W}</code> (nunca na chave), <code>M = {Q, R, T, U}</code>.</li>
    <li><code>(PQ)+ = {P,Q,R,T,U,W}</code>, <code>(PR)+ = S</code>, <code>(PT)+ = S</code> &rarr; chaves = <code>{PQ, PR, PT}</code>. Nota: <code>(PU)+ = {P,U,W}</code> (não é chave!).</li>
    <li>Como <code>R &rarr; U</code> usa subconjunto próprio de <code>{PR}</code> para o não-primo <code>U</code>, viola a <strong>2FN (Definição Geral)</strong>.</li>
  </ul>
</div>
"""
}


# ---------------------------------------------------------------------------
# Dicionário Principal de Exercícios da Rodada 4 (R4.1 .. R4.10)
# ---------------------------------------------------------------------------

ROUND4_EXERCISES = {
    "R4.1": {
        "title": "R4.1 (Oficial/EER) — Opções 1/2/3 de Hierarquias &amp; Álgebra Relacional (Cinemateca)",
        "type": "oficial",
        "mode": "structured",
        "study_guide": STUDY_GUIDE_G11,
        "context_html": """
<p><strong>Questão Clássica de Prova (<code>ibd-parte5.pdf</code> — Regras 6 e 7):</strong> Considere as duas hierarquias abaixo de uma plataforma de catálogo audiovisual:</p>
<div style="text-align:center; margin: 12px 0;">
<svg viewBox="0 0 760 190" width="100%" style="max-width:740px; background:#0d1117; border:1px solid #30363d; border-radius:8px;">
  <!-- Hierarchy 1: MIDIA -> {FILME, SERIE} {d, total} -->
  <rect x="85" y="16" width="175" height="42" rx="4" fill="#161b22" stroke="#58a6ff" stroke-width="2"/>
  <text x="172" y="34" text-anchor="middle" fill="#f0f6fc" font-size="11" font-weight="700">MIDIA</text>
  <text x="172" y="49" text-anchor="middle" fill="#8b949e" font-size="9">(<u>CodMidia</u>, Titulo, Ano)</text>
  <!-- Double line total + d -->
  <line x1="169" y1="58" x2="169" y2="82" stroke="#f2cc60" stroke-width="1.6"/>
  <line x1="175" y1="58" x2="175" y2="82" stroke="#f2cc60" stroke-width="1.6"/>
  <circle cx="172" cy="96" r="13" fill="#161b22" stroke="#f2cc60" stroke-width="2"/>
  <text x="172" y="100" text-anchor="middle" fill="#f2cc60" font-size="11" font-weight="700">d</text>
  <line x1="160" y1="103" x2="95" y2="128" stroke="#8b949e" stroke-width="1.5"/>
  <line x1="184" y1="103" x2="250" y2="128" stroke="#8b949e" stroke-width="1.5"/>
  <rect x="20" y="128" width="142" height="42" rx="4" fill="#161b22" stroke="#3fb950" stroke-width="1.8"/>
  <text x="91" y="147" text-anchor="middle" fill="#f0f6fc" font-size="11" font-weight="700">FILME</text>
  <text x="91" y="161" text-anchor="middle" fill="#8b949e" font-size="9">(DuracaoMin)</text>
  <rect x="182" y="128" width="142" height="42" rx="4" fill="#161b22" stroke="#3fb950" stroke-width="1.8"/>
  <text x="253" y="147" text-anchor="middle" fill="#f0f6fc" font-size="11" font-weight="700">SERIE</text>
  <text x="253" y="161" text-anchor="middle" fill="#8b949e" font-size="9">(NumTemporadas)</text>

  <line x1="380" y1="15" x2="380" y2="175" stroke="#30363d" stroke-dasharray="5,5"/>

  <!-- Hierarchy 2: COLABORADOR -> {DIRETOR, ROTEIRISTA} {o, parcial} -->
  <rect x="480" y="16" width="185" height="42" rx="4" fill="#161b22" stroke="#58a6ff" stroke-width="2"/>
  <text x="572" y="34" text-anchor="middle" fill="#f0f6fc" font-size="11" font-weight="700">COLABORADOR</text>
  <text x="572" y="49" text-anchor="middle" fill="#8b949e" font-size="9">(<u>CPF</u>, Nome, Pais)</text>
  <!-- Single line partial + o -->
  <line x1="572" y1="58" x2="572" y2="82" stroke="#8b949e" stroke-width="1.6"/>
  <circle cx="572" cy="96" r="13" fill="#161b22" stroke="#d2a8ff" stroke-width="2"/>
  <text x="572" y="100" text-anchor="middle" fill="#d2a8ff" font-size="11" font-weight="700">o</text>
  <line x1="560" y1="103" x2="490" y2="128" stroke="#8b949e" stroke-width="1.5"/>
  <line x1="584" y1="103" x2="655" y2="128" stroke="#8b949e" stroke-width="1.5"/>
  <rect x="415" y="128" width="146" height="42" rx="4" fill="#161b22" stroke="#d2a8ff" stroke-width="1.8"/>
  <text x="488" y="147" text-anchor="middle" fill="#f0f6fc" font-size="11" font-weight="700">DIRETOR</text>
  <text x="488" y="161" text-anchor="middle" fill="#8b949e" font-size="9">(EstiloVisual)</text>
  <rect x="582" y="128" width="152" height="42" rx="4" fill="#161b22" stroke="#d2a8ff" stroke-width="1.8"/>
  <text x="658" y="147" text-anchor="middle" fill="#f0f6fc" font-size="11" font-weight="700">ROTEIRISTA</text>
  <text x="658" y="161" text-anchor="middle" fill="#8b949e" font-size="9">(NumRoteiros)</text>
</svg>
</div>
<p>Avalie a validade da <strong>Opção 3 (Somente Subclasses / 8B)</strong>, da <strong>Opção 2 (Tabela Única)</strong> e das fórmulas de <strong>Álgebra Relacional</strong> dos slides de <code>ibd-parte5.pdf</code>.</p>
""",
        "answer_sheet_html": """
<div class="answer-sheet-box">
  <h4>Gabarito Explicado — R4.1 (Opções de Hierarquia &amp; AR)</h4>
  <ul>
    <li><strong><code>MIDIA &rarr; {FILME, SERIE} {d, total}</code>:</strong> Como é <strong>total e disjunta</strong>, a <strong>Opção 3 (Somente Subclasses: <code>FILME(<u>CodMidia</u>, Titulo, Ano, DuracaoMin)</code> e <code>SERIE(<u>CodMidia</u>, Titulo, Ano, NumTemporadas)</code>)</strong> funciona sem duplicação de tuplas e sem gerar nenhum <code>NULL</code>! Se fosse mapeada na Opção 2 (Tabela Única <code>MIDIA</code>), a restrição de disjunção em Álgebra Relacional seria <code>&pi;_CodMidia(&sigma;_{DuracaoMin &ne; null}(MIDIA)) &cap; &pi;_CodMidia(&sigma;_{NumTemporadas &ne; null}(MIDIA)) = &empty;</code>.</li>
    <li><strong><code>COLABORADOR &rarr; {DIRETOR, ROTEIRISTA} {o, parcial}</code>:</strong> A Opção 3 é <strong>proibida/inválida</strong> porque a participação é <strong>parcial</strong> (um editor de áudio ou ator cadastrado só em <code>COLABORADOR</code> sumiria do banco!), além da sobreposição duplicar <code>Nome</code> e <code>Pais</code> em diretores que também escrevem roteiros.</li>
  </ul>
</div>
""",
        "fields": [
            {
                "id": "f1",
                "label": "1) Por que a Opção 3 (Somente Subclasses / 8B) é adequada em MIDIA, mas INVIÁVEL em COLABORADOR?",
                "options": [
                    "Porque MIDIA possui menos atributos comuns e COLABORADOR tem chave primária textual (CPF).",
                    "Porque MIDIA é {d, total} (sem perda nem duplicação), enquanto COLABORADOR é parcial (perderia quem não é diretor nem roteirista).",
                    "Porque a Opção 3 exige obrigatoriamente que a especialização seja sobreposta 'o' para evitar NULLs.",
                    "Porque COLABORADOR não pode ser mapeado pela Opção 1 nem pela Opção 2 no modelo relacional."
                ],
                "answer": "Porque MIDIA é {d, total} (sem perda nem duplicação), enquanto COLABORADOR é parcial (perderia quem não é diretor nem roteirista).",
                "explanation": "Na Opção 3 (8B), a tabela da superclasse desaparece. Em especialização parcial, instâncias que pertencem apenas à superclasse ficariam sem lugar para serem armazenadas."
            },
            {
                "id": "f2",
                "label": "2) Se MIDIA for mapeada pela Opção 2 (Tabela Única MIDIA(CodMidia, Titulo, Ano, DuracaoMin, NumTemporadas)), qual expressão em Álgebra Relacional garante a disjunção (d)?",
                "options": [
                    "π_CodMidia(σ_{DuracaoMin ≠ null}(MIDIA)) ∪ π_CodMidia(σ_{NumTemporadas ≠ null}(MIDIA)) = π_CodMidia(MIDIA)",
                    "π_CodMidia(FILME) - π_CodMidia(SERIE) = π_CodMidia(MIDIA)",
                    "π_CodMidia(σ_{DuracaoMin = null}(MIDIA)) ∩ π_CodMidia(σ_{NumTemporadas = null}(MIDIA)) = π_CodMidia(MIDIA)",
                    "π_CodMidia(σ_{DuracaoMin ≠ null}(MIDIA)) ∩ π_CodMidia(σ_{NumTemporadas ≠ null}(MIDIA)) = ∅"
                ],
                "answer": "π_CodMidia(σ_{DuracaoMin ≠ null}(MIDIA)) ∩ π_CodMidia(σ_{NumTemporadas ≠ null}(MIDIA)) = ∅",
                "explanation": "A interseção dos códigos onde DuracaoMin não é nulo com os códigos onde NumTemporadas não é nulo deve ser vazia (= ∅) para impedir que uma mídia seja Filme e Série ao mesmo tempo."
            },
            {
                "id": "f3",
                "label": "3) Caso a tabela MIDIA tivesse 8 atributos específicos exclusivos de FILME e 8 de SERIE, qual vantagem prática teria a Opção 1 (1-1) sobre a Opção 2 (Tabela Única)?",
                "options": [
                    "Eliminaria valores NULL em massa nas tuplas, mantendo cada tabela apenas com os atributos daquela subclasse.",
                    "Dispensaria qualquer uso de JOIN ao consultar simultaneamente Titulo e DuracaoMin de todos os filmes.",
                    "Garantiria automaticamente a totalidade e a disjunção sem precisar de assertions nem triggers SQL.",
                    "Permitiria remover a chave primária CodMidia das tabelas FILME e SERIE para economizar espaço em disco."
                ],
                "answer": "Eliminaria valores NULL em massa nas tuplas, mantendo cada tabela apenas com os atributos daquela subclasse.",
                "explanation": "Com muitos atributos exclusivos nas subclasses, a Opção 2 deixa metade da tupla nula em cada registro; a Opção 1 (1-1) separa em tabelas enxutas sem NULLs estruturais."
            }
        ]
    },

    "R4.2": {
        "title": "R4.2 (Lab SQL DDL) — Tabela Única {d, total} (CHECK) &amp; Participação Parcial (-n-&gt; SET NULL)",
        "type": "oficial",
        "mode": "sql_ddl",
        "study_guide": STUDY_GUIDE_G11,
        "setup": "",
        "context_html": """
<p><strong>Prática DDL Estilo Prova UFMG (<code>ibd-parte5.pdf</code>):</strong> Modele em SQLite DDL o esquema de uma locadora de veículos combinando dois padrões de alta incidência em provas:</p>
<ol>
  <li><strong>Tabela <code>INSPETOR</code>:</strong> <code>CodInsp INTEGER PRIMARY KEY</code>, <code>Nome TEXT NOT NULL</code>.</li>
  <li><strong>Tabela <code>VEICULO</code> (Opção 2 — Tabela Única para especialização <code>{d, total}</code> em <code>PASSEIO</code> ou <code>UTILITARIO</code>):</strong>
    <ul>
      <li><code>Placa TEXT PRIMARY KEY</code>, <code>Modelo TEXT NOT NULL</code></li>
      <li><code>NumPortas INTEGER</code> (atributo exclusivo de <code>PASSEIO</code>; nulo em utilitário)</li>
      <li><code>CargaMaxKg REAL</code> (atributo exclusivo de <code>UTILITARIO</code>; nulo em passeio)</li>
      <li><code>CodInsp INTEGER</code> &mdash; relacionamento <code>N:1</code> <strong>parcial</strong> (<code>(0,1)</code>, nem todo veículo já passou por vistoria) referenciando <code>INSPETOR(CodInsp)</code> com política <strong><code>-n-&gt;</code> (<code>ON DELETE SET NULL</code>)</strong>!</li>
      <li>Cláusula <strong><code>CHECK</code></strong> garantindo disjunção + totalidade: exatamente um dos dois atributos (<code>NumPortas</code> ou <code>CargaMaxKg</code>) deve ser <code>NOT NULL</code>!</li>
    </ul>
  </li>
</ol>
""",
        "answer_sheet_html": """
<div class="answer-sheet-box">
  <h4>Gabarito DDL de Referência — R4.2</h4>
  <pre class="sql-code">CREATE TABLE INSPETOR (
  CodInsp INTEGER PRIMARY KEY,
  Nome    TEXT NOT NULL
);

CREATE TABLE VEICULO (
  Placa      TEXT PRIMARY KEY,
  Modelo     TEXT NOT NULL,
  NumPortas  INTEGER,
  CargaMaxKg REAL,
  CodInsp    INTEGER,
  FOREIGN KEY (CodInsp) REFERENCES INSPETOR(CodInsp) ON DELETE SET NULL,
  CHECK (
    (NumPortas IS NOT NULL AND CargaMaxKg IS NULL) OR
    (NumPortas IS NULL AND CargaMaxKg IS NOT NULL)
  )
);</pre>
</div>
""",
        "ddl_tests": [
            {
                "name": "Existência das tabelas INSPETOR e VEICULO",
                "type": "tables_exist",
                "tables": ["INSPETOR", "VEICULO"],
                "hint": "Crie exatamente as tabelas INSPETOR e VEICULO."
            },
            {
                "name": "Aceitar veículo de passeio com inspetor, utilitário sem inspetor e validar totalidade",
                "type": "must_succeed",
                "sql": """
                    INSERT INTO INSPETOR VALUES (1, 'Carlos');
                    INSERT INTO VEICULO VALUES ('ABC1234', 'Hatch', 4, NULL, 1);
                    INSERT INTO VEICULO VALUES ('XYZ9876', 'Furgão', NULL, 1500.0, NULL);
                """,
                "hint": "CodInsp deve aceitar NULL (participação parcial), e exatamente um entre NumPortas e CargaMaxKg deve estar preenchido."
            },
            {
                "name": "Bloquear veículo que viola disjunção (ambos NumPortas e CargaMaxKg preenchidos)",
                "type": "must_fail",
                "sql": "INSERT INTO VEICULO VALUES ('DUP0001', 'Híbrido', 4, 800.0, NULL);",
                "hint": "Adicione CHECK garantindo XOR entre NumPortas IS NOT NULL e CargaMaxKg IS NOT NULL."
            },
            {
                "name": "Bloquear veículo que viola totalidade (ambos NumPortas e CargaMaxKg nulos)",
                "type": "must_fail",
                "sql": "INSERT INTO VEICULO VALUES ('NUL0002', 'Indefinido', NULL, NULL, NULL);",
                "hint": "Em especialização total {d, total}, nenhum veículo pode ficar sem nenhum atributo de subclasse preenchido."
            },
            {
                "name": "Política -n-> (ON DELETE SET NULL): apagar inspetor preserva veículo com CodInsp = NULL",
                "type": "cascade_check",
                "sql_setup": """
                    INSERT INTO INSPETOR VALUES (10, 'Mariana');
                    INSERT INTO VEICULO VALUES ('MOT1111', 'Sedan', 4, NULL, 10);
                    DELETE FROM INSPETOR WHERE CodInsp = 10;
                """,
                "verify_query": "SELECT COUNT(*) FROM VEICULO WHERE Placa = 'MOT1111' AND CodInsp IS NULL;",
                "expected_scalar": 1,
                "hint": "Use FOREIGN KEY (CodInsp) REFERENCES INSPETOR(CodInsp) ON DELETE SET NULL."
            }
        ]
    },

    "R4.3": {
        "title": "R4.3 (Oficial/Armadilha) — Ternário com Lado 1 (M:N:1) &amp; Escolha de RIRs (-b/-p/-n)",
        "type": "oficial",
        "mode": "structured",
        "study_guide": STUDY_GUIDE_G11,
        "context_html": """
<p><strong>Padrão Elmasri / Provas de Projeto Lógico:</strong> Analise o diagrama ER do programa de estágios abaixo com atenção máxima às cardinalidades do relacionamento ternário <code>ORIENTA_ESTAGIO</code> e das associações binárias:</p>
<div style="text-align:center; margin: 10px 0;">
<svg viewBox="0 0 760 220" width="100%" style="max-width:740px; background:#0d1117; border:1px solid #30363d; border-radius:8px;">
  <rect x="24" y="25" width="145" height="44" rx="4" fill="#161b22" stroke="#58a6ff" stroke-width="2"/>
  <text x="96" y="44" text-anchor="middle" fill="#f0f6fc" font-size="11" font-weight="700">ALUNO</text>
  <text x="96" y="59" text-anchor="middle" fill="#8b949e" font-size="9">(<u>Matr</u>, Nome)</text>

  <rect x="580" y="25" width="155" height="44" rx="4" fill="#161b22" stroke="#58a6ff" stroke-width="2"/>
  <text x="657" y="44" text-anchor="middle" fill="#f0f6fc" font-size="11" font-weight="700">EMPRESA</text>
  <text x="657" y="59" text-anchor="middle" fill="#8b949e" font-size="9">(<u>CNPJ</u>, RazaoSoc)</text>

  <!-- Diamond ORIENTA_ESTAGIO -->
  <polygon points="325,52 380,20 435,52 380,84" fill="#1f2937" stroke="#f2cc60" stroke-width="2"/>
  <text x="380" y="56" text-anchor="middle" fill="#f2cc60" font-size="10" font-weight="700">ESTAGIO</text>
  <text x="380" y="102" text-anchor="middle" fill="#e6edf3" font-size="9">Attr: CargaSemanal</text>

  <line x1="169" y1="47" x2="325" y2="52" stroke="#8b949e" stroke-width="1.6"/>
  <text x="245" y="40" text-anchor="middle" fill="#79c0ff" font-size="11" font-weight="700">N</text>
  <line x1="435" y1="52" x2="580" y2="47" stroke="#8b949e" stroke-width="1.6"/>
  <text x="508" y="40" text-anchor="middle" fill="#79c0ff" font-size="11" font-weight="700">M</text>

  <line x1="380" y1="84" x2="380" y2="148" stroke="#8b949e" stroke-width="1.6"/>
  <text x="396" y="128" text-anchor="middle" fill="#ffa657" font-size="12" font-weight="700">1</text>

  <rect x="290" y="148" width="180" height="44" rx="4" fill="#161b22" stroke="#3fb950" stroke-width="2"/>
  <text x="380" y="167" text-anchor="middle" fill="#f0f6fc" font-size="11" font-weight="700">ORIENTADOR</text>
  <text x="380" y="182" text-anchor="middle" fill="#8b949e" font-size="9">(<u>SIAPE</u>, NomeProf, IdLab?)</text>

  <!-- Partial N:1 ORIENTADOR -> LAB -->
  <line x1="470" y1="170" x2="578" y2="170" stroke="#8b949e" stroke-width="1.5"/>
  <text x="500" y="162" text-anchor="middle" fill="#ffa657" font-size="9">(0,1)</text>
  <text x="556" y="162" text-anchor="middle" fill="#79c0ff" font-size="9">(0,N)</text>
  <rect x="578" y="148" width="155" height="44" rx="4" fill="#161b22" stroke="#58a6ff" stroke-width="2"/>
  <text x="655" y="167" text-anchor="middle" fill="#f0f6fc" font-size="11" font-weight="700">LABORATORIO</text>
  <text x="655" y="182" text-anchor="middle" fill="#8b949e" font-size="9">(<u>IdLab</u>, Sala)</text>
</svg>
</div>
<p><strong>Regra de negócio explícita:</strong> Um mesmo par <code>(ALUNO, EMPRESA)</code> possui no máximo <strong>1</strong> <code>ORIENTADOR</code> responsável (indicado pelo <code>1</code> na perna de <code>ORIENTADOR</code>). Além disso, cada <code>ORIENTADOR</code> pode estar vinculado opcionalmente <code>(0,1)</code> a um <code>LABORATORIO</code>.</p>
""",
        "answer_sheet_html": """
<div class="answer-sheet-box">
  <h4>Gabarito Explicado — R4.3 (Ternário M:N:1 &amp; RIRs)</h4>
  <ul>
    <li><strong>Chave Primária do Ternário <code>M:N:1</code>:</strong> Como um par <code>(Matr, CNPJ)</code> determina no máximo um <code>SIAPE</code> (lado <code>1</code>), a PK da tabela <code>ESTAGIO</code> é formada apenas pelos dois lados <code>M/N</code>: <code>ESTAGIO(<u>Matr</u>, <u>CNPJ</u>, SIAPE, CargaSemanal)</code>, sendo <code>SIAPE</code> atributo FK não pertencente à PK!</li>
    <li><strong>RIRs em <code>ESTAGIO</code> vs <code>ORIENTADOR[IdLab]</code>:</strong> Como <code>Matr</code> e <code>CNPJ</code> compõem a PK de <code>ESTAGIO</code>, usam <code>-p-&gt;</code> (<code>CASCADE</code>) ou <code>-b-&gt;</code> conforme critério, nunca <code>-n-&gt;</code>. Já <code>ORIENTADOR[IdLab]</code> tem participação parcial <code>(0,1)</code>, podendo aceitar <code>NULL</code>: logo, se um laboratório for desativado sem demitir professores, usa-se <code>ORIENTADOR[IdLab] -n-&gt; LABORATORIO[IdLab]</code> (<code>SET NULL</code>).</li>
  </ul>
</div>
""",
        "fields": [
            {
                "id": "f1",
                "label": "1) Considerando que há cardinalidade '1' na perna de ORIENTADOR e 'M, N' em ALUNO e EMPRESA, qual é a chave primária exata da relação ESTAGIO?",
                "options": [
                    "A chave tripla composta (Matr, CNPJ, SIAPE), pois toda relação ternária obrigatoriamente inclui as 3 FKs na PK.",
                    "Apenas (SIAPE) isolado, acompanhado de Matr e CNPJ como atributos comuns da tabela.",
                    "A chave composta dos lados muitos (Matr, CNPJ), ficando SIAPE apenas como FK não-chave (NOT NULL).",
                    "Duas tabelas separadas ALUNO_EMP(Matr, CNPJ) e ORIENT_EMP(SIAPE, CNPJ) sem juntar as três FKs."
                ],
                "answer": "A chave composta dos lados muitos (Matr, CNPJ), ficando SIAPE apenas como FK não-chave (NOT NULL).",
                "explanation": "Em ternários M:N:1, como o par (Matr, CNPJ) mapeia para no máximo 1 SIAPE, (Matr, CNPJ) identifica unicamente a tupla e proíbe dois orientadores para o mesmo aluno na mesma empresa."
            },
            {
                "id": "f2",
                "label": "2) Se um LABORATÓRIO for extinto e os ORIENTADORES vinculados a ele permanecerem ativos no sistema sem laboratório, qual RIR deve ser usada?",
                "options": [
                    "ORIENTADOR[IdLab] -n-> LABORATORIO[IdLab] (ON DELETE SET NULL), possível pois IdLab é opcional (0,1).",
                    "ORIENTADOR[IdLab] -p-> LABORATORIO[IdLab] (ON DELETE CASCADE), pois o orientador é entidade fraca.",
                    "LABORATORIO[IdLab] -b-> ORIENTADOR[SIAPE], invertendo a chave estrangeira para dentro de LABORATORIO.",
                    "ESTAGIO[Matr] -n-> ALUNO[Matr], anulando a matrícula quando o aluno troca de laboratório."
                ],
                "answer": "ORIENTADOR[IdLab] -n-> LABORATORIO[IdLab] (ON DELETE SET NULL), possível pois IdLab é opcional (0,1).",
                "explanation": "Participação parcial (0,1) torna IdLab anulável; -n-> (SET NULL) desvincula o orientador sem removê-lo do banco."
            },
            {
                "id": "f3",
                "label": "3) Por que NÃO é possível aplicar a política -n-> (SET NULL) em ESTAGIO[Matr] ou ESTAGIO[CNPJ] ao remover um aluno ou empresa?",
                "options": [
                    "Porque o modelo SQL-92 proíbe mais de uma política de anulação no mesmo diagrama ER.",
                    "Porque Matr e CNPJ compõem a PRIMARY KEY de ESTAGIO e chaves primárias jamais podem conter NULL.",
                    "Porque ALUNO e EMPRESA formam uma especialização disjunta que impede exclusões em cascata.",
                    "Porque CargaSemanal passaria a ser chave candidata caso CNPJ recebesse valor nulo."
                ],
                "answer": "Porque Matr e CNPJ compõem a PRIMARY KEY de ESTAGIO e chaves primárias jamais podem conter NULL.",
                "explanation": "Pela restrição de integridade de entidade, nenhum atributo componente de chave primária pode assumir NULL; logo usa-se -p-> ou -b->."
            }
        ]
    },

    "R4.4": {
        "title": "R4.4 (Aberto / Lista Oficial Style) — Mapeamento Lógico Completo + RIRs (Cooperativa Bancária)",
        "type": "oficial",
        "mode": "open_design",
        "study_guide": STUDY_GUIDE_G11,
        "context_html": """
<p><strong>Exercício Completo Estilo <code>ExercicioProjetoLogico.pdf</code> (Resolução no Caderno + Conferência no Gabarito Oficial):</strong><br>
Dado o Diagrama ER/EER abaixo de uma Cooperativa de Crédito, <strong>escreva em seu caderno TODO o Esquema Lógico Formal</strong> no formato dos slides da UFMG (indicando PK sublinhada, <code>(nn)</code> nos campos obrigatórios e todas as setas RIR <code>Rel[FK] -b/-p/-n-&gt; Pai[PK]</code>):</p>
<div style="text-align:center; margin: 12px 0;">
<svg viewBox="0 0 760 280" width="100%" style="max-width:740px; background:#0d1117; border:1px solid #30363d; border-radius:8px;">
  <!-- COOPERATIVA -->
  <rect x="24" y="24" width="142" height="44" rx="4" fill="#161b22" stroke="#58a6ff" stroke-width="2"/>
  <text x="95" y="43" text-anchor="middle" fill="#f0f6fc" font-size="11" font-weight="700">COOPERATIVA</text>
  <text x="95" y="58" text-anchor="middle" fill="#8b949e" font-size="9">(<u>CodCoop</u>, Razao)</text>
  <line x1="166" y1="46" x2="215" y2="46" stroke="#8b949e" stroke-width="1.5"/>
  <text x="190" y="37" text-anchor="middle" fill="#79c0ff" font-size="9">(1,N)</text>
  <polygon points="215,46 250,23 285,46 250,69" fill="#1f2937" stroke="#f0883e" stroke-width="1.8"/>
  <polygon points="221,46 250,28 279,46 250,64" fill="none" stroke="#f0883e" stroke-width="1.2"/>
  <text x="250" y="50" text-anchor="middle" fill="#f0883e" font-size="9" font-weight="700">MANTEM</text>
  <line x1="285" y1="43" x2="328" y2="43" stroke="#f0883e" stroke-width="1.5"/>
  <line x1="285" y1="49" x2="328" y2="49" stroke="#f0883e" stroke-width="1.5"/>
  <text x="306" y="34" text-anchor="middle" fill="#ffa657" font-size="9">(1,1)</text>
  <!-- POSTO (Weak) -->
  <rect x="328" y="22" width="138" height="48" rx="4" fill="#161b22" stroke="#f0883e" stroke-width="2"/>
  <rect x="333" y="27" width="128" height="38" rx="2" fill="none" stroke="#f0883e" stroke-width="1.2"/>
  <text x="397" y="43" text-anchor="middle" fill="#f0f6fc" font-size="11" font-weight="700">POSTO</text>
  <text x="397" y="58" text-anchor="middle" fill="#ffa657" font-size="9">({NumPosto}, Bairro)</text>

  <!-- POSTO -- ABRE -- CONTA -->
  <line x1="466" y1="46" x2="510" y2="46" stroke="#8b949e" stroke-width="1.5"/>
  <text x="488" y="37" text-anchor="middle" fill="#79c0ff" font-size="9">(0,N)</text>
  <polygon points="510,46 544,24 578,46 544,68" fill="#1f2937" stroke="#d2a8ff" stroke-width="1.8"/>
  <text x="544" y="50" text-anchor="middle" fill="#d2a8ff" font-size="9" font-weight="700">SEDE</text>
  <line x1="578" y1="43" x2="616" y2="43" stroke="#58a6ff" stroke-width="1.5"/>
  <line x1="578" y1="49" x2="616" y2="49" stroke="#58a6ff" stroke-width="1.5"/>
  <text x="597" y="34" text-anchor="middle" fill="#79c0ff" font-size="9">(1,1)</text>

  <!-- CONTA -->
  <rect x="616" y="24" width="124" height="44" rx="4" fill="#161b22" stroke="#58a6ff" stroke-width="2"/>
  <text x="678" y="43" text-anchor="middle" fill="#f0f6fc" font-size="11" font-weight="700">CONTA</text>
  <text x="678" y="58" text-anchor="middle" fill="#8b949e" font-size="9">(<u>NumConta</u>, Saldo)</text>

  <!-- ASSOCIADO {d, total} -> PF, PJ + multivalued Telefones -->
  <rect x="180" y="135" width="150" height="44" rx="4" fill="#161b22" stroke="#58a6ff" stroke-width="2"/>
  <text x="255" y="153" text-anchor="middle" fill="#f0f6fc" font-size="11" font-weight="700">ASSOCIADO</text>
  <text x="255" y="168" text-anchor="middle" fill="#8b949e" font-size="9">(<u>IdAssoc</u>, Email, {{Fones}})</text>

  <!-- Double line + d -->
  <line x1="252" y1="179" x2="252" y2="199" stroke="#f2cc60" stroke-width="1.5"/>
  <line x1="258" y1="179" x2="258" y2="199" stroke="#f2cc60" stroke-width="1.5"/>
  <circle cx="255" cy="212" r="12" fill="#161b22" stroke="#f2cc60" stroke-width="1.8"/>
  <text x="255" y="216" text-anchor="middle" fill="#f2cc60" font-size="11" font-weight="700">d</text>
  <line x1="244" y1="220" x2="185" y2="236" stroke="#8b949e" stroke-width="1.4"/>
  <line x1="266" y1="220" x2="325" y2="236" stroke="#8b949e" stroke-width="1.4"/>
  <rect x="120" y="236" width="122" height="32" rx="4" fill="#161b22" stroke="#3fb950" stroke-width="1.6"/>
  <text x="181" y="256" text-anchor="middle" fill="#f0f6fc" font-size="10" font-weight="700">PF (<u>CPF</u>, Nome)</text>
  <rect x="268" y="236" width="132" height="32" rx="4" fill="#161b22" stroke="#3fb950" stroke-width="1.6"/>
  <text x="334" y="256" text-anchor="middle" fill="#f0f6fc" font-size="10" font-weight="700">PJ (<u>CNPJ</u>, Fantasia)</text>

  <!-- ASSOCIADO -- TITULAR (M:N, Papel) -- CONTA -->
  <line x1="330" y1="157" x2="465" y2="157" stroke="#8b949e" stroke-width="1.5"/>
  <text x="396" y="149" text-anchor="middle" fill="#79c0ff" font-size="9">(0,N)</text>
  <polygon points="465,157 512,132 559,157 512,182" fill="#1f2937" stroke="#d2a8ff" stroke-width="1.8"/>
  <text x="512" y="161" text-anchor="middle" fill="#d2a8ff" font-size="9" font-weight="700">TITULAR</text>
  <text x="512" y="196" text-anchor="middle" fill="#e6edf3" font-size="9">Attr: Papel</text>
  <line x1="559" y1="154" x2="678" y2="154" stroke="#58a6ff" stroke-width="1.5"/>
  <line x1="559" y1="160" x2="678" y2="160" stroke="#58a6ff" stroke-width="1.5"/>
  <line x1="678" y1="157" x2="678" y2="68" stroke="#58a6ff" stroke-width="1.5"/>
  <text x="618" y="145" text-anchor="middle" fill="#79c0ff" font-size="9">(1,N)</text>
</svg>
</div>
<p><em>Dica:</em> Atenção à chave estrangeira composta que sai de <code>CONTA</code> para a entidade fraca <code>POSTO</code>, à escolha de opção EER em <code>ASSOCIADO</code> e às RIRs (<code>b/p/n</code>) em todas as setas!</p>
""",
        "answer_sheet_html": """
<div class="answer-sheet-box">
  <h4>Gabarito Oficial Completo (Notação UFMG) — R4.4</h4>
  <pre class="sql-code">-- 1. Fortes e Fraca (Propagação de CodCoop):
COOPERATIVA(<u>CodCoop</u>, Razao)
POSTO(<u>CodCoop</u>, <u>NumPosto</u>, Bairro)
  POSTO[CodCoop] -p-&gt; COOPERATIVA[CodCoop]

-- 2. CONTA herdando PK composta do posto sede (1:1/N:1 total):
CONTA(<u>NumConta</u>, Saldo, CodCoop(nn), NumPosto(nn))
  CONTA[CodCoop, NumPosto] -b-&gt; POSTO[CodCoop, NumPosto]

-- 3. ASSOCIADO + Multivalorado Fones + Opção 1 (1-1) para {d, total}:
ASSOCIADO(<u>IdAssoc</u>, Email)
ASSOC_FONES(<u>IdAssoc</u>, <u>Fone</u>)
  ASSOC_FONES[IdAssoc] -p-&gt; ASSOCIADO[IdAssoc]
PF(<u>IdAssoc</u>, CPF(unique, nn), Nome(nn))
  PF[IdAssoc] -p-&gt; ASSOCIADO[IdAssoc]
PJ(<u>IdAssoc</u>, CNPJ(unique, nn), Fantasia(nn))
  PJ[IdAssoc] -p-&gt; ASSOCIADO[IdAssoc]
-- (Opcional na Opção 1: Assertions garantindo disjunção PF ∩ PJ = ∅ e totalidade PF ∪ PJ = ASSOCIADO)

-- 4. Relacionamento M:N TITULAR:
TITULAR(<u>IdAssoc</u>, <u>NumConta</u>, Papel(nn))
  TITULAR[IdAssoc] -p-&gt; ASSOCIADO[IdAssoc]
  TITULAR[NumConta] -p-&gt; CONTA[NumConta]</pre>
</div>
""",
        "fields": []
    },

    "R4.5": {
        "title": "R4.5 (Lab Assertions SQL-92) — Equações de Álgebra Relacional EER em Biblioteca",
        "type": "oficial",
        "mode": "sql_assertion",
        "study_guide": STUDY_GUIDE_G11,
        "setup": """
CREATE TABLE ACERVO (
  CodItem INTEGER PRIMARY KEY,
  Titulo TEXT NOT NULL
);
CREATE TABLE LIVRO_FISICO (
  CodItem INTEGER PRIMARY KEY REFERENCES ACERVO(CodItem),
  ISBN TEXT NOT NULL
);
CREATE TABLE PERIODICO (
  CodItem INTEGER PRIMARY KEY REFERENCES ACERVO(CodItem),
  ISSN TEXT NOT NULL
);
INSERT INTO ACERVO VALUES (1, 'Sistemas de BD (Elmasri)'), (2, 'ACM TODS Vol. 48');
INSERT INTO LIVRO_FISICO VALUES (1, '978-85-7936');
INSERT INTO PERIODICO VALUES (2, '0362-5915');
""",
        "context_html": """
<p><strong>Tradução Direta Álgebra Relacional &rarr; SQL-92 (<code>ibd-parte5.pdf</code>):</strong> A hierarquia <strong><code>ACERVO &rarr; {LIVRO_FISICO, PERIODICO} {d, total}</code></strong> foi mapeada pela <strong>Opção 1 (1-1 / Tabelas Separadas)</strong> e carregada no banco.</p>
<p>Nos slides da disciplina, as duas restrições estruturais obrigatórias são escritas em Álgebra Relacional:</p>
<ol>
  <li><strong>Disjunção:</strong> <code>&pi;_CodItem(LIVRO_FISICO) &cap; &pi;_CodItem(PERIODICO) = &empty;</code></li>
  <li><strong>Totalidade:</strong> <code>&pi;_CodItem(LIVRO_FISICO) &cup; &pi;_CodItem(PERIODICO) = &pi;_CodItem(ACERVO)</code></li>
</ol>
<p>Implemente essas duas regras em SQL-92 usando <strong>duas declarações <code>CREATE ASSERTION ... CHECK (NOT EXISTS (...));</code></strong> separadas por ponto-e-vírgula.</p>
""",
        "answer_sheet_html": """
<div class="answer-sheet-box">
  <h4>Gabarito de Referência — R4.5 (AR &rarr; ASSERTION)</h4>
  <pre class="sql-code">CREATE ASSERTION ACERVO_DISJUNTO CHECK (
  NOT EXISTS (
    SELECT 1 FROM LIVRO_FISICO l
    JOIN PERIODICO p ON l.CodItem = p.CodItem
  )
);

CREATE ASSERTION ACERVO_TOTAL CHECK (
  NOT EXISTS (
    SELECT 1 FROM ACERVO a
    WHERE a.CodItem NOT IN (SELECT CodItem FROM LIVRO_FISICO)
      AND a.CodItem NOT IN (SELECT CodItem FROM PERIODICO)
  )
);</pre>
</div>
""",
        "assertion_tests": [
            {
                "name": "Estado inicial consistente (1 livro, 1 periódico, ambos em ACERVO)",
                "violation_sql": None,
                "should_pass": True,
                "hint": "O estado inicial satisfaz disjunção e totalidade."
            },
            {
                "name": "Permitir inserir novo periódico válido (ACERVO + PERIODICO)",
                "violation_sql": "INSERT INTO ACERVO VALUES (3, 'IEEE TKDE'); INSERT INTO PERIODICO VALUES (3, '1041-4347');",
                "should_pass": True,
                "hint": "Novo item em ACERVO e em exatamente uma subclasse deve passar."
            },
            {
                "name": "Bloquear violação de disjunção (Item 1 em LIVRO_FISICO e PERIODICO)",
                "violation_sql": "INSERT INTO PERIODICO VALUES (1, '0000-1111');",
                "should_pass": False,
                "hint": "Sua asserção de disjunção deve verificar LIVRO_FISICO JOIN PERIODICO."
            },
            {
                "name": "Bloquear violação de totalidade (Item 99 em ACERVO sem subclasse)",
                "violation_sql": "INSERT INTO ACERVO VALUES (99, 'Obra Sem Categoria');",
                "should_pass": False,
                "hint": "Todo CodItem de ACERVO precisa estar em LIVRO_FISICO ou em PERIODICO."
            }
        ]
    },

    "R4.6": {
        "title": "R4.6 (Lab SQL) — Auditoria de Instância &amp; Contra-exemplos de DF (Turmas)",
        "type": "oficial",
        "mode": "sql_query",
        "study_guide": STUDY_GUIDE_G12,
        "setup": """
CREATE TABLE MATRICULA_HIST (
  IdReg INTEGER PRIMARY KEY,
  CodDisc TEXT NOT NULL,
  Turma TEXT NOT NULL,
  Semestre TEXT NOT NULL,
  CPFProf TEXT NOT NULL,
  NomeProf TEXT NOT NULL,
  Sala TEXT NOT NULL,
  Capacidade INTEGER NOT NULL
);
INSERT INTO MATRICULA_HIST VALUES
  (1, 'DCC011', 'T1', '2026/1', '111', 'Prof. Marcos',  'ICEx-1022', 60),
  (2, 'DCC222', 'T1', '2026/1', '222', 'Profa. Raquel', 'ICEx-1022', 60),
  (3, 'DCC011', 'T2', '2026/1', '111', 'Prof. Marcos',  'ICEx-2010', 45),
  (4, 'DCC033', 'T1', '2026/1', '333', 'Prof. Wagner',  'ICEx-2010', 45),
  (5, 'DCC044', 'T1', '2026/2', '222', 'Profa. Raquel', 'ICEx-1015', 80);
""",
        "context_html": """
<p><strong>Auditoria de Dependências Funcionais em Instâncias (<code>ibd-parte6.pdf</code>):</strong> Dada a extensão populada <code>MATRICULA_HIST(IdReg, CodDisc, Turma, Semestre, CPFProf, NomeProf, Sala, Capacidade)</code>:</p>
<ul>
  <li>Note que <code>Sala &rarr; Capacidade</code> vale na tabela inteira (<code>ICEx-1022</code> sempre tem capacidade <code>60</code>; <code>ICEx-2010</code> sempre tem <code>45</code>).</li>
  <li>Já um colega afirmou que <code>Sala &rarr; CPFProf</code> também valeria porque toda turma teria um único professor na sala!</li>
</ul>
<p><strong>Sua Tarefa SQL:</strong> Escreva uma consulta SQL retornando todos os pares ordenados (<code>a.IdReg &lt; b.IdReg</code>) que <strong>refutam a DF <code>Sala &rarr; CPFProf</code></strong> (mesma <code>Sala</code> com <code>CPFProf</code> distintos).</p>
<p><strong>Colunas esperadas:</strong> <code>Id1</code>, <code>Id2</code>, <code>Sala</code>, <code>CPF1</code>, <code>CPF2</code>.</p>
""",
        "answer_sheet_html": """
<div class="answer-sheet-box">
  <h4>Gabarito SQL — R4.6 (Refutação de DF na Prática)</h4>
  <pre class="sql-code">SELECT a.IdReg AS Id1,
       b.IdReg AS Id2,
       a.Sala,
       a.CPFProf AS CPF1,
       b.CPFProf AS CPF2
FROM MATRICULA_HIST a
JOIN MATRICULA_HIST b
  ON a.Sala = b.Sala
 AND a.CPFProf &lt;&gt; b.CPFProf
 AND a.IdReg &lt; b.IdReg;</pre>
  <p>Retorna os pares <code>(1, 2, 'ICEx-1022', '111', '222')</code> e <code>(3, 4, 'ICEx-2010', '111', '333')</code>, provando que <code>Sala</code> NÃO determina <code>CPFProf</code>.</p>
</div>
""",
        "expected_columns": ["Id1", "Id2", "Sala", "CPF1", "CPF2"],
        "expected_rows": [
            [1, 2, "ICEx-1022", "111", "222"],
            [3, 4, "ICEx-2010", "111", "333"]
        ]
    },

    "R4.7": {
        "title": "R4.7 (Oficial/Teórico) — Axiomas de Armstrong &amp; Equivalência de Conjuntos (F ≡ G)",
        "type": "oficial",
        "mode": "structured",
        "study_guide": STUDY_GUIDE_G12,
        "context_html": """
<p><strong>Questão Clássica de Prova Teórica (<code>ibd-parte6.pdf</code> — Seção 3):</strong> Considere os conjuntos de dependências funcionais abaixo definidos sobre <code>R(A, B, C, D, E)</code>:</p>
<pre class="sql-code">F = { A &rarr; B,  AB &rarr; C,  D &rarr; AC,  D &rarr; E }
G = { A &rarr; BC, D &rarr; AE }</pre>
<p>E compare também com o segundo par de conjuntos sobre <code>R2(A, B, C)</code>:</p>
<pre class="sql-code">P = { A &rarr; B,  B &rarr; C,  A &rarr; C }
Q = { A &rarr; BC }</pre>
<p>Aplique os axiomas de Armstrong e o algoritmo de cobertura (fecho <code>X+</code>) para verificar equivalência e derivabilidade.</p>
""",
        "answer_sheet_html": """
<div class="answer-sheet-box">
  <h4>Gabarito Explicado — R4.7 (Armstrong &amp; Equivalência)</h4>
  <ul>
    <li><strong>Derivação em <code>F</code>:</strong> De <code>A &rarr; B</code> (por Aumento com <code>A</code> temos <code>AA &rarr; AB</code>, isto é, <code>A &rarr; AB</code>) + <code>AB &rarr; C</code> (Transitiva) obtemos <strong><code>A &rarr; C</code></strong> (Regra da Pseudotransitividade).</li>
    <li><strong>Comparando <code>F</code> e <code>G</code>:</strong>
      <ul>
        <li><code>F</code> cobre <code>G</code>? Sob <code>F</code>: <code>A+ = {A, B, C}</code> (cobre <code>A &rarr; BC</code>) e <code>D+ = {D, A, C, E, B}</code> (cobre <code>D &rarr; AE</code>). <strong>Sim!</strong></li>
        <li><code>G</code> cobre <code>F</code>? Sob <code>G</code>: <code>A+ = {A, B, C}</code> (cobre <code>A &rarr; B</code> e <code>AB &rarr; C</code>) e <code>D+ = {D, A, E, B, C}</code> (cobre <code>D &rarr; AC</code> e <code>D &rarr; E</code>). <strong>Sim!</strong> Logo <strong><code>F &equiv; G</code></strong>!</li>
      </ul>
    </li>
    <li><strong>Comparando <code>P</code> e <code>Q</code>:</strong> <code>P</code> cobre <code>Q</code> (<code>A+<sub>P</sub> = {A, B, C}</code>), mas <code>Q</code> <strong>NÃO</strong> cobre <code>P</code> porque <code>B+<sub>Q</sub> = {B}</code> (não deriva <code>B &rarr; C</code>!). Logo <code>P &nequiv; Q</code>.</li>
  </ul>
</div>
""",
        "fields": [
            {
                "id": "f1",
                "label": "1) Como a dependência A → C é formalmente inferida a partir de { A → B, AB → C } pelos axiomas de Armstrong?",
                "options": [
                    "Pela regra da Reflexividade direta, já que C está contido na união de A com AB.",
                    "Pela regra da Decomposição aplicada a AB → C, removendo B automaticamente sem usar A → B.",
                    "Pela regra da Simetria entre B e C, invertendo AB → C para C → AB.",
                    "Aplicando Aumento em A → B (dando A → AB) e depois Transitividade com AB → C (Pseudotransitividade)."
                ],
                "answer": "Aplicando Aumento em A → B (dando A → AB) e depois Transitividade com AB → C (Pseudotransitividade).",
                "explanation": "Por Aumento com A em A -> B obtemos AA -> AB, que equivale a A -> AB; aplicando a Transitiva em (A -> AB, AB -> C) obtemos A -> C."
            },
            {
                "id": "f2",
                "label": "2) Sobre a equivalência lógica entre F = { A → B, AB → C, D → AC, D → E } e G = { A → BC, D → AE }:",
                "options": [
                    "F cobre G, mas G não cobre F porque AB → C possui dois atributos no determinante.",
                    "G cobre F, mas F não cobre G porque B e C aparecem separados dentro de F.",
                    "F ≡ G (são equivalentes), pois todo fecho calculado em F cobre G e todo fecho em G cobre F.",
                    "Nem F cobre G nem G cobre F, pois D → C aparece apenas no conjunto F original."
                ],
                "answer": "F ≡ G (são equivalentes), pois todo fecho calculado em F cobre G e todo fecho em G cobre F.",
                "explanation": "Sob F: A+ = ABC, D+ = ABCDE (cobre G). Sob G: A+ = ABC, (AB)+ = ABC, D+ = ABCDE (cobre F). Assim F+ = G+ (são equivalentes)."
            },
            {
                "id": "f3",
                "label": "3) Ao comparar P = { A → B, B → C, A → C } e Q = { A → BC }, o que ocorre na verificação de cobertura?",
                "options": [
                    "P ≡ Q, pois B → C é sempre uma dependência redundante derivável apenas a partir de A → BC.",
                    "P cobre Q (P ⊇ Q), mas Q NÃO cobre P porque B+ sob Q vale apenas {B} (não deriva B → C).",
                    "Q cobre P (Q ⊇ P), mas P NÃO cobre Q porque A → BC tem dois atributos no lado direito.",
                    "P e Q têm exatamente o mesmo fechamento B+ = {B, C}, variando apenas na chave primária."
                ],
                "answer": "P cobre Q (P ⊇ Q), mas Q NÃO cobre P porque B+ sob Q vale apenas {B} (não deriva B → C).",
                "explanation": "Apenas de A -> BC não se pode inferir B -> C (duas tuplas com mesmo B mas A diferentes podem ter C diferentes!). Logo B+_Q = {B} e Q não cobre P."
            }
        ]
    },

    "R4.8": {
        "title": "R4.8 (Oficial/Algoritmo) — Particionamento (L / M / R) &amp; Múltiplas Chaves em R(A,B,C,D,E,G)",
        "type": "oficial",
        "mode": "structured",
        "study_guide": STUDY_GUIDE_G12,
        "context_html": """
<p><strong>Técnica Mais Rápida de Prova (<code>ExerciciosNormalizacaoSemResposta.pdf</code>):</strong> Seja a relação <code>R(A, B, C, D, E, G)</code> com as dependências funcionais:</p>
<pre class="sql-code">F = { AB &rarr; C,  C &rarr; DE,  E &rarr; B,  D &rarr; G }</pre>
<p>Aplique o <strong>método dos 3 conjuntos</strong> (<code>Somente Esquerda</code>, <code>Meio/Ambos</code>, <code>Somente Direita</code>) para encontrar todas as chaves candidatas, separar atributos primos de não-primos e diagnosticar a maior forma normal satisfeita por <code>R</code>.</p>
""",
        "answer_sheet_html": """
<div class="answer-sheet-box">
  <h4>Gabarito Passo a Passo — R4.8 (Método do Particionamento)</h4>
  <ul>
    <li><strong>Partição em 3 Conjuntos:</strong>
      <ul>
        <li><code>Somente Esquerda (L)</code> = <code>{A}</code> (nunca aparece no RHS &rarr; obrigatório em TODA chave!)</li>
        <li><code>Somente Direita (R)</code> = <code>{G}</code> (nunca aparece no LHS &rarr; nunca entra em chave mínima!)</li>
        <li><code>Meio (M)</code> = <code>{B, C, D, E}</code> (testar combinações com <code>A</code>).</li>
      </ul>
    </li>
    <li><strong>Cálculo dos Fechos:</strong> <code>A+ = {A}</code> (não basta). Combinando <code>A</code> com 1 atributo de <code>M</code>:<br>
    <code>(AB)+ = ABCDEG</code> &checkmark; &bull; <code>(AC)+ = ABCDEG</code> &checkmark; &bull; <code>(AE)+ = ABCDEG</code> &checkmark; &bull; <code>(AD)+ = {A, D, G}</code> (falha!).</li>
    <li><strong>Chaves &amp; Classificação:</strong> Chaves = <code>{AB, AC, AE}</code> &bull; Primos = <code>{A, B, C, E}</code> &bull; Não-primos = <code>{D, G}</code>.<br>
    Como <code>C &rarr; D</code> usa subconjunto próprio da chave <code>{AC}</code> para determinar o não-primo <code>D</code>, <code>R</code> <strong>viola a 2FN (Definição Geral)</strong> e está apenas em <strong>1FN</strong>!</li>
  </ul>
</div>
""",
        "fields": [
            {
                "id": "f1",
                "label": "1) Aplicando o particionamento (Somente Esquerda, Meio, Somente Direita) em R(A,B,C,D,E,G), quais atributos são obrigatórios vs descartáveis para chaves mínimas?",
                "options": [
                    "Somente Esquerda = {A} (obrigatório em toda chave) e Somente Direita = {G} (nunca entra em chave mínima).",
                    "Somente Esquerda = {A, B} (obrigatórios) e Somente Direita = {D, G} (descartáveis).",
                    "Somente Esquerda = {C} (obrigatório) e Somente Direita = {E, G} (nunca entram na chave).",
                    "Não existe atributo em Somente Esquerda porque A aparece determinado por E → B indiretamente."
                ],
                "answer": "Somente Esquerda = {A} (obrigatório em toda chave) e Somente Direita = {G} (nunca entra em chave mínima).",
                "explanation": "A só aparece no LHS (L = {A}) e G só aparece no RHS (R = {G}); B, C, D e E aparecem em ambos os lados (M = {B, C, D, E})."
            },
            {
                "id": "f2",
                "label": "2) Qual é o conjunto EXATO de todas as chaves candidatas de R(A, B, C, D, E, G) sob F?",
                "options": [
                    "{AB} e {AC} apenas, porque E+ = {E, B} não alcança os atributos D e G.",
                    "{AB}, {AC} e {AE} (enquanto {AD}+ = {A, D, G} não forma chave candidata).",
                    "{AB}, {AC}, {AD} e {AE}, pois todo par contendo A fecha todos os 6 atributos.",
                    "{ABC} e {CDE}, pois nenhuma dupla de atributos determina G sozinho."
                ],
                "answer": "{AB}, {AC} e {AE} (enquanto {AD}+ = {A, D, G} não forma chave candidata).",
                "explanation": "AB -> C -> DE -> G cobre tudo; AC -> DE -> B -> G cobre tudo; AE -> B -> C -> DE -> G cobre tudo; já AD -> G para em {A, D, G}."
            },
            {
                "id": "f3",
                "label": "3) Considerando todas as chaves candidatas encontradas, qual é a maior forma normal satisfeita por R?",
                "options": [
                    "Está em 3FN (pois B e E são primos), violando apenas a BCNF em C → DE.",
                    "Está em 2FN, violando a 3FN apenas por causa da transitiva C → D → G.",
                    "Está apenas em 1FN (viola a 2FN pela Definição Geral), pois C → D determina o não-primo D usando parte de {AC}.",
                    "Está em BCNF plena porque todas as chaves candidatas possuem tamanho 2."
                ],
                "answer": "Está apenas em 1FN (viola a 2FN pela Definição Geral), pois C → D determina o não-primo D usando parte de {AC}.",
                "explanation": "D e G não pertencem a nenhuma chave candidata (são não-primos). Como C é subconjunto próprio da chave {AC} e C -> D (e C -> DE), há dependência parcial sobre chave candidata, violando a 2FN."
            }
        ]
    },

    "R4.9": {
        "title": "R4.9 (Aberto / Prova Discursiva) — Decomposição Completa 1FN &rarr; 2FN &rarr; 3FN (Boletim Escolar)",
        "type": "oficial",
        "mode": "open_design",
        "study_guide": STUDY_GUIDE_G12,
        "context_html": """
<p><strong>Exercício Aberto Estilo Lista Oficial (<code>ExerciciosNormalizacaoSemResposta.pdf</code> — Resolução no Caderno + Gabarito Comentado):</strong><br>
Considere o registro não-normalizado do boletim anual de um colégio:</p>
<pre class="sql-code">BOLETIM_ANUAL(<u>CodAluno</u>, NomeAluno, Serie, NomeSerie,
  { Disciplinas(<u>CodDisc</u>, NomeDisc, CPFProf, NomeProf, NotaFinal) })</pre>
<p><strong>Regras de negócio:</strong> Um aluno cursa várias disciplinas no ano (grupo repetitivo <code>Disciplinas(...)</code>); cada aluno pertence a uma única <code>Serie</code>, e <code>Serie &rarr; NomeSerie</code>; cada <code>CodDisc</code> tem seu <code>NomeDisc</code> e é ministrada por um único <code>CPFProf</code> no ano (<code>CodDisc &rarr; NomeDisc, CPFProf</code>), e <code>CPFProf &rarr; NomeProf</code>; a <code>NotaFinal</code> depende da dupla <code>(CodAluno, CodDisc)</code>.</p>
<p><strong>Tarefa no Caderno:</strong> Execute explicitamente as <strong>3 etapas (1FN, 2FN e 3FN)</strong> sublinhando as PKs e destacando as FKs em cada passo, e confira na Folha de Gabarito abaixo.</p>
""",
        "answer_sheet_html": """
<div class="answer-sheet-box">
  <h4>Gabarito Passo a Passo (1FN &rarr; 2FN &rarr; 3FN) — R4.9</h4>
  <ol>
    <li><strong>Passagem para 1FN (Remover grupo repetitivo <code>Disciplinas</code>):</strong><br>
    <code>ALUNO_1FN(<u>CodAluno</u>, NomeAluno, Serie, NomeSerie)</code><br>
    <code>NOTA_DISC_1FN(<u>CodAluno</u>, <u>CodDisc</u>, NomeDisc, CPFProf, NomeProf, NotaFinal)</code></li>
    <li><strong>Passagem para 2FN (Remover parciais em <code>NOTA_DISC_1FN</code>):</strong> Como <code>CodDisc &rarr; NomeDisc, CPFProf, NomeProf</code> depende apenas de parte da PK composta <code>(CodAluno, CodDisc)</code>:<br>
    <code>ALUNO_2FN(<u>CodAluno</u>, NomeAluno, Serie, NomeSerie)</code><br>
    <code>MATRICULA_2FN(<u>CodAluno</u>, <u>CodDisc</u>, NotaFinal)</code><br>
    <code>DISCIPLINA_2FN(<u>CodDisc</u>, NomeDisc, CPFProf, NomeProf)</code></li>
    <li><strong>Passagem para 3FN (Remover transitivas via não-primos):</strong>
      <ul>
        <li>Em <code>ALUNO_2FN</code>: <code>CodAluno &rarr; Serie &rarr; NomeSerie</code> &rArr; extrair <code>SERIE(<u>Serie</u>, NomeSerie)</code>.</li>
        <li>Em <code>DISCIPLINA_2FN</code>: <code>CodDisc &rarr; CPFProf &rarr; NomeProf</code> &rArr; extrair <code>PROFESSOR(<u>CPFProf</u>, NomeProf)</code>.</li>
      </ul>
    </li>
    <li><strong>Esquema Final Normalizado em 3FN/BCNF (5 tabelas):</strong><br>
    <code>SERIE(<u>Serie</u>, NomeSerie)</code><br>
    <code>ALUNO(<u>CodAluno</u>, NomeAluno, Serie)</code> [FK: Serie]<br>
    <code>PROFESSOR(<u>CPFProf</u>, NomeProf)</code><br>
    <code>DISCIPLINA(<u>CodDisc</u>, NomeDisc, CPFProf)</code> [FK: CPFProf]<br>
    <code>HISTORICO(<u>CodAluno</u>, <u>CodDisc</u>, NotaFinal)</code> [FKs: CodAluno, CodDisc]</li>
  </ol>
</div>
""",
        "fields": []
    },

    "R4.10": {
        "title": "R4.10 (Revisão Relâmpago) — Anomalias, Sem Perda &amp; Normalização (Oficina &amp; Plantão)",
        "type": "oficial",
        "mode": "structured",
        "study_guide": STUDY_GUIDE_G12,
        "context_html": """
<p><strong>Bateria Mista de Prova Final (<code>ibd-parte6.pdf</code> — Guidelines, Anomalias &amp; 2FN/3FN):</strong> Três cenários curtos e diretos que costumam valer pontos preciosos em questões objetivas da prova final:</p>
<ol>
  <li><strong>Cenário 1 (<code>PLANTAO_MEDICO(<u>CRM</u>, <u>CodAla</u>, NomeAla, AndarAla, Turno)</code>):</strong> Considere que um hospital inaugurou uma nova ala cardiológica (<code>CodAla='C4'</code>, <code>Andar=4</code>), mas ainda não alocou nenhum médico nela. Ao tentar cadastrar a nova ala na tabela única <code>PLANTAO_MEDICO</code>, o SGBD recusa por <code>CRM NOT NULL</code>!</li>
  <li><strong>Cenário 2 (<code>OS_OFICINA(<u>NumOS</u>, <u>IdPeca</u>, DataOS, CPFCliente, NomeCliente, DescPeca, Qtd)</code>):</strong> Um aluno propôs decompor colocando <code>NomeCliente</code> dentro de <code>OS_PESSOA(<u>NumOS</u>, DataOS, CPFCliente, NomeCliente)</code>.</li>
  <li><strong>Cenário 3 (Decomposição de <code>EMP(<u>CPF</u>, CodDepto, NomeDepto)</code>):</strong> Um colega sugeriu quebrar <code>EMP</code> em <code>D1 = { E1(CPF, NomeDepto), E2(CodDepto, NomeDepto) }</code>.</li>
</ol>
""",
        "answer_sheet_html": """
<div class="answer-sheet-box">
  <h4>Gabarito Explicado — R4.10</h4>
  <ul>
    <li><strong>Cenário 1:</strong> Trata-se da clássica <strong>Anomalia de Inserção</strong> (impossibilidade de registrar um fato independente — uma nova Ala — sem a presença da entidade associada — um Médico com <code>CRM NOT NULL</code>).</li>
    <li><strong>Cenário 2:</strong> A decomposição ainda <strong>viola a 3FN</strong> porque <code>OS_PESSOA</code> mantém a dependência transitiva <code>NumOS &rarr; CPFCliente &rarr; NomeCliente</code> (além da parcial <code>IdPeca &rarr; DescPeca</code> dever ir para <code>PECA</code>).</li>
    <li><strong>Cenário 3:</strong> Em <code>E1(CPF, NomeDepto)</code> e <code>E2(CodDepto, NomeDepto)</code>, a interseção é <code>{NomeDepto}</code>. Se duas diretorias homônimas (<code>'Pesquisa'</code>) existirem com <code>CodDepto</code> distintos (ex.: BH e Montes Claros), <code>NomeDepto</code> não é chave de <code>E2</code> nem de <code>E1</code> &rArr; gera <strong>tuplas espúrias (perda de informação)</strong> e ainda <strong>perde a DF <code>CPF &rarr; CodDepto</code></strong>! O correto é juntar por <code>CodDepto</code> (PK de <code>DEPTO(<u>CodDepto</u>, NomeDepto)</code>).</li>
  </ul>
</div>
""",
        "fields": [
            {
                "id": "f1",
                "label": "1) No Cenário 1 (tentar cadastrar a nova Ala sem médicos em PLANTAO_MEDICO), qual problema clássico da Diretriz 2 ocorre?",
                "options": [
                    "Anomalia de Modificação, porque o andar de todos os médicos já cadastrados precisaria ser alterado.",
                    "Anomalia de Remoção, pois a criação da ala apagaria automaticamente os plantões anteriores do hospital.",
                    "Anomalia de Inserção, pois não é possível registrar a nova ala sem inventar um CRM fictício (PK não-nula).",
                    "Geração de tuplas espúrias por junção natural sobre atributo não-chave entre médicos e alas."
                ],
                "answer": "Anomalia de Inserção, pois não é possível registrar a nova ala sem inventar um CRM fictício (PK não-nula).",
                "explanation": "Não conseguir inserir uma nova instância de entidade independente (Ala) porque falta a chave do outro parceiro na PK composta (CRM) define a Anomalia de Inserção."
            },
            {
                "id": "f2",
                "label": "2) No Cenário 2, por que o esquema proposto OS_PESSOA(NumOS, DataOS, CPFCliente, NomeCliente) ainda NÃO atinge a 3FN?",
                "options": [
                    "Porque contém a dependência transitiva NumOS → CPFCliente → NomeCliente via atributo não-primo CPFCliente.",
                    "Porque DataOS depende parcialmente da chave composta (NumOS, IdPeca) na tabela de ordens.",
                    "Porque CPFCliente e NomeCliente são ambos atributos primos integrantes de duas chaves candidatas.",
                    "Porque a tabela exige juntar novamente o atributo Qtd para preservar a cobertura mínima original."
                ],
                "answer": "Porque contém a dependência transitiva NumOS → CPFCliente → NomeCliente via atributo não-primo CPFCliente.",
                "explanation": "Mesmo após separar as dependências parciais da 2FN, deixar NomeCliente dependente de CPFCliente dentro de OS_PESSOA gera dependência transitiva (viola 3FN)."
            },
            {
                "id": "f3",
                "label": "3) No Cenário 3, por que decompor EMP(CPF, CodDepto, NomeDepto) em { E1(CPF, NomeDepto), E2(CodDepto, NomeDepto) } falha gravemente se dois departamentos distintos puderem ter o mesmo NomeDepto?",
                "options": [
                    "Porque NomeDepto se torna chave primária de E1, proibindo dois empregados de trabalharem no mesmo setor.",
                    "Porque o SGBD bloqueia automaticamente qualquer coluna com o prefixo Nome dentro de duas tabelas.",
                    "Porque CPF passa a determinar NomeDepto de maneira parcial sobre uma chave candidata composta inexistente.",
                    "Porque E1 ∩ E2 = {NomeDepto} não é superchave nem de E1 nem de E2 (perde DFs e gera tuplas espúrias)."
                ],
                "answer": "Porque E1 ∩ E2 = {NomeDepto} não é superchave nem de E1 nem de E2 (perde DFs e gera tuplas espúrias).",
                "explanation": "O atributo de junção precisa ser chave (superchave) em pelo menos um dos lados — ou seja, CodDepto em EMP_OK(CPF, CodDepto) e DEPTO(CodDepto, NomeDepto)."
            }
        ]
    }
}
