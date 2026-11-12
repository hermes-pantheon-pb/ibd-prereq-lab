#!/usr/bin/env python3
"""
Round 1 Exam Mastery Exercises (R1.1 to R1.10) for Modules 7 & 8:
- Module 7 (Projeto Lógico: Mapeamento ER / EER -> Relacional): R1.1, R1.2, R1.3, R1.4, R1.5
- Module 8 (Normalização: DFs, Fecho X+, Cobertura Mínima, 1FN/2FN/3FN): R1.6, R1.7, R1.8, R1.9, R1.10

Includes:
- Authentic ER and EER SVG diagrams rendered in the exercise statement
- Study Guides (Cheat Sheets) with exact UFMG coursework references and parallel-domain worked examples
- Complete Step-by-Step Answer Sheets (Folha de Gabarito Oficial) for open-ended/layout resolution
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
    <!-- Connectors / Lines -->
    <!-- ALA_HOSPITALAR (1,1) == CHEFIADA_POR == (0,1) MEDICO -->
    <line x1="210" y1="95" x2="390" y2="95" stroke="#38bdf8" stroke-width="3"/>
    <line x1="210" y1="101" x2="390" y2="101" stroke="#38bdf8" stroke-width="3"/>
    <line x1="510" y1="98" x2="680" y2="98" stroke="#94a3b8" stroke-width="2"/>
    <text x="235" y="86" fill="#38bdf8" font-size="12" font-weight="bold">(1, 1)</text>
    <text x="615" y="86" fill="#e2e8f0" font-size="12" font-weight="bold">(0, 1)</text>

    <!-- ALA_HOSPITALAR (0,N) -- INTERNADO_EM -- (0,1) PACIENTE -->
    <line x1="130" y1="125" x2="130" y2="195" stroke="#94a3b8" stroke-width="2"/>
    <line x1="130" y1="255" x2="130" y2="315" stroke="#94a3b8" stroke-width="2"/>
    <text x="138" y="152" fill="#e2e8f0" font-size="12" font-weight="bold">(0, N)</text>
    <text x="138" y="302" fill="#e2e8f0" font-size="12" font-weight="bold">(0, 1)</text>

    <!-- MEDICO (0,N) -- PRESCRICAO -- (0,N) PACIENTE -->
    <line x1="740" y1="125" x2="450" y2="215" stroke="#94a3b8" stroke-width="2"/>
    <line x1="390" y1="225" x2="210" y2="335" stroke="#94a3b8" stroke-width="2"/>
    <text x="625" y="152" fill="#e2e8f0" font-size="12" font-weight="bold">(0, N)</text>
    <text x="235" y="302" fill="#e2e8f0" font-size="12" font-weight="bold">(0, N)</text>

    <!-- PACIENTE (0,N) -- REALIZA_EXAME (Weak ID) == (1,1) EXAME_LABORATORIAL -->
    <line x1="210" y1="350" x2="390" y2="350" stroke="#94a3b8" stroke-width="2"/>
    <line x1="510" y1="347" x2="660" y2="347" stroke="#f59e0b" stroke-width="3"/>
    <line x1="510" y1="353" x2="660" y2="353" stroke="#f59e0b" stroke-width="3"/>
    <text x="235" y="340" fill="#e2e8f0" font-size="12" font-weight="bold">(0, N)</text>
    <text x="585" y="338" fill="#f59e0b" font-size="12" font-weight="bold">(1, 1)</text>

    <!-- Strong Entity: ALA_HOSPITALAR -->
    <rect x="50" y="70" width="160" height="55" rx="4" fill="#1e293b" stroke="#38bdf8" stroke-width="2.5"/>
    <text x="130" y="102" fill="#f8fafc" font-size="13" font-weight="bold" text-anchor="middle">ALA_HOSPITALAR</text>
    <!-- Attributes of ALA_HOSPITALAR -->
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
    <!-- Attributes of MEDICO -->
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
    <!-- Partial Key & Attributes of EXAME_LABORATORIAL -->
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
    <!-- Single line (Partial) to (o) circle -->
    <line x1="190" y1="90" x2="190" y2="145" stroke="#94a3b8" stroke-width="2.5"/>
    <circle cx="190" cy="162" r="17" fill="#1e293b" stroke="#38bdf8" stroke-width="2.5"/>
    <text x="190" y="167" fill="#38bdf8" font-size="14" font-weight="bold" text-anchor="middle">o</text>
    <text x="255" y="125" fill="#94a3b8" font-size="11">Parcial / Sobreposta</text>
    <!-- Branches to DOCENTE and ALUNO_POS -->
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
    <!-- Double line (Total) to (d) circle -->
    <line x1="697" y1="90" x2="697" y2="145" stroke="#f59e0b" stroke-width="3"/>
    <line x1="703" y1="90" x2="703" y2="145" stroke="#f59e0b" stroke-width="3"/>
    <circle cx="700" cy="162" r="17" fill="#1e293b" stroke="#f59e0b" stroke-width="2.5"/>
    <text x="700" y="167" fill="#fde68a" font-size="14" font-weight="bold" text-anchor="middle">d</text>
    <text x="775" y="125" fill="#fde68a" font-size="11" font-weight="bold">Total (Linha Dupla) / Disjunta</text>
    <!-- Branches to BOLSA_MESTRADO and BOLSA_DOUTORADO -->
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
# STUDY GUIDES (CHEAT SHEETS WITH PARALLEL DOMAIN EXAMPLES)
# ==============================================================================

STUDY_GUIDE_G1 = {
    "id": "G1",
    "title": "📘 Ficha de Estudo G1 — Mapeamento ER Básico, Entidades Fracas e Políticas RIR (b, p, n)",
    "file_path": "study_guides/G1_Mapeamento_ER_Basico_e_RIRs.md",
    "coursework_ref": "ibd-parte5.pdf (Etapa 1: Regras 1 a 6 e Políticas de Remoção b, p, n) + ExercicioProjetoLogico.pdf",
    "summary_html": """
      <div class="sg-section">
        <h4>📌 Base Teórica nos Slides (<code>ibd-parte5.pdf</code> — Etapa 1)</h4>
        <ul>
          <li><strong>Regra 2a (Atributo Composto):</strong> Achata-se (<em>flattening</em>) incluindo apenas os sub-atributos componentes simples na relação da entidade dona.</li>
          <li><strong>Regra 2b (Atributo Multivalorado <code>{M}</code>):</strong> Cria-se nova relação <code>R_M(PK_Dona(nn), M(nn))</code> com chave primária composta por ambos os atributos e RIR com política <strong><code>p</code> (propagação / CASCADE)</strong>.</li>
          <li><strong>Regra 3 (Entidade Fraca <code>W</code>):</strong> A relação <code>W</code> importa a PK da entidade forte dona como FK <code>(nn)</code>. A PK de <code>W</code> é composta por <code>(PK_Dona, ChaveParcial_W)</code> e a RIR tem obrigatoriamente política <strong><code>p</code> (propagação)</strong>.</li>
          <li><strong>Regra 4 (Relacionamento 1:1):</strong> Se um lado tem participação <strong>total <code>(1,1)</code></strong> e o outro <strong>parcial <code>(0,1)</code></strong>, a relação do lado <strong>total <code>(1,1)</code></strong> absorve a PK do outro lado como FK <code>(nn)</code> + atributos do relacionamento (evitando valores <code>NULL</code>!).</li>
          <li><strong>Regra 5 (Relacionamento 1:N):</strong> A relação do lado <strong>N</strong> (que possui cardinalidade máxima <code>1</code> na notação <code>(min, max)</code>) absorve a PK do lado <strong>1</strong> como FK + atributos do relacionamento.</li>
          <li><strong>Regra 6 (Relacionamento M:N):</strong> Cria-se nova relação associativa com PK composta pelas FKs das duas entidades participantes e política <strong><code>p</code></strong>.</li>
        </ul>
      </div>
      <div class="sg-example-box">
        <h4>🔄 Exemplo Análogo Resolvido (Domínio Diferente: <em>Rede Bancária — BANCO e AGENCIA</em>)</h4>
        <p>Imagine um banco onde <code>BANCO(CodBanco, Sede(Cidade, UF), {TelefonesSAC})</code> identifica a entidade fraca <code>AGENCIA(NumAgencia, Bairro)</code>, cada <code>AGENCIA (1,1)</code> é gerenciada por um <code>FUNCIONARIO(CPF, Nome) (0,1)</code> desde <code>DataPosse</code>, e cada <code>FUNCIONARIO (0,1)</code> trabalha em uma <code>AGENCIA (0,N)</code>:</p>
        <pre><code>1. BANCO(CodBanco(nn), Cidade, UF)                  -- Sede foi achatado!
