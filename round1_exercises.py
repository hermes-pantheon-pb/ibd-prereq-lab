#!/usr/bin/env python3
"""
Round 1 Exam Mastery Exercises (R1.1 to R1.10) for Modules 7 & 8:
- Module 7 (Projeto Lógico: Mapeamento ER / EER -> Relacional): R1.1, R1.2, R1.3, R1.4, R1.5
- Module 8 (Normalização: DFs, Fecho X+, Cobertura Mínima, 1FN/2FN/3FN): R1.6, R1.7, R1.8, R1.9, R1.10

Includes:
- Authentic ER and EER SVG diagrams rendered in the exercise statement
- Visual FD / Schema Grids (zero raw LaTeX, zero walls of text)
- 2-Column Study Guides (Cheat Sheets) with exact UFMG coursework references and parallel-domain worked examples
- Step-Card Answer Sheets (Folha de Gabarito Oficial) for open-ended/layout resolution
- Balanced multiple-choice checkpoints and live SQL DDL / SQL Query validation suites
"""

from typing import Dict, Any

# ==============================================================================
# SVG DIAGRAMS FOR ROUND 1 (Authentic Chen / Elmasri & Navathe / UFMG Notation)
# ==============================================================================

HOSPITAL_ER_SVG = """
<div class="er-diagram-box">
  <div class="er-diagram-title">📐 Esquema ER Oficial — Estudo de Caso: Sistema Hospitalar &amp; Prontuário Clínico (Elmasri &amp; Navathe)</div>
  <svg viewBox="0 0 920 430" width="100%" height="auto" xmlns="http://www.w3.org/2000/svg" style="background:#0f172a; border-radius:8px; border:1px solid #334155; font-family:'Inter',sans-serif;">
    <!-- ALA_HOSPITALAR (1,1) == CHEFIADA_POR == (0,1) MEDICO -->
    <line x1="210" y1="95" x2="390" y2="95" stroke="#38bdf8" stroke-width="3"/>
    <line x1="210" y1="101" x2="390" y2="101" stroke="#38bdf8" stroke-width="3"/>
    <line x1="510" y1="98" x2="680" y2="98" stroke="#94a3b8" stroke-width="2"/>
    <text x="235" y="86" fill="#38bdf8" font-size="12" font-weight="bold">(1, 1)</text>
    <text x="615" y="86" fill="#e2e8f0" font-size="12" font-weight="bold">(0, 1)</text>

    <!-- ALA_HOSPITALAR (0,N) / INTERNADO_EM / (0,1) PACIENTE -->
    <line x1="130" y1="125" x2="130" y2="195" stroke="#94a3b8" stroke-width="2"/>
    <line x1="130" y1="255" x2="130" y2="315" stroke="#94a3b8" stroke-width="2"/>
    <text x="138" y="152" fill="#e2e8f0" font-size="12" font-weight="bold">(0, N)</text>
    <text x="138" y="302" fill="#e2e8f0" font-size="12" font-weight="bold">(0, 1)</text>

    <!-- MEDICO (0,N) / PRESCRICAO / (0,N) PACIENTE -->
    <line x1="740" y1="125" x2="450" y2="215" stroke="#94a3b8" stroke-width="2"/>
    <line x1="390" y1="225" x2="210" y2="335" stroke="#94a3b8" stroke-width="2"/>
    <text x="625" y="152" fill="#e2e8f0" font-size="12" font-weight="bold">(0, N)</text>
    <text x="235" y="302" fill="#e2e8f0" font-size="12" font-weight="bold">(0, N)</text>

    <!-- PACIENTE (0,N) / REALIZA_EXAME (Weak ID) / (1,1) EXAME_LABORATORIAL -->
    <line x1="210" y1="350" x2="390" y2="350" stroke="#94a3b8" stroke-width="2"/>
    <line x1="510" y1="347" x2="660" y2="347" stroke="#f59e0b" stroke-width="3"/>
    <line x1="510" y1="353" x2="660" y2="353" stroke="#f59e0b" stroke-width="3"/>
    <text x="235" y="340" fill="#e2e8f0" font-size="12" font-weight="bold">(0, N)</text>
    <text x="585" y="338" fill="#f59e0b" font-size="12" font-weight="bold">(1, 1)</text>

    <!-- Strong Entity: ALA_HOSPITALAR -->
    <rect x="50" y="70" width="160" height="55" rx="4" fill="#1e293b" stroke="#38bdf8" stroke-width="2.5"/>
    <text x="130" y="102" fill="#f8fafc" font-size="13" font-weight="bold" text-anchor="middle">ALA_HOSPITALAR</text>
    <line x1="80" y1="70" x2="60" y2="35" stroke="#64748b" stroke-width="1.5"/>
    <ellipse cx="55" cy="25" rx="42" ry="15" fill="#0f172a" stroke="#94a3b8" stroke-width="1.5"/>
    <text x="55" y="29" fill="#f8fafc" font-size="11" text-decoration="underline" text-anchor="middle">CodAla</text>
    <line x1="130" y1="70" x2="145" y2="35" stroke="#64748b" stroke-width="1.5"/>
    <ellipse cx="150" cy="25" rx="45" ry="15" fill="#0f172a" stroke="#94a3b8" stroke-width="1.5"/>
    <text x="150" y="29" fill="#cbd5e1" font-size="11" text-anchor="middle">NomeAla</text>
    <line x1="180" y1="70" x2="230" y2="35" stroke="#64748b" stroke-width="1.5"/>
    <ellipse cx="240" cy="25" rx="35" ry="15" fill="#0f172a" stroke="#94a3b8" stroke-width="1.5"/>
    <text x="240" y="29" fill="#cbd5e1" font-size="11" text-anchor="middle">Andar</text>

    <!-- Relationship 1:1 CHEFIADA_POR -->
    <polygon points="450,68 510,98 450,128 390,98" fill="#1e293b" stroke="#a855f7" stroke-width="2"/>
    <text x="450" y="102" fill="#e9d5ff" font-size="11" font-weight="bold" text-anchor="middle">CHEFIADA_POR</text>
    <line x1="450" y1="68" x2="450" y2="38" stroke="#64748b" stroke-width="1.5"/>
    <ellipse cx="450" cy="25" rx="48" ry="14" fill="#0f172a" stroke="#a855f7" stroke-width="1.5"/>
    <text x="450" y="29" fill="#e9d5ff" font-size="11" text-anchor="middle">DataPosse</text>

    <!-- Strong Entity: MEDICO -->
    <rect x="680" y="70" width="150" height="55" rx="4" fill="#1e293b" stroke="#38bdf8" stroke-width="2.5"/>
    <text x="755" y="102" fill="#f8fafc" font-size="13" font-weight="bold" text-anchor="middle">MEDICO</text>
    <line x1="705" y1="70" x2="660" y2="35" stroke="#64748b" stroke-width="1.5"/>
    <ellipse cx="650" cy="25" rx="36" ry="15" fill="#0f172a" stroke="#94a3b8" stroke-width="1.5"/>
    <text x="650" y="29" fill="#f8fafc" font-size="11" text-decoration="underline" text-anchor="middle">CRM</text>
    <line x1="755" y1="70" x2="755" y2="38" stroke="#64748b" stroke-width="1.5"/>
    <ellipse cx="755" cy="25" rx="45" ry="15" fill="#0f172a" stroke="#94a3b8" stroke-width="1.5"/>
    <text x="755" y="29" fill="#cbd5e1" font-size="11" text-anchor="middle">NomeMed</text>
    <!-- Multivalued Attribute: Especialidades -->
    <line x1="805" y1="70" x2="855" y2="42" stroke="#64748b" stroke-width="1.5"/>
    <ellipse cx="855" cy="27" rx="58" ry="18" fill="#0f172a" stroke="#f59e0b" stroke-width="1.5"/>
    <ellipse cx="855" cy="27" rx="54" ry="14" fill="#0f172a" stroke="#f59e0b" stroke-width="1.5"/>
    <text x="855" y="31" fill="#fde68a" font-size="10.5" text-anchor="middle">Especialidades</text>
    <!-- Composite Attribute: Endereco(Rua, CEP) -->
    <line x1="830" y1="105" x2="860" y2="145" stroke="#64748b" stroke-width="1.5"/>
    <ellipse cx="855" cy="160" rx="46" ry="15" fill="#0f172a" stroke="#38bdf8" stroke-width="1.5"/>
    <text x="855" y="164" fill="#bae6fd" font-size="11" text-anchor="middle">Endereco</text>
    <line x1="835" y1="174" x2="810" y2="202" stroke="#64748b" stroke-width="1.5"/>
    <ellipse cx="805" cy="214" rx="28" ry="12" fill="#0f172a" stroke="#94a3b8" stroke-width="1.2"/>
    <text x="805" y="218" fill="#cbd5e1" font-size="10" text-anchor="middle">Rua</text>
    <line x1="875" y1="174" x2="885" y2="202" stroke="#64748b" stroke-width="1.5"/>
    <ellipse cx="885" cy="214" rx="28" ry="12" fill="#0f172a" stroke="#94a3b8" stroke-width="1.2"/>
    <text x="885" y="218" fill="#cbd5e1" font-size="10" text-anchor="middle">CEP</text>

    <!-- Relationship 1:N INTERNADO_EM -->
    <polygon points="130,195 195,225 130,255 65,225" fill="#1e293b" stroke="#a855f7" stroke-width="2"/>
    <text x="130" y="229" fill="#e9d5ff" font-size="10.5" font-weight="bold" text-anchor="middle">INTERNADO_EM</text>
    <line x1="195" y1="225" x2="240" y2="225" stroke="#64748b" stroke-width="1.5"/>
    <ellipse cx="278" cy="225" rx="42" ry="14" fill="#0f172a" stroke="#a855f7" stroke-width="1.5"/>
    <text x="278" y="229" fill="#e9d5ff" font-size="11" text-anchor="middle">NumLeito</text>

    <!-- Relationship M:N PRESCRICAO -->
    <polygon points="450,195 510,225 450,255 390,225" fill="#1e293b" stroke="#a855f7" stroke-width="2"/>
    <text x="450" y="229" fill="#e9d5ff" font-size="11" font-weight="bold" text-anchor="middle">PRESCRICAO</text>
    <line x1="510" y1="225" x2="555" y2="225" stroke="#64748b" stroke-width="1.5"/>
    <ellipse cx="595" cy="225" rx="44" ry="14" fill="#0f172a" stroke="#a855f7" stroke-width="1.5"/>
    <text x="595" y="229" fill="#e9d5ff" font-size="11" text-anchor="middle">Dosagem</text>

    <!-- Strong Entity: PACIENTE -->
    <rect x="50" y="320" width="160" height="55" rx="4" fill="#1e293b" stroke="#38bdf8" stroke-width="2.5"/>
    <text x="130" y="352" fill="#f8fafc" font-size="13" font-weight="bold" text-anchor="middle">PACIENTE</text>
    <line x1="85" y1="375" x2="65" y2="398" stroke="#64748b" stroke-width="1.5"/>
    <ellipse cx="60" cy="410" rx="35" ry="14" fill="#0f172a" stroke="#94a3b8" stroke-width="1.5"/>
    <text x="60" y="414" fill="#f8fafc" font-size="11" text-decoration="underline" text-anchor="middle">CNS</text>
    <line x1="155" y1="375" x2="175" y2="398" stroke="#64748b" stroke-width="1.5"/>
    <ellipse cx="180" cy="410" rx="45" ry="14" fill="#0f172a" stroke="#94a3b8" stroke-width="1.5"/>
    <text x="180" y="414" fill="#cbd5e1" font-size="11" text-anchor="middle">NomePac</text>

    <!-- Weak Identifying Relationship: REALIZA_EXAME (Double Diamond) -->
    <polygon points="450,316 514,350 450,384 386,350" fill="#1e293b" stroke="#f59e0b" stroke-width="2"/>
    <polygon points="450,322 506,350 450,378 394,350" fill="#1e293b" stroke="#f59e0b" stroke-width="1.5"/>
    <text x="450" y="354" fill="#fde68a" font-size="10.5" font-weight="bold" text-anchor="middle">REALIZA_EXAME</text>

    <!-- Weak Entity: EXAME_LABORATORIAL (Double Rectangle) -->
    <rect x="660" y="320" width="210" height="58" rx="4" fill="#1e293b" stroke="#f59e0b" stroke-width="2.5"/>
    <rect x="665" y="325" width="200" height="48" rx="3" fill="#1e293b" stroke="#f59e0b" stroke-width="1.5"/>
    <text x="765" y="354" fill="#fde68a" font-size="12.5" font-weight="bold" text-anchor="middle">EXAME_LABORATORIAL</text>
    <line x1="710" y1="378" x2="685" y2="398" stroke="#64748b" stroke-width="1.5"/>
    <ellipse cx="675" cy="410" rx="58" ry="14" fill="#0f172a" stroke="#f59e0b" stroke-width="1.5"/>
    <text x="675" y="413" fill="#fde68a" font-size="11" text-anchor="middle">NumSeqExame</text>
    <line x1="635" y1="418" x2="715" y2="418" stroke="#fde68a" stroke-width="1.5" stroke-dasharray="4,3"/>
    <line x1="815" y1="378" x2="835" y2="398" stroke="#64748b" stroke-width="1.5"/>
    <ellipse cx="840" cy="410" rx="48" ry="14" fill="#0f172a" stroke="#94a3b8" stroke-width="1.5"/>
    <text x="840" y="414" fill="#cbd5e1" font-size="11" text-anchor="middle">TipoExame</text>
  </svg>
</div>
"""

