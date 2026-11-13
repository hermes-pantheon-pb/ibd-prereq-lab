# -*- coding: utf-8 -*-
"""
Banco de Exercícios Oficial / Estilo Prova — Rodada 3 (Módulos 7 e 8)
2 Simulados Integrados Completos Estilo UFMG (5 etapas cada = 10 questões):
  - Simulado A (R3.1–R3.5, Grupo G9): Congresso Científico (Requisitos -> Desenho EER -> Leitura/Opções -> Mapeamento Lógico + RIRs -> SQL DDL -> Normalização Legado até 3FN)
  - Simulado B (R3.6–R3.10, Grupo G10): Plataforma de Leilões Online & Logística BCNF (Auditoria EER -> ASSERTION SQL-92 -> Detetive SQL DF -> R(M,N,P,Q,S) 3FN vs BCNF -> Definição Geral ENTREGA_DRONE)
"""

# ---------------------------------------------------------------------------
# Fichas de Estudo (Study Guides G9 & G10 — domínios paralelos aos simulados)
# ---------------------------------------------------------------------------

STUDY_GUIDE_G9 = {
    "id": "G9",
    "title": "G9 — Simulado A: Do Enunciado &amp; EER até DDL e 3FN",
    "file_path": "study_guides/G9_Simulado_A_Congresso_EER_para_3FN.md",
    "coursework_ref": "ibd-parte5.pdf (Etapas 1–2, EER o/d, Ternários, RIRs b/p/n) &amp; ibd-parte6.pdf (Normalização 1FN–3FN)",
    "quick_rules_html": """
<div class="sg-rules-box">
  <h4>Guia Rápido de Simulado — Prova A (Grupo G9)</h4>
  <ul>
    <li><strong>Etapa 1 (Requisitos &rarr; EER):</strong>
      <ul>
        <li>Papéis que uma mesma pessoa acumula simultaneamente usam sobreposição <code>o</code>; participação parcial usa linha simples.</li>
        <li>Subunidades numeradas dentro de outra entidade (ex.: sala dentro de evento/trilha) são <strong>Entidades Fracas</strong> (dupla borda + chave parcial pontilhada).</li>
      </ul>
    </li>
    <li><strong>Etapa 2 &amp; 3 (Mapeamento + RIRs):</strong> Opção <code>8A</code> para especialização <code>o</code> (tabelas separadas com <code>Si[PK] -p-&gt; C[PK]</code>); atributo multivalorado gera nova tabela com <code>-p-&gt;</code>; ternário gera tabela com PK tripla (se todos forem lado N).</li>
    <li><strong>Etapa 4 &amp; 5 (DDL &amp; 3FN):</strong> Traduza PK composta e <code>ON DELETE CASCADE</code> para SQLite e normalize tabelas legadas separando parciais (2FN) e transitivas (3FN).</li>
  </ul>
</div>
""",
    "example_html": """
<div class="sg-example-box">
  <h4>Exemplo Análogo: Mostra de Cinema (Domínio Diferente da Tarefa)</h4>
  <ul>
    <li><strong>Hierarquia <code>{o, parcial}</code> (8A):</strong> <code>PESSOA(<u>CPF</u>, Nome)</code>, <code>CURADOR(<u>CPF</u>, Reg)</code>, <code>CINEASTA(<u>CPF</u>, DRT)</code> com <code>-p-&gt; PESSOA</code>.</li>
    <li><strong>Fraca &amp; Ternário:</strong> <code>MOSTRA(<u>CodMostra</u>)</code> &rarr; <code>EXIBICAO(<u>CodMostra</u>, <u>SeqExib</u>, Sala)</code> (<code>CASCADE</code>); <code>JURADO_AVALIA(<u>CPF_Curador</u>, <u>CodFilme</u>, <u>CodCateg</u>, Pontos)</code> com <code>CHECK (Pontos BETWEEN 0 AND 100)</code>.</li>
    <li><strong>Planilha Legada de Ingressos:</strong> <code>VENDA_BRUTA(<u>NumBilhete</u>, <u>CodSecao</u>, Hora, CPF, Nome, CodCupom, PercDesc)</code> &rarr; 2FN separa <code>SECAO(<u>CodSecao</u>, Hora)</code> e <code>BILHETE</code> &rarr; 3FN separa <code>COMPRADOR(<u>CPF</u>, Nome)</code> e <code>CUPOM(<u>CodCupom</u>, PercDesc)</code>.</li>
  </ul>
</div>
"""
}

STUDY_GUIDE_G10 = {
    "id": "G10",
    "title": "G10 — Simulado B: Auditoria SQL, ASSERTION, 3FN vs BCNF &amp; Def. Geral",
    "file_path": "study_guides/G10_Simulado_B_Auditoria_SQL_BCNF_e_Chaves.md",
    "coursework_ref": "ibd-parte5.pdf (CREATE ASSERTION) &amp; ibd-parte6.pdf (Violação DF em SQL, Chaves Múltiplas, 2FN Geral, BCNF vs 3FN, NJP)",
    "quick_rules_html": """
<div class="sg-rules-box">
  <h4>Guia Rápido de Simulado — Prova B (Grupo G10)</h4>
  <ul>
    <li><strong>Invariantes SQL-92:</strong> Restrições que cruzam tabelas (como proibir auto-ação ou checar estado na tabela pai) usam <code>CREATE ASSERTION nome CHECK (NOT EXISTS (SELECT ... JOIN ...))</code>.</li>
    <li><strong>Violação de DF em SQL:</strong> Uma DF <code>X &rarr; Y</code> é refutada quando duas linhas compartilham o mesmo <code>X</code> mas possuem <code>Y</code> diferentes (<code>t1.X = t2.X AND t1.Y &lt;&gt; t2.Y AND t1.PK &lt; t2.PK</code>).</li>
    <li><strong>Múltiplas Chaves Candidatas &amp; BCNF:</strong> Calcule TODAS as chaves candidatas antes de testar 2FN (Definição Geral) e 3FN vs BCNF (se <code>A</code> for primo em <code>X &rarr; A</code>, aceito na 3FN mas proibido na BCNF).</li>
  </ul>
</div>
""",
    "example_html": """
<div class="sg-example-box">
  <h4>Exemplos Análogos: Galeria de Arte &amp; Esquema Abstrato <code>K(U, V, W, X, Y)</code></h4>
  <pre class="sql-code">-- Proibir curador de avaliar própria obra na Galeria:
CREATE ASSERTION SEM_AUTO_AVALIACAO CHECK (
  NOT EXISTS (
    SELECT 1 FROM AVALIACAO a JOIN OBRA o ON a.IdObra = o.IdObra
    WHERE a.CPFAvaliador = o.CPFArtista
  )
);</pre>
  <p><strong>Esquema Formal <code>K(U, V, W, X, Y)</code> com <code>F = { UV &rarr; W, VW &rarr; X, X &rarr; Y, Y &rarr; U }</code>:</strong></p>
  <ul>
    <li><strong>Chaves candidatas:</strong> <code>{UV}, {VW}, {VX}, {VY}</code> (todos os 5 atributos são <strong>primos</strong>!).</li>
    <li><strong>Classificação:</strong> Está em <strong>3FN</strong> (todo RHS é primo), porém viola <strong>BCNF</strong> (<code>X</code> e <code>Y</code> não são superchaves).</li>
    <li><strong>NJP binária:</strong> <code>D = { K1(U, V, W, X), K2(X, Y) }</code> tem interseção <code>{X}</code> e <code>X+ = {X, Y, U} &supseteq; K2</code> &rarr; <strong>Sem Perda</strong>!</li>
  </ul>
</div>
"""
}


# ---------------------------------------------------------------------------
# Exercícios da Rodada 3 (R3.1 .. R3.10)
# ---------------------------------------------------------------------------