2. BANCO_TELEFONES(CodBanco(nn), TelefoneSAC(nn))   -- PK: (CodBanco, TelefoneSAC) | RIR: -p-> BANCO
3. AGENCIA(CodBanco(nn), NumAgencia(nn), Bairro, CPFGerente(nn), DataPosse)
     PK: (CodBanco, NumAgencia) | UNIQUE: CPFGerente
     RIR 1: AGENCIA[CodBanco] -p-> BANCO[CodBanco]       (Entidade fraca = propagação p)
     RIR 2: AGENCIA[CPFGerente] -b-> FUNCIONARIO[CPF]    (1:1 total em AGENCIA absorve FK nn)
4. FUNCIONARIO(CPF(nn), Nome(nn), CodBancoLot, NumAgenciaLot)
     RIR: FUNCIONARIO[CodBancoLot, NumAgenciaLot] -n-> AGENCIA[CodBanco, NumAgencia]</code></pre>
      </div>
    """
}

STUDY_GUIDE_G2 = {
    "id": "G2",
    "title": "📘 Ficha de Estudo G2 — Mapeamento EER: Hierarquias (d/o, Total/Parcial), CHECK e Ternários",
    "file_path": "study_guides/G2_Mapeamento_EER_Hierarquias_e_Ternarios.md",
    "coursework_ref": "ibd-parte5.pdf (Etapa 2: Opções 1, 2 e 3 para Hierarquias EER, Cláusula CHECK e Relacionamentos Ternários)",
    "summary_html": """
      <div class="sg-section">
        <h4>📌 Base Teórica nos Slides (<code>ibd-parte5.pdf</code> — Etapa 2)</h4>
        <ul>
          <li><strong>Opção 1 (Tabela Única na Superclasse):</strong> Funde superclasse e subclasses em uma só relação com atributos específicos anuláveis. Exige cláusula <code>CHECK</code> de tupla para garantir disjunção (<code>d</code>) e/ou cobertura total.</li>
          <li><strong>Opção 2 (Apenas Tabelas das Subclasses):</strong> Elimina a tabela da superclasse, replicando a PK e os atributos gerais nas subclasses. <strong>Só é válida quando a hierarquia é TOTAL (linha dupla)!</strong> Se for sobreposta (<code>o</code>), causa redundância dos atributos gerais.</li>
          <li><strong>Opção 3 (Superclasse + Tabelas das Subclasses):</strong> Universal. Cada subclasse importa a PK da superclasse como sua própria PK e FK com política <strong><code>p</code> (propagação / CASCADE)</strong>.</li>
          <li><strong>Relacionamento Ternário (M:N:P):</strong> Cria-se nova relação cuja PK é composta pelas 3 FKs das entidades participantes (todas com política <code>p</code>).</li>
        </ul>
      </div>
      <div class="sg-example-box">
        <h4>🔄 Exemplo Análogo Resolvido (Domínio Diferente: <em>Frota Marítima — EMBARCACAO</em>)</h4>
        <p>Considere <code>EMBARCACAO(CodIMO, NomeNavio)</code> especializada de forma <strong>Disjunta e Total (<code>d</code>, linha dupla)</strong> em <code>PETROLEIRO(CapacidadeBarris)</code> e <code>PORTA_CONTENTOR(MaximoTEUs)</code>:</p>
        <pre><code>-- Opção 1 (Tabela Única com CHECK para Disjunção + Totalidade / OU-Exclusivo):
CREATE TABLE EMBARCACAO (
    CodIMO VARCHAR(15) NOT NULL PRIMARY KEY,
    NomeNavio VARCHAR(80) NOT NULL,
    CapacidadeBarris INTEGER,
    MaximoTEUs INTEGER,
    CHECK (
        (CapacidadeBarris IS NOT NULL AND MaximoTEUs IS NULL)
        OR
        (CapacidadeBarris IS NULL AND MaximoTEUs IS NOT NULL)
    )
);</code></pre>
      </div>
    """
}

STUDY_GUIDE_G3 = {
    "id": "G3",
    "title": "📘 Ficha de Estudo G3 — DFs em Instâncias, Axiomas de Armstrong e Fecho X+ (Múltiplas Chaves)",
    "file_path": "study_guides/G3_Dependencias_Funcionais_Instancias_e_Fecho.md",
    "coursework_ref": "ibd-parte6.pdf (Seções 1, 2 e 3: Semântica de DFs, Satisfação em Instâncias r(R), Fecho X+ e Chaves Candidatas)",
    "summary_html": """
      <div class="sg-section">
        <h4>📌 Base Teórica nos Slides (<code>ibd-parte6.pdf</code> — Seções 2 e 3)</h4>
        <ul>
          <li><strong>Refutação de DF por Instância:</strong> Uma DF <code>X -> Y</code> é violada em uma extensão <code>r(R)</code> se existirem duas tuplas <code>t1, t2</code> tais que <code>t1[X] = t2[X]</code> mas <code>t1[Y] &lt;&gt; t2[Y]</code>. Jamais se prova que uma DF vale em todos os estados apenas olhando uma instância, mas um único contraexemplo refuta a DF!</li>
          <li><strong>Método do Particionamento para Achar TODAS as Chaves Candidatas:</strong>
            <ol>
              <li><strong>Conjunto Essencial <code>L</code> (Nunca aparece no lado direito de nenhuma DF):</strong> Faz parte obrigatoriamente de <em>todas</em> as chaves candidatas!</li>
              <li><strong>Conjunto Somente-Direita <code>D</code> (Nunca aparece no lado esquerdo):</strong> Jamais entra em nenhuma chave candidata mínima.</li>
              <li><strong>Conjunto Intermediário <code>M</code> (Aparece em ambos os lados):</strong> Se <code>L+ != R</code>, teste adicionar elementos de <code>M</code> ao conjunto <code>L</code> um a um.</li>
            </ol>
          </li>
          <li><strong>Atributo Primo vs. Não-Primo:</strong> Atributo primo é todo atributo que participa de <strong>pelo menos uma</strong> chave candidata de <code>R</code>.</li>
        </ul>
      </div>
      <div class="sg-example-box">
        <h4>🔄 Exemplo Análogo Resolvido (Domínio Diferente: <em>Esquema S(P, Q, R, T, U)</em>)</h4>
        <p>Dado <code>S(P, Q, R, T, U)</code> com <code>F = { PQ -> R,  R -> P,  QR -> T,  T -> U }</code>:</p>
        <pre><code>1. Atributos que NUNCA aparecem no lado direito (RHS = {R, P, T, U}):
   -> L = {Q}. Logo Q pertence a TODAS as chaves candidatas!