UNIVERSITY_EER_SVG = """
<div class="er-diagram-box">
  <div class="er-diagram-title">📐 Esquema EER Oficial — Estudo de Caso: Pós-Graduação &amp; Pesquisa Universitária (Hierarquias d/o &amp; Ternário)</div>
  <svg viewBox="0 0 920 420" width="100%" height="auto" xmlns="http://www.w3.org/2000/svg" style="background:#0f172a; border-radius:8px; border:1px solid #334155; font-family:'Inter',sans-serif;">
    <!-- Left Hierarchy: PESSOA -> (o, partial) -> DOCENTE, ALUNO_POS -->
    <rect x="110" y="40" width="160" height="50" rx="4" fill="#1e293b" stroke="#38bdf8" stroke-width="2.5"/>
    <text x="190" y="70" fill="#f8fafc" font-size="13" font-weight="bold" text-anchor="middle">PESSOA (CPF, Nome)</text>
    <line x1="190" y1="90" x2="190" y2="145" stroke="#94a3b8" stroke-width="2.5"/>
    <circle cx="190" cy="162" r="17" fill="#1e293b" stroke="#38bdf8" stroke-width="2.5"/>
    <text x="190" y="167" fill="#38bdf8" font-size="14" font-weight="bold" text-anchor="middle">o</text>
    <text x="255" y="125" fill="#94a3b8" font-size="11">Parcial / Sobreposta</text>
    <line x1="175" y1="172" x2="95" y2="225" stroke="#94a3b8" stroke-width="2"/>
    <line x1="205" y1="172" x2="285" y2="225" stroke="#94a3b8" stroke-width="2"/>
    <rect x="25" y="225" width="145" height="50" rx="4" fill="#1e293b" stroke="#38bdf8" stroke-width="2"/>
    <text x="97" y="247" fill="#f8fafc" font-size="12" font-weight="bold" text-anchor="middle">DOCENTE</text>
    <text x="97" y="264" fill="#94a3b8" font-size="10.5" text-anchor="middle">(Siape, RegimeDed)</text>
    <rect x="210" y="225" width="155" height="50" rx="4" fill="#1e293b" stroke="#38bdf8" stroke-width="2"/>
    <text x="287" y="247" fill="#f8fafc" font-size="12" font-weight="bold" text-anchor="middle">ALUNO_POS</text>
    <text x="287" y="264" fill="#94a3b8" font-size="10.5" text-anchor="middle">(NumMatr, CoefRend)</text>

    <!-- Ternary Relationship: BANCA_DEFESA connecting DOCENTE, ALUNO_POS, AUDITORIO -->
    <line x1="97" y1="275" x2="190" y2="350" stroke="#a855f7" stroke-width="2"/>
    <line x1="287" y1="275" x2="250" y2="350" stroke="#a855f7" stroke-width="2"/>
    <polygon points="220,320 285,355 220,390 155,355" fill="#1e293b" stroke="#a855f7" stroke-width="2"/>
    <text x="220" y="359" fill="#e9d5ff" font-size="10.5" font-weight="bold" text-anchor="middle">BANCA_DEFESA</text>
    <line x1="285" y1="355" x2="365" y2="355" stroke="#a855f7" stroke-width="2"/>
    <rect x="365" y="330" width="150" height="50" rx="4" fill="#1e293b" stroke="#38bdf8" stroke-width="2"/>
    <text x="440" y="352" fill="#f8fafc" font-size="12" font-weight="bold" text-anchor="middle">AUDITORIO</text>
    <text x="440" y="368" fill="#94a3b8" font-size="10.5" text-anchor="middle">(CodAud, Bloco)</text>
    <text x="120" y="325" fill="#e9d5ff" font-size="11" font-weight="bold">M</text>
    <text x="280" y="325" fill="#e9d5ff" font-size="11" font-weight="bold">N</text>
    <text x="330" y="347" fill="#e9d5ff" font-size="11" font-weight="bold">P</text>

    <!-- Right Hierarchy: BOLSA_PESQUISA == (d, total) ==> BOLSA_MESTRADO, BOLSA_DOUTORADO -->
    <rect x="575" y="40" width="250" height="50" rx="4" fill="#1e293b" stroke="#f59e0b" stroke-width="2.5"/>
    <text x="700" y="63" fill="#fde68a" font-size="12.5" font-weight="bold" text-anchor="middle">BOLSA_PESQUISA</text>
    <text x="700" y="80" fill="#cbd5e1" font-size="10.5" text-anchor="middle">(CodBolsa, AgenciaFomento, ValorMensal)</text>
    <line x1="697" y1="90" x2="697" y2="145" stroke="#f59e0b" stroke-width="3"/>
    <line x1="703" y1="90" x2="703" y2="145" stroke="#f59e0b" stroke-width="3"/>
    <circle cx="700" cy="162" r="17" fill="#1e293b" stroke="#f59e0b" stroke-width="2.5"/>
    <text x="700" y="167" fill="#fde68a" font-size="14" font-weight="bold" text-anchor="middle">d</text>
    <text x="775" y="125" fill="#fde68a" font-size="11" font-weight="bold">Total (Linha Dupla) / Disjunta</text>
    <line x1="685" y1="172" x2="600" y2="225" stroke="#f59e0b" stroke-width="2"/>
    <line x1="715" y1="172" x2="800" y2="225" stroke="#f59e0b" stroke-width="2"/>
    <rect x="515" y="225" width="175" height="55" rx="4" fill="#1e293b" stroke="#f59e0b" stroke-width="2"/>
    <text x="602" y="248" fill="#fde68a" font-size="12" font-weight="bold" text-anchor="middle">BOLSA_MESTRADO</text>
    <text x="602" y="266" fill="#cbd5e1" font-size="10.5" text-anchor="middle">(MesesDuracaoMestrado)</text>
    <rect x="715" y="225" width="185" height="55" rx="4" fill="#1e293b" stroke="#f59e0b" stroke-width="2"/>
    <text x="807" y="248" fill="#fde68a" font-size="12" font-weight="bold" text-anchor="middle">BOLSA_DOUTORADO</text>
    <text x="807" y="266" fill="#cbd5e1" font-size="10.5" text-anchor="middle">(TaxaBancadaDoutorado)</text>
  </svg>
</div>
"""

# ==============================================================================
# 2-COLUMN VISUAL STUDY GUIDES (CHEAT SHEETS WITH PARALLEL DOMAIN EXAMPLES)
# ==============================================================================

STUDY_GUIDE_G1 = {
    "id": "G1",
    "title": "Regras 1–6 (Mapeamento ER) e Políticas RIR (b, p, n)",
    "file_path": "study_guides/G1_Mapeamento_ER_Basico_e_RIRs.md",
    "coursework_ref": "ibd-parte5.pdf (Etapa 1: Regras 1 a 6)",
    "quick_rules_html": """
      <table class="compact-rule-table">
        <thead>
          <tr><th>Construção ER</th><th>Regra no Modelo Relacional</th><th>RIR</th></tr>
        </thead>
        <tbody>
          <tr><td><strong>2a. Composto</strong></td><td>Achatamento (<em>flattening</em>): entram só os sub-atributos simples.</td><td>—</td></tr>
          <tr><td><strong>2b. Multivalorado</strong></td><td>Nova relação <code>R_M(<u>PK_Dona(nn), M(nn)</u>)</code> com PK composta.</td><td><code>-p-&gt;</code></td></tr>
          <tr><td><strong>3. Entidade Fraca</strong></td><td>Importa <code>PK_Dona(nn)</code>; PK composta <code>(<u>PK_Dona, ChaveParcial</u>)</code>.</td><td><code>-p-&gt;</code></td></tr>
          <tr><td><strong>4. Rel. 1:1</strong></td><td>Lado de participação <strong>total <code>(1,1)</code></strong> absorve FK <code>(nn)</code> + <code>UNIQUE</code>.</td><td><code>-b-&gt;</code></td></tr>
          <tr><td><strong>5. Rel. 1:N</strong></td><td>Lado <strong>N</strong> (máximo <code>1</code> em <code>(min,max)</code>) absorve a FK do lado <strong>1</strong>.</td><td><code>-b-&gt; / -n-&gt;</code></td></tr>
          <tr><td><strong>6. Rel. M:N</strong></td><td>Nova tabela associativa <code>R(<u>PK_A(nn), PK_B(nn)</u>, Atrib)</code>.</td><td><code>-p-&gt;</code></td></tr>
        </tbody>
      </table>
    """,
    "example_html": """
      <div class="sg-example-drawer-inner">
        <div class="sg-example-header">
          <strong>🔄 Exemplo Análogo Resolvido (Domínio Diferente: <em>Rede Bancária</em>)</strong>
          <span>📄 Arquivo completo: <code>study_guides/G1_Mapeamento_ER_Basico_e_RIRs.md</code></span>
        </div>
        <p class="sg-hint-text">Considere <code>BANCO(CodBanco, Sede(Cidade, UF), {TelefonesSAC})</code> identificando a entidade fraca <code>AGENCIA(NumAgencia, Bairro)</code>, onde <code>AGENCIA (1,1)</code> é gerenciada por <code>FUNCIONARIO (0,1)</code>:</p>
        <pre><code>1. BANCO(CodBanco(nn), Cidade, UF)
   -- Atributo composto Sede(Cidade, UF) foi achatado (Regra 2a)

2. BANCO_TELEFONES(CodBanco(nn), TelefoneSAC(nn))
   PK: (CodBanco, TelefoneSAC) | RIR: BANCO_TELEFONES[CodBanco] -p-> BANCO[CodBanco] (Regra 2b)

3. AGENCIA(CodBanco(nn), NumAgencia(nn), Bairro, CPFGerente(nn), DataPosse)
   PK: (CodBanco, NumAgencia)  | UNIQUE: CPFGerente (Regra 3 + Regra 4 no lado total)
   RIR 1: AGENCIA[CodBanco]   -p-> BANCO[CodBanco]      (Entidade Fraca -> CASCADE)
   RIR 2: AGENCIA[CPFGerente] -b-> FUNCIONARIO[CPF]     (Gerente -> RESTRICT)</code></pre>
      </div>
    """
}