ROUND3_EXERCISES = {
    "R3.1": {
        "title": "R3.1 [Simulado A — Etapa 1] Requisitos -> Modelagem EER (Congresso Científico)",
        "type": "oficial",
        "mode": "open_design",
        "study_guide": STUDY_GUIDE_G9,
        "context_html": """
<p><strong>Simulado A (Etapa 1 de 5 — Modelagem Conceitual Aberta):</strong> Leia atentamente o levantamento de requisitos abaixo e <strong>desenhe no seu caderno o Diagrama EER completo</strong> na notação dos slides (<code>(min, max)</code>, retângulo duplo, elipse dupla, círculo <code>o</code>/<code>d</code>):</p>
<div class="sg-rules-box">
  <ol>
    <li>O congresso cadastra <strong>Pessoas</strong> identificadas por <code>CPF</code>, com <code>Nome</code> e um atributo multivalorado <code>Emails</code>. Uma pessoa pode atuar opcionalmente como <strong>Autor</strong> (<code>Instituicao</code>) e/ou como <strong>Revisor</strong> (<code>AreaEspecialidade</code>), sendo perfeitamente comum que um autor também seja revisor (ou que seja apenas um palestrante convidado não enquadrado em nenhum dos dois grupos).</li>
    <li>Existem <strong>Trilhas</strong> temáticas (<code>CodTrilha</code>, <code>TituloTrilha</code>). Dentro de cada trilha existem várias <strong>Sessões</strong> numeradas sequencialmente a partir de 1 dentro da trilha (<code>NumSessao</code>, <code>Sala</code>), não existindo sessão sem trilha associada.</li>
    <li>Cada <strong>Artigo</strong> (<code>CodArtigo</code>, <code>Titulo</code>) pertence obrigatoriamente a uma única trilha e é escrito por pelo menos um autor (<code>M:N</code>, com atributo <code>OrdemAutoria</code>).</li>
    <li>A avaliação de um artigo envolve simultaneamente um <strong>Revisor</strong>, um <strong>Artigo</strong> e um <strong>Critério de Avaliação</strong> (<code>CodCrit</code>, <code>Descricao</code>), registrando uma <code>Nota</code> numérica na relação ternária <strong>PARECER</strong>.</li>
  </ol>
</div>
<p><em>Após desenhar o modelo no caderno, abra a Folha de Gabarito Visual abaixo para conferir seu diagrama com a solução oficial.</em></p>
""",
        "answer_sheet_html": """
<div class="answer-sheet-box">
  <h4>Gabarito Visual Oficial (Etapa 1 do Simulado A) — Diagrama EER do Congresso</h4>
  <div style="text-align:center; margin: 10px 0;">
  <svg viewBox="0 0 800 365" width="100%" style="max-width:780px; background:#0d1117; border:1px solid #30363d; border-radius:8px;">
    <!-- PESSOA + multivalued Emails -->
    <rect x="40" y="34" width="148" height="46" rx="4" fill="#161b22" stroke="#58a6ff" stroke-width="2.2"/>
    <text x="114" y="54" text-anchor="middle" fill="#f0f6fc" font-size="12" font-weight="700">PESSOA</text>
    <text x="114" y="70" text-anchor="middle" fill="#8b949e" font-size="10">(<tspan text-decoration="underline">CPF</tspan>, Nome)</text>
    <ellipse cx="242" cy="40" rx="42" ry="18" fill="#161b22" stroke="#79c0ff" stroke-width="1.4"/>
    <ellipse cx="242" cy="40" rx="37" ry="13" fill="none" stroke="#79c0ff" stroke-width="1.2"/>
    <text x="242" y="44" text-anchor="middle" fill="#e6edf3" font-size="10">Emails</text>
    <line x1="188" y1="48" x2="200" y2="43" stroke="#8b949e" stroke-width="1.4"/>

    <!-- EER (o, partial): single line + circle 'o' -->
    <line x1="114" y1="80" x2="114" y2="106" stroke="#8b949e" stroke-width="1.6"/>
    <circle cx="114" cy="120" r="14" fill="#161b22" stroke="#3fb950" stroke-width="2"/>
    <text x="114" y="124" text-anchor="middle" fill="#3fb950" font-size="12" font-weight="700">o</text>
    <line x1="102" y1="128" x2="62" y2="155" stroke="#8b949e" stroke-width="1.5"/>
    <line x1="126" y1="128" x2="180" y2="155" stroke="#8b949e" stroke-width="1.5"/>

    <!-- AUTOR -->
    <rect x="14" y="155" width="106" height="44" rx="4" fill="#161b22" stroke="#3fb950" stroke-width="1.8"/>
    <text x="67" y="174" text-anchor="middle" fill="#f0f6fc" font-size="11" font-weight="700">AUTOR</text>
    <text x="67" y="189" text-anchor="middle" fill="#8b949e" font-size="9">(Instituicao)</text>

    <!-- REVISOR -->
    <rect x="132" y="155" width="122" height="44" rx="4" fill="#161b22" stroke="#3fb950" stroke-width="1.8"/>
    <text x="193" y="174" text-anchor="middle" fill="#f0f6fc" font-size="11" font-weight="700">REVISOR</text>
    <text x="193" y="189" text-anchor="middle" fill="#8b949e" font-size="9">(AreaEspecial.)</text>

    <!-- M:N ESCREVE between AUTOR and ARTIGO -->
    <line x1="67" y1="199" x2="67" y2="275" stroke="#8b949e" stroke-width="1.5"/>
    <text x="48" y="236" text-anchor="middle" fill="#79c0ff" font-size="10">(0,N)</text>
    <polygon points="105,275 152,248 199,275 152,302" fill="#1f2937" stroke="#d2a8ff" stroke-width="1.8"/>
    <text x="152" y="279" text-anchor="middle" fill="#d2a8ff" font-size="10" font-weight="700">ESCREVE</text>
    <text x="152" y="317" text-anchor="middle" fill="#e6edf3" font-size="9">(OrdemAutoria)</text>
    <line x1="67" y1="275" x2="105" y2="275" stroke="#8b949e" stroke-width="1.5"/>
    <line x1="199" y1="272" x2="295" y2="272" stroke="#58a6ff" stroke-width="1.5"/>
    <line x1="199" y1="278" x2="295" y2="278" stroke="#58a6ff" stroke-width="1.5"/>
    <text x="247" y="264" text-anchor="middle" fill="#79c0ff" font-size="10">(1, N)</text>

    <!-- ARTIGO -->
    <rect x="295" y="252" width="136" height="46" rx="4" fill="#161b22" stroke="#58a6ff" stroke-width="2.2"/>
    <text x="363" y="272" text-anchor="middle" fill="#f0f6fc" font-size="12" font-weight="700">ARTIGO</text>
    <text x="363" y="288" text-anchor="middle" fill="#8b949e" font-size="10">(<tspan text-decoration="underline">CodArtigo</tspan>, Titulo)</text>

    <!-- Ternary PARECER (Revisor, Artigo, Criterio) -->
    <polygon points="348,170 400,142 452,170 400,198" fill="#1f2937" stroke="#f2cc60" stroke-width="2"/>
    <text x="400" y="174" text-anchor="middle" fill="#f2cc60" font-size="10" font-weight="700">PARECER</text>
    <text x="400" y="134" text-anchor="middle" fill="#f2cc60" font-size="9">Attr: Nota</text>
    <line x1="254" y1="172" x2="348" y2="170" stroke="#8b949e" stroke-width="1.5"/>
    <text x="301" y="163" text-anchor="middle" fill="#ffa657" font-size="10">N</text>
    <line x1="400" y1="198" x2="363" y2="252" stroke="#8b949e" stroke-width="1.5"/>
    <text x="394" y="228" text-anchor="middle" fill="#ffa657" font-size="10">M</text>
    <line x1="452" y1="170" x2="520" y2="170" stroke="#8b949e" stroke-width="1.5"/>
    <text x="486" y="162" text-anchor="middle" fill="#ffa657" font-size="10">P</text>

    <!-- CRITERIO -->
    <rect x="520" y="148" width="132" height="44" rx="4" fill="#161b22" stroke="#58a6ff" stroke-width="2"/>
    <text x="586" y="168" text-anchor="middle" fill="#f0f6fc" font-size="11" font-weight="700">CRITERIO</text>
    <text x="586" y="183" text-anchor="middle" fill="#8b949e" font-size="10">(<tspan text-decoration="underline">CodCrit</tspan>, Desc)</text>

    <!-- TRILHA -> TEM -> SESSAO (Weak) and ARTIGO -> PERTENCE -> TRILHA -->
    <rect x="330" y="34" width="142" height="46" rx="4" fill="#161b22" stroke="#58a6ff" stroke-width="2.2"/>
    <text x="401" y="54" text-anchor="middle" fill="#f0f6fc" font-size="12" font-weight="700">TRILHA</text>
    <text x="401" y="70" text-anchor="middle" fill="#8b949e" font-size="10">(<tspan text-decoration="underline">CodTrilha</tspan>, TituloTr.)</text>

    <!-- ARTIGO / PERTENCE / TRILHA -->
    <line x1="431" y1="272" x2="490" y2="272" stroke="#58a6ff" stroke-width="1.5"/>
    <line x1="431" y1="278" x2="490" y2="278" stroke="#58a6ff" stroke-width="1.5"/>
    <text x="460" y="264" text-anchor="middle" fill="#79c0ff" font-size="9">(1,1)</text>
    <polygon points="490,275 535,248 580,275 535,302" fill="#1f2937" stroke="#58a6ff" stroke-width="1.8"/>
    <text x="535" y="279" text-anchor="middle" fill="#79c0ff" font-size="9" font-weight="700">PERTENCE</text>
    <path d="M 580,275 L 705,275 L 705,108 L 401,108 L 401,80" fill="none" stroke="#8b949e" stroke-width="1.5"/>
    <text x="422" y="99" text-anchor="middle" fill="#79c0ff" font-size="9">(0,N)</text>

    <!-- Identifying TEM_SESSAO -->
    <line x1="472" y1="57" x2="522" y2="57" stroke="#8b949e" stroke-width="1.5"/>
    <text x="497" y="48" text-anchor="middle" fill="#79c0ff" font-size="9">(1,N)</text>
    <polygon points="522,57 556,34 590,57 556,80" fill="#1f2937" stroke="#f0883e" stroke-width="2"/>
    <polygon points="528,57 556,39 584,57 556,75" fill="none" stroke="#f0883e" stroke-width="1.2"/>
    <text x="556" y="61" text-anchor="middle" fill="#f0883e" font-size="9" font-weight="700">TEM</text>
    <line x1="590" y1="54" x2="625" y2="54" stroke="#f0883e" stroke-width="1.5"/>
    <line x1="590" y1="60" x2="625" y2="60" stroke="#f0883e" stroke-width="1.5"/>
    <text x="607" y="45" text-anchor="middle" fill="#ffa657" font-size="9">(1,1)</text>

    <!-- SESSAO (Weak) -->
    <rect x="625" y="32" width="128" height="50" rx="4" fill="#161b22" stroke="#f0883e" stroke-width="2"/>
    <rect x="630" y="37" width="118" height="40" rx="2" fill="none" stroke="#f0883e" stroke-width="1.2"/>
    <text x="689" y="54" text-anchor="middle" fill="#f0f6fc" font-size="11" font-weight="700">SESSAO</text>
    <text x="689" y="69" text-anchor="middle" fill="#ffa657" font-size="9">({NumSessao}, Sala)</text>
  </svg>
  </div>
  <ul>
    <li><strong>Checklist de Conferência:</strong> (1) Círculo <code>o</code> com linha simples para <code>PESSOA</code> (parcial + sobreposição); (2) Elipse dupla em <code>Emails</code>; (3) Retângulo duplo e losango identificador para <code>SESSAO</code> (chave parcial <code>NumSessao</code>); (4) Relação ternária <code>PARECER(Nota)</code> ligando <code>REVISOR</code>, <code>ARTIGO</code> e <code>CRITERIO</code>.</li>
  </ul>
</div>
""",
        "fields": []
    },

    "R3.2": {
        "title": "R3.2 [Simulado A — Etapa 2] Leitura do EER &amp; Decisões de Projeto (8A vs 8C)",
        "type": "oficial",
        "mode": "structured",
        "study_guide": STUDY_GUIDE_G9,
        "context_html": """
<p><strong>Simulado A (Etapa 2 de 5 — Leitura Crítica do EER Oficial):</strong> Considere o Diagrama EER consolidado do <strong>Congresso Científico</strong> abaixo para responder às decisões de projeto lógico antes da geração das tabelas:</p>
<div style="text-align:center; margin: 10px 0;">
<svg viewBox="0 0 780 265" width="100%" style="max-width:760px; background:#0d1117; border:1px solid #30363d; border-radius:8px;">
  <rect x="24" y="20" width="160" height="42" rx="4" fill="#161b22" stroke="#58a6ff" stroke-width="2"/>
  <text x="104" y="38" text-anchor="middle" fill="#f0f6fc" font-size="11" font-weight="700">PESSOA (<tspan text-decoration="underline">CPF</tspan>, Nome)</text>
  <text x="104" y="53" text-anchor="middle" fill="#79c0ff" font-size="9">Multivalorado: {{Emails}}</text>
  <line x1="104" y1="62" x2="104" y2="85" stroke="#8b949e" stroke-width="1.5"/>
  <circle cx="104" cy="98" r="12" fill="#161b22" stroke="#3fb950" stroke-width="2"/>
  <text x="104" y="102" text-anchor="middle" fill="#3fb950" font-size="11" font-weight="700">o</text>
  <line x1="94" y1="106" x2="56" y2="132" stroke="#8b949e" stroke-width="1.5"/>
  <line x1="114" y1="106" x2="156" y2="132" stroke="#8b949e" stroke-width="1.5"/>
  <rect x="12" y="132" width="88" height="36" rx="4" fill="#161b22" stroke="#3fb950" stroke-width="1.8"/>
  <text x="56" y="154" text-anchor="middle" fill="#f0f6fc" font-size="10" font-weight="700">AUTOR</text>
  <rect x="110" y="132" width="92" height="36" rx="4" fill="#161b22" stroke="#3fb950" stroke-width="1.8"/>
  <text x="156" y="154" text-anchor="middle" fill="#f0f6fc" font-size="10" font-weight="700">REVISOR</text>

  <!-- Center: TRILHA -> TEM -> SESSAO (Weak) -->
  <rect x="265" y="20" width="142" height="42" rx="4" fill="#161b22" stroke="#58a6ff" stroke-width="2"/>
  <text x="336" y="38" text-anchor="middle" fill="#f0f6fc" font-size="11" font-weight="700">TRILHA</text>
  <text x="336" y="53" text-anchor="middle" fill="#8b949e" font-size="9">(<tspan text-decoration="underline">CodTrilha</tspan>, Titulo)</text>
  <line x1="407" y1="41" x2="450" y2="41" stroke="#8b949e" stroke-width="1.5"/>
  <text x="428" y="32" text-anchor="middle" fill="#79c0ff" font-size="9">(1,N)</text>
  <polygon points="450,41 484,18 518,41 484,64" fill="#1f2937" stroke="#f0883e" stroke-width="1.8"/>
  <polygon points="456,41 484,23 512,41 484,59" fill="none" stroke="#f0883e" stroke-width="1.2"/>
  <text x="484" y="45" text-anchor="middle" fill="#f0883e" font-size="9" font-weight="700">TEM</text>
  <line x1="518" y1="38" x2="560" y2="38" stroke="#f0883e" stroke-width="1.5"/>
  <line x1="518" y1="44" x2="560" y2="44" stroke="#f0883e" stroke-width="1.5"/>
  <text x="539" y="30" text-anchor="middle" fill="#ffa657" font-size="9">(1,1)</text>
  <rect x="560" y="18" width="134" height="46" rx="4" fill="#161b22" stroke="#f0883e" stroke-width="2"/>
  <rect x="565" y="23" width="124" height="36" rx="2" fill="none" stroke="#f0883e" stroke-width="1.2"/>
  <text x="627" y="39" text-anchor="middle" fill="#f0f6fc" font-size="11" font-weight="700">SESSAO</text>
  <text x="627" y="53" text-anchor="middle" fill="#ffa657" font-size="9">({NumSessao}, Sala)</text>

  <!-- Bottom: Ternary PARECER (REVISOR, ARTIGO, CRITERIO) -->
  <rect x="305" y="102" width="132" height="42" rx="4" fill="#161b22" stroke="#58a6ff" stroke-width="2"/>
  <text x="371" y="121" text-anchor="middle" fill="#f0f6fc" font-size="11" font-weight="700">ARTIGO</text>
  <text x="371" y="135" text-anchor="middle" fill="#8b949e" font-size="9">(<tspan text-decoration="underline">CodArtigo</tspan>, Titulo)</text>

  <polygon points="322,204 371,176 420,204 371,232" fill="#1f2937" stroke="#f2cc60" stroke-width="2"/>
  <text x="371" y="208" text-anchor="middle" fill="#f2cc60" font-size="10" font-weight="700">PARECER</text>
  <text x="415" y="247" text-anchor="middle" fill="#e6edf3" font-size="9">Attr: Nota</text>

  <!-- REVISOR(N) -> PARECER -->
  <path d="M 156,168 L 156,204 L 322,204" fill="none" stroke="#8b949e" stroke-width="1.5"/>
  <text x="235" y="196" text-anchor="middle" fill="#ffa657" font-size="10">N</text>
  <!-- ARTIGO(M) -> PARECER -->
  <line x1="371" y1="144" x2="371" y2="176" stroke="#8b949e" stroke-width="1.5"/>
  <text x="383" y="164" text-anchor="middle" fill="#ffa657" font-size="10">M</text>
  <!-- CRITERIO(P) -> PARECER -->
  <line x1="420" y1="204" x2="545" y2="204" stroke="#8b949e" stroke-width="1.5"/>
  <text x="482" y="196" text-anchor="middle" fill="#ffa657" font-size="10">P</text>

  <rect x="545" y="182" width="142" height="44" rx="4" fill="#161b22" stroke="#58a6ff" stroke-width="2"/>
  <text x="616" y="201" text-anchor="middle" fill="#f0f6fc" font-size="11" font-weight="700">CRITERIO</text>
  <text x="616" y="216" text-anchor="middle" fill="#8b949e" font-size="9">(<tspan text-decoration="underline">CodCrit</tspan>, Desc)</text>
</svg>
</div>
""",
        "answer_sheet_html": """
<div class="answer-sheet-box">
  <h4>Gabarito Explicado — R3.2 (Simulado A — Etapa 2)</h4>
  <ul>
    <li><strong>Hierarquia <code>{o, parcial}</code>:</strong> Como <code>AUTOR</code> participa de <code>ESCREVE</code> e <code>REVISOR</code> participa de <code>PARECER</code> (além de ser sobreposta <code>o</code> e parcial), a <strong>Opção 8A</strong> (3 tabelas: <code>PESSOA</code>, <code>AUTOR</code> e <code>REVISOR</code>) evita <code>NULL</code>s em massa e permite FKs separadas precisas.</li>
    <li><strong><code>SESSAO</code> (Fraca):</strong> Sua chave primária no relacional obrigatoriamente é <code>(CodTrilha, NumSessao)</code>; <code>NumSessao</code> sozinho é apenas discriminador parcial.</li>
    <li><strong>Relação Ternária <code>PARECER</code>:</strong> Não se reduz a 3 relações binárias sem perder qual nota foi atribuída por qual revisor em qual critério para o artigo; cria-se uma tabela com a PK composta das 3 chaves <code>(CPF_Revisor, CodArtigo, CodCrit)</code>.</li>
  </ul>
</div>
""",
        "fields": [
            {
                "id": "f1",
                "label": "1) Qual opção de mapeamento EER melhor traduz PESSOA -> {AUTOR, REVISOR} (sobreposta 'o' e parcial) quando cada subclasse possui relacionamentos próprios?",
                "options": [
                    "Opção 8B apenas, apagando PESSOA e duplicando Nome completo tanto em AUTOR quanto em REVISOR.",
                    "Opção 8C com um único atributo TipoPessoa CHAR(1) impedindo que um autor seja simultaneamente revisor.",
                    "Opção 8A (tabelas PESSOA, AUTOR e REVISOR ligadas por PK/FK CPF), evitando múltiplos NULLs e mantendo FKs específicas.",
                    "Eliminar as subclasses do modelo lógico e colocar AreaEspecialidade opcional dentro de ARTIGO."
                ],
                "answer": "Opção 8A (tabelas PESSOA, AUTOR e REVISOR ligadas por PK/FK CPF), evitando múltiplos NULLs e mantendo FKs específicas.",
                "explanation": "A Opção 8A funciona para qualquer especialização (d ou o, total ou parcial) e mantém os relacionamentos específicos ESCREVE (em AUTOR) e PARECER (em REVISOR) íntegros."
            },
            {
                "id": "f2",
                "label": "2) Sobre a entidade fraca SESSAO ligada a TRILHA por TEM, qual afirmação é verdadeira no Diagrama EER?",
                "options": [
                    "NumSessao é apenas uma chave parcial (sublinhado pontilhado) e só identifica unicamente uma sessão quando combinada a CodTrilha.",
                    "SESSAO não precisa participar totalmente (1,1) de TEM, podendo existir sessões independentes sem trilha.",
                    "NumSessao já é chave primária global única, dispensando propagar CodTrilha para a relação SESSAO.",
                    "A linha dupla entre TRILHA e TEM indica que toda trilha tem no máximo uma única sessão cadastrada."
                ],
                "answer": "NumSessao é apenas uma chave parcial (sublinhado pontilhado) e só identifica unicamente uma sessão quando combinada a CodTrilha.",
                "explanation": "A sessão 1 da Trilha A e a sessão 1 da Trilha B têm o mesmo NumSessao; a participação total (1,1) na linha dupla e o losango identificador exigem a chave composta (CodTrilha, NumSessao)."
            },
            {
                "id": "f3",
                "label": "3) Por que o relacionamento ternário PARECER(Revisor, Artigo, Criterio) não pode ser substituído por três relacionamentos binários equivalentes?",
                "options": [
                    "Porque o modelo relacional proíbe mais de duas FKs dentro de uma tabela associativa com atributos.",
                    "Porque relações binárias separadas perdem a associação exata de qual revisor deu qual nota em qual critério do artigo.",
                    "Porque toda relação envolvendo uma subclasse EER exige grau igual ou inferior a dois no diagrama final.",
                    "Porque o atributo Nota precisa ser armazenado diretamente dentro da entidade CRITERIO sem repetir por artigo."
                ],
                "answer": "Porque relações binárias separadas perdem a associação exata de qual revisor deu qual nota em qual critério do artigo.",
                "explanation": "Três relações binárias (Revisor-Artigo, Artigo-Critério, Revisor-Critério) gerariam junções espúrias e não saberiam vincular a Nota específica ao trio exato."
            }
        ]
    },

    "R3.3": {
        "title": "R3.3 [Simulado A — Etapa 3] Esquema Lógico Completo &amp; RIRs (-b->, -p->, -n->)",
        "type": "oficial",
        "mode": "structured",
        "study_guide": STUDY_GUIDE_G9,
        "context_html": """
<p><strong>Simulado A (Etapa 3 de 5 — Esquema Lógico Formal e RIRs):</strong> A partir do mesmo diagrama EER do <strong>Congresso Científico</strong>, o aluno escreveu um rascunho de mapeamento lógico contendo todas as relações e políticas de remoção (<code>-b-&gt;</code> bloqueia/restrict, <code>-p-&gt;</code> propaga/cascade, <code>-n-&gt;</code> anula/set null).</p>
<pre class="sql-code">PESSOA(<u>CPF</u>, Nome)
PESSOA_EMAILS(<u>CPF</u>, <u>Email</u>)
AUTOR(<u>CPF</u>, Instituicao)
REVISOR(<u>CPF</u>, AreaEspecialidade)
TRILHA(<u>CodTrilha</u>, TituloTrilha)
SESSAO(<u>CodTrilha</u>, <u>NumSessao</u>, Sala)
ARTIGO(<u>CodArtigo</u>, Titulo, CodTrilha)
ESCREVE(<u>CPF_Autor</u>, <u>CodArtigo</u>, OrdemAutoria)
CRITERIO(<u>CodCrit</u>, Descricao)
PARECER(<u>CPF_Revisor</u>, <u>CodArtigo</u>, <u>CodCrit</u>, Nota)</pre>
<p>Avalie exatamente as <strong>chaves primárias</strong> e <strong>políticas RIR</strong> ideais para esse esquema lógico.</p>
""",
        "answer_sheet_html": """
<div class="answer-sheet-box">
  <h4>Gabarito Explicado — R3.3 (Simulado A — Etapa 3)</h4>
  <ul>
    <li><strong><code>PESSOA_EMAILS</code> e <code>SESSAO</code>:</strong> Ambos carregam a PK do dono dentro de sua própria PK; logo o padrão é <code>-p-&gt;</code> (<code>CASCADE</code>): se a pessoa ou a trilha forem apagadas, não podem existir e-mails ou sessões órfãs nem FKs nulas em PK.</li>
    <li><strong><code>ARTIGO[CodTrilha]</code>:</strong> Como cada artigo pertence obrigatoriamente a uma trilha (<code>NOT NULL</code>), usa-se <code>-b-&gt; TRILHA[CodTrilha]</code> (<code>RESTRICT</code>) para impedir a exclusão acidental de uma trilha que já recebeu submissões (não pode usar <code>-n-&gt;</code> porque <code>CodTrilha</code> é <code>NOT NULL</code>).</li>
    <li><strong><code>PARECER</code>:</strong> A PK composta das três FKs <code>(CPF_Revisor, CodArtigo, CodCrit)</code> impede perda de identidade da nota avaliada.</li>
  </ul>
</div>
""",
        "fields": [
            {
                "id": "f1",
                "label": "1) Qual política RIR deve ser declarada nas FKs de PESSOA_EMAILS[CPF] e SESSAO[CodTrilha] ao apagar o pai?",
                "options": [
                    "Anulação (-n->), definindo CPF ou CodTrilha como NULL quando o registro pai for removido.",
                    "Apenas índice único sem declaração de RIR, permitindo que e-mails e sessões sobrevivam livres.",
                    "Anulação (-n->) em SESSAO e bloqueio (-b->) apenas para emails primários duplicados.",
                    "Propagação (-p-> / ON DELETE CASCADE), pois a FK compõe a própria chave primária da dependente."
                ],
                "answer": "Propagação (-p-> / ON DELETE CASCADE), pois a FK compõe a própria chave primária da dependente.",
                "explanation": "Tanto no atributo multivalorado PESSOA_EMAILS quanto na entidade fraca SESSAO, a FK faz parte da PK (jamais aceita NULL), usando-se propagação (-p->) na exclusão do pai."
            },
            {
                "id": "f2",
                "label": "2) Para ARTIGO(CodArtigo, Titulo, CodTrilha) com CodTrilha NOT NULL, qual RIR evita excluir uma trilha com artigos submetidos?",
                "options": [
                    "ARTIGO[CodTrilha] -n-> TRILHA[CodTrilha] (SET NULL na exclusão da trilha).",
                    "ARTIGO[CodTrilha] -b-> TRILHA[CodTrilha] (RESTRICT / bloqueia exclusão se houver artigos).",
                    "TRILHA[CodTrilha] -p-> ARTIGO[CodArtigo] invertendo o sentido da chave estrangeira.",
                    "ARTIGO[CodArtigo] -p-> TRILHA[CodTrilha] removendo todos os revisores da trilha."
                ],
                "answer": "ARTIGO[CodTrilha] -b-> TRILHA[CodTrilha] (RESTRICT / bloqueia exclusão se houver artigos).",
                "explanation": "Como todo artigo tem participação total (1,1) em TRILHA (CodTrilha NOT NULL), não se pode anular (-n->); usa-se bloqueio (-b->) para proteger artigos já submetidos."
            },
            {
                "id": "f3",
                "label": "3) Qual é a chave primária correta da tabela associativa M:N ESCREVE e da ternária PARECER?",
                "options": [
                    "ESCREVE(CPF_Autor) com OrdemAutoria única, e PARECER(CodArtigo, Nota) permitindo múltiplos critérios.",
                    "ESCREVE(CodArtigo, OrdemAutoria) e PARECER(CPF_Revisor, CodCrit) sem incluir CodArtigo na PK.",
                    "ESCREVE(CPF_Autor, CodArtigo) com FK dupla, e PARECER(CPF_Revisor, CodArtigo, CodCrit) com FK tripla.",
                    "ESCREVE(CPF_Autor, CodArtigo, OrdemAutoria) e PARECER(CodArtigo) como tabela de relação 1:N."
                ],
                "answer": "ESCREVE(CPF_Autor, CodArtigo) com FK dupla, e PARECER(CPF_Revisor, CodArtigo, CodCrit) com FK tripla.",
                "explanation": "Em M:N, a PK concatena as PKs dos dois lados (CPF_Autor, CodArtigo); no ternário M:N:P, concatena todas as três PKs participantes."
            }
        ]
    },

    "R3.4": {
        "title": "R3.4 [Simulado A — Etapa 4] SQL DDL do Congresso (Fraca, RIR &amp; CHECK)",
        "type": "oficial",
        "mode": "sql_ddl",
        "study_guide": STUDY_GUIDE_G9,
        "setup": "",
        "context_html": """
<p><strong>Simulado A (Etapa 4 de 5 — Implementação SQL DDL):</strong> Implemente em SQLite DDL o núcleo estrutural do Congresso abaixo com todas as chaves primárias, estrangeiras, políticas de deleção e regra de domínio:</p>
<ul>
  <li><code>TRILHA(CodTrilha INTEGER PK, Titulo TEXT NOT NULL)</code></li>
  <li><code>SESSAO(CodTrilha INTEGER, NumSessao INTEGER, Sala TEXT NOT NULL)</code> &mdash; entidade fraca de <code>TRILHA</code> com PK composta e <code>ON DELETE CASCADE</code>.</li>
  <li><code>ARTIGO(CodArtigo INTEGER PK, Titulo TEXT NOT NULL, CodTrilha INTEGER NOT NULL)</code> &mdash; FK para <code>TRILHA</code> com <code>ON DELETE RESTRICT</code>.</li>
  <li><code>PARECER(CPFRevisor TEXT, CodArtigo INTEGER, CodCrit INTEGER, Nota REAL NOT NULL)</code> &mdash; PK tripla <code>(CPFRevisor, CodArtigo, CodCrit)</code>, FK para <code>ARTIGO(CodArtigo)</code> e restrição <code>CHECK (Nota &gt;= 0 AND Nota &lt;= 10)</code>.</li>
</ul>
""",
        "answer_sheet_html": """
<div class="answer-sheet-box">
  <h4>Gabarito SQL DDL — R3.4 (Simulado A — Etapa 4)</h4>
  <pre class="sql-code">CREATE TABLE TRILHA (
  CodTrilha INTEGER PRIMARY KEY,
  Titulo    TEXT NOT NULL
);

CREATE TABLE SESSAO (
  CodTrilha INTEGER NOT NULL,
  NumSessao INTEGER NOT NULL,
  Sala      TEXT NOT NULL,
  PRIMARY KEY (CodTrilha, NumSessao),
  FOREIGN KEY (CodTrilha) REFERENCES TRILHA(CodTrilha) ON DELETE CASCADE
);

CREATE TABLE ARTIGO (
  CodArtigo INTEGER PRIMARY KEY,
  Titulo    TEXT NOT NULL,
  CodTrilha INTEGER NOT NULL,
  FOREIGN KEY (CodTrilha) REFERENCES TRILHA(CodTrilha) ON DELETE RESTRICT
);

CREATE TABLE PARECER (
  CPFRevisor TEXT NOT NULL,
  CodArtigo  INTEGER NOT NULL,
  CodCrit    INTEGER NOT NULL,
  Nota       REAL NOT NULL CHECK (Nota &gt;= 0 AND Nota &lt;= 10),
  PRIMARY KEY (CPFRevisor, CodArtigo, CodCrit),
  FOREIGN KEY (CodArtigo) REFERENCES ARTIGO(CodArtigo)
);</pre>
</div>
""",
        "ddl_tests": [
            {
                "name": "Existência das 4 tabelas (TRILHA, SESSAO, ARTIGO, PARECER)",
                "type": "tables_exist",
                "tables": ["TRILHA", "SESSAO", "ARTIGO", "PARECER"],
                "hint": "Verifique os nomes exatos: TRILHA, SESSAO, ARTIGO e PARECER."
            },
            {
                "name": "Aceitar sessões homônimas em trilhas distintas e parecer com nota válida",
                "type": "must_succeed",
                "sql": """
                    INSERT INTO TRILHA VALUES (1, 'Banco de Dados'), (2, 'Inteligência Artificial');
                    INSERT INTO SESSAO VALUES (1, 1, 'Aud. 1'), (2, 1, 'Aud. 2');
                    INSERT INTO ARTIGO VALUES (100, 'BCNF na Prática', 1);
                    INSERT INTO PARECER VALUES ('111', 100, 1, 9.5), ('222', 100, 1, 8.0);
                """,
                "hint": "Sessões (1, 1) e (2, 1) e pareceres com Nota entre 0 e 10 devem ser aceitos."
            },
            {
                "name": "Bloquear Nota fora de [0, 10] via CHECK em PARECER",
                "type": "must_fail",
                "sql": """
                    INSERT INTO TRILHA VALUES (1, 'BD');
                    INSERT INTO ARTIGO VALUES (100, 'Artigo X', 1);
                    INSERT INTO PARECER VALUES ('111', 100, 1, 12.5);
                """,
                "hint": "Adicione CHECK (Nota >= 0 AND Nota <= 10) na tabela PARECER."
            },
            {
                "name": "Bloquear remoção de TRILHA que possui ARTIGO (ON DELETE RESTRICT)",
                "type": "must_fail",
                "sql": """
                    INSERT INTO TRILHA VALUES (1, 'BD');
                    INSERT INTO ARTIGO VALUES (100, 'Artigo X', 1);
                    DELETE FROM TRILHA WHERE CodTrilha = 1;
                """,
                "hint": "ARTIGO.CodTrilha deve referenciar TRILHA(CodTrilha) com ON DELETE RESTRICT."
            },
            {
                "name": "Propagar remoção de TRILHA para suas SESSOES (ON DELETE CASCADE)",
                "type": "cascade_check",
                "sql_setup": """
                    INSERT INTO TRILHA VALUES (1, 'BD'), (2, 'IA');
                    INSERT INTO SESSAO VALUES (1, 1, 'S101'), (1, 2, 'S102'), (2, 1, 'S201');
                    DELETE FROM TRILHA WHERE CodTrilha = 1;
                """,
                "verify_query": "SELECT COUNT(*) FROM SESSAO WHERE CodTrilha = 1;",
                "expected_scalar": 0,
                "hint": "SESSAO deve ter ON DELETE CASCADE na FK CodTrilha."
            }
        ]
    },

    "R3.5": {
        "title": "R3.5 [Simulado A — Etapa 5] Normalização da Planilha Legada do Congresso (1FN &rarr; 3FN)",
        "type": "oficial",
        "mode": "structured",
        "study_guide": STUDY_GUIDE_G9,
        "context_html": """
<p><strong>Simulado A (Etapa 5 de 5 — Fechamento com Normalização):</strong> Antes da implantação do novo banco, a secretaria do congresso controlava inscrições e trilhas em uma planilha legada já em 1FN:</p>
<pre class="sql-code">INSC_BRUTA(<u>CodInscr</u>, <u>CodTrilha</u>, DataAloc, CPF, NomeAutor, Instituicao, CodPacote, ValorPacote, TituloTrilha)</pre>
<p><strong>Dependências funcionais observadas:</strong></p>
<pre class="sql-code">F = {
  {CodInscr, CodTrilha} &rarr; DataAloc
  CodInscr &rarr; CPF, CodPacote
  CPF &rarr; NomeAutor, Instituicao
  CodPacote &rarr; ValorPacote
  CodTrilha &rarr; TituloTrilha
}</pre>
<p>Normalize <code>INSC_BRUTA</code> até a <strong>3FN</strong> sem perda de informação.</p>
""",
        "answer_sheet_html": """
<div class="answer-sheet-box">
  <h4>Gabarito Completo — R3.5 (Simulado A — Etapa 5)</h4>
  <ul>
    <li><strong>Violação de 2FN:</strong> A única chave candidata é <code>{CodInscr, CodTrilha}</code>. Porém, <code>CodTrilha &rarr; TituloTrilha</code> e <code>CodInscr &rarr; CPF, NomeAutor, Instituicao, CodPacote, ValorPacote</code> dependem apenas de parte da chave.</li>
    <li><strong>Saída da 2FN:</strong><br>
    <code>TRILHA(<u>CodTrilha</u>, TituloTrilha)</code> (já em 3FN)<br>
    <code>INSC_TRILHA(<u>CodInscr</u>, <u>CodTrilha</u>, DataAloc)</code> (já em 3FN)<br>
    <code>INSC_2FN(<u>CodInscr</u>, CPF, NomeAutor, Instituicao, CodPacote, ValorPacote)</code> (ainda viola <strong>3FN</strong>!).</li>
    <li><strong>Violação de 3FN em <code>INSC_2FN</code>:</strong> Existem duas cadeias transitivas: <code>CodInscr &rarr; CPF &rarr; {NomeAutor, Instituicao}</code> e <code>CodInscr &rarr; CodPacote &rarr; ValorPacote</code>.</li>
    <li><strong>Esquema Final 3FN (5 tabelas):</strong> <code>AUTOR(<u>CPF</u>, NomeAutor, Instituicao)</code>, <code>PACOTE(<u>CodPacote</u>, ValorPacote)</code>, <code>INSCRICAO(<u>CodInscr</u>, CPF, CodPacote)</code>, <code>TRILHA(<u>CodTrilha</u>, TituloTrilha)</code>, <code>INSC_TRILHA(<u>CodInscr</u>, <u>CodTrilha</u>, DataAloc)</code>.</li>
  </ul>
</div>
""",
        "fields": [
            {
                "id": "f1",
                "label": "1) Quais dependências funcionais causam violação da 2FN em INSC_BRUTA?",
                "options": [
                    "As dependências parciais CodInscr → CPF, CodPacote (e transitivas delas) e CodTrilha → TituloTrilha sobre a PK composta.",
                    "Exclusivamente {CodInscr, CodTrilha} → DataAloc, porque DataAloc depende da união completa da chave.",
                    "Apenas CPF → NomeAutor, pois CPF não pertence diretamente à chave primária composta da relação.",
                    "Nenhuma dependência viola a 2FN, uma vez que DataAloc já depende de toda a chave primária."
                ],
                "answer": "As dependências parciais CodInscr → CPF, CodPacote (e transitivas delas) e CodTrilha → TituloTrilha sobre a PK composta.",
                "explanation": "Todos os atributos que dependem somente de CodInscr ou somente de CodTrilha são dependências parciais da chave candidata {CodInscr, CodTrilha}."
            },
            {
                "id": "f2",
                "label": "2) Após passar para a 2FN isolando TRILHA e INSC_TRILHA, por que INSC_2FN(CodInscr, CPF, NomeAutor, Instituicao, CodPacote, ValorPacote) ainda não está em 3FN?",
                "options": [
                    "Porque CodInscr pode aparecer associado a múltiplos pacotes simultâneos em uma mesma inscrição.",
                    "Porque Instituicao forma uma chave candidata alternativa composta junto com TituloTrilha.",
                    "Porque CPF depende parcialmente de DataAloc fora da chave primária composta inicial.",
                    "Porque possui duas dependências transitivas via atributos não-primos: CPF → {NomeAutor, Instituicao} e CodPacote → ValorPacote."
                ],
                "answer": "Porque possui duas dependências transitivas via atributos não-primos: CPF → {NomeAutor, Instituicao} e CodPacote → ValorPacote.",
                "explanation": "CPF e CodPacote não são superchaves em INSC_2FN, mas determinam NomeAutor/Instituicao e ValorPacote respectivamente."
            },
            {
                "id": "f3",
                "label": "3) Qual é o esquema relacional final completo em 3FN sem perda de informação?",
                "options": [
                    "INSC(CodInscr, CPF, CodPacote, ValorPacote), AUTOR(CPF, NomeAutor), TRILHA(CodTrilha, TituloTrilha) e ALOC(CodInscr, CodTrilha).",
                    "INSCRICAO(CodInscr, CPF, CodPacote), AUTOR(CPF, NomeAutor, Instituicao), PACOTE(CodPacote, ValorPacote), TRILHA(CodTrilha, TituloTrilha) e INSC_TRILHA(CodInscr, CodTrilha, DataAloc).",
                    "INSC_TOTAL(CodInscr, CodTrilha, DataAloc, CPF, CodPacote), AUTOR(CPF, NomeAutor, Instituicao) e TRILHA(CodTrilha, TituloTrilha).",
                    "AUTOR(CPF, NomeAutor, Instituicao, CodPacote, ValorPacote), TRILHA(CodTrilha, TituloTrilha) e INSC(CodInscr, CodTrilha, DataAloc)."
                ],
                "answer": "INSCRICAO(CodInscr, CPF, CodPacote), AUTOR(CPF, NomeAutor, Instituicao), PACOTE(CodPacote, ValorPacote), TRILHA(CodTrilha, TituloTrilha) e INSC_TRILHA(CodInscr, CodTrilha, DataAloc).",
                "explanation": "Cada determinante não-superchave (CPF, CodPacote, CodTrilha) ganha sua tabela própria e INSC_TRILHA mantém DataAloc dependendo da chave composta completa."
            }
        ]
    },

    "R3.6": {
        "title": "R3.6 [Simulado B — Etapa 1] Auditoria de Armadilhas ER/EER (Leilões Online)",
        "type": "oficial",
        "mode": "structured",
        "study_guide": STUDY_GUIDE_G10,
        "context_html": """
<p><strong>Simulado B (Etapa 1 de 5 — Correção Crítica de EER):</strong> Um analista júnior desenhou o Diagrama EER abaixo para uma plataforma de leilões online. Audite os erros de modelagem comparando com os requisitos de negócio:</p>
<ul>
  <li>Todo <code>USUARIO(<u>IdUser</u>, Nome)</code> pode atuar simultaneamente como <code>VENDEDOR</code> e <code>COMPRADOR</code> (não há usuário sem papel).</li>
  <li>Cada <code>LEILAO(<u>CodLeilao</u>, Titulo, Status)</code> é aberto por um único vendedor e recebe um histórico completo de <code>LANCE(<u>SeqLance</u>, Valor, Instante)</code> numerados dentro de cada leilão.</li>
</ul>
<div style="text-align:center; margin: 10px 0;">
<svg viewBox="0 0 800 205" width="100%" style="max-width:780px; background:#0d1117; border:1px solid #30363d; border-radius:8px;">
  <rect x="24" y="20" width="150" height="42" rx="4" fill="#161b22" stroke="#58a6ff" stroke-width="2"/>
  <text x="99" y="45" text-anchor="middle" fill="#f0f6fc" font-size="11" font-weight="700">USUARIO (<tspan text-decoration="underline">IdUser</tspan>)</text>
  <!-- Double line total + 'o' -->
  <line x1="96" y1="62" x2="96" y2="85" stroke="#f2cc60" stroke-width="1.6"/>
  <line x1="102" y1="62" x2="102" y2="85" stroke="#f2cc60" stroke-width="1.6"/>
  <circle cx="99" cy="99" r="13" fill="#161b22" stroke="#f2cc60" stroke-width="2"/>
  <text x="99" y="103" text-anchor="middle" fill="#f2cc60" font-size="11" font-weight="700">o</text>
  <line x1="88" y1="107" x2="54" y2="132" stroke="#8b949e" stroke-width="1.5"/>
  <line x1="110" y1="107" x2="146" y2="132" stroke="#8b949e" stroke-width="1.5"/>
  <rect x="12" y="132" width="90" height="36" rx="4" fill="#161b22" stroke="#3fb950" stroke-width="1.8"/>
  <text x="57" y="154" text-anchor="middle" fill="#f0f6fc" font-size="10" font-weight="700">VENDEDOR</text>
  <rect x="112" y="132" width="96" height="36" rx="4" fill="#161b22" stroke="#3fb950" stroke-width="1.8"/>
  <text x="160" y="154" text-anchor="middle" fill="#f0f6fc" font-size="10" font-weight="700">COMPRADOR</text>

  <!-- LEILAO -->
  <rect x="268" y="20" width="154" height="44" rx="4" fill="#161b22" stroke="#58a6ff" stroke-width="2"/>
  <text x="345" y="39" text-anchor="middle" fill="#f0f6fc" font-size="11" font-weight="700">LEILAO</text>
  <text x="345" y="54" text-anchor="middle" fill="#8b949e" font-size="9">(<tspan text-decoration="underline">CodLeilao</tspan>, Status, IdVend)</text>

  <!-- Identifying RECEBE -> LANCE -->
  <line x1="422" y1="42" x2="468" y2="42" stroke="#8b949e" stroke-width="1.5"/>
  <text x="445" y="33" text-anchor="middle" fill="#79c0ff" font-size="9">(0,N)</text>
  <polygon points="468,42 505,18 542,42 505,66" fill="#1f2937" stroke="#f0883e" stroke-width="1.8"/>
  <polygon points="474,42 505,23 536,42 505,61" fill="none" stroke="#f0883e" stroke-width="1.2"/>
  <text x="505" y="46" text-anchor="middle" fill="#f0883e" font-size="9" font-weight="700">RECEBE</text>
  <line x1="542" y1="39" x2="582" y2="39" stroke="#f0883e" stroke-width="1.5"/>
  <line x1="542" y1="45" x2="582" y2="45" stroke="#f0883e" stroke-width="1.5"/>
  <text x="562" y="31" text-anchor="middle" fill="#ffa657" font-size="9">(1,1)</text>
  <rect x="582" y="18" width="194" height="48" rx="4" fill="#161b22" stroke="#f0883e" stroke-width="2"/>
  <rect x="587" y="23" width="184" height="38" rx="2" fill="none" stroke="#f0883e" stroke-width="1.2"/>
  <text x="679" y="39" text-anchor="middle" fill="#f0f6fc" font-size="11" font-weight="700">LANCE</text>
  <text x="679" y="54" text-anchor="middle" fill="#ffa657" font-size="9">({SeqLance}, Valor, Instante)</text>

  <!-- OFERTA from COMPRADOR to LANCE -->
  <line x1="208" y1="150" x2="365" y2="150" stroke="#8b949e" stroke-width="1.5"/>
  <text x="285" y="142" text-anchor="middle" fill="#79c0ff" font-size="9">(0,N)</text>
  <polygon points="365,150 405,126 445,150 405,174" fill="#1f2937" stroke="#d2a8ff" stroke-width="1.8"/>
  <text x="405" y="154" text-anchor="middle" fill="#d2a8ff" font-size="9" font-weight="700">FAZ</text>
  <path d="M 445,147 L 676,147 L 676,66" fill="none" stroke="#58a6ff" stroke-width="1.5"/>
  <path d="M 445,153 L 682,153 L 682,66" fill="none" stroke="#58a6ff" stroke-width="1.5"/>
  <text x="560" y="139" text-anchor="middle" fill="#79c0ff" font-size="9">(1,1)</text>
</svg>
</div>
""",
        "answer_sheet_html": """
<div class="answer-sheet-box">
  <h4>Gabarito Explicado — R3.6 (Simulado B — Etapa 1)</h4>
  <ul>
    <li><strong>Círculo <code>o</code> + Linha Dupla:</strong> Representa especialização com <strong>sobreposição e totalidade</strong> (<code>{o, total}</code>): um mesmo usuário pode ser vendedor e comprador, e não existe usuário que não seja ao menos um deles.</li>
    <li><strong><code>LANCE</code> como Entidade Fraca vs Atributo:</strong> Se um colega sugerisse substituir <code>LANCE</code> por um atributo simples <code>MaiorValor</code> dentro de <code>LEILAO</code>, perderia-se todo o histórico de lances e quem efetuou cada lance.</li>
    <li><strong>PK e FK de <code>LANCE</code>:</strong> Como <code>LANCE</code> é fraca de <code>LEILAO</code> e participa em <code>(1,1)</code> de <code>FAZ</code> com <code>COMPRADOR</code>, mapeia-se <code>LANCE(<u>CodLeilao</u>, <u>SeqLance</u>, IdComprador, Valor, Instante)</code> onde <code>IdComprador NOT NULL</code> vem da relação <code>1:N</code> <code>FAZ</code>.</li>
  </ul>
</div>
""",
        "fields": [
            {
                "id": "f1",
                "label": "1) O que significa exatamente a notação de círculo 'o' com linha dupla saindo de USUARIO no diagrama EER?",
                "options": [
                    "Especialização disjunta e parcial: cada usuário é apenas vendedor OU comprador, podendo não ser nenhum.",
                    "Especialização sobreposta e total: todo usuário participa de VENDEDOR e/ou COMPRADOR, podendo acumular ambos.",
                    "Agregação obrigatória: um vendedor só existe após comprar pelo menos um item dentro de um leilão.",
                    "Generalização exclusiva disjunta: impede em nível de tabela que o mesmo IdUser esteja nas duas subclasses."
                ],
                "answer": "Especialização sobreposta e total: todo usuário participa de VENDEDOR e/ou COMPRADOR, podendo acumular ambos.",
                "explanation": "O 'o' indica Overlapping (sobreposição) e a linha dupla entre superclasse e círculo indica participação Total (todo USUARIO pertence a pelo menos uma subclasse)."
            },
            {
                "id": "f2",
                "label": "2) Se o júnior tivesse modelado LANCE como uma relação M:N direta (COMPRADOR --<LANCE>-- LEILAO) sem entidade fraca, qual limitação surgiria?",
                "options": [
                    "Tornaria impossível registrar qualquer comprador diferente dando lance dentro de um mesmo leilão.",
                    "Proibiria cada comprador de dar lances em dois leilões distintos em horários separados.",
                    "Com PK apenas (IdComprador, CodLeilao), um comprador não poderia dar múltiplos lances diferentes no mesmo leilão.",
                    "Faria com que o atributo Valor ficasse armazenado dentro da superclasse USUARIO."
                ],
                "answer": "Com PK apenas (IdComprador, CodLeilao), um comprador não poderia dar múltiplos lances diferentes no mesmo leilão.",
                "explanation": "Um relacionamento binário M:N padrão entre COMPRADOR e LEILAO tem PK (IdComprador, CodLeilao), permitindo no máximo 1 lance por comprador naquele leilão — impossibilitando disputas sucessivas!"
            },
            {
                "id": "f3",
                "label": "3) Qual esquema relacional mapeia corretamente a entidade fraca LANCE e suas duas associações?",
                "options": [
                    "LANCE(CodLeilao, SeqLance, IdComprador, Valor, Instante) com PK (CodLeilao, SeqLance) e IdComprador NOT NULL.",
                    "LANCE(SeqLance, Valor, Instante) sem FK para LEILAO, guardando apenas IdComprador como chave estrangeira.",
                    "LANCE(CodLeilao, IdComprador, Valor) utilizando IdComprador como única chave primária da tabela inteira.",
                    "LANCE(CodLeilao, SeqLance, IdVendedor, Valor) dispensando registrar quem efetuou o lance comprador."
                ],
                "answer": "LANCE(CodLeilao, SeqLance, IdComprador, Valor, Instante) com PK (CodLeilao, SeqLance) e IdComprador NOT NULL.",
                "explanation": "A relação identificadora RECEBE dá a PK composta (CodLeilao, SeqLance), enquanto a relação 1:N total FAZ propaga IdComprador NOT NULL para LANCE."
            }
        ]
    },

    "R3.7": {
        "title": "R3.7 [Simulado B — Etapa 2] Contrato SQL-92 CREATE ASSERTION (Auto-lance &amp; Leilão Aberto)",
        "type": "oficial",
        "mode": "sql_assertion",
        "study_guide": STUDY_GUIDE_G10,
        "setup": """
CREATE TABLE LEILAO (
  CodLeilao INTEGER PRIMARY KEY,
  IdVendedor TEXT NOT NULL,
  Status TEXT NOT NULL
);
CREATE TABLE LANCE (
  CodLeilao INTEGER NOT NULL,
  SeqLance INTEGER NOT NULL,
  IdComprador TEXT NOT NULL,
  Valor REAL NOT NULL,
  PRIMARY KEY (CodLeilao, SeqLance),
  FOREIGN KEY (CodLeilao) REFERENCES LEILAO(CodLeilao)
);
INSERT INTO LEILAO VALUES (1, 'U10', 'ABERTO'), (2, 'U20', 'ENCERRADO');
INSERT INTO LANCE VALUES (1, 1, 'U20', 500.0);
""",
        "context_html": """
<p><strong>Simulado B (Etapa 2 de 5 — Restrições Globais em SQL-92):</strong> O esquema acima (<code>LEILAO(<u>CodLeilao</u>, IdVendedor, Status)</code> e <code>LANCE(<u>CodLeilao</u>, <u>SeqLance</u>, IdComprador, Valor)</code>) já está carregado com 2 leilões e 1 lance válido.</p>
<p>Escreva <strong>duas declarações <code>CREATE ASSERTION ... CHECK (NOT EXISTS (...));</code></strong> separadas por ponto-e-vírgula para impor os invariantes inter-tabelas:</p>
<ol>
  <li><strong>Proibir Auto-lance:</strong> nenhum lance pode ter <code>IdComprador</code> igual ao <code>IdVendedor</code> do respectivo <code>LEILAO</code>.</li>
  <li><strong>Somente em Leilão Aberto:</strong> nenhum lance pode existir vinculado a um <code>LEILAO</code> cujo <code>Status &lt;&gt; 'ABERTO'</code>.</li>
</ol>
""",
        "answer_sheet_html": """
<div class="answer-sheet-box">
  <h4>Gabarito de Referência — R3.7 (Assertions de Negócio)</h4>
  <pre class="sql-code">CREATE ASSERTION SEM_AUTOLANCE CHECK (
  NOT EXISTS (
    SELECT 1 FROM LANCE l
    JOIN LEILAO a ON l.CodLeilao = a.CodLeilao
    WHERE l.IdComprador = a.IdVendedor
  )
);

CREATE ASSERTION APENAS_LEILAO_ABERTO CHECK (
  NOT EXISTS (
    SELECT 1 FROM LANCE l
    JOIN LEILAO a ON l.CodLeilao = a.CodLeilao
    WHERE a.Status &lt;&gt; 'ABERTO'
  )
);</pre>
</div>
""",
        "assertion_tests": [
            {
                "name": "Estado inicial válido (lance de U20 no leilão ABERTO de U10)",
                "violation_sql": None,
                "should_pass": True,
                "hint": "O estado inicial não viola nenhuma das duas asserções."
            },
            {
                "name": "Aceitar novo lance de U30 em leilão ABERTO de U10",
                "violation_sql": "INSERT INTO LANCE VALUES (1, 2, 'U30', 650.0);",
                "should_pass": True,
                "hint": "U30 <> U10 e Leilão 1 está ABERTO: deve ser aceito."
            },
            {
                "name": "Bloquear auto-lance (vendedor U10 dando lance no próprio leilão 1)",
                "violation_sql": "INSERT INTO LANCE VALUES (1, 3, 'U10', 999.0);",
                "should_pass": False,
                "hint": "Sua asserção deve detectar IdComprador = IdVendedor via JOIN entre LANCE e LEILAO."
            },
            {
                "name": "Bloquear lance em leilão encerrado (Leilão 2 está ENCERRADO)",
                "violation_sql": "INSERT INTO LANCE VALUES (2, 1, 'U10', 300.0);",
                "should_pass": False,
                "hint": "Verifique Status <> 'ABERTO' na junção de LANCE com LEILAO."
            }
        ]
    },

    "R3.8": {
        "title": "R3.8 [Simulado B — Etapa 3] Auditoria SQL de Violação de DF em Instância",
        "type": "oficial",
        "mode": "sql_query",
        "study_guide": STUDY_GUIDE_G10,
        "setup": """
CREATE TABLE LANCE_AUDIT (
  IdLance INTEGER PRIMARY KEY,
  CodLeilao INTEGER NOT NULL,
  CPFVendedor TEXT NOT NULL,
  NomeVendedor TEXT NOT NULL,
  CEPVendedor TEXT NOT NULL,
  CidadeVendedor TEXT NOT NULL,
  Valor REAL NOT NULL
);
INSERT INTO LANCE_AUDIT VALUES
  (1, 10, '111.111.111-11', 'Ana Costa',    '30130-000', 'Belo Horizonte', 120.0),
  (2, 11, '222.222.222-22', 'Bruno Reis',   '30130-000', 'Belo Horizonte', 250.0),
  (3, 12, '111.111.111-11', 'Ana Costa',    '30130-000', 'Belo Horizonte', 180.0),
  (4, 13, '333.333.333-33', 'Carla Dias',   '20040-002', 'Rio de Janeiro', 500.0),
  (5, 14, '444.444.444-44', 'Diego Alves',  '01310-100', 'São Paulo',      310.0),
  (6, 15, '555.555.555-55', 'Eva Nogueira', '01310-100', 'São Paulo',      410.0);
""",
        "context_html": """
<p><strong>Simulado B (Etapa 3 de 5 — Detetive Empírico de DFs):</strong> Considere a tabela legada populada <code>LANCE_AUDIT(IdLance, CodLeilao, CPFVendedor, NomeVendedor, CEPVendedor, CidadeVendedor, Valor)</code>.</p>
<p>Um colega afirmou que a dependência funcional <strong><code>CEPVendedor &rarr; CPFVendedor</code></strong> seria válida nessa tabela. Prove que a afirmação é falsa escrevendo uma consulta SQL que encontre todos os pares distintos de lances (<code>a.IdLance &lt; b.IdLance</code>) com <strong>mesmo <code>CEPVendedor</code></strong> e <strong><code>CPFVendedor</code> diferentes</strong>.</p>
<p><strong>Colunas exatas esperadas:</strong> <code>IdLance1</code>, <code>IdLance2</code>, <code>CEPVendedor</code>, <code>CPF1</code>, <code>CPF2</code>.</p>
""",
        "answer_sheet_html": """
<div class="answer-sheet-box">
  <h4>Gabarito SQL — R3.8 (Simulado B — Etapa 3)</h4>
  <pre class="sql-code">SELECT a.IdLance AS IdLance1,
       b.IdLance AS IdLance2,
       a.CEPVendedor,
       a.CPFVendedor AS CPF1,
       b.CPFVendedor AS CPF2
FROM LANCE_AUDIT a
JOIN LANCE_AUDIT b
  ON a.CEPVendedor = b.CEPVendedor
 AND a.CPFVendedor &lt;&gt; b.CPFVendedor
 AND a.IdLance &lt; b.IdLance;</pre>
  <p>Retorna exatamente 3 pares contra-exemplo: <code>(1, 2)</code> e <code>(2, 3)</code> em <code>'30130-000'</code>, além de <code>(5, 6)</code> em <code>'01310-100'</code>. Note que <code>CEPVendedor &rarr; CidadeVendedor</code> é satisfeita, mas <code>CEPVendedor &rarr; CPFVendedor</code> é refutada!</p>
</div>
""",
        "expected_columns": ["IdLance1", "IdLance2", "CEPVendedor", "CPF1", "CPF2"],
        "expected_rows": [
            [1, 2, "30130-000", "111.111.111-11", "222.222.222-22"],
            [2, 3, "30130-000", "222.222.222-22", "111.111.111-11"],
            [5, 6, "01310-100", "444.444.444-44", "555.555.555-55"]
        ]
    },

    "R3.9": {
        "title": "R3.9 [Simulado B — Etapa 4] Chaves Candidatas, 3FN vs BCNF &amp; NJP em R(M,N,P,Q,S)",
        "type": "oficial",
        "mode": "structured",
        "study_guide": STUDY_GUIDE_G10,
        "context_html": """
<p><strong>Simulado B (Etapa 4 de 5 — Análise Formal de Normalização):</strong> Seja a relação abstrata <code>R(M, N, P, Q, S)</code> submetida ao seguinte conjunto de dependências funcionais:</p>
<pre class="sql-code">F = { MN &rarr; P,  NP &rarr; Q,  Q &rarr; S,  S &rarr; M }</pre>
<p>Calcule todos os fechos necessários para responder com rigor sobre chaves candidatas, forma normal atual, teste de junção sem perda (NJP) e decomposição BCNF.</p>
""",
        "answer_sheet_html": """
<div class="answer-sheet-box">
  <h4>Gabarito Passo a Passo — R3.9 (Simulado B — Etapa 4)</h4>
  <ul>
    <li><strong>Chaves Candidatas:</strong> Como <code>N</code> nunca aparece do lado direito, toda chave deve conter <code>N</code>. Calculando fechos de pares com <code>N</code>: <code>(MN)+ = MNPQS</code>, <code>(NP)+ = MNPQS</code>, <code>(NQ)+ = MNPQS</code>, <code>(NS)+ = MNPQS</code>. Logo há <strong>4 chaves candidatas</strong>: <code>{MN, NP, NQ, NS}</code> e <strong>todos os 5 atributos são primos</strong>!</li>
    <li><strong>3FN vs BCNF:</strong> Como todo atributo à direita é primo, <code>R</code> já está em <strong>3FN</strong>, mas <strong>viola BCNF</strong> por causa de <code>Q &rarr; S</code> e <code>S &rarr; M</code> (nem <code>Q</code> nem <code>S</code> são superchaves).</li>
    <li><strong>Teste Binário NJP:</strong> Para <code>D_A = { R1(M, N, P, Q), R2(Q, S) }</code>, a interseção <code>{Q}</code> tem <code>Q+ = {M, Q, S} &supseteq; R2</code> (<strong>Sem Perda!</strong>). Já <code>D_B = { R1(M, N, P), R2(P, Q, S) }</code> tem interseção <code>{P}</code> com <code>P+ = {P}</code> (<strong>COM Perda!</strong>).</li>
    <li><strong>Decomposição BCNF:</strong> Quebrando por <code>S &rarr; M</code> &rarr; <code>R_a(<u>S</u>, M)</code> e <code>R_b(N, P, Q, S)</code>; depois por <code>Q &rarr; S</code> &rarr; <code>R_b1(<u>Q</u>, S)</code> e <code>R_b2(<u>N</u>, <u>P</u>, Q)</code>. Todas ficam em BCNF, porém a DF <code>MN &rarr; P</code> <strong>deixa de ser preservada</strong>.</li>
  </ul>
</div>
""",
        "fields": [
            {
                "id": "f1",
                "label": "1) Quais são todas as chaves candidatas de R(M, N, P, Q, S) e qual é sua maior forma normal atual?",
                "options": [
                    "Chave única {MN}, fazendo com que R esteja apenas em 2FN devido a Q → S.",
                    "Chaves {MN} e {NP} apenas, levando R a violar tanto a 3FN quanto a BCNF.",
                    "Chaves {MN}, {NP}, {NQ} e {NS}; todos os atributos são primos, logo R está em 3FN (mas não BCNF).",
                    "Chaves {QS}, {MN} e {NP}; logo R já satisfaz integralmente tanto a 3FN quanto a BCNF."
                ],
                "answer": "Chaves {MN}, {NP}, {NQ} e {NS}; todos os atributos são primos, logo R está em 3FN (mas não BCNF).",
                "explanation": "N nunca aparece no RHS. Testando todos os pares com N, os quatro pares determinam MNPQS. Logo M, N, P, Q e S são todos primos (satisfaz 3FN), mas Q e S não são superchaves (viola BCNF)."
            },
            {
                "id": "f2",
                "label": "2) Comparando D_A = { R1(M,N,P,Q), R2(Q,S) } e D_B = { R1(M,N,P), R2(P,Q,S) } quanto à Junção Sem Perda:",
                "options": [
                    "D_A tem junção sem perda (pois Q → QS está em F+), enquanto D_B tem perda de informação (P+ = {P}).",
                    "Ambas D_A e D_B possuem junção sem perda, porque R1 ∩ R2 não é vazio em nenhuma das duas.",
                    "D_B tem junção sem perda porque NP está presente em R1, enquanto D_A tem perda em M.",
                    "Nenhuma das duas decomposições possui junção sem perda, pois N ficou isolado em R1."
                ],
                "answer": "D_A tem junção sem perda (pois Q → QS está em F+), enquanto D_B tem perda de informação (P+ = {P}).",
                "explanation": "Em D_A, R1 ∩ R2 = {Q} e Q+ = {M,Q,S} contém todo R2(Q,S). Em D_B, R1 ∩ R2 = {P} e P+ = {P}, que não determina R1 nem R2."
            },
            {
                "id": "f3",
                "label": "3) Ao decompor R para BCNF obtendo { R1(S, M), R2(Q, S), R3(N, P, Q) }, qual propriedade é sacrificada?",
                "options": [
                    "Perde-se a junção sem perda, tornando impossível reconstruir as tuplas originais de R sem falsas combinações.",
                    "Perde-se a terceira forma normal na tabela R3(N, P, Q), pois NP → Q passa a ser dependência transitiva.",
                    "Perdem-se todas as chaves candidatas da relação inicial, deixando R3 sem qualquer determinante único.",
                    "Perde-se a preservação de dependências funcionais, pois MN → P não pode mais ser verificada localmente."
                ],
                "answer": "Perde-se a preservação de dependências funcionais, pois MN → P não pode mais ser verificada localmente.",
                "explanation": "A decomposição BCNF sempre garante junção sem perda, mas aqui separou M (em R1) de N e P (em R3), impossibilitando checar MN → P sem junção."
            }
        ]
    },

    "R3.10": {
        "title": "R3.10 [Simulado B — Etapa 5] Normalização pela Definição Geral (ENTREGA_DRONE)",
        "type": "oficial",
        "mode": "structured",
        "study_guide": STUDY_GUIDE_G10,
        "context_html": """
<p><strong>Simulado B (Etapa 5 de 5 — Fechamento com Definição Geral &amp; Múltiplas Chaves):</strong> Considere o esquema de rastreamento logístico de drones já em 1FN:</p>
<pre class="sql-code">ENTREGA_DRONE(IdEntrega, CodDrone, DataHora, ModeloDrone, PesoMax, BairroDestino, CodBase, NomeBase)</pre>
<p><strong>Regras de negócio (Dependências Funcionais):</strong></p>
<pre class="sql-code">F = {
  IdEntrega &rarr; CodDrone, DataHora, BairroDestino
  {CodDrone, DataHora} &rarr; IdEntrega, BairroDestino    (um drone faz no máximo 1 entrega num instante)
  CodDrone &rarr; ModeloDrone
  ModeloDrone &rarr; PesoMax
  BairroDestino &rarr; CodBase
  CodBase &rarr; NomeBase
}</pre>
<p>Aplique a <strong>Definição Geral</strong> de 2FN, 3FN e BCNF para auditar todas as chaves candidatas e chegar ao esquema final normalizado.</p>
""",
        "answer_sheet_html": """
<div class="answer-sheet-box">
  <h4>Gabarito Completo — R3.10 (Simulado B — Etapa 5)</h4>
  <ul>
    <li><strong>Chaves Candidatas:</strong> <code>{IdEntrega}</code> e <code>{CodDrone, DataHora}</code>! Logo, atributos primos = <code>{IdEntrega, CodDrone, DataHora}</code>.</li>
    <li><strong>Armadilha da 2FN (Definição Geral):</strong> Embora <code>IdEntrega</code> seja chave simples, <code>CodDrone &rarr; ModeloDrone</code> (e <code>PesoMax</code>) viola a <strong>2FN</strong> porque <code>CodDrone</code> é subconjunto próprio da segunda chave candidata <code>{CodDrone, DataHora}</code> e <code>ModeloDrone</code> é não-primo!</li>
    <li><strong>Remoção de Transitivas (3FN):</strong> Separam-se <code>MODELO(<u>ModeloDrone</u>, PesoMax)</code>, <code>DRONE(<u>CodDrone</u>, ModeloDrone)</code>, <code>BASE(<u>CodBase</u>, NomeBase)</code>, <code>BAIRRO(<u>BairroDestino</u>, CodBase)</code> e <code>ENTREGA(<u>IdEntrega</u>, CodDrone, DataHora, BairroDestino)</code>.</li>
    <li><strong>Verificação BCNF:</strong> Em todas as 5 tabelas finais (incluindo <code>ENTREGA</code>, onde tanto <code>IdEntrega</code> quanto <code>{CodDrone, DataHora}</code> são superchaves!), todo determinante é superchave &rarr; esquema final em <strong>BCNF</strong>!</li>
  </ul>
</div>
""",
        "fields": [
            {
                "id": "f1",
                "label": "1) Aplicando a Definição Geral de 2FN a ENTREGA_DRONE (considerando todas as chaves candidatas), por que ela já viola a 2FN?",
                "options": [
                    "Não viola a 2FN, porque a chave primária escolhida {IdEntrega} possui um único atributo atômico.",
                    "Viola a 2FN exclusivamente devido a BairroDestino → CodBase, já que BairroDestino depende de IdEntrega.",
                    "Viola a 2FN porque DataHora sozinho determina CodBase mesmo sem estar ligado ao drone.",
                    "Viola a 2FN porque CodDrone → ModeloDrone (e PesoMax) é dependência parcial da chave candidata {CodDrone, DataHora}."
                ],
                "answer": "Viola a 2FN porque CodDrone → ModeloDrone (e PesoMax) é dependência parcial da chave candidata {CodDrone, DataHora}.",
                "explanation": "Na Definição Geral, a 2FN proíbe dependência parcial sobre QUALQUER chave candidata (não apenas a PK primária!). Como {CodDrone, DataHora} é chave candidata e CodDrone -> ModeloDrone usa só parte dela, há violação de 2FN."
            },
            {
                "id": "f2",
                "label": "2) Além de separar DRONE/MODELO, quantas relações auxiliares e cadeias transitivas precisam ser extraídas da parte geográfica (BairroDestino → CodBase → NomeBase) para atingir a 3FN?",
                "options": [
                    "Apenas uma tabela GEO(BairroDestino, CodBase, NomeBase) contendo todas as três colunas juntas.",
                    "Duas tabelas em 3FN: BAIRRO(BairroDestino, CodBase) e BASE(CodBase, NomeBase), eliminando a transitiva.",
                    "Nenhuma tabela nova, pois BairroDestino e CodBase permanecem em ENTREGA junto com PesoMax.",
                    "Três tabelas com PK IdEntrega replicada em cada uma para manter a integridade referencial."
                ],
                "answer": "Duas tabelas em 3FN: BAIRRO(BairroDestino, CodBase) e BASE(CodBase, NomeBase), eliminando a transitiva.",
                "explanation": "Se ficassem juntas em BAIRRO(BairroDestino, CodBase, NomeBase), ainda haveria dependência transitiva CodBase -> NomeBase."
            },
            {
                "id": "f3",
                "label": "3) Sobre o esquema final decomposto { ENTREGA, DRONE, MODELO, BAIRRO, BASE }, qual afirmação é exata?",
                "options": [
                    "Está apenas em 2FN, pois a tabela ENTREGA mantém duas chaves candidatas distintas simultaneamente.",
                    "Está em 3FN, mas viola a BCNF em ENTREGA porque {CodDrone, DataHora} não é chave primária.",
                    "Está em 3FN e também em BCNF plena, pois todo determinante em todas as 5 tabelas é superchave.",
                    "Não possui junção sem perda caso um drone realize mais de uma entrega em horários diferentes."
                ],
                "answer": "Está em 3FN e também em BCNF plena, pois todo determinante em todas as 5 tabelas é superchave.",
                "explanation": "Ter duas chaves candidatas (IdEntrega e {CodDrone, DataHora}) onde ambas determinam toda a tupla faz com que ambos os determinantes sejam superchaves, satisfazendo BCNF!"
            }
        ]
    }
}