2. Atributos que aparecem APENAS no lado direito:
   -> D = {U}. Logo U nunca pertence a chave candidata.
3. Fecho de {Q}+ = {Q} != S. Combinamos Q com os intermediários M = {P, R, T}:
   • {P, Q}+ = {P, Q, R, T, U} = S  ==> {P, Q} é Chave Candidata (CK1)!
   • {Q, R}+ = {Q, R, P, T, U} = S  ==> {Q, R} é Chave Candidata (CK2)!
   • {Q, T}+ = {Q, T, U} != S       ==> Não é superchave.
4. Atributos Primos = {P, Q, R} | Atributos Não-Primos = {T, U}.</code></pre>
      </div>
    """
}

STUDY_GUIDE_G4 = {
    "id": "G4",
    "title": "📘 Ficha de Estudo G4 — Cobertura Mínima (3 Passos) e Decomposição 1FN -> 2FN -> 3FN",
    "file_path": "study_guides/G4_Cobertura_Minima_e_Normalizacao_1FN_2FN_3FN.md",
    "coursework_ref": "ibd-parte6.pdf (Seção 3.4: Cobertura Mínima; Seção 4: 1FN, 2FN, 3FN Geral) + ExerciciosNormalizacaoSemResposta.pdf",
    "summary_html": """
      <div class="sg-section">
        <h4>📌 Base Teórica nos Slides (<code>ibd-parte6.pdf</code> — Seções 3.4 e 4)</h4>
        <ul>
          <li><strong>Os 3 Passos da Cobertura Mínima (Irredutível) <code>Fc</code>:</strong>
            <ol>
              <li><strong>Passo 1 (RHS Unitário):</strong> Decompor <code>X -> {A, B}</code> em <code>X -> A</code> e <code>X -> B</code>.</li>
              <li><strong>Passo 2 (LHS Sem Atributos Estranhos):</strong> Em <code>XY -> Z</code>, se <code>Y</code> pertence a <code>{X}+</code> (ou <code>Z</code> pertence a <code>{X}+</code>), então <code>Y</code> é redundante no lado esquerdo e fica apenas <code>X -> Z</code>.</li>
              <li><strong>Passo 3 (Sem DFs Redundantes):</strong> Para cada <code>f: X -> A</code>, calcule <code>{X}+</code> em <code>F - {f}</code>. Se <code>A</code> continuar no fecho, elimine <code>f</code>!</li>
            </ol>
          </li>
          <li><strong>Definição Geral de 2FN e 3FN (Múltiplas Chaves Candidatas):</strong>
            <ul>
              <li><strong>Viola 2FN:</strong> Atributo <strong>não-primo</strong> depende parcialmente de um subconjunto próprio de <em>qualquer</em> chave candidata.</li>
              <li><strong>Viola 3FN:</strong> Existe <code>X -> A</code> não-trivial onde <code>X</code> <strong>não é superchave</strong> E <code>A</code> <strong>não é atributo primo</strong>.</li>
            </ul>
          </li>
        </ul>
      </div>
      <div class="sg-example-box">
        <h4>🔄 Exemplo Análogo Resolvido (Domínio Diferente: <em>Festival de Música — SHOW_FESTIVAL</em>)</h4>
        <p>Seja <code>SHOW_FESTIVAL(CodFestival, OrdemShow, CodPalco, Horario, IdBanda, NomeBanda, CidadeFestival, CapacidadePalco)</code> com chaves candidatas <code>CK1 = {CodFestival, OrdemShow}</code> e <code>CK2 = {CodPalco, Horario}</code>:</p>
        <pre><code>• Atributos Primos: {CodFestival, OrdemShow, CodPalco, Horario}
• Violações de 2FN (Dependências Parciais de CK1 e CK2):
  - CodFestival -> CidadeFestival (parcial de CK1)  ==> Cria FESTIVAL(CodFestival(nn), CidadeFestival)
  - CodPalco -> CapacidadePalco   (parcial de CK2)  ==> Cria PALCO(CodPalco(nn), CapacidadePalco)
• Violação de 3FN (Dependência Transitiva entre não-primos):
  - IdBanda -> NomeBanda                            ==> Cria BANDA(IdBanda(nn), NomeBanda)
• Relação Principal em 3FN:
  - SHOW(CodFestival(nn), OrdemShow(nn), CodPalco(nn), Horario(nn), IdBanda(nn))
    PK: (CodFestival, OrdemShow) | UNIQUE: (CodPalco, Horario)</code></pre>
      </div>
    """
}

# ==============================================================================
# 10 HIGH-QUALITY ROUND 1 EXERCISES (R1.1 TO R1.10)
# ==============================================================================

ROUND1_EXERCISES: Dict[str, Dict[str, Any]] = {
    "R1.1": {
        "title": "[Rodada 1] Hospital ER (Parte 1): Entidades Fortes, Atributos Compostos/Multivalorados e Entidade Fraca",
        "type": "oficial",
        "mode": "structured",
        "context_html": HOSPITAL_ER_SVG + """
        <div class="problem-narrative">
          <strong>Tarefa Completa (Discursiva + Checkpoints):</strong> Observe o esquema ER do <em>Sistema Hospitalar</em> acima. No seu <strong>Caderno de Resolução Discursiva</strong> abaixo, escreva o esquema relacional completo (com <code>(nn)</code>, chaves primárias e RIRs <code>-b-&gt;</code>, <code>-p-&gt;</code>, <code>-n-&gt;</code>) para as entidades <code>ALA_HOSPITALAR</code>, <code>MEDICO</code> (incluindo <code>Endereco</code> e <code>{Especialidades}</code>), <code>PACIENTE</code> e a entidade fraca <code>EXAME_LABORATORIAL</code>. Em seguida, confira a <strong>Folha de Gabarito Oficial</strong> e valide os 3 checkpoints estruturados.
        </div>
        """,
        "study_guide": STUDY_GUIDE_G1,
        "answer_sheet_html": """
        <h4>🔑 Folha de Gabarito Oficial Passo a Passo — Exercício R1.1</h4>
        <ol>
          <li><strong>Mapeamento das Entidades Fortes e Achatamento de Atributo Composto (Regras 1 e 2a):</strong>
            <pre><code>ALA_HOSPITALAR(CodAla(nn), NomeAla(nn), Andar)
  PK: CodAla