STUDY_GUIDE_G2 = {
    "id": "G2",
    "title": "Hierarquias EER (Opções 1, 2 e 3), CHECK e Ternários",
    "file_path": "study_guides/G2_Mapeamento_EER_Hierarquias_e_Ternarios.md",
    "coursework_ref": "ibd-parte5.pdf (Etapa 2: EER e Ternários)",
    "quick_rules_html": """
      <table class="compact-rule-table">
        <thead>
          <tr><th>Opção EER</th><th>Tabelas Criadas</th><th>Quando Usar / Restrição</th></tr>
        </thead>
        <tbody>
          <tr><td><strong>Opção 1</strong></td><td>Tabela única na Superclasse</td><td>Usa <code>CHECK</code> de tupla para impor <code>d</code> (disjunção) e/ou Totalidade.</td></tr>
          <tr><td><strong>Opção 2</strong></td><td>Apenas Tabelas das Subclasses</td><td><strong>Proibida se Parcial!</strong> Se for <code>o</code> (sobreposta), gera redundância.</td></tr>
          <tr><td><strong>Opção 3</strong></td><td>Superclasse + Subclasses</td><td>Universal. Subclasses herdam PK da superclasse com RIR <code>-p-&gt;</code>.</td></tr>
          <tr><td><strong>Ternário</strong></td><td>Tabela <code>R(<u>PK1, PK2, PK3</u>)</code></td><td>PK composta pelas 3 FKs participantes (ou 2 FKs se um lado for <code>1</code>).</td></tr>
        </tbody>
      </table>
    """,
    "example_html": """
      <div class="sg-example-drawer-inner">
        <div class="sg-example-header">
          <strong>🔄 Exemplo Análogo Resolvido (Domínio Diferente: <em>Frota Marítima</em>)</strong>
          <span>📄 Arquivo completo: <code>study_guides/G2_Mapeamento_EER_Hierarquias_e_Ternarios.md</code></span>
        </div>
        <p class="sg-hint-text"><code>EMBARCACAO(CodIMO, NomeNavio)</code> especializada de forma <strong>Disjunta e Total (<code>d</code>, linha dupla)</strong> em <code>PETROLEIRO(CapBarris)</code> e <code>PORTA_CONTENTOR(MaxTEUs)</code> mapeada pela <strong>Opção 1</strong>:</p>
        <pre><code>CREATE TABLE EMBARCACAO (
    CodIMO VARCHAR(15) NOT NULL PRIMARY KEY,
    NomeNavio VARCHAR(80) NOT NULL,
    CapBarris INTEGER,
    MaxTEUs INTEGER,
    CHECK (
        (CapBarris IS NOT NULL AND MaxTEUs IS NULL)
        OR
        (CapBarris IS NULL AND MaxTEUs IS NOT NULL)
    )
);</code></pre>
      </div>
    """
}

STUDY_GUIDE_G3 = {
    "id": "G3",
    "title": "DFs em Instâncias, Fecho X+ e Múltiplas Chaves",
    "file_path": "study_guides/G3_Dependencias_Funcionais_Instancias_e_Fecho.md",
    "coursework_ref": "ibd-parte6.pdf (Seções 1–3: DFs, X+ e Chaves)",
    "quick_rules_html": """
      <table class="compact-rule-table">
        <thead>
          <tr><th>Classe de Atributos</th><th>Onde Aparece nas DFs</th><th>Papel nas Chaves Candidatas</th></tr>
        </thead>
        <tbody>
          <tr><td><strong>Essenciais (<code>L</code>)</strong></td><td><strong>Nunca</strong> no lado direito (RHS)</td><td>Pertence obrigatoriamente a <strong>TODAS</strong> as chaves candidatas!</td></tr>
          <tr><td><strong>Somente-Direita (<code>D</code>)</strong></td><td><strong>Apenas</strong> no lado direito (RHS)</td><td><strong>Jamais</strong> faz parte de nenhuma chave candidata mínima.</td></tr>
          <tr><td><strong>Intermediários (<code>M</code>)</strong></td><td>Ambos os lados (LHS e RHS)</td><td>Se <code>L+ ≠ R</code>, estenda <code>L</code> com elementos de <code>M</code>.</td></tr>
          <tr><td><strong>Atributo Primo</strong></td><td>Pertence a <strong>alguma</strong> CK</td><td>Qualquer atributo em <code>CK1 ∪ CK2 ∪ ...</code> é primo!</td></tr>
        </tbody>
      </table>
    """,
    "example_html": """
      <div class="sg-example-drawer-inner">
        <div class="sg-example-header">
          <strong>🔄 Exemplo Análogo Resolvido (Domínio Diferente: <em>Esquema S(P, Q, R, T, U)</em>)</strong>
          <span>📄 Arquivo completo: <code>study_guides/G3_Dependencias_Funcionais_Instancias_e_Fecho.md</code></span>
        </div>
        <p class="sg-hint-text">Dado <code>S(P, Q, R, T, U)</code> com <code>F = { PQ → R, R → P, QR → T, T → U }</code>:</p>
        <pre><code>1. Nunca no RHS: L = {Q}  ==> Q está em toda chave!
2. Apenas no RHS: D = {U} ==> U nunca entra em chave.
3. Fecho {Q}+ = {Q} ≠ S. Testando pares com M = {P, R, T}:
   • {P, Q}+ = {P, Q, R, T, U} = S  ==> CK1 = {P, Q}
   • {Q, R}+ = {Q, R, P, T, U} = S  ==> CK2 = {Q, R}
   • {Q, T}+ = {Q, T, U} ≠ S        ==> Não é superchave.
4. Primos: {P, Q, R}  |  Não-Primos: {T, U}.</code></pre>
      </div>
    """
}

STUDY_GUIDE_G4 = {
    "id": "G4",
    "title": "Cobertura Mínima (3 Passos) e Formas Normais (1FN–3FN)",
    "file_path": "study_guides/G4_Cobertura_Minima_e_Normalizacao_1FN_2FN_3FN.md",
    "coursework_ref": "ibd-parte6.pdf (Seções 3.4 e 4: Fc, 2FN e 3FN)",
    "quick_rules_html": """
      <table class="compact-rule-table">
        <thead>
          <tr><th>Etapa / Forma Normal</th><th>Critério Formal dos Slides (<code>ibd-parte6.pdf</code>)</th></tr>
        </thead>
        <tbody>
          <tr><td><strong>Fc — Passo 1 (RHS)</strong></td><td>Decompor lado direito para conter apenas <strong>1 atributo</strong>: <code>X → AB</code> vira <code>X → A, X → B</code>.</td></tr>
          <tr><td><strong>Fc — Passo 2 (LHS)</strong></td><td>Atributo estranho no LHS: em <code>XY → Z</code>, se <code>Y ∈ {X}+</code>, simplifique para <code>X → Z</code>.</td></tr>
          <tr><td><strong>Fc — Passo 3 (DF)</strong></td><td>DF redundante: se <code>A ∈ {X}+</code> usando <code>F - {X → A}</code>, elimine <code>X → A</code>.</td></tr>
          <tr><td><strong>2FN (Geral)</strong></td><td>Nenhum atributo <strong>não-primo</strong> depende parcialmente de <em>qualquer</em> chave candidata.</td></tr>
          <tr><td><strong>3FN (Geral)</strong></td><td>Para toda <code>X → A</code> não-trivial: ou <code>X</code> é <strong>superchave</strong>, ou <code>A</code> é <strong>primo</strong>.</td></tr>
        </tbody>
      </table>
    """,
    "example_html": """
      <div class="sg-example-drawer-inner">
        <div class="sg-example-header">
          <strong>🔄 Exemplo Análogo Resolvido (Domínio Diferente: <em>SHOW_FESTIVAL</em>)</strong>
          <span>📄 Arquivo completo: <code>study_guides/G4_Cobertura_Minima_e_Normalizacao_1FN_2FN_3FN.md</code></span>
        </div>
        <p class="sg-hint-text"><code>SHOW(<u>CodFest, Ordem</u>, CodPalco, Horario, IdBanda, NomeBanda, CidadeFest, CapPalco)</code> com <code>CK1 = {CodFest, Ordem}</code> e <code>CK2 = {CodPalco, Horario}</code>:</p>
        <pre><code>• Atributos Primos: {CodFest, Ordem, CodPalco, Horario}
• Violações de 2FN (Parciais sobre CK1 e CK2):
  - CodFest → CidadeFest  ==> FESTIVAL(CodFest(nn), CidadeFest)
  - CodPalco → CapPalco   ==> PALCO(CodPalco(nn), CapPalco)
• Violação de 3FN (Transitiva entre não-primos):
  - IdBanda → NomeBanda   ==> BANDA(IdBanda(nn), NomeBanda)
• Relação Principal em 3FN:
  - SHOW(CodFest(nn), Ordem(nn), CodPalco(nn), Horario(nn), IdBanda(nn))</code></pre>
      </div>
    """
}

# ==============================================================================
# 10 HIGH-QUALITY ROUND 1 EXERCISES (R1.1 TO R1.10) — CLEAN VISUAL HTML
# ==============================================================================