MEDICO(CRM(nn), NomeMed(nn), Rua, CEP)
  PK: CRM
  -- Nota: O atributo composto Endereco(Rua, CEP) foi achatado (flattening) em colunas atômicas.

PACIENTE(CNS(nn), NomePac(nn), CodAlaInternacao, NumLeito)
  PK: CNS</code></pre>
          </li>
          <li><strong>Mapeamento do Atributo Multivalorado <code>{Especialidades}</code> (Regra 2b):</strong>
            <pre><code>MEDICO_ESPECIALIDADES(CRM(nn), Especialidade(nn))
  PK: (CRM, Especialidade)
  RIR: MEDICO_ESPECIALIDADES[CRM] -p-> MEDICO[CRM]  (ON DELETE CASCADE)</code></pre>
          </li>
          <li><strong>Mapeamento da Entidade Fraca <code>EXAME_LABORATORIAL</code> e Relacionamento Identificador <code>REALIZA_EXAME</code> (Regra 3):</strong>
            <pre><code>EXAME_LABORATORIAL(CNS(nn), NumSeqExame(nn), TipoExame(nn))
  PK: (CNS, NumSeqExame)
  RIR: EXAME_LABORATORIAL[CNS] -p-> PACIENTE[CNS]   (Política p obrigatória para entidade fraca)</code></pre>
          </li>
        </ol>
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
        <div class="problem-narrative">
          <strong>Tarefa Completa (Discursiva + Checkpoints):</strong> Ainda sobre o diagrama ER do <em>Sistema Hospitalar</em> acima, analise os relacionamentos <code>CHEFIADA_POR</code> (<code>1:1</code> entre <code>ALA_HOSPITALAR (1,1)</code> e <code>MEDICO (0,1)</code> com atributo <code>DataPosse</code>), <code>INTERNADO_EM</code> (<code>1:N</code> entre <code>ALA_HOSPITALAR (0,N)</code> e <code>PACIENTE (0,1)</code> com atributo <code>NumLeito</code>) e <code>PRESCRICAO</code> (<code>M:N</code> entre <code>MEDICO (0,N)</code> e <code>PACIENTE (0,N)</code> com atributo <code>Dosagem</code>). Escreva as chaves estrangeiras e RIRs no seu <strong>Caderno de Resolução</strong>, consulte o <strong>Gabarito Oficial</strong> e responda aos checkpoints.
        </div>
        """,
        "study_guide": STUDY_GUIDE_G1,
        "answer_sheet_html": """
        <h4>🔑 Folha de Gabarito Oficial Passo a Passo — Exercício R1.2</h4>
        <ol>
          <li><strong>Relacionamento 1:1 <code>CHEFIADA_POR</code> (Regra 4 — Participação Total vs. Parcial):</strong>
            <ul>
              <li><code>ALA_HOSPITALAR</code> tem participação <strong>total <code>(1,1)</code></strong> e <code>MEDICO</code> tem participação <strong>parcial <code>(0,1)</code></strong>.</li>
              <li>Logo, a chave estrangeira <code>CRMChefe(nn)</code> e o atributo <code>DataPosse</code> são incluídos em <code>ALA_HOSPITALAR</code>! Assim nenhum valor <code>NULL</code> é gerado.</li>
              <li>Para garantir que o mesmo médico não chefie duas alas (<code>1:1</code>), <code>CRMChefe</code> recebe restrição de chave alternativa (<code>UNIQUE</code>).</li>
              <li>Política RIR: <code>ALA_HOSPITALAR[CRMChefe] -b-> MEDICO[CRM]</code> (bloqueio, pois a ala não pode ficar sem chefe).</li>
            </ul>
          </li>
          <li><strong>Relacionamento 1:N <code>INTERNADO_EM</code> (Regra 5 — Participação Parcial no Lado N):</strong>
            <ul>
              <li>O lado <strong>N</strong> é <code>PACIENTE</code> (pois cada paciente ocupa no máximo 1 ala: <code>(0,1)</code>, enquanto a ala abriga vários pacientes: <code>(0,N)</code>).</li>
              <li><code>PACIENTE</code> recebe a FK <strong>anulável</strong> <code>CodAla</code> e o atributo do relacionamento <code>NumLeito</code> (pois pacientes ambulatoriais não estão internados).</li>
              <li>Política RIR: <code>PACIENTE[CodAla] -b-> ALA_HOSPITALAR[CodAla]</code> (impede demolir/excluir uma ala com pacientes internados).</li>
            </ul>
          </li>
          <li><strong>Relacionamento M:N <code>PRESCRICAO</code> (Regra 6):</strong>
            <pre><code>PRESCRICAO(CRM(nn), CNS(nn), Dosagem)
  PK: (CRM, CNS)
  RIR 1: PRESCRICAO[CRM] -b-> MEDICO[CRM]      (ou -p-> conforme regra de auditoria)
  RIR 2: PRESCRICAO[CNS] -p-> PACIENTE[CNS]</code></pre>
          </li>
        </ol>
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
        <div class="problem-narrative">
          <strong>Tarefa Prática SQL DDL (Injeção de Falhas):</strong> Traduza o núcleo do esquema ER Hospitalar para comandos <code>CREATE TABLE</code> executáveis criando exatamente as 3 tabelas abaixo:
          <ul style="margin-top:8px; margin-left:20px; color:var(--text-secondary);">
            <li><code>ALA_HOSPITALAR(CodAla INTEGER NOT NULL, NomeAla TEXT NOT NULL, Andar INTEGER)</code> com <code>PRIMARY KEY (CodAla)</code>.</li>
            <li><code>PACIENTE(CNS TEXT NOT NULL, NomePac TEXT NOT NULL, CodAla INTEGER, NumLeito INTEGER)</code> com <code>PRIMARY KEY (CNS)</code> e <code>FOREIGN KEY (CodAla) REFERENCES ALA_HOSPITALAR(CodAla) ON DELETE RESTRICT</code>.</li>
            <li><code>EXAME_LABORATORIAL(CNS TEXT NOT NULL, NumSeqExame INTEGER NOT NULL, TipoExame TEXT NOT NULL)</code> com chave primária composta <code>PRIMARY KEY (CNS, NumSeqExame)</code> e <code>FOREIGN KEY (CNS) REFERENCES PACIENTE(CNS) ON DELETE CASCADE</code>.</li>
          </ul>
        </div>
        """,
        "study_guide": STUDY_GUIDE_G1,
        "answer_sheet_html": """
        <h4>🔑 Folha de Gabarito Oficial — Script DDL Completo (Exercício R1.3)</h4>
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
        <div class="problem-narrative">
          <strong>Tarefa Completa (Discursiva + Checkpoints):</strong> Observe o diagrama EER acima contendo duas hierarquias de especialização/generalização (<code>PESSOA</code> $\\to$ <code>{DOCENTE, ALUNO_POS}</code> parcial e sobreposta <code>o</code>; e <code>BOLSA_PESQUISA</code> $\\to$ <code>{BOLSA_MESTRADO, BOLSA_DOUTORADO}</code> total e disjunta <code>d</code>) e o relacionamento ternário <code>BANCA_DEFESA</code>. No seu <strong>Caderno de Resolução Discursiva</strong>, escreva o mapeamento relacional de ambas as hierarquias (comparando as Opções 1, 2 e 3 de <code>ibd-parte5.pdf</code>) e do relacionamento ternário. Depois confira a <strong>Folha de Gabarito Oficial</strong> e valide os checkpoints.
        </div>
        """,
        "study_guide": STUDY_GUIDE_G2,
        "answer_sheet_html": """
        <h4>🔑 Folha de Gabarito Oficial Passo a Passo — Exercício R1.4</h4>
        <ol>
          <li><strong>Hierarquia 1: <code>PESSOA -> {DOCENTE, ALUNO_POS}</code> (Parcial e Sobreposta <code>o</code>):</strong>
            <ul>
              <li><strong>Por que a Opção 2 (apenas subclasses) é PROIBIDA aqui?</strong> Porque a especialização é <strong>parcial</strong> (uma pessoa pode não ser nem docente nem aluno de pós) e <strong>sobreposta</strong> (um docente que também faz doutorado teria <code>Nome</code> duplicado nas duas tabelas).</li>
              <li><strong>Mapeamento pela Opção 3 (Superclasse + Subclasses):</strong>
                <pre><code>PESSOA(CPF(nn), Nome(nn))
  PK: CPF

DOCENTE(CPF(nn), Siape(nn), RegimeDed)
  PK: CPF | RIR: DOCENTE[CPF] -p-> PESSOA[CPF]

ALUNO_POS(CPF(nn), NumMatr(nn), CoefRend)
  PK: CPF | RIR: ALUNO_POS[CPF] -p-> PESSOA[CPF]</code></pre>
              </li>
            </ul>
          </li>
          <li><strong>Hierarquia 2: <code>BOLSA_PESQUISA -> {BOLSA_MESTRADO, BOLSA_DOUTORADO}</code> (Total e Disjunta <code>d</code>):</strong>
            <ul>
              <li>Aqui todas as 3 opções são válidas! Pela <strong>Opção 1 (Tabela Única + CHECK)</strong>:
                <pre><code>BOLSA_PESQUISA(CodBolsa(nn), AgenciaFomento(nn), ValorMensal(nn), MesesDuracaoMestrado, TaxaBancadaDoutorado)
  PK: CodBolsa
  CHECK ((MesesDuracaoMestrado IS NOT NULL AND TaxaBancadaDoutorado IS NULL)
      OR (MesesDuracaoMestrado IS NULL AND TaxaBancadaDoutorado IS NOT NULL))</code></pre>
              </li>
            </ul>
          </li>
          <li><strong>Relacionamento Ternário <code>BANCA_DEFESA (M:N:P)</code>:</strong>
            <pre><code>BANCA_DEFESA(CPFDocente(nn), CPFAlunoPos(nn), CodAud(nn))
  PK: (CPFDocente, CPFAlunoPos, CodAud)
  RIR 1: BANCA_DEFESA[CPFDocente] -p-> DOCENTE[CPF]
  RIR 2: BANCA_DEFESA[CPFAlunoPos] -p-> ALUNO_POS[CPF]
  RIR 3: BANCA_DEFESA[CodAud] -p-> AUDITORIO[CodAud]</code></pre>
          </li>
        </ol>
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
        <div class="problem-narrative">
          <strong>Tarefa Prática SQL DDL (Opção 1 + CHECK):</strong> Mapeie a hierarquia <strong>Disjunta e Total (<code>d</code>, linha dupla)</strong> de <code>BOLSA_PESQUISA</code> (lado direito do diagrama EER acima) em uma <strong>única tabela</strong> chamada <code>BOLSA_PESQUISA</code> contendo:
          <ul style="margin-top:8px; margin-left:20px; color:var(--text-secondary);">
            <li><code>CodBolsa INTEGER NOT NULL PRIMARY KEY</code></li>
            <li><code>AgenciaFomento TEXT NOT NULL</code></li>
            <li><code>ValorMensal REAL NOT NULL</code></li>
            <li><code>MesesDuracaoMestrado INTEGER</code> (atributo específico de <code>BOLSA_MESTRADO</code>)</li>
            <li><code>TaxaBancadaDoutorado REAL</code> (atributo específico de <code>BOLSA_DOUTORADO</code>)</li>
            <li>Uma restrição <code>CHECK</code> de tupla que garanta simultaneamente a <strong>disjunção (<code>d</code>)</strong> e a <strong>totalidade (linha dupla)</strong> entre as duas subclasses!</li>
          </ul>
        </div>
        """,
        "study_guide": STUDY_GUIDE_G2,
        "answer_sheet_html": """
        <h4>🔑 Folha de Gabarito Oficial — Script DDL Completo (Exercício R1.5)</h4>
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
        <div class="problem-narrative">
          <strong>Tarefa Híbrida (Consulta SQL de Auditoria + Análise de Instância):</strong> Na Seção 2 de <code>ibd-parte6.pdf</code>, vimos que uma Dependência Funcional $X \\to Y$ é refutada em uma extensão $r(R)$ se existirem duas tuplas $t_1, t_2$ tais que $t_1[X] = t_2[X]$ e $t_1[Y] \\neq t_2[Y]$.<br><br>
          A tabela <code>ESCALA_NAVIO(IdEscala, NomeNavio, TipoNavio, Porto, PaisPorto, Comandante, Tonelagem)</code> está carregada no banco de dados. Escreva uma consulta SQL que retorne <strong>todas as colunas (<code>IdEscala, NomeNavio, Comandante, Porto</code>)</strong> das tuplas que <strong>violam a dependência funcional proposta <code>NomeNavio -&gt; Comandante</code></strong>, ordenadas por <code>IdEscala</code>. Além disso, use a <strong>Folha de Gabarito Oficial</strong> para revisar quais outras DFs são refutadas ou satisfeitas nesta instância!
        </div>
        """,
        "study_guide": STUDY_GUIDE_G3,
        "answer_sheet_html": """
        <h4>🔑 Folha de Gabarito Oficial Passo a Passo — Exercício R1.6</h4>
        <ol>
          <li><strong>Consulta SQL para Refutar <code>NomeNavio -&gt; Comandante</code>:</strong>
            <pre><code>SELECT DISTINCT e1.IdEscala, e1.NomeNavio, e1.Comandante, e1.Porto
FROM ESCALA_NAVIO e1
JOIN ESCALA_NAVIO e2
  ON e1.NomeNavio = e2.NomeNavio
 AND e1.Comandante &lt;&gt; e2.Comandante