ROUND1_EXERCISES: Dict[str, Dict[str, Any]] = {
    "R1.1": {
        "title": "[Rodada 1] Hospital ER (Parte 1): Entidades Fortes, Atributos Compostos/Multivalorados e Entidade Fraca",
        "type": "oficial",
        "mode": "structured",
        "context_html": HOSPITAL_ER_SVG + """
        <div class="task-checklist-bar">
          <div class="task-chip"><strong>1. Entidades Fortes:</strong> <code>ALA_HOSPITALAR</code>, <code>MEDICO</code>, <code>PACIENTE</code></div>
          <div class="task-chip"><strong>2. Atributos Especiais:</strong> Composto <code>Endereco(Rua, CEP)</code> e Multivalorado <code>{Especialidades}</code></div>
          <div class="task-chip"><strong>3. Entidade Fraca:</strong> <code>EXAME_LABORATORIAL</code> (chave parcial <code>NumSeqExame</code>)</div>
        </div>
        """,
        "study_guide": STUDY_GUIDE_G1,
        "answer_sheet_html": """
        <div class="ans-steps-grid">
          <div class="ans-step-card">
            <span class="ans-step-badge">PASSO 1 — ENTIDADES FORTES &amp; ATRIBUTO COMPOSTO (REGRAS 1 E 2A)</span>
            <p>O atributo composto <code>Endereco(Rua, CEP)</code> é achatado (<em>flattening</em>) em colunas atômicas dentro de <code>MEDICO</code>:</p>
            <pre><code>ALA_HOSPITALAR(CodAla(nn), NomeAla(nn), Andar)       -- PK: CodAla
MEDICO(CRM(nn), NomeMed(nn), Rua, CEP)               -- PK: CRM
PACIENTE(CNS(nn), NomePac(nn), CodAla, NumLeito)     -- PK: CNS</code></pre>
          </div>
          <div class="ans-step-card">
            <span class="ans-step-badge">PASSO 2 — ATRIBUTO MULTIVALORADO &amp; ENTIDADE FRACA (REGRAS 2B E 3)</span>
            <p>Tanto o atributo multivalorado quanto a entidade fraca exigem PK composta e RIR com política <strong><code>p</code> (propagação / CASCADE)</strong>:</p>
            <pre><code>MEDICO_ESPECIALIDADES(CRM(nn), Especialidade(nn))
  PK: (CRM, Especialidade)  |  RIR: MEDICO_ESPECIALIDADES[CRM] -p-> MEDICO[CRM]

EXAME_LABORATORIAL(CNS(nn), NumSeqExame(nn), TipoExame(nn))
  PK: (CNS, NumSeqExame)    |  RIR: EXAME_LABORATORIAL[CNS] -p-> PACIENTE[CNS]</code></pre>
          </div>
        </div>
        """,
        "fields": [
            {
                "id": "q1",
                "label": "1. Como os atributos Endereco(Rua, CEP) (composto) e {Especialidades} (multivalorado) da entidade MEDICO devem ser mapeados segundo a Etapa 1 de ibd-parte5.pdf?",
                "options": [
                    "Endereco vira uma nova tabela MEDICO_ENDERECO(CRM(nn), Rua, CEP) e Especialidades vira uma coluna simples de texto separado por vírgulas diretamente na relação MEDICO",
                    "Rua e CEP são achatados na relação MEDICO, enquanto Especialidades gera a relação MEDICO_ESPECIALIDADES(CRM(nn), Especialidade(nn)) com PK simples CRM e política b",
                    "Rua e CEP são achatados em MEDICO, e Especialidades gera a relação MEDICO_ESPECIALIDADES(CRM(nn), Especialidade(nn)) com PK (CRM, Especialidade) e RIR com política p",
                    "Tanto Endereco(Rua, CEP) quanto Especialidades geram relações separadas referenciando MEDICO[CRM] com chave primária simples CRM e política de remoção n (SET NULL)"
                ],
                "answer": "Rua e CEP são achatados em MEDICO, e Especialidades gera a relação MEDICO_ESPECIALIDADES(CRM(nn), Especialidade(nn)) com PK (CRM, Especialidade) e RIR com política p",
                "explanation": "Pela Regra 2a, atributos compostos são achatados (Rua e CEP entram em MEDICO). Pela Regra 2b, atributos multivalorados exigem uma nova relação cuja PK é a concatenação da PK da entidade dona com o próprio atributo, ligada por RIR de propagação (p)."
            },
            {
                "id": "q2",
                "label": "2. Qual é o mapeamento correto da entidade fraca EXAME_LABORATORIAL e de seu relacionamento identificador REALIZA_EXAME com PACIENTE?",
                "options": [
                    "EXAME_LABORATORIAL(NumSeqExame(nn), CNS(nn), TipoExame) com PK simples NumSeqExame e RIR EXAME_LABORATORIAL[CNS] -b-> PACIENTE[CNS]",
                    "EXAME_LABORATORIAL(CNS(nn), NumSeqExame(nn), TipoExame) com PK composta (CNS, NumSeqExame) e RIR EXAME_LABORATORIAL[CNS] -p-> PACIENTE[CNS]",
                    "EXAME_LABORATORIAL(NumSeqExame(nn), TipoExame) e uma tabela associativa separada REALIZA_EXAME(CNS(nn), NumSeqExame(nn)) com política de bloqueio b",
                    "EXAME_LABORATORIAL(CNS, NumSeqExame(nn), TipoExame) com chave estrangeira CNS anulável e RIR EXAME_LABORATORIAL[CNS] -n-> PACIENTE[CNS]"
                ],
                "answer": "EXAME_LABORATORIAL(CNS(nn), NumSeqExame(nn), TipoExame) com PK composta (CNS, NumSeqExame) e RIR EXAME_LABORATORIAL[CNS] -p-> PACIENTE[CNS]",
                "explanation": "Pela Regra 3 (Entidades Fracas), a relação EXAME_LABORATORIAL absorve a PK da entidade proprietária PACIENTE (CNS) para compor sua chave primária (CNS, NumSeqExame), sem criar tabela extra para o relacionamento identificador, e usa política p (propagação)."
            },
            {
                "id": "q3",
                "label": "3. Se um paciente tivesse vários exames registrados e tentássemos mapear EXAME_LABORATORIAL com PK simples apenas em (NumSeqExame) ou apenas em (CNS), qual anomalia estrutural ocorreria?",
                "options": [
                    "Com PK simples (CNS), cada paciente poderia realizar vários exames no mesmo dia, mas todos precisariam ter obrigatoriamente o mesmo TipoExame",
                    "Com PK simples (NumSeqExame), o SGBD impediria que qualquer paciente cadastrado realizasse o primeiro exame de número sequencial igual a 1",
                    "Com PK simples (NumSeqExame), dois pacientes distintos poderiam ter o exame nº 1, mas o mesmo paciente ficaria impedido de ter o exame nº 2",
                    "Com PK (CNS), um paciente só poderia ter 1 exame na vida; e com PK (NumSeqExame), dois pacientes distintos não poderiam ter ambos o exame nº 1"
                ],
                "answer": "Com PK (CNS), um paciente só poderia ter 1 exame na vida; e com PK (NumSeqExame), dois pacientes distintos não poderiam ter ambos o exame nº 1",
                "explanation": "A chave parcial NumSeqExame (1, 2, 3...) só é única dentro do escopo de um mesmo paciente (CNS). Por isso a chave primária precisa ser exatamente o par composto (CNS, NumSeqExame)."
            }
        ]
    },

    "R1.2": {
        "title": "[Rodada 1] Hospital ER (Parte 2): Relacionamentos 1:1, 1:N e M:N e Políticas de Remoção (b, p, n)",
        "type": "oficial",
        "mode": "structured",
        "context_html": HOSPITAL_ER_SVG + """
        <div class="task-checklist-bar">
          <div class="task-chip"><strong>1. Rel. 1:1 <code>CHEFIADA_POR</code>:</strong> <code>ALA_HOSPITALAR (1,1)</code> ↔ <code>MEDICO (0,1)</code> + <code>DataPosse</code></div>
          <div class="task-chip"><strong>2. Rel. 1:N <code>INTERNADO_EM</code>:</strong> <code>ALA_HOSPITALAR (0,N)</code> ↔ <code>PACIENTE (0,1)</code> + <code>NumLeito</code></div>
          <div class="task-chip"><strong>3. Rel. M:N <code>PRESCRICAO</code>:</strong> <code>MEDICO (0,N)</code> ↔ <code>PACIENTE (0,N)</code> + <code>Dosagem</code></div>
        </div>
        """,
        "study_guide": STUDY_GUIDE_G1,
        "answer_sheet_html": """
        <div class="ans-steps-grid">
          <div class="ans-step-card">
            <span class="ans-step-badge">PASSO 1 — RELACIONAMENTO 1:1 CHEFIADA_POR (REGRA 4)</span>
            <p><code>ALA_HOSPITALAR</code> tem participação <strong>total <code>(1,1)</code></strong>, logo absorve <code>CRMChefe(nn)</code> com <code>UNIQUE</code> e <code>DataPosse</code> (zero nulos!):</p>
            <pre><code>ALA_HOSPITALAR(CodAla(nn), NomeAla(nn), Andar, CRMChefe(nn), DataPosse)
  PK: CodAla  |  Chave Alternativa (UNIQUE): CRMChefe
  RIR: ALA_HOSPITALAR[CRMChefe] -b-> MEDICO[CRM]</code></pre>
          </div>
          <div class="ans-step-card">
            <span class="ans-step-badge">PASSO 2 — RELACIONAMENTOS 1:N INTERNADO_EM &amp; M:N PRESCRICAO (REGRAS 5 E 6)</span>
            <p><code>PACIENTE</code> está no lado N (cardinalidade máxima 1 em <code>(0,1)</code>) e recebe <code>CodAla</code> e <code>NumLeito</code> anuláveis. Já <code>PRESCRICAO</code> vira nova tabela:</p>
            <pre><code>PACIENTE(CNS(nn), NomePac(nn), CodAla, NumLeito)
  PK: CNS  |  RIR: PACIENTE[CodAla] -b-> ALA_HOSPITALAR[CodAla]

PRESCRICAO(CRM(nn), CNS(nn), Dosagem)
  PK: (CRM, CNS)
  RIR 1: PRESCRICAO[CRM] -b-> MEDICO[CRM]  |  RIR 2: PRESCRICAO[CNS] -p-> PACIENTE[CNS]</code></pre>
          </div>
        </div>
        """,
        "fields": [
            {
                "id": "q1",
                "label": "1. No relacionamento 1:1 CHEFIADA_POR entre ALA_HOSPITALAR (1,1) e MEDICO (0,1) com atributo DataPosse, qual é a melhor escolha de posicionamento da chave estrangeira para evitar valores NULL?",
                "options": [
                    "Incluir CodAlaChefiada(nn) e DataPosse na relação MEDICO, declarando CodAlaChefiada como chave alternativa UNIQUE e política b",
                    "Fundir ALA_HOSPITALAR e MEDICO em uma única relação ALA_MEDICO(CodAla(nn), CRM(nn), NomeAla, NomeMed, DataPosse) sem chaves estrangeiras",
                    "Incluir CRMChefe(nn) e DataPosse em ALA_HOSPITALAR (participação total), declarando UNIQUE(CRMChefe) e RIR com política b",
                    "Criar obrigatoriamente uma terceira relação associativa CHEFIADA_POR(CodAla(nn), CRM(nn), DataPosse) com PK composta (CodAla, CRM)"
                ],
                "answer": "Incluir CRMChefe(nn) e DataPosse em ALA_HOSPITALAR (participação total), declarando UNIQUE(CRMChefe) e RIR com política b",
                "explanation": "Em relacionamentos 1:1 onde apenas um lado tem participação total (1,1), a relação de participação total (ALA_HOSPITALAR) absorve a FK (CRMChefe) com restrição NOT NULL e UNIQUE, evitando nulos nos médicos que não são chefes."
            },
            {
                "id": "q2",
                "label": "2. No relacionamento 1:N INTERNADO_EM entre ALA_HOSPITALAR (0,N) e PACIENTE (0,1) com o atributo NumLeito, onde devem ficar a chave estrangeira e o atributo NumLeito?",
                "options": [
                    "Na relação PACIENTE, que recebe CodAla (anulável) e NumLeito (anulável), pois PACIENTE está no lado N (cardinalidade máxima 1)",
                    "Na relação ALA_HOSPITALAR, que recebe CNSPaciente(nn) e NumLeito(nn), pois ALA_HOSPITALAR possui cardinalidade máxima igual a N",
                    "O atributo NumLeito fica na relação ALA_HOSPITALAR e a chave estrangeira CodAla fica na relação PACIENTE com restrição NOT NULL",
                    "Ambos os atributos devem ser migrados para a relação fraca EXAME_LABORATORIAL para manter todas as chaves estrangeiras reunidas"
                ],
                "answer": "Na relação PACIENTE, que recebe CodAla (anulável) e NumLeito (anulável), pois PACIENTE está no lado N (cardinalidade máxima 1)",
                "explanation": "Na notação (min, max), PACIENTE tem (0,1), o que significa que cada paciente está internado em no máximo 1 ala (lado N na notação tradicional). Como min = 0 (participação parcial), CodAla e NumLeito ficam em PACIENTE e permitem NULL."
            },
            {
                "id": "q3",
                "label": "3. Compare as políticas de remoção de RIR adequadas para ALA_HOSPITALAR[CRMChefe] -> MEDICO[CRM] e EXAME_LABORATORIAL[CNS] -> PACIENTE[CNS]:",
                "options": [
                    "Ambas as restrições devem usar política n (substituição por nulos / SET NULL), pois tanto CRMChefe quanto CNS aceitam valores nulos",
                    "ALA_HOSPITALAR[CRMChefe] usa política p (propagação em cascata) e EXAME_LABORATORIAL[CNS] usa política b (bloqueio / RESTRICT)",
                    "ALA_HOSPITALAR[CRMChefe] usa política n (substituição por nulos) e EXAME_LABORATORIAL[CNS] usa política b (bloqueio / RESTRICT)",
                    "ALA_HOSPITALAR[CRMChefe] usa política b (bloqueio, pois a FK é nn) e EXAME_LABORATORIAL[CNS] usa política p (entidade fraca)"
                ],
                "answer": "ALA_HOSPITALAR[CRMChefe] usa política b (bloqueio, pois a FK é nn) e EXAME_LABORATORIAL[CNS] usa política p (entidade fraca)",
                "explanation": "Como toda ala exige um chefe (CRMChefe é nn) e uma ala não deve ser apagada se seu médico chefe sair sem substituto, usa-se b (bloqueio). Já EXAME_LABORATORIAL depende existencialmente de PACIENTE, exigindo política p (propagação)."
            }
        ]
    },

    "R1.3": {
        "title": "[Rodada 1] Hospital DDL: Implementação SQL de Entidade Fraca e Políticas ON DELETE",
        "type": "oficial",
        "mode": "sql_ddl",
        "context_html": HOSPITAL_ER_SVG + """
        <div class="task-checklist-bar">
          <div class="task-chip"><strong>Tabela 1:</strong> <code>ALA_HOSPITALAR(<u>CodAla</u>, NomeAla, Andar)</code></div>
          <div class="task-chip"><strong>Tabela 2:</strong> <code>PACIENTE(<u>CNS</u>, NomePac, CodAla, NumLeito)</code> com <code>ON DELETE RESTRICT</code></div>
          <div class="task-chip"><strong>Tabela 3:</strong> <code>EXAME_LABORATORIAL(<u>CNS, NumSeqExame</u>, TipoExame)</code> com <code>ON DELETE CASCADE</code></div>
        </div>
        """,
        "study_guide": STUDY_GUIDE_G1,
        "answer_sheet_html": """
        <div class="ans-steps-grid">
          <div class="ans-step-card">
            <span class="ans-step-badge">GABARITO OFICIAL — SCRIPT SQL DDL COMPLETO (R1.3)</span>
            <pre><code>CREATE TABLE ALA_HOSPITALAR (
    CodAla INTEGER NOT NULL,
    NomeAla TEXT NOT NULL,
    Andar INTEGER,
    PRIMARY KEY (CodAla)
);

CREATE TABLE PACIENTE (
    CNS TEXT NOT NULL,
    NomePac TEXT NOT NULL,
    CodAla INTEGER,
    NumLeito INTEGER,
    PRIMARY KEY (CNS),
    FOREIGN KEY (CodAla) REFERENCES ALA_HOSPITALAR(CodAla) ON DELETE RESTRICT
);

CREATE TABLE EXAME_LABORATORIAL (
    CNS TEXT NOT NULL,
    NumSeqExame INTEGER NOT NULL,
    TipoExame TEXT NOT NULL,
    PRIMARY KEY (CNS, NumSeqExame),
    FOREIGN KEY (CNS) REFERENCES PACIENTE(CNS) ON DELETE CASCADE
);</code></pre>
          </div>
        </div>
        """,
        "setup": "",
        "ddl_tests": [
            {
                "name": "1. Verificar criação das tabelas ALA_HOSPITALAR, PACIENTE e EXAME_LABORATORIAL",
                "type": "tables_exist",
                "tables": ["ALA_HOSPITALAR", "PACIENTE", "EXAME_LABORATORIAL"]
            },
            {
                "name": "2. Inserir alas, pacientes (internados e ambulatoriais) e exames com mesmo NumSeqExame para pacientes distintos",
                "type": "must_succeed",
                "sql": """
                    INSERT INTO ALA_HOSPITALAR (CodAla, NomeAla, Andar) VALUES (10, 'Cardiologia', 2);
                    INSERT INTO PACIENTE (CNS, NomePac, CodAla, NumLeito) VALUES ('7001', 'Ana Costa', 10, 204);
                    INSERT INTO PACIENTE (CNS, NomePac, CodAla, NumLeito) VALUES ('7002', 'Carlos Lima', NULL, NULL);
                    INSERT INTO EXAME_LABORATORIAL (CNS, NumSeqExame, TipoExame) VALUES ('7001', 1, 'Hemograma');
                    INSERT INTO EXAME_LABORATORIAL (CNS, NumSeqExame, TipoExame) VALUES ('7001', 2, 'Ecocardiograma');
                    INSERT INTO EXAME_LABORATORIAL (CNS, NumSeqExame, TipoExame) VALUES ('7002', 1, 'Raio-X');
                """,
                "hint": "As tabelas devem aceitar pacientes com CodAla NULL e diferentes pacientes com NumSeqExame = 1."
            },
            {
                "name": "3. Rejeitar duplicata da chave composta (CNS, NumSeqExame) para o mesmo paciente",
                "type": "must_fail",
                "sql": """
                    INSERT INTO ALA_HOSPITALAR (CodAla, NomeAla, Andar) VALUES (10, 'Cardiologia', 2);
                    INSERT INTO PACIENTE (CNS, NomePac, CodAla, NumLeito) VALUES ('7001', 'Ana Costa', 10, 204);
                    INSERT INTO EXAME_LABORATORIAL (CNS, NumSeqExame, TipoExame) VALUES ('7001', 1, 'Hemograma');
                    INSERT INTO EXAME_LABORATORIAL (CNS, NumSeqExame, TipoExame) VALUES ('7001', 1, 'Glicemia');
                """,
                "hint": "A chave primária de EXAME_LABORATORIAL deve ser composta por PRIMARY KEY (CNS, NumSeqExame)."
            },
            {
                "name": "4. Bloquear exclusão de ALA_HOSPITALAR que possui paciente internado (ON DELETE RESTRICT)",
                "type": "must_fail",
                "sql": """
                    INSERT INTO ALA_HOSPITALAR (CodAla, NomeAla, Andar) VALUES (10, 'Cardiologia', 2);
                    INSERT INTO PACIENTE (CNS, NomePac, CodAla, NumLeito) VALUES ('7001', 'Ana Costa', 10, 204);
                    DELETE FROM ALA_HOSPITALAR WHERE CodAla = 10;
                """,
                "hint": "A FK CodAla em PACIENTE deve usar ON DELETE RESTRICT (política de bloqueio b)."
            },
            {
                "name": "5. Propagar exclusão de PACIENTE apagando seus exames laboratoriais (ON DELETE CASCADE)",
                "type": "cascade_check",
                "sql_setup": """
                    INSERT INTO PACIENTE (CNS, NomePac, CodAla, NumLeito) VALUES ('7002', 'Carlos Lima', NULL, NULL);
                    INSERT INTO EXAME_LABORATORIAL (CNS, NumSeqExame, TipoExame) VALUES ('7002', 1, 'Raio-X');
                    INSERT INTO EXAME_LABORATORIAL (CNS, NumSeqExame, TipoExame) VALUES ('7002', 2, 'Tomografia');
                    DELETE FROM PACIENTE WHERE CNS = '7002';
                """,
                "verify_query": "SELECT COUNT(*) FROM EXAME_LABORATORIAL WHERE CNS = '7002';",
                "expected_scalar": 0,
                "hint": "A FK CNS na entidade fraca EXAME_LABORATORIAL deve ter ON DELETE CASCADE (política de propagação p)."
            }
        ]
    },

    "R1.4": {
        "title": "[Rodada 1] Universidade EER: Hierarquias (Sobreposta/Parcial vs. Disjunta/Total) e Relacionamento Ternário",
        "type": "oficial",
        "mode": "structured",
        "context_html": UNIVERSITY_EER_SVG + """
        <div class="task-checklist-bar">
          <div class="task-chip"><strong>1. Hierarquia Esquerda:</strong> <code>PESSOA</code> → <code>{DOCENTE, ALUNO_POS}</code> (Parcial e Sobreposta <code>o</code>)</div>
          <div class="task-chip"><strong>2. Hierarquia Direita:</strong> <code>BOLSA_PESQUISA</code> ⇒ <code>{MESTRADO, DOUTORADO}</code> (Total e Disjunta <code>d</code>)</div>
          <div class="task-chip"><strong>3. Relacionamento Ternário:</strong> <code>BANCA_DEFESA (M:N:P)</code> entre Docente, Aluno e Auditório</div>
        </div>
        """,
        "study_guide": STUDY_GUIDE_G2,
        "answer_sheet_html": """
        <div class="ans-steps-grid">
          <div class="ans-step-card">
            <span class="ans-step-badge">PASSO 1 — HIERARQUIA PARCIAL &amp; SOBREPOSTA PESSOA (OPÇÃO 3)</span>
            <p>A Opção 2 (apenas subclasses) é proibida pois a cobertura é <strong>parcial</strong> e <strong>sobreposta</strong>. Pela Opção 3:</p>
            <pre><code>PESSOA(CPF(nn), Nome(nn))                        -- PK: CPF
DOCENTE(CPF(nn), Siape(nn), RegimeDed)           -- PK: CPF | RIR: -p-> PESSOA[CPF]
ALUNO_POS(CPF(nn), NumMatr(nn), CoefRend)        -- PK: CPF | RIR: -p-> PESSOA[CPF]</code></pre>
          </div>
          <div class="ans-step-card">
            <span class="ans-step-badge">PASSO 2 — HIERARQUIA TOTAL &amp; DISJUNTA BOLSA (OPÇÃO 1) E TERNÁRIO BANCA_DEFESA</span>
            <pre><code>BOLSA_PESQUISA(CodBolsa(nn), AgenciaFomento(nn), ValorMensal(nn), MesesDuracaoMestrado, TaxaBancadaDoutorado)
  PK: CodBolsa | CHECK ((MesesDuracaoMestrado IS NOT NULL AND TaxaBancadaDoutorado IS NULL)
                     OR (MesesDuracaoMestrado IS NULL AND TaxaBancadaDoutorado IS NOT NULL))

BANCA_DEFESA(CPFDocente(nn), CPFAlunoPos(nn), CodAud(nn))
  PK: (CPFDocente, CPFAlunoPos, CodAud) | 3 RIRs com política -p-></code></pre>
          </div>
        </div>
        """,
        "fields": [
            {
                "id": "q1",
                "label": "1. Por que a Opção 2 da Etapa 2 de ibd-parte5.pdf (criar apenas as tabelas DOCENTE e ALUNO_POS, eliminando a tabela PESSOA) NÃO deve ser aplicada à hierarquia PESSOA?",
                "options": [
                    "Porque a Opção 2 só é permitida pelo SGBD quando todas as subclasses possuem chaves parciais tracejadas distintas da superclasse",
                    "Porque a hierarquia é parcial (perdendo pessoas fora das subclasses) e sobreposta 'o' (duplicando Nome para docente/aluno)",
                    "Porque a Opção 2 obriga o uso de chaves estrangeiras circulares mútuas entre DOCENTE e ALUNO_POS com política de bloqueio b",
                    "Porque o relacionamento ternário BANCA_DEFESA impede que as subclasses DOCENTE e ALUNO_POS herdem a chave primária CPF de PESSOA"
                ],
                "answer": "Porque a hierarquia é parcial (perdendo pessoas fora das subclasses) e sobreposta 'o' (duplicando Nome para docente/aluno)",
                "explanation": "Conforme ibd-parte5.pdf (Etapa 2), a Opção 2 descarta a relação da superclasse; logo, se a cobertura for parcial, entidades da superclasse que não pertencem a nenhuma subclasse não podem ser armazenadas. Além disso, em hierarquias sobrepostas ('o'), os atributos gerais são replicados com redundância."
            },
            {
                "id": "q2",
                "label": "2. Ao mapear a hierarquia PESSOA -> {DOCENTE, ALUNO_POS} pela Opção 3 (uma relação para a superclasse e uma para cada subclasse), quais são as chaves primárias e as RIRs de DOCENTE e ALUNO_POS?",
                "options": [
                    "Ambas têm PK CPF (herdada de PESSOA) e RIRs DOCENTE[CPF] -p-> PESSOA[CPF] e ALUNO_POS[CPF] -p-> PESSOA[CPF] com política p",
                    "DOCENTE tem PK simples Siape e ALUNO_POS tem PK simples NumMatr, sem declarar nenhuma chave estrangeira apontando para PESSOA[CPF]",
                    "Ambas têm PK simples CPF e RIRs DOCENTE[CPF] -n-> PESSOA[CPF] e ALUNO_POS[CPF] -n-> PESSOA[CPF] com política n (SET NULL)",
                    "A relação PESSOA importa Siape e NumMatr como chaves estrangeiras anuláveis referenciando as subclasses com política b (bloqueio)"
                ],
                "answer": "Ambas têm PK CPF (herdada de PESSOA) e RIRs DOCENTE[CPF] -p-> PESSOA[CPF] e ALUNO_POS[CPF] -p-> PESSOA[CPF] com política p",
                "explanation": "Na Opção 3, cada relação de subclasse importa a chave primária da superclasse (CPF) como sua própria PK e simultaneamente como FK referenciando a superclasse com política de propagação (p)."
            },
            {
                "id": "q3",
                "label": "3. Como deve ser mapeado o relacionamento ternário BANCA_DEFESA (M:N:P) entre DOCENTE, ALUNO_POS e AUDITORIO?",
                "options": [
                    "Incluindo CodAud(nn) e CPFDocente(nn) como chaves estrangeiras simples diretamente na relação ALUNO_POS com política de bloqueio b",
                    "Criando duas tabelas binárias independentes DEFESA_DOCENTE(CPFDocente, CPFAlunoPos) e DEFESA_SALA(CPFAlunoPos, CodAud) com política p",
                    "Incluindo os atributos CPFAlunoPos e CPFDocente como colunas de chave estrangeira diretamente dentro da relação forte AUDITORIO",
                    "Criando BANCA_DEFESA(CPFDocente(nn), CPFAlunoPos(nn), CodAud(nn)) com PK composta pelos 3 atributos e 3 RIRs com política p"
                ],
                "answer": "Criando BANCA_DEFESA(CPFDocente(nn), CPFAlunoPos(nn), CodAud(nn)) com PK composta pelos 3 atributos e 3 RIRs com política p",
                "explanation": "Um relacionamento ternário M:N:P exige uma relação própria cuja chave primária é a união das chaves primárias das três entidades participantes (CPFDocente, CPFAlunoPos, CodAud)."
            }
        ]
    },

    "R1.5": {
        "title": "[Rodada 1] Universidade DDL: Hierarquia Disjunta e Total com Cláusula CHECK (Opção 1)",
        "type": "oficial",
        "mode": "sql_ddl",
        "context_html": UNIVERSITY_EER_SVG + """
        <div class="task-checklist-bar">
          <div class="task-chip"><strong>Tabela Única:</strong> <code>BOLSA_PESQUISA(<u>CodBolsa</u>, AgenciaFomento, ValorMensal, MesesDuracaoMestrado, TaxaBancadaDoutorado)</code></div>
          <div class="task-chip"><strong>Restrição CHECK:</strong> Impor <strong>Disjunção (<code>d</code>)</strong> + <strong>Totalidade (Linha Dupla)</strong> entre Mestrado e Doutorado</div>
        </div>
        """,
        "study_guide": STUDY_GUIDE_G2,
        "answer_sheet_html": """
        <div class="ans-steps-grid">
          <div class="ans-step-card">
            <span class="ans-step-badge">GABARITO OFICIAL — SCRIPT SQL DDL COMPLETO (R1.5)</span>
            <pre><code>CREATE TABLE BOLSA_PESQUISA (
    CodBolsa INTEGER NOT NULL,
    AgenciaFomento TEXT NOT NULL,
    ValorMensal REAL NOT NULL,
    MesesDuracaoMestrado INTEGER,
    TaxaBancadaDoutorado REAL,
    PRIMARY KEY (CodBolsa),
    CHECK (
        (MesesDuracaoMestrado IS NOT NULL AND TaxaBancadaDoutorado IS NULL)
        OR
        (MesesDuracaoMestrado IS NULL AND TaxaBancadaDoutorado IS NOT NULL)
    )
);</code></pre>
          </div>
        </div>
        """,
        "setup": "",
        "ddl_tests": [
            {
                "name": "1. Verificar criação da tabela BOLSA_PESQUISA",
                "type": "tables_exist",
                "tables": ["BOLSA_PESQUISA"]
            },
            {
                "name": "2. Aceitar uma bolsa válida de Mestrado e uma bolsa válida de Doutorado",
                "type": "must_succeed",
                "sql": """
                    INSERT INTO BOLSA_PESQUISA (CodBolsa, AgenciaFomento, ValorMensal, MesesDuracaoMestrado, TaxaBancadaDoutorado)
                    VALUES (1, 'CAPES', 2100.0, 24, NULL);
                    INSERT INTO BOLSA_PESQUISA (CodBolsa, AgenciaFomento, ValorMensal, MesesDuracaoMestrado, TaxaBancadaDoutorado)
                    VALUES (2, 'CNPq', 3100.0, NULL, 1200.0);
                """,
                "hint": "A tabela BOLSA_PESQUISA deve aceitar bolsas exclusivamente de mestrado ou exclusivamente de doutorado."
            },
            {
                "name": "3. Rejeitar violação de Disjunção ('d'): bolsa com ambos os atributos preenchidos",
                "type": "must_fail",
                "sql": """
                    INSERT INTO BOLSA_PESQUISA (CodBolsa, AgenciaFomento, ValorMensal, MesesDuracaoMestrado, TaxaBancadaDoutorado)
                    VALUES (3, 'FAPEMIG', 3500.0, 24, 1000.0);
                """,
                "hint": "Sua cláusula CHECK precisa impedir que MesesDuracaoMestrado e TaxaBancadaDoutorado sejam ambos NOT NULL."
            },
            {
                "name": "4. Rejeitar violação de Totalidade (Linha Dupla): bolsa com ambos os atributos NULL",
                "type": "must_fail",
                "sql": """
                    INSERT INTO BOLSA_PESQUISA (CodBolsa, AgenciaFomento, ValorMensal, MesesDuracaoMestrado, TaxaBancadaDoutorado)
                    VALUES (4, 'CAPES', 2100.0, NULL, NULL);
                """,
                "hint": "Como a hierarquia é TOTAL (linha dupla), sua cláusula CHECK deve rejeitar tuplas onde ambos os atributos específicos sejam NULL."
            }
        ]
    },

    "R1.6": {
        "title": "[Rodada 1] Detetive de DFs em Instância: Auditoria SQL de Violação em ESCALA_NAVIO",
        "type": "oficial",
        "mode": "sql_query",
        "context_html": """
        <div class="schema-card-box">
          <div class="schema-card-header">🗄️ Esquema Analisado: <code>ESCALA_NAVIO(<u>IdEscala</u>, NomeNavio, TipoNavio, Porto, PaisPorto, Comandante, Tonelagem)</code></div>
          <div class="fd-grid">
            <div class="fd-chip fd-target">🔍 DF Auditada no SQL: <strong>NomeNavio → Comandante</strong></div>
            <div class="fd-chip">Condição de Violação: <code>t1[NomeNavio] = t2[NomeNavio]</code> E <code>t1[Comandante] &lt;&gt; t2[Comandante]</code></div>
            <div class="fd-chip">Colunas Esperadas: <code>IdEscala, NomeNavio, Comandante, Porto</code> (ordenadas por <code>IdEscala</code>)</div>
          </div>
        </div>
        """,
        "study_guide": STUDY_GUIDE_G3,
        "answer_sheet_html": """
        <div class="ans-steps-grid">
          <div class="ans-step-card">
            <span class="ans-step-badge">PASSO 1 — CONSULTA SQL DE AUDITORIA (SELF-JOIN DE CONTRAEXEMPLO)</span>
            <pre><code>SELECT DISTINCT e1.IdEscala, e1.NomeNavio, e1.Comandante, e1.Porto
FROM ESCALA_NAVIO e1
JOIN ESCALA_NAVIO e2
  ON e1.NomeNavio = e2.NomeNavio
 AND e1.Comandante &lt;&gt; e2.Comandante
ORDER BY e1.IdEscala;</code></pre>
          </div>
          <div class="ans-step-card">
            <span class="ans-step-badge">PASSO 2 — DIAGNÓSTICO DAS DEMAIS DFs NA INSTÂNCIA ESCALA_NAVIO</span>
            <pre><code>• NomeNavio → Comandante : REFUTADA! ('Mercator' tem 'Cap. Rocha' nas escalas 1 e 4, mas 'Cap. Viana' na 6)
• Porto → PaisPorto      : SATISFEITA na instância ('Santos' → 'Brasil', etc.)
• NomeNavio → Tonelagem  : SATISFEITA na instância ('Mercator' → 85000, 'Solaris' → 62000)</code></pre>
          </div>
        </div>
        """,
        "setup": """
            CREATE TABLE ESCALA_NAVIO (
                IdEscala INTEGER PRIMARY KEY,
                NomeNavio TEXT,
                TipoNavio TEXT,
                Porto TEXT,
                PaisPorto TEXT,
                Comandante TEXT,
                Tonelagem INTEGER
            );
            INSERT INTO ESCALA_NAVIO VALUES
                (1, 'Mercator', 'Porta-Contentor', 'Santos', 'Brasil', 'Cap. Rocha', 85000),
                (2, 'Solaris', 'Graneleiro', 'Paranagua', 'Brasil', 'Cap. Mendes', 62000),
                (3, 'Boreal', 'Petroleiro', 'Rotterdam', 'Holanda', 'Cap. Silva', 110000),
                (4, 'Mercator', 'Porta-Contentor', 'Hamburgo', 'Alemanha', 'Cap. Rocha', 85000),
                (5, 'Solaris', 'Graneleiro', 'Santos', 'Brasil', 'Cap. Mendes', 62000),
                (6, 'Mercator', 'Porta-Contentor', 'Antuerpia', 'Belgica', 'Cap. Viana', 85000);
        """,
        "expected_columns": ["IdEscala", "NomeNavio", "Comandante", "Porto"],
        "expected_rows": [
            [1, "Mercator", "Cap. Rocha", "Santos"],
            [4, "Mercator", "Cap. Rocha", "Hamburgo"],
            [6, "Mercator", "Cap. Viana", "Antuerpia"]
        ]
    },

    "R1.7": {
        "title": "[Rodada 1] Fecho X+ e Múltiplas Chaves Candidatas em R(A, B, C, D, E, G)",
        "type": "oficial",
        "mode": "structured",
        "context_html": """
        <div class="schema-card-box">
          <div class="schema-card-header">📐 Esquema Relacional: <code>R(A, B, C, D, E, G)</code> — Descoberta de Todas as Chaves Candidatas</div>
          <div class="fd-grid">
            <div class="fd-chip"><strong>DF1:</strong> <code>A, B → C</code></div>
            <div class="fd-chip"><strong>DF2:</strong> <code>C → A</code></div>
            <div class="fd-chip"><strong>DF3:</strong> <code>B, C → D</code></div>
            <div class="fd-chip"><strong>DF4:</strong> <code>A, C, D → B</code></div>
            <div class="fd-chip"><strong>DF5:</strong> <code>D → E, G</code></div>
            <div class="fd-chip"><strong>DF6:</strong> <code>B, E → C</code></div>
          </div>
          <div class="task-checklist-bar" style="margin-top:10px;">
            <div class="task-chip"><strong>1. Calcular Fechos:</strong> <code>{C, D}+</code> e <code>{A, D}+</code></div>
            <div class="task-chip"><strong>2. Encontrar TODAS as Chaves Candidatas</strong> de tamanho 2</div>
            <div class="task-chip"><strong>3. Separar:</strong> Atributos Primos vs. Não-Primos</div>
          </div>
        </div>
        """,
        "study_guide": STUDY_GUIDE_G3,
        "answer_sheet_html": """
        <div class="ans-steps-grid">
          <div class="ans-step-card">
            <span class="ans-step-badge">PASSO 1 — PARTICIONAMENTO DOS ATRIBUTOS DE R(A, B, C, D, E, G)</span>
            <pre><code>• Somente à Direita (Nunca no LHS): D_dir = {G}  ==> G jamais pertencerá a uma chave candidata!
• Atributos Unitários: {A}+={A}, {B}+={B}, {C}+={A,C}, {D}+={D,E,G}, {E}+={E} (nenhum fecha R sozinho).</code></pre>
          </div>
          <div class="ans-step-card">
            <span class="ans-step-badge">PASSO 2 — AS 5 CHAVES CANDIDATAS E ATRIBUTOS PRIMOS / NÃO-PRIMOS</span>
            <pre><code>1. {A, B}+ = {A, B, C, D, E, G} = R   (CK1)
2. {B, C}+ = {A, B, C, D, E, G} = R   (CK2 — via C → A e BC → D → EG)
3. {B, D}+ = {A, B, C, D, E, G} = R   (CK3 — via D → EG, BE → C e C → A)
4. {B, E}+ = {A, B, C, D, E, G} = R   (CK4 — via BE → C, BC → D → EG e C → A)
5. {C, D}+ = {A, B, C, D, E, G} = R   (CK5 — via C → A, ACD → B e D → EG)

• Atributos Primos (em CK1..CK5): {A, B, C, D, E}
• Único Atributo Não-Primo:       {G}</code></pre>
          </div>
        </div>
        """,
        "fields": [
            {
                "id": "q1",
                "label": "1. Calcule os fechos {C, D}+ e {A, D}+ sob o conjunto F = {AB -> C, C -> A, BC -> D, ACD -> B, D -> EG, BE -> C}:",
                "options": [
                    "{C, D}+ = {A, B, C, D, E, G} (é chave candidata)  e  {A, D}+ = {A, D, E, G} (não é superchave)",
                    "{C, D}+ = {A, C, D, E, G} (não é superchave)  e  {A, D}+ = {A, B, C, D, E, G} (é chave candidata)",
                    "{C, D}+ = {C, D, E, G} (não é superchave)  e  {A, D}+ = {A, B, D, E, G} (não é superchave)",
                    "{C, D}+ = {A, B, C, D, E, G} (é chave candidata)  e  {A, D}+ = {A, B, C, D, E, G} (é chave candidata)"
                ],
                "answer": "{C, D}+ = {A, B, C, D, E, G} (é chave candidata)  e  {A, D}+ = {A, D, E, G} (não é superchave)",
                "explanation": "A partir de {C, D}, usamos C -> A para obter {A, C, D}; em seguida ACD -> B gera {A, B, C, D}; e D -> EG gera {A, B, C, D, E, G} = R. Já {A, D} só dispara D -> EG, parando em {A, D, E, G}."
            },
            {
                "id": "q2",
                "label": "2. Qual é o conjunto completo de todas as chaves candidatas mínimas da relação R(A, B, C, D, E, G)?",
                "options": [
                    "Apenas {A, B} e {B, C}, pois D e E são determinados transitivamente a partir de BC -> D",
                    "Apenas {A, B, D} e {B, C, E}, pois chaves candidatas precisam conter pelo menos três atributos",
                    "Exatamente 5 chaves candidatas de tamanho 2: {A, B}, {B, C}, {B, D}, {B, E} e {C, D}",
                    "Exatamente 3 chaves candidatas de tamanho 2: {A, B}, {A, C} e {A, D}"
                ],
                "answer": "Exatamente 5 chaves candidatas de tamanho 2: {A, B}, {B, C}, {B, D}, {B, E} e {C, D}",
                "explanation": "Nenhum atributo unitário fecha R, e exatamente os cinco pares {A, B}, {B, C}, {B, D}, {B, E} e {C, D} têm fecho igual a {A, B, C, D, E, G}."
            },
            {
                "id": "q3",
                "label": "3. Com base nas chaves candidatas encontradas, quais são os atributos NÃO-PRIMOS da relação R(A, B, C, D, E, G)?",
                "options": [
                    "Os atributos {D, E, G}, pois aparecem no lado direito de BC -> D e D -> EG",
                    "Apenas o atributo {G}, pois A, B, C, D e E participam de pelo menos uma chave candidata",
                    "Os atributos {E, G}, pois ambos são determinados diretamente pelo atributo não-chave D",
                    "Os atributos {A, C, D, E, G}, pois apenas B está presente na maioria das chaves"
                ],
                "answer": "Apenas o atributo {G}, pois A, B, C, D e E participam de pelo menos uma chave candidata",
                "explanation": "Pela definição formal de ibd-parte6.pdf, um atributo é primo se pertence a QUALQUER chave candidata. Como as chaves candidatas são {AB, BC, BD, BE, CD}, os atributos {A, B, C, D, E} são todos primos, restando apenas {G} como não-primo!"
            }
        ]
    },

    "R1.8": {
        "title": "[Rodada 1] Cobertura Mínima (Irredutível) Passo a Passo em 3 Etapas Formais",
        "type": "oficial",
        "mode": "structured",
        "context_html": """
        <div class="schema-card-box">
          <div class="schema-card-header">📐 Conjunto Inicial de Dependências Funcionais em <code>R(A, B, C, D, E)</code>:</div>
          <div class="fd-grid">
            <div class="fd-chip"><strong>1:</strong> <code>A → B, C</code></div>
            <div class="fd-chip"><strong>2:</strong> <code>B → C</code></div>
            <div class="fd-chip"><strong>3:</strong> <code>A → B</code></div>
            <div class="fd-chip"><strong>4:</strong> <code>A, B → D</code></div>
            <div class="fd-chip"><strong>5:</strong> <code>D → E</code></div>
            <div class="fd-chip"><strong>6:</strong> <code>A → E</code></div>
          </div>
          <div class="task-checklist-bar" style="margin-top:10px;">
            <div class="task-chip"><strong>Passo 1:</strong> Desmembrar RHS composto (<code>A → B, C</code>)</div>
            <div class="task-chip"><strong>Passo 2:</strong> Testar atributo estranho no LHS de <code>A, B → D</code></div>
            <div class="task-chip"><strong>Passo 3:</strong> Eliminar DFs transitivas redundantes</div>
          </div>
        </div>
        """,
        "study_guide": STUDY_GUIDE_G4,
        "answer_sheet_html": """
        <div class="ans-steps-grid">
          <div class="ans-step-card">
            <span class="ans-step-badge">PASSO 1 E PASSO 2 — RHS UNITÁRIO E REMOÇÃO DE ATRIBUTO ESTRANHO NO LHS</span>
            <pre><code>• Passo 1 (RHS Unitário):
  F1 = { A → B,  A → C,  B → C,  AB → D,  D → E,  A → E }

• Passo 2 (Atributo Estranho em AB → D):
  Calculamos {A}+ = {A, B, C, D, E}. Como B ∈ {A}+ (via A → B), B é estranho em AB → D!
  F2 = { A → B,  A → C,  B → C,  A → D,  D → E,  A → E }</code></pre>
          </div>
          <div class="ans-step-card">
            <span class="ans-step-badge">PASSO 3 — REMOÇÃO DE DFs REDUNDANTES E COBERTURA MÍNIMA FINAL Fc</span>
            <pre><code>• Teste de A → C: Sem ela, {A}+ ainda contém C (via A → B e B → C) ==> Redundante!
• Teste de A → E: Sem ela, {A}+ ainda contém E (via A → D e D → E) ==> Redundante!

• Cobertura Mínima Final:
  Fc = { A → B,   B → C,   A → D,   D → E }</code></pre>
          </div>
        </div>
        """,
        "fields": [
            {
                "id": "q1",
                "label": "1. No Passo 2 do algoritmo de Cobertura Mínima aplicado à dependência AB -> D, qual atributo do lado esquerdo é estranho (redundante) e por quê?",
                "options": [
                    "O atributo A é estranho em AB -> D, pois B -> C implica diretamente B -> D pelo axioma da pseudotransitividade",
                    "Nenhum atributo é estranho em AB -> D, pois D não aparece no lado esquerdo de A -> B nem de B -> C",
                    "O atributo B é estranho em AB -> D, pois B pertence ao fecho {A}+ (via A -> B), reduzindo AB -> D para A -> D",
                    "Ambos A e B são estranhos em AB -> D, permitindo eliminar completamente a determinação do atributo D"
                ],
                "answer": "O atributo B é estranho em AB -> D, pois B pertence ao fecho {A}+ (via A -> B), reduzindo AB -> D para A -> D",
                "explanation": "Em AB -> D, ao testar se B é estranho, calculamos {A}+. Como A -> B pertence a F, temos B ∈ {A}+, logo A sozinho já determina AB e consequentemente D. Portanto, B é estranho e AB -> D simplifica-se para A -> D."
            },
            {
                "id": "q2",
                "label": "2. No Passo 3 (remoção de DFs inteiras redundantes), quais dependências são eliminadas de F2 = {A -> B, A -> C, B -> C, A -> D, D -> E, A -> E}?",
                "options": [
                    "São eliminadas B -> C e D -> E, mantendo no conjunto canônico apenas as dependências cujo determinante é a chave primária A",
                    "São eliminadas A -> B e A -> D, pois ambas possuem o atributo primo A isolado no lado esquerdo da dependência funcional",
                    "Nenhuma dependência pode ser eliminada no Passo 3 após a simplificação do lado esquerdo de AB -> D realizada no Passo 2",
                    "São eliminadas A -> C (derivável por transitividade de A -> B e B -> C) e A -> E (derivável de A -> D e D -> E)"
                ],
                "answer": "São eliminadas A -> C (derivável por transitividade de A -> B e B -> C) e A -> E (derivável de A -> D e D -> E)",
                "explanation": "Ao remover A -> C, o fecho {A}+ continua contendo C graças à cadeia A -> B -> C. Ao remover A -> E, o fecho {A}+ continua contendo E graças à cadeia A -> D -> E. Logo, ambas são redundantes."
            },
            {
                "id": "q3",
                "label": "3. Qual é a Cobertura Mínima (Conjunto Canônico Irredutível) Fc final do conjunto F?",
                "options": [
                    "Fc = { A -> B,  A -> C,  A -> D,  A -> E }",
                    "Fc = { A -> BC,  AB -> D,  D -> E }",
                    "Fc = { A -> B,  B -> C,  A -> D,  D -> E }",
                    "Fc = { A -> B,  B -> C,  AB -> D,  A -> E }"
                ],
                "answer": "Fc = { A -> B,  B -> C,  A -> D,  D -> E }",
                "explanation": "Fc = {A -> B, B -> C, A -> D, D -> E} possui lado direito unitário em todas as DFs, lado esquerdo irredutível e nenhuma DF redundante."
            }
        ]
    },

    "R1.9": {
        "title": "[Rodada 1] Normalização Clássica (Elmasri CAR_SALE & Ordem de Compra): 1FN -> 2FN -> 3FN",
        "type": "oficial",
        "mode": "structured",
        "context_html": """
        <div class="schema-card-box">
          <div class="schema-card-header">📐 Caso A (Não-1FN): <code>ORDEM_COMPRA(<u>NumOrdem</u>, DataOrdem, CNPJFornecedor, RazaoFornecedor, {<u>CodPeca</u>, NomePeca, Qtde, PrecoUnit})</code></div>
          <div class="schema-card-header" style="margin-top:8px;">📐 Caso B (Elmasri Cap. 14): <code>CAR_SALE(<u>Car#, Salesperson#</u>, Date_sold, Commission%, Discount_amt)</code></div>
          <div class="fd-grid">
            <div class="fd-chip"><strong>PK de CAR_SALE:</strong> <code>{Car#, Salesperson#}</code></div>
            <div class="fd-chip"><strong>DF1:</strong> <code>Car# → Date_sold, Discount_amt</code></div>
            <div class="fd-chip"><strong>DF2:</strong> <code>Date_sold → Discount_amt</code></div>
            <div class="fd-chip"><strong>DF3:</strong> <code>Salesperson# → Commission%</code></div>
          </div>
        </div>
        """,
        "study_guide": STUDY_GUIDE_G4,
        "answer_sheet_html": """
        <div class="ans-steps-grid">
          <div class="ans-step-card">
            <span class="ans-step-badge">CASO A — DECOMPOSIÇÃO DE ORDEM_COMPRA (1FN → 2FN → 3FN)</span>
            <pre><code>• 1FN (Remove grupo repetitivo):
  ORDEM(NumOrdem(nn), DataOrdem, CNPJFornecedor(nn), RazaoFornecedor)
  ITEM_ORDEM(NumOrdem(nn), CodPeca(nn), NomePeca, Qtde, PrecoUnit)

• 2FN (Remove parcial CodPeca → NomePeca) e 3FN (Remove transitiva CNPJ → Razao):
  FORNECEDOR(CNPJFornecedor(nn), RazaoFornecedor)
  ORDEM_3FN(NumOrdem(nn), DataOrdem, CNPJFornecedor(nn))
  PECA(CodPeca(nn), NomePeca)
  ITEM_ORDEM_3FN(NumOrdem(nn), CodPeca(nn), Qtde, PrecoUnit)</code></pre>
          </div>
          <div class="ans-step-card">
            <span class="ans-step-badge">CASO B — DECOMPOSIÇÃO DE CAR_SALE (ELMASRI &amp; NAVATHE)</span>
            <pre><code>• 2FN (Remove parciais Car# → {Date_sold, Discount_amt} e Salesperson# → Commission%):
  R1_VENDA(Car#(nn), Salesperson#(nn))           -- PK: (Car#, Salesperson#)
  R2_VENDEDOR(Salesperson#(nn), Commission%)     -- PK: Salesperson#
  R3_CARRO(Car#(nn), Date_sold, Discount_amt)    -- PK: Car#

• 3FN (Remove transitiva Date_sold → Discount_amt de R3_CARRO):
  R31_CARRO(Car#(nn), Date_sold)                 -- PK: Car# | FK: Date_sold
  R32_DESCONTO(Date_sold(nn), Discount_amt)      -- PK: Date_sold</code></pre>
          </div>
        </div>
        """,
        "fields": [
            {
                "id": "q1",
                "label": "1. Ao colocar ORDEM_COMPRA na 1FN separando ITEM_ORDEM(NumOrdem(nn), CodPeca(nn), NomePeca, Quantidade, PrecoUnitario), qual violação de forma normal ainda permanece em ITEM_ORDEM?",
                "options": [
                    "Violação da 2FN, pois NomePeca depende parcialmente apenas de CodPeca (subconjunto próprio da chave composta {NumOrdem, CodPeca})",
                    "Violação da 3FN, pois Quantidade depende transitivamente de PrecoUnitario através do atributo não-primo NomePeca",
                    "Violação da 1FN, pois uma chave primária composta por dois atributos (NumOrdem, CodPeca) fere a atomicidade relacional",
                    "Nenhuma violação permanece, pois toda tabela gerada pela remoção de um atributo multivalorado já nasce automaticamente em 3FN"
                ],
                "answer": "Violação da 2FN, pois NomePeca depende parcialmente apenas de CodPeca (subconjunto próprio da chave composta {NumOrdem, CodPeca})",
                "explanation": "Em ITEM_ORDEM, a chave primária é composta por (NumOrdem, CodPeca), mas o nome da peça (NomePeca) depende funcionalmente apenas de CodPeca (CodPeca -> NomePeca), caracterizando uma dependência parcial que viola a 2FN."
            },
            {
                "id": "q2",
                "label": "2. Na relação CAR_SALE(Car#, Salesperson#, Date_sold, Commission%, Discount_amt) com PK {Car#, Salesperson#}, por que ela NÃO está na 2FN?",
                "options": [
                    "Porque Date_sold determina Discount_amt por meio de uma dependência transitiva entre dois atributos não-primos",
                    "Porque Date_sold e Discount_amt dependem parcialmente de Car#, e Commission% depende parcialmente de Salesperson#",
                    "Porque a chave composta {Car#, Salesperson#} não determina unicamente nem Commission% nem Date_sold",
                    "Porque Discount_amt é um atributo derivado que deveria ser calculado dinamicamente a partir de Commission%"
                ],
                "answer": "Porque Date_sold e Discount_amt dependem parcialmente de Car#, e Commission% depende parcialmente de Salesperson#",
                "explanation": "Tanto Car# -> {Date_sold, Discount_amt} quanto Salesperson# -> Commission% têm como determinante um subconjunto próprio da chave primária composta {Car#, Salesperson#}, violando diretamente a 2FN."
            },
            {
                "id": "q3",
                "label": "3. Qual é o esquema final de CAR_SALE totalmente normalizado em 3FN (sem perda de junção e preservando todas as DFs)?",
                "options": [
                    "R1(Car#, Salesperson#),  R2(Salesperson#, Commission%),  R3(Car#, Date_sold)  e  R4(Date_sold, Discount_amt)",
                    "R1(Car#, Salesperson#, Date_sold, Discount_amt)  e  R2(Salesperson#, Commission%)",
                    "R1(Car#, Salesperson#, Commission%)  e  R2(Car#, Date_sold, Discount_amt)",
                    "R1(Car#, Date_sold),  R2(Salesperson#, Commission%)  e  R3(Date_sold, Discount_amt) — descartando (Car#, Salesperson#)"
                ],
                "answer": "R1(Car#, Salesperson#),  R2(Salesperson#, Commission%),  R3(Car#, Date_sold)  e  R4(Date_sold, Discount_amt)",
                "explanation": "Para atingir a 2FN separamos R1(Car#, Salesperson#), R2(Salesperson#, Commission%) e R3(Car#, Date_sold, Discount_amt). Como Date_sold -> Discount_amt é transitiva em R3, decompomos R3 em R31(Car#, Date_sold) e R32(Date_sold, Discount_amt) para chegar à 3FN."
            }
        ]
    },

    "R1.10": {
        "title": "[Rodada 1] Projeto Completo de Normalização (Definição Geral de 2FN e 3FN com Múltiplas Chaves)",
        "type": "oficial",
        "mode": "structured",
        "context_html": """
        <div class="schema-card-box">
          <div class="schema-card-header">📐 Relação Universal: <code>SESSAO_CONGRESSO(<u>CodTrilha, NumSessao</u>, Sala, Horario, CPFPalestrante, NomePalestrante, CNPJPatrocinador, RazaoPatrocinador, CapacidadeSala)</code></div>
          <div class="fd-grid">
            <div class="fd-chip"><strong>DF1:</strong> <code>{CodTrilha, NumSessao} → {Sala, Horario, CPFPalestrante, CNPJPatrocinador}</code></div>
            <div class="fd-chip"><strong>DF2:</strong> <code>{Sala, Horario} → {CodTrilha, NumSessao}</code></div>
            <div class="fd-chip"><strong>DF3:</strong> <code>CodTrilha → CNPJPatrocinador</code></div>
            <div class="fd-chip"><strong>DF4:</strong> <code>CNPJPatrocinador → RazaoPatrocinador</code></div>
            <div class="fd-chip"><strong>DF5:</strong> <code>Sala → CapacidadeSala</code></div>
            <div class="fd-chip"><strong>DF6:</strong> <code>CPFPalestrante → NomePalestrante</code></div>
          </div>
        </div>
        """,
        "study_guide": STUDY_GUIDE_G4,
        "answer_sheet_html": """
        <div class="ans-steps-grid">
          <div class="ans-step-card">
            <span class="ans-step-badge">PASSO 1 E PASSO 2 — CHAVES CANDIDATAS, PRIMOS E DECOMPOSIÇÃO PARA 2FN</span>
            <pre><code>• Chaves Candidatas: CK1 = {CodTrilha, NumSessao} (PK)  e  CK2 = {Sala, Horario} (AK/UNIQUE)
• Atributos Primos:  {CodTrilha, NumSessao, Sala, Horario}
• Violações de 2FN:  CodTrilha → {CNPJ, Razao} (parcial em CK1) e Sala → CapacidadeSala (parcial em CK2)

  TRILHA_2FN(CodTrilha(nn), CNPJPatrocinador(nn), RazaoPatrocinador)
  SALA_2FN(Sala(nn), CapacidadeSala(nn))
  SESSAO_2FN(CodTrilha(nn), NumSessao(nn), Sala(nn), Horario(nn), CPFPalestrante(nn), NomePalestrante)</code></pre>
          </div>
          <div class="ans-step-card">
            <span class="ans-step-badge">PASSO 3 — ESQUEMA FINAL EM 3FN (5 RELAÇÕES SEM TRANSITIVIDADES)</span>
            <pre><code>1. PATROCINADOR(CNPJPatrocinador(nn), RazaoPatrocinador(nn))      -- PK: CNPJPatrocinador
2. TRILHA(CodTrilha(nn), CNPJPatrocinador(nn))                    -- PK: CodTrilha | FK: CNPJPatrocinador
3. SALA_CONGRESSO(Sala(nn), CapacidadeSala(nn))                   -- PK: Sala
4. PALESTRANTE(CPFPalestrante(nn), NomePalestrante(nn))           -- PK: CPFPalestrante
5. SESSAO(CodTrilha(nn), NumSessao(nn), Sala(nn), Horario(nn), CPFPalestrante(nn))
     PK: (CodTrilha, NumSessao)  |  UNIQUE: (Sala, Horario)</code></pre>
          </div>
        </div>
        """,
        "fields": [
            {
                "id": "q1",
                "label": "1. Pela Definição Geral de Formas Normais (ibd-parte6.pdf), quais são todas as chaves candidatas e os atributos primos de SESSAO_CONGRESSO?",
                "options": [
                    "A única chave candidata é {CodTrilha, NumSessao}, logo apenas os dois atributos CodTrilha e NumSessao são classificados como primos",
                    "As chaves candidatas são {CodTrilha, NumSessao} e {Sala, Horario}; os atributos primos são {CodTrilha, NumSessao, Sala, Horario}",
                    "As chaves candidatas são {CodTrilha}, {Sala} e {CPFPalestrante}; todos os demais atributos da relação são classificados como não-primos",
                    "As chaves candidatas são {CodTrilha, NumSessao} e {CPFPalestrante, Horario}; o atributo Sala é classificado como atributo não-primo"
                ],
                "answer": "As chaves candidatas são {CodTrilha, NumSessao} e {Sala, Horario}; os atributos primos são {CodTrilha, NumSessao, Sala, Horario}",
                "explanation": "Por DF1 e DF2, tanto {CodTrilha, NumSessao} quanto {Sala, Horario} determinam todos os atributos da relação e são mínimas. Logo, os 4 atributos que compõem CK1 e CK2 são primos."
            },
            {
                "id": "q2",
                "label": "2. Por que a dependência funcional DF5 (Sala -> CapacidadeSala) viola a Segunda Forma Normal (2FN) na relação original SESSAO_CONGRESSO?",
                "options": [
                    "Porque Sala é um atributo não-primo que determina transitivamente o atributo não-primo CapacidadeSala dentro da relação principal",
                    "Porque CapacidadeSala é um atributo primo que depende parcialmente da chave primária composta principal {CodTrilha, NumSessao}",
                    "Porque CapacidadeSala (não-primo) depende parcialmente de Sala, que é subconjunto próprio da chave candidata {Sala, Horario}",
                    "Porque DF5 viola a Primeira Forma Normal (1FN) ao armazenar a capacidade numérica junto ao código identificador da sala"
                ],
                "answer": "Porque CapacidadeSala (não-primo) depende parcialmente de Sala, que é subconjunto próprio da chave candidata {Sala, Horario}",
                "explanation": "Pela Definição Geral da 2FN (ibd-parte6.pdf), uma relação viola a 2FN quando um atributo não-primo depende parcialmente de QUALQUER chave candidata de R. Como {Sala, Horario} é chave candidata (CK2), Sala -> CapacidadeSala é uma dependência parcial sobre CK2!"
            },
            {
                "id": "q3",
                "label": "3. Quantas relações compõem o esquema final de SESSAO_CONGRESSO após a decomposição completa até a 3FN (preservando junção sem perda e todas as DFs)?",
                "options": [
                    "3 relações: TRILHA(CodTrilha, CNPJ, Razao), SALA(Sala, Horario, Capacidade) e SESSAO(CodTrilha, NumSessao, CPFPalestrante, NomePalestrante)",
                    "4 relações: TRILHA(CodTrilha, CNPJ, Razao), SALA(Sala, Capacidade), PALESTRANTE(CPF, Nome) e SESSAO(CodTrilha, NumSessao, Sala, Horario, CPF)",
                    "6 relações: criando duas tabelas separadas para SESSAO, uma com PK (CodTrilha, NumSessao) e outra tabela independente com PK (Sala, Horario)",
                    "5 relações: PATROCINADOR(CNPJ, Razao), TRILHA(CodTrilha, CNPJ), SALA(Sala, Cap), PALESTRANTE(CPF, Nome) e SESSAO(CodTrilha, NumSessao, Sala, Horario, CPF)"
                ],
                "answer": "5 relações: PATROCINADOR(CNPJ, Razao), TRILHA(CodTrilha, CNPJ), SALA(Sala, Cap), PALESTRANTE(CPF, Nome) e SESSAO(CodTrilha, NumSessao, Sala, Horario, CPF)",
                "explanation": "A decomposição para 2FN extrai TRILHA e SALA; e a decomposição para 3FN separa PATROCINADOR (eliminando CodTrilha -> CNPJ -> Razao) e PALESTRANTE (eliminando CPF -> Nome), resultando nas 5 relações em 3FN."
            }
        ]
    }
}