ORDER BY e1.IdEscala;</code></pre>
          </li>
          <li><strong>Análise Completa de Todas as DFs na Instância <code>ESCALA_NAVIO</code>:</strong>
            <ul>
              <li><code>NomeNavio -&gt; TipoNavio</code> e <code>NomeNavio -&gt; Tonelagem</code>: <strong>Satisfeitas na instância</strong> (Mercator é sempre Porta-Contentor/85000; Solaris é sempre Graneleiro/62000; Boreal é sempre Petroleiro/110000).</li>
              <li><code>NomeNavio -&gt; Comandante</code>: <strong>REFUTADA (Falsa!)</strong> — O navio <code>'Mercator'</code> aparece nas escalas 1 e 4 com <code>'Cap. Rocha'</code>, mas na escala 6 aparece com <code>'Cap. Viana'</code>!</li>
              <li><code>TipoNavio -&gt; Tonelagem</code>: <strong>REFUTADA (Falsa!)</strong> — Se houvesse dois navios do mesmo tipo com tonelagens diferentes; na instância atual cada tipo tem 1 navio, mas semântica do mini-mundo diz que dois porta-contentores podem ter tonelagens distintas (lembre-se: uma instância nunca prova que uma DF é regra do esquema!).</li>
            </ul>
          </li>
        </ol>
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
        <div class="problem-narrative">
          <strong>Problema Clássico de Exame (Silberschatz / UFMG — Múltiplas Chaves Candidatas):</strong><br>
          Considere o esquema de relação $R(A, B, C, D, E, G)$ e o conjunto de Dependências Funcionais:<br>
          $$F = \\{ AB \\to C, \\quad C \\to A, \\quad BC \\to D, \\quad ACD \\to B, \\quad D \\to EG, \\quad BE \\to C \\}$$
          Use o seu <strong>Caderno de Resolução Discursiva</strong> para aplicar o método de particionamento de atributos (Essenciais à esquerda $L$, Somente à direita $D$, Intermediários $M$), calcular os fechos e determinar <strong>todas as chaves candidatas</strong> e os <strong>atributos primos e não-primos</strong> de $R$. Em seguida, valide os 3 checkpoints e confira a <strong>Folha de Gabarito Oficial</strong>.
        </div>
        """,
        "study_guide": STUDY_GUIDE_G3,
        "answer_sheet_html": """
        <h4>🔑 Folha de Gabarito Oficial Passo a Passo — Exercício R1.7</h4>
        <ol>
          <li><strong>Passo 1 — Classificação dos Atributos de $R = \\{A, B, C, D, E, G\\}$:</strong>
            <ul>
              <li>Atributos que aparecem no lado direito (RHS) de alguma DF em $F$: $\\{C, A, B, D, E, G\\}$? Não! Olhe com cuidado:
                <ul>
                  <li>$AB \\to C$ (RHS: $C$)</li>
                  <li>$C \\to A$ (RHS: $A$)</li>
                  <li>$BC \\to D$ (RHS: $D$)</li>
                  <li>$ACD \\to B$ (RHS: $B$)</li>
                  <li>$D \\to EG$ (RHS: $E, G$)</li>
                  <li>$BE \\to C$ (RHS: $C$)</li>
                </ul>
              </li>
              <li>Atributos que aparecem <strong>apenas no lado direito (nunca no LHS)</strong>: **$G$** (logo $G$ jamais pertencerá a uma chave candidata!).</li>
              <li>Algum atributo unitário determina tudo sozinho?
                <ul>
                  <li>$\\{A\\}^+ = \\{A\\}$</li>
                  <li>$\\{B\\}^+ = \\{B\\}$</li>
                  <li>$\\{C\\}^+ = \\{A, C\\}$</li>
                  <li>$\\{D\\}^+ = \\{D, E, G\\}$</li>
                  <li>$\\{E\\}^+ = \\{E\\}$</li>
                </ul>
                Nenhum atributo isolado é superchave!
              </li>
            </ul>
          </li>
          <li><strong>Passo 2 — Teste Sistemático dos Pares (2 atributos):</strong>
            <ul>
              <li><strong>$\\{A, B\\}^+$:</strong> $\\{A, B\\} \\xrightarrow{AB \\to C} \\{A, B, C\\} \\xrightarrow{BC \\to D} \\{A, B, C, D\\} \\xrightarrow{D \\to EG} \\{A, B, C, D, E, G\\} = R$ $\\implies$ <strong>$\\{A, B\\}$ é Chave Candidata!</strong></li>
              <li><strong>$\\{B, C\\}^+$:</strong> $\\{B, C\\} \\xrightarrow{C \\to A} \\{A, B, C\\} \\xrightarrow{BC \\to D} \\{A, B, C, D\\} \\xrightarrow{D \\to EG} \\{A, B, C, D, E, G\\} = R$ $\\implies$ <strong>$\\{B, C\\}$ é Chave Candidata!</strong></li>
              <li><strong>$\\{B, D\\}^+$:</strong> $\\{B, D\\} \\xrightarrow{D \\to EG} \\{B, D, E, G\\} \\xrightarrow{BE \\to C} \\{B, C, D, E, G\\} \\xrightarrow{C \\to A} \\{A, B, C, D, E, G\\} = R$ $\\implies$ <strong>$\\{B, D\\}$ é Chave Candidata!</strong></li>
              <li><strong>$\\{B, E\\}^+$:</strong> $\\{B, E\\} \\xrightarrow{BE \\to C} \\{B, C, E\\} \\xrightarrow{BC \\to D} \\{B, C, D, E\\} \\xrightarrow{D \\to EG} \\{B, C, D, E, G\\} \\xrightarrow{C \\to A} \\{A, B, C, D, E, G\\} = R$ $\\implies$ <strong>$\\{B, E\\}$ é Chave Candidata!</strong></li>
              <li><strong>$\\{A, C\\}^+ = \\{A, C\\}$</strong>; <strong>$\\{A, D\\}^+ = \\{A, D, E, G\\}$</strong>; <strong>$\\{C, D\\}^+ = \\{A, C, D, E, G\\} \\xrightarrow{ACD \\to B} \\{A, B, C, D, E, G\\} = R$ $\\implies$ $\\{C, D\\}$ também é Chave Candidata!</strong></li>
            </ul>
          </li>
          <li><strong>Passo 3 — Resumo Final:</strong>
            <ul>
              <li><strong>Todas as 5 Chaves Candidatas de $R$:</strong> $\\{A, B\\}$, $\\{B, C\\}$, $\\{B, D\\}$, $\\{B, E\\}$ e $\\{C, D\\}$.</li>
              <li><strong>Atributos Primos:</strong> $\\{A, B, C, D, E\\}$ (todos exceto $G$!).</li>
              <li><strong>Único Atributo Não-Primo:</strong> $\\{G\\}$.</li>
            </ul>
          </li>
        </ol>
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
        <div class="problem-narrative">
          <strong>Problema Algorítmico (<code>ibd-parte6.pdf</code>, Seção 3.4 — Cobertura Mínima):</strong><br>
          Seja o esquema $R(A, B, C, D, E)$ e o conjunto inicial de Dependências Funcionais:<br>
          $$F = \\{ A \\to BC, \\quad B \\to C, \\quad A \\to B, \\quad AB \\to D, \\quad D \\to E, \\quad A \\to E \\}$$
          No seu <strong>Caderno de Resolução Discursiva</strong>, execute os <strong>3 passos formais</strong> do algoritmo de Cobertura Mínima ($F_c$):
          <ol style="margin-top:6px; margin-left:20px; color:var(--text-secondary);">
            <li><strong>Passo 1:</strong> Reescrever todas as DFs com um único atributo no lado direito (RHS canônico).</li>
            <li><strong>Passo 2:</strong> Testar e eliminar atributos estranhos no lado esquerdo de $AB \\to D$.</li>
            <li><strong>Passo 3:</strong> Testar e eliminar DFs redundantes calculando o fecho em $F - \\{f\\}$.</li>
          </ol>
        </div>
        """,
        "study_guide": STUDY_GUIDE_G4,
        "answer_sheet_html": """
        <h4>🔑 Folha de Gabarito Oficial Passo a Passo — Exercício R1.8</h4>
        <ol>
          <li><strong>Passo 1 — Lado Direito Unitário (Decomposição de $A \\to BC$):</strong>
            $$F_1 = \\{ A \\to B, \\; A \\to C, \\; B \\to C, \\; AB \\to D, \\; D \\to E, \\; A \\to E \\}$$
            *(Nota: $A \\to B$ aparecia duas vezes e é unificada).*
          </li>
          <li><strong>Passo 2 — Eliminação de Atributo Estranho no Lado Esquerdo de $AB \\to D$:</strong>
            <ul>
              <li>Testamos se $B$ é estranho em $AB \\to D$: calculamos $\\{A\\}^+$ sob $F_1$:
                $$\\{A\\}^+ = \\{A, B, C, D, E\\}$$
                Como $B \\in \\{A\\}^+$ (pois já temos $A \\to B$), o atributo $B$ é <strong>estranho (redundante)</strong> no lado esquerdo de $AB \\to D$!</li>
              <li>Substituímos $AB \\to D$ por **$A \\to D$**:
                $$F_2 = \\{ A \\to B, \\; A \\to C, \\; B \\to C, \\; A \\to D, \\; D \\to E, \\; A \\to E \\}$$
              </li>
            </ul>
          </li>
          <li><strong>Passo 3 — Eliminação de Dependências Funcionais Redundantes:</strong>
            <ul>
              <li>Teste de **$A \\to C$**: Removendo $A \\to C$, calculamos $\\{A\\}^+$ usando $\\{A \\to B, B \\to C, A \\to D, D \\to E, A \\to E\\} \\implies \\{A, B, C, D, E\\}$. Como $C$ continua no fecho (via $A \\to B$ e $B \\to C$), **$A \\to C$ é redundante e é removida!**</li>
              <li>Teste de **$A \\to E$**: Removendo $A \\to E$, calculamos $\\{A\\}^+$ usando $\\{A \\to B, B \\to C, A \\to D, D \\to E\\} \\implies \\{A, B, C, D, E\\}$. Como $E$ continua no fecho (via $A \\to D$ e $D \\to E$), **$A \\to E$ é redundante e é removida!**</li>
            </ul>
          </li>
          <li><strong>Cobertura Mínima Final ($F_c$):</strong>
            $$F_c = \\{ A \\to B, \\quad B \\to C, \\quad A \\to D, \\quad D \\to E \\}$$
          </li>
        </ol>
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
        <div class="problem-narrative">
          <strong>Estudo de Caso Clássico (Elmasri &amp; Navathe Cap. 14 — <code>CAR_SALE</code> &amp; <code>ORDEM_COMPRA</code>):</strong><br>
          <strong>Parte A (1FN):</strong> Uma tabela não-normalizada <code>ORDEM_COMPRA(<u>NumOrdem</u>, DataOrdem, CNPJFornecedor, RazaoFornecedor, {<u>CodPeca</u>, NomePeca, Quantidade, PrecoUnitario})</code> contém um grupo repetitivo multivalorado de itens comprados.<br>
          <strong>Parte B (2FN e 3FN — Elmasri <code>CAR_SALE</code>):</strong> Considere a relação já em 1FN:<br>
          $$\\text{CAR\\_SALE}(\\underline{\\text{Car}\\#, \\text{Salesperson}\\#}, \\text{Date\\_sold}, \\text{Commission}\\%, \\text{Discount\\_amt})$$
          Onde a chave primária é composta por $\\{\\text{Car}\\#, \\text{Salesperson}\\#\\}$ e valem as seguintes DFs adicionais além da determinação pela PK:
          <ul style="margin-top:6px; margin-left:20px; color:var(--text-secondary);">
            <li>$\\text{Car}\\# \\to \\{\\text{Date\\_sold}, \\text{Discount\\_amt}\\}$</li>
            <li>$\\text{Date\\_sold} \\to \\text{Discount\\_amt}$</li>
            <li>$\\text{Salesperson}\\# \\to \\text{Commission}\\%$</li>
          </ul>
          Escreva a decomposição completa de ambas na sua área de rascunho, confira a <strong>Folha de Gabarito Oficial</strong> e valide os checkpoints.
        </div>
        """,
        "study_guide": STUDY_GUIDE_G4,
        "answer_sheet_html": """
        <h4>🔑 Folha de Gabarito Oficial Passo a Passo — Exercício R1.9</h4>
        <ol>
          <li><strong>Parte A — Normalização de <code>ORDEM_COMPRA</code> para 1FN, 2FN e 3FN:</strong>
            <ul>
              <li><strong>Passagem para 1FN (Eliminação do grupo multivalorado):</strong>
                <pre><code>ORDEM(NumOrdem(nn), DataOrdem, CNPJFornecedor(nn), RazaoFornecedor) -- PK: NumOrdem
ITEM_ORDEM(NumOrdem(nn), CodPeca(nn), NomePeca, Quantidade, PrecoUnitario) -- PK: (NumOrdem, CodPeca)</code></pre>
              </li>
              <li><strong>Passagem para 2FN (Eliminando dependência parcial <code>CodPeca -> NomePeca</code> em <code>ITEM_ORDEM</code>):</strong>
                <pre><code>PECA(CodPeca(nn), NomePeca) -- PK: CodPeca
ITEM_ORDEM_2FN(NumOrdem(nn), CodPeca(nn), Quantidade, PrecoUnitario) -- PK: (NumOrdem, CodPeca)</code></pre>
              </li>
              <li><strong>Passagem para 3FN (Eliminando dependência transitiva <code>CNPJFornecedor -> RazaoFornecedor</code> em <code>ORDEM</code>):</strong>
                <pre><code>FORNECEDOR(CNPJFornecedor(nn), RazaoFornecedor) -- PK: CNPJFornecedor
ORDEM_3FN(NumOrdem(nn), DataOrdem, CNPJFornecedor(nn)) -- PK: NumOrdem | FK: CNPJFornecedor</code></pre>
              </li>
            </ul>
          </li>
          <li><strong>Parte B — Decomposição de <code>CAR_SALE</code> (Elmasri &amp; Navathe) para 2FN e 3FN:</strong>
            <ul>
              <li><strong>Diagnóstico em <code>CAR_SALE</code>:</strong>
                <ul>
                  <li>Viola <strong>2FN</strong> porque <code>Date_sold</code> e <code>Discount_amt</code> dependem apenas de <code>Car#</code> (subconjunto próprio da PK), e <code>Commission%</code> depende apenas de <code>Salesperson#</code> (subconjunto próprio da PK)!</li>
                  <li>Assim, após extrair as dependências parciais para atingir a <strong>2FN</strong>, obtemos:
                    <pre><code>R1_VENDA(Car#(nn), Salesperson#(nn))                  -- PK: (Car#, Salesperson#)
R2_VENDEDOR(Salesperson#(nn), Commission%)            -- PK: Salesperson#
R3_CARRO(Car#(nn), Date_sold, Discount_amt)           -- PK: Car#</code></pre>
                  </li>
                  <li>Porém, <code>R3_CARRO</code> ainda viola a <strong>3FN</strong>, pois <code>Car# -> Date_sold -> Discount_amt</code> é uma dependência transitiva! Decompondo <code>R3_CARRO</code> para <strong>3FN</strong>:
                    <pre><code>R31_CARRO(Car#(nn), Date_sold)                        -- PK: Car# | FK: Date_sold -> R32_DESCONTO
R32_DESCONTO(Date_sold(nn), Discount_amt)             -- PK: Date_sold</code></pre>
                  </li>
                </ul>
              </li>
            </ul>
          </li>
        </ol>
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
        <div class="problem-narrative">
          <strong>Problema Nível Prova Final UFMG (<code>ibd-parte6.pdf</code>, Seção 4 — Definição Geral de 2FN e 3FN):</strong><br>
          Considere a relação universal <code>SESSAO_CONGRESSO</code> que registra apresentações em um congresso científico:<br>
          $$\\text{SESSAO\\_CONGRESSO}(\\underline{\\text{CodTrilha}, \\text{NumSessao}}, \\text{Sala}, \\text{Horario}, \\text{CPFPalestrante}, \\text{NomePalestrante}, \\text{CNPJPatrocinador}, \\text{RazaoPatrocinador}, \\text{CapacidadeSala})$$
          As regras de negócio (Dependências Funcionais $F$) são:
          <ul style="margin-top:6px; margin-left:20px; color:var(--text-secondary);">
            <li><strong>DF1:</strong> $\\{\\text{CodTrilha}, \\text{NumSessao}\\} \\to \\{\\text{Sala}, \\text{Horario}, \\text{CPFPalestrante}, \\text{CNPJPatrocinador}\\}$</li>
            <li><strong>DF2:</strong> $\\{\\text{Sala}, \\text{Horario}\\} \\to \\{\\text{CodTrilha}, \\text{NumSessao}\\}$ <em>(Uma sala em um horário abriga no máximo uma sessão do congresso)</em></li>
            <li><strong>DF3:</strong> $\\text{CodTrilha} \\to \\text{CNPJPatrocinador}$ <em>(Cada trilha temática tem um único patrocinador oficial)</em></li>
            <li><strong>DF4:</strong> $\\text{CNPJPatrocinador} \\to \\text{RazaoPatrocinador}$</li>
            <li><strong>DF5:</strong> $\\text{Sala} \\to \\text{CapacidadeSala}$</li>
            <li><strong>DF6:</strong> $\\text{CPFPalestrante} \\to \\text{NomePalestrante}$</li>
          </ul>
          Use o seu <strong>Caderno de Resolução Discursiva</strong> para listar todas as chaves candidatas, atributos primos, decomposição para 2FN e decomposição para 3FN. Depois consulte a <strong>Folha de Gabarito Oficial</strong> e valide os checkpoints.
        </div>
        """,
        "study_guide": STUDY_GUIDE_G4,
        "answer_sheet_html": """
        <h4>🔑 Folha de Gabarito Oficial Passo a Passo — Exercício R1.10</h4>
        <ol>
          <li><strong>Passo 1 — Chaves Candidatas e Atributos Primos:</strong>
            <ul>
              <li><strong>Chave Candidata 1 (PK):</strong> $CK_1 = \\{\\text{CodTrilha}, \\text{NumSessao}\\}$</li>
              <li><strong>Chave Candidata 2 (AK / UNIQUE):</strong> $CK_2 = \\{\\text{Sala}, \\text{Horario}\\}$ (pois $\\{\\text{Sala}, \\text{Horario}\\} \\to \\{\\text{CodTrilha}, \\text{NumSessao}\\}$, que determina toda a tupla!).</li>
              <li><strong>Atributos Primos (pertencem a $CK_1 \\cup CK_2$):</strong> <code>CodTrilha, NumSessao, Sala, Horario</code>.</li>
              <li><strong>Atributos Não-Primos:</strong> <code>CPFPalestrante, NomePalestrante, CNPJPatrocinador, RazaoPatrocinador, CapacidadeSala</code>.</li>
            </ul>
          </li>
          <li><strong>Passo 2 — Decomposição para 2FN (Pela Definição Geral de <code>ibd-parte6.pdf</code>):</strong>
            <ul>
              <li><strong>Violação 1 (Parcial sobre $CK_1$):</strong> $\\text{CodTrilha} \\to \\{\\text{CNPJPatrocinador}, \\text{RazaoPatrocinador}\\}$ (dependem apenas de parte de $CK_1$).</li>
              <li><strong>Violação 2 (Parcial sobre $CK_2$):</strong> $\\text{Sala} \\to \\text{CapacidadeSala}$ (<code>CapacidadeSala</code> é não-primo e depende apenas de <code>Sala</code>, que é subconjunto próprio da chave candidata $CK_2 = \\{\\text{Sala}, \\text{Horario}\\}$!).</li>
              <li><strong>Relações na 2FN:</strong>
                <pre><code>TRILHA_2FN(CodTrilha(nn), CNPJPatrocinador(nn), RazaoPatrocinador)   -- PK: CodTrilha
SALA_2FN(Sala(nn), CapacidadeSala)                                   -- PK: Sala
SESSAO_2FN(CodTrilha(nn), NumSessao(nn), Sala(nn), Horario(nn), CPFPalestrante(nn), NomePalestrante)
  PK: (CodTrilha, NumSessao) | Chave Alternativa: (Sala, Horario)</code></pre>
              </li>
            </ul>
          </li>
          <li><strong>Passo 3 — Decomposição para 3FN (Eliminando Dependências Transitivas):</strong>
            <ul>
              <li>Em <code>TRILHA_2FN</code>: $\\text{CodTrilha} \\to \\text{CNPJPatrocinador} \\to \\text{RazaoPatrocinador}$ viola 3FN!</li>
              <li>Em <code>SESSAO_2FN</code>: $\\text{CPFPalestrante} \\to \\text{NomePalestrante}$ viola 3FN!</li>
              <li><strong>Esquema Final Completo em 3FN (5 Relações):</strong>
                <pre><code>1. PATROCINADOR(CNPJPatrocinador(nn), RazaoPatrocinador(nn))
     PK: CNPJPatrocinador

2. TRILHA(CodTrilha(nn), CNPJPatrocinador(nn))
     PK: CodTrilha | FK: CNPJPatrocinador -> PATROCINADOR

3. SALA_CONGRESSO(Sala(nn), CapacidadeSala(nn))
     PK: Sala

4. PALESTRANTE(CPFPalestrante(nn), NomePalestrante(nn))
     PK: CPFPalestrante

5. SESSAO(CodTrilha(nn), NumSessao(nn), Sala(nn), Horario(nn), CPFPalestrante(nn))
     PK: (CodTrilha, NumSessao)
     Chave Alternativa (UNIQUE): (Sala, Horario)
     FK 1: CodTrilha -> TRILHA
     FK 2: Sala -> SALA_CONGRESSO
     FK 3: CPFPalestrante -> PALESTRANTE</code></pre>
              </li>
            </ul>
          </li>
        </ol>
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
