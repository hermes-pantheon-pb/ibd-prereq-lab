/**
 * IBD Prerequisite Studio — Client Application Logic
 */

let curriculumData = null;
let currentExerciseId = "T1.1";
let currentExerciseMeta = null;
let solvedExercises = new Set();
let structuredAnswers = {};

// Load saved solved exercises from localStorage
try {
  const saved = localStorage.getItem("ibd_prereq_solved");
  if (saved) {
    solvedExercises = new Set(JSON.parse(saved));
  }
} catch (e) {
  console.warn("Storage not available:", e);
}

document.addEventListener("DOMContentLoaded", async () => {
  await loadCurriculum();
  setupUIEventListeners();
  setupKeyboardShortcuts();
  updateProgressUI();
  await selectExercise("T1.1");
});

async function loadCurriculum() {
  try {
    const res = await fetch("curriculum.json");
    curriculumData = await res.json();
    renderSidebar();
  } catch (err) {
    console.error("Falha ao carregar currículo:", err);
    showToast("Erro ao carregar dados do currículo.");
  }
}

function setupUIEventListeners() {
  // Tabs: Concepts vs Practice
  document.querySelectorAll(".tab-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".tab-btn").forEach((b) => b.classList.remove("active"));
      document.querySelectorAll(".tab-panel").forEach((p) => p.classList.remove("active"));
      btn.classList.add("active");
      const targetId = btn.getAttribute("data-target");
      const targetPanel = document.getElementById(targetId);
      if (targetPanel) targetPanel.classList.add("active");
    });
  });

  // Output Tabs: Results vs Expected vs Schema
  document.querySelectorAll(".out-tab").forEach((tab) => {
    tab.addEventListener("click", () => {
      document.querySelectorAll(".out-tab").forEach((t) => t.classList.remove("active"));
      document.querySelectorAll(".out-view").forEach((v) => v.classList.remove("active"));
      tab.classList.add("active");
      const targetId = tab.getAttribute("data-target");
      const targetView = document.getElementById(targetId);
      if (targetView) targetView.classList.add("active");
    });
  });

  // Jump from Theory to Practice
  document.getElementById("btn-jump-to-practice").addEventListener("click", () => {
    document.getElementById("tab-btn-practice").click();
  });

  // Action Buttons
  document.getElementById("btn-validate-structured").addEventListener("click", validateStructured);
  document.getElementById("btn-reset-structured").addEventListener("click", resetStructured);

  document.getElementById("btn-run-code").addEventListener("click", runCode);
  document.getElementById("btn-validate-code").addEventListener("click", validateCode);
  document.getElementById("btn-clear-editor").addEventListener("click", () => {
    document.getElementById("sql-editor").value = "";
    document.getElementById("sql-editor").focus();
  });
  document.getElementById("btn-show-hint").addEventListener("click", showHint);


  // Exam Modal
  const modalExam = document.getElementById("modal-exam");
  const btnExam = document.getElementById("btn-exam-modal");
  const btnCloseExam = document.getElementById("btn-close-exam");
  if (btnExam && modalExam) {
    btnExam.addEventListener("click", () => modalExam.classList.add("active"));
  }
  if (btnCloseExam && modalExam) {
    btnCloseExam.addEventListener("click", () => modalExam.classList.remove("active"));
  }
  if (modalExam) {
    modalExam.addEventListener("click", (e) => {
      if (e.target === modalExam) modalExam.classList.remove("active");
    });
  }

  // Cheat Sheet Modal
  const modalCheat = document.getElementById("modal-cheatsheet");
  document.getElementById("btn-cheatsheet-modal").addEventListener("click", () => {
    modalCheat.classList.add("active");
  });
  document.getElementById("btn-close-cheatsheet").addEventListener("click", () => {
    modalCheat.classList.remove("active");
  });
  modalCheat.addEventListener("click", (e) => {
    if (e.target === modalCheat) modalCheat.classList.remove("active");
  });

  // Sidebar search
  document.getElementById("exercise-search").addEventListener("input", (e) => {
    const term = e.target.value.toLowerCase().trim();
    document.querySelectorAll(".module-group").forEach((group) => {
      let groupHasMatch = false;
      group.querySelectorAll(".exercise-nav-item").forEach((item) => {
        const text = item.innerText.toLowerCase();
        const match = term === "" || text.includes(term);
        item.style.display = match ? "flex" : "none";
        if (match && term !== "") groupHasMatch = true;
      });
      if (term !== "") {
        if (groupHasMatch) {
          group.classList.add("open");
          group.style.display = "block";
        } else {
          group.style.display = "none";
        }
      } else {
        group.style.display = "block";
      }
    });
  });

  // Collapse / Expand all
  document.getElementById("btn-collapse-all").addEventListener("click", () => {
    document.querySelectorAll(".module-group").forEach((grp) => grp.classList.remove("open"));
  });
  document.getElementById("btn-expand-all").addEventListener("click", () => {
    document.querySelectorAll(".module-group").forEach((grp) => grp.classList.add("open"));
  });

  // Expandable Drawer 1: Worked Example
  const btnToggleExample = document.getElementById("btn-toggle-example");
  if (btnToggleExample) {
    btnToggleExample.addEventListener("click", () => {
      const exDrawer = document.getElementById("sg-example-drawer");
      if (exDrawer) {
        const isHidden = exDrawer.style.display === "none";
        exDrawer.style.display = isHidden ? "block" : "none";
        btnToggleExample.innerText = isHidden
          ? "🙈 Fechar Exemplo Análogo"
          : "📘 Ver Exemplo Análogo Resolvido";
      }
    });
  }

  // Expandable Drawer 2: Official Step-by-Step Answer Sheet
  const btnToggleAns = document.getElementById("btn-toggle-answersheet");
  if (btnToggleAns) {
    btnToggleAns.addEventListener("click", () => {
      const ansBox = document.getElementById("answer-sheet-box");
      if (ansBox) {
        const isHidden = ansBox.style.display === "none";
        ansBox.style.display = isHidden ? "block" : "none";
        btnToggleAns.innerText = isHidden
          ? "🙈 Ocultar Gabarito Oficial"
          : "🔑 Ver Gabarito Passo a Passo";
      }
    });
  }

  // Persist Open Scratchpad per exercise
  const scratchpad = document.getElementById("open-scratchpad");
  if (scratchpad) {
    scratchpad.addEventListener("input", (e) => {
      try {
        localStorage.setItem(`ibd_scratch_${currentExerciseId}`, e.target.value);
      } catch (err) {
        // ignore storage quota errors
      }
    });
  }
}

function setupKeyboardShortcuts() {
  window.addEventListener("keydown", (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
      e.preventDefault();
      if (currentExerciseMeta && currentExerciseMeta.mode === "structured") {
        validateStructured();
      } else {
        validateCode();
      }
    }
  });
}

function renderSidebar() {
  const container = document.getElementById("modules-nav");
  container.innerHTML = "";

  curriculumData.modules.forEach((mod) => {
    const group = document.createElement("div");
    group.className = "module-group";
    group.id = `mod-group-${mod.id}`;

    const header = document.createElement("div");
    header.className = "module-header";
    header.innerHTML = `
      <div class="mod-title-area">
        <span class="mod-badge">${mod.badge}</span>
        <span class="mod-name">${mod.title.split(":")[1]?.trim() || mod.title}</span>
      </div>
      <span class="mod-chevron">▶</span>
    `;

    header.addEventListener("click", () => {
      group.classList.toggle("open");
    });

    const exList = document.createElement("div");
    exList.className = "module-exercises-list";

    mod.exercises.forEach((exId) => {
      const item = document.createElement("div");
      item.className = "exercise-nav-item";
      item.id = `nav-ex-${exId}`;
      const isSolved = solvedExercises.has(exId);
      const isTreino = exId.startsWith("T");
      if (isTreino) item.classList.add("item-treino");

      item.innerHTML = `
        <div class="ex-nav-left">
          <span class="ex-tag-num">${exId}</span>
          <span class="ex-nav-title">${escapeHtml(getExerciseShortTitle(exId))}</span>
        </div>
        <span class="ex-status-icon">${isSolved ? "✅" : "⚪"}</span>
      `;

      item.addEventListener("click", (e) => {
        e.stopPropagation();
        selectExercise(exId);
      });

      exList.appendChild(item);
    });

    group.appendChild(header);
    group.appendChild(exList);
    container.appendChild(group);
  });
}

function getExerciseShortTitle(exId) {
  const titles = {
    "T1.1": "Esquema vs. Instância e 3 Níveis",
    "T1.2": "Independência Lógica vs. Física",
    "E1.1": "[Oficial] Sublinguagens DDL/DML",
    "T2.1": "Classificação de Atributos ER",
    "T2.2": "Cardinalidade 1:N vs. (min, max)",
    "T2.3": "Entidades Fracas e Chave Parcial",
    "E2.1": "[Oficial] Auditoria Esquema COMPANY",
    "T3.1": "Hierarquias EER (d/o, Total/Parcial)",
    "T3.2": "Ternários vs. Três Binários",
    "T3.3": "Modelagem em Notação UML",
    "E3.1": "[Oficial] Estudo de Caso GLT Library",
    "T4.1": "Superchaves, Candidatas e PK",
    "T4.2": "Auditoria de Violações e Atualizações",
    "E4.1": "[Oficial] Chaves Estrangeiras e RIR",
    "E4.2": "[Oficial] Políticas de Remoção (b, p, n)",
    "T5.1": "Diferença (R - S): Sem Dependentes",
    "T5.2": "Divisão (÷): Projetos de John Smith",
    "T5.3": "Restrições em Álgebra Relacional",
    "E5.1": "[Oficial] Trabalham em TODOS Projetos",
    "E5.2": "[Oficial] Gerentes Sem Dependentes",
    "T6.1": "DDL: PK, UNIQUE e RIR ON DELETE",
    "T6.2": "CHECK: Otimização de Hierarquias",
    "T6.3": "Visões e Modificação de Consulta",
    "E6.1": "[Oficial] Depto 5, Homônimos, Franklin",
    "E6.2": "[Oficial] ASSERTION: Salário Gerente",
    "E6.3": "[Oficial] ASSERTION: Hierarquia Total/d",
    "T7.1": "Mapeamento ER: Entidades, Multivalorados e Fracas",
    "T7.2": "Mapeamento M:N e Agregações EER",
    "T7.3": "Mapeamento Otimizado de Hierarquias (d vs. o)",
    "E7.1": "[Oficial Exame] Voo, Trecho_Voo e Aeroporto",
    "E7.2": "[Oficial Exame] Aeronave e Pode_Pousar",
    "E7.3": "[Oficial Exame] Reserva, Assento e Tarifa",
    "T8.1": "Fechamento (X+) e Determinação de Chaves",
    "T8.2": "Diagnóstico de Violações 2FN e 3FN",
    "T8.3": "Axiomas de Armstrong e Conjunto Minimal",
    "E8.1": "[Oficial Normalização] Q1: Chave de R(A..E)",
    "E8.2": "[Oficial Normalização] Q2: Decomposição 2FN/3FN",
    "E8.3": "[Oficial Normalização] Q3: Sistema Cursos/Turmas",
    "R1.1": "[Rodada 1] Hospital ER: Entidades e Fraca",
    "R1.2": "[Rodada 1] Hospital ER: 1:1, 1:N, M:N e RIRs",
    "R1.3": "[Rodada 1] Hospital DDL: Fraca & ON DELETE",
    "R1.4": "[Rodada 1] Universidade EER: d/o & Ternário",
    "R1.5": "[Rodada 1] Universidade DDL: Opção 1 + CHECK",
    "R1.6": "[Rodada 1] Detetive SQL: Violação DF Navios",
    "R1.7": "[Rodada 1] Fecho X+ e 5 Chaves em R(A..G)",
    "R1.8": "[Rodada 1] Cobertura Mínima (3 Passos)",
    "R1.9": "[Rodada 1] Elmasri CAR_SALE & Ordem (1FN-3FN)",
    "R1.10": "[Rodada 1] Congresso: 2FN/3FN Geral (2 CKs)"
  };
  return titles[exId] || exId;
}

async function selectExercise(exId) {
  try {
    currentExerciseId = exId;
    const res = await fetch(`/api/exercise/${exId}`);
    currentExerciseMeta = await res.json();

    if (currentExerciseMeta.error) {
      console.error(currentExerciseMeta.error);
      return;
    }

    // Determine current module
    const mod = curriculumData.modules.find((m) => m.exercises.includes(exId));
    if (mod) {
      document.querySelectorAll(".module-group").forEach((g) => g.classList.remove("active"));
      const activeGrp = document.getElementById(`mod-group-${mod.id}`);
      if (activeGrp) {
        activeGrp.classList.add("open", "active");
      }
      renderModuleConcepts(mod);
    }

    // Update active highlight in sidebar
    document.querySelectorAll(".exercise-nav-item").forEach((it) => it.classList.remove("active"));
    const activeNav = document.getElementById(`nav-ex-${exId}`);
    if (activeNav) activeNav.classList.add("active");

    // Header badge
    document.getElementById("header-ex-label").innerText = `${exId}: ${currentExerciseMeta.title}`;

    // Exercise details
    document.getElementById("ex-number-badge").innerText = exId;
    document.getElementById("ex-number-badge").style.background = exId.startsWith("T")
      ? "var(--accent-purple)"
      : exId.startsWith("R")
      ? "#10b981"
      : "var(--accent-blue)";
    document.getElementById("ex-mode-tag").innerText = currentExerciseMeta.mode.toUpperCase();
    document.getElementById("ex-title").innerText = currentExerciseMeta.title;

    // Side-by-Side Workbench: Problem Schema (Left) + Quick Rules & Scratchpad (Right)
    const wb = document.getElementById("ex-workbench");
    const ctxContainer = document.getElementById("ex-context-container");
    const companionCol = document.getElementById("ex-companion-col");
    const sgContainer = document.getElementById("ex-study-guide-container");
    const orContainer = document.getElementById("ex-open-resolution-container");
    const exDrawer = document.getElementById("sg-example-drawer");
    const ansBox = document.getElementById("answer-sheet-box");
    const btnToggleExample = document.getElementById("btn-toggle-example");
    const btnToggleAns = document.getElementById("btn-toggle-answersheet");

    const hasCtx = Boolean(currentExerciseMeta.contextHtml);
    const hasSg = Boolean(currentExerciseMeta.studyGuide);
    const hasRes = Boolean(currentExerciseMeta.answerSheetHtml);

    // 1. Populate Left Schema & Context (Always visible)
    if (ctxContainer) {
      ctxContainer.innerHTML = hasCtx ? currentExerciseMeta.contextHtml : "";
      ctxContainer.style.display = hasCtx ? "flex" : "none";
    }

    // 2. Populate Quick Rule Summary (Always visible in companion col alongside schema)
    if (sgContainer) {
      if (hasSg) {
        const sg = currentExerciseMeta.studyGuide;
        document.getElementById("sg-title").innerText = sg.title || "Regras da Questão";
        document.getElementById("sg-coursework-ref").innerText = sg.coursework_ref || "";
        document.getElementById("sg-body").innerHTML = sg.quick_rules_html || sg.summary_html || "";
        sgContainer.style.display = "block";

        if (exDrawer) {
          exDrawer.innerHTML = sg.example_html || "";
          exDrawer.style.display = "none";
        }
        if (btnToggleExample) {
          btnToggleExample.style.display = sg.example_html ? "inline-flex" : "none";
          btnToggleExample.innerText = "📘 Ver Exemplo Análogo Resolvido";
        }
      } else {
        sgContainer.style.display = "none";
        if (exDrawer) exDrawer.style.display = "none";
      }
    }

    // 3. Populate Scratchpad (Always visible alongside schema) and Answer Sheet Drawer
    if (orContainer) {
      if (hasRes) {
        const scratchpad = document.getElementById("open-scratchpad");
        if (scratchpad) {
          scratchpad.value = localStorage.getItem(`ibd_scratch_${exId}`) || "";
        }
        if (ansBox) {
          ansBox.innerHTML = currentExerciseMeta.answerSheetHtml;
          ansBox.style.display = "none";
        }
        if (btnToggleAns) {
          btnToggleAns.style.display = "inline-flex";
          btnToggleAns.innerText = "🔑 Ver Gabarito Passo a Passo";
        }
        orContainer.style.display = "flex";
      } else {
        orContainer.style.display = "none";
        if (ansBox) ansBox.style.display = "none";
        if (btnToggleAns) btnToggleAns.style.display = "none";
      }
    }

    // Show/Hide Entire Workbench
    if (wb) {
      wb.style.display = (hasCtx || hasSg || hasRes) ? "flex" : "none";
    }

    // Workspace mode switcher
    const structPane = document.getElementById("structured-pane");
    const codePane = document.getElementById("code-workspace-grid");

    if (currentExerciseMeta.mode === "structured") {
      structPane.style.display = "block";
      codePane.style.display = "none";
      document.getElementById("ex-statement").innerText = "Responda às questões conceituais baseadas diretamente nos slides e nas listas oficiais do Prof. Marcos André Gonçalves:";
      document.getElementById("ex-intuition-text").innerText = "Leia com atenção os termos formais. Diferencie conceitos estruturais (esquema) de transientes (instância), e atente-se às regras de inversão de lado em (min, max).";
      renderStructuredQuestions(currentExerciseMeta.fields);
    } else {
      structPane.style.display = "none";
      codePane.style.display = "grid";

      const modeLabels = {
        "sql_query": "Consulta SQL / Equivalência com Álgebra Relacional",
        "sql_ddl": "Comandos DDL (CREATE TABLE, PRIMARY KEY, UNIQUE, CHECK, FOREIGN KEY)",
        "sql_assertion": "Asserção SQL-92: CREATE ASSERTION <nome> CHECK (NOT EXISTS (...));"
      };
      document.getElementById("editor-mode-label").innerText = modeLabels[currentExerciseMeta.mode] || "Editor de Código";

      if (currentExerciseMeta.mode === "sql_query") {
        document.getElementById("ex-statement").innerText = "Escreva a consulta SQL equivalente à operação descrita nos slides ou listas oficiais:";
        document.getElementById("ex-intuition-text").innerText = "Lembre-se da ordem de execução lógica (FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY).";
        document.getElementById("sql-editor").value = `-- Exercício ${exId}: ${currentExerciseMeta.title}\n-- Escreva sua consulta SQL e pressione Ctrl + Enter para validar:\n`;
      } else if (currentExerciseMeta.mode === "sql_ddl") {
        document.getElementById("ex-statement").innerText = "Escreva os comandos DDL completos em SQL com todas as restrições estruturais exigidas:";
        document.getElementById("ex-intuition-text").innerText = "O avaliador executará uma bateria de injeção de falhas (tentando inserir dados ilegais e verificar propagação em cascata). Todas as restrições devem estar ativas!";
        document.getElementById("sql-editor").value = `-- Exercício ${exId}: ${currentExerciseMeta.title}\n-- Escreva os comandos CREATE TABLE com PRIMARY KEY, UNIQUE, CHECK e FOREIGN KEY:\n`;
      } else if (currentExerciseMeta.mode === "sql_assertion") {
        document.getElementById("ex-statement").innerText = "Escreva a Asserção Geral de Integridade padrão SQL-92 (CREATE ASSERTION):";
        document.getElementById("ex-intuition-text").innerText = "Use a estrutura formal dos slides: CREATE ASSERTION <nome> CHECK (NOT EXISTS (SELECT ... WHERE <condicao_de_violacao>));";
        document.getElementById("sql-editor").value = `-- Exercício ${exId}: ${currentExerciseMeta.title}\nCREATE ASSERTION NOME_ASSERCAO\nCHECK (NOT EXISTS (\n    SELECT *\n    FROM ...\n    WHERE ...\n));\n`;
      }

      // Reset output tabs
      document.getElementById("validation-banner").style.display = "none";
      document.getElementById("result-table-container").innerHTML = `
        <div class="empty-state">
          <span class="empty-icon">⚡</span>
          <p>Clique em <strong>Executar</strong> ou <strong>Validar</strong> para testar seu código.</p>
        </div>
      `;
      document.getElementById("stats-summary").innerText = "Aguardando execução...";
      document.getElementById("stats-time").innerText = "0 ms";

      renderExpectedCriteria();
      renderSchemaTables(currentExerciseMeta.tables);
    }
  } catch (err) {
    console.error("Erro ao selecionar exercício:", err);
  }
}

function renderModuleConcepts(mod) {
  document.getElementById("module-badge").innerText = mod.badge;
  document.getElementById("module-title").innerText = mod.title;
  document.getElementById("module-summary").innerText = mod.summary;

  const grid = document.getElementById("concepts-grid");
  grid.innerHTML = "";

  mod.concepts.forEach((concept) => {
    const card = document.createElement("div");
    card.className = "concept-card";
    card.innerHTML = `
      <div class="concept-card-header">
        <h3>${concept.title}</h3>
      </div>
      <div class="concept-card-body">${formatMarkdown(concept.content)}</div>
    `;
    grid.appendChild(card);
  });
}

function renderStructuredQuestions(fields) {
  const container = document.getElementById("questions-container");
  container.innerHTML = "";
  structuredAnswers = {};
  const letters = ["A", "B", "C", "D", "E", "F"];

  fields.forEach((f, qIdx) => {
    const block = document.createElement("div");
    block.className = "question-block";
    block.id = `qblock-${f.id}`;

    let html = `
      <div class="q-header-row">
        <span class="q-item-badge">QUESTÃO ${qIdx + 1} DE ${fields.length}</span>
        <div class="question-title">${formatQuestionText(f.label)}</div>
      </div>
    `;
    html += `<div class="options-list">`;
    f.options.forEach((opt, idx) => {
      const letter = letters[idx] || String(idx + 1);
      html += `
        <label class="option-item" id="opt-${f.id}-${idx}">
          <input type="radio" name="radio-${f.id}" value="${escapeHtml(opt)}" class="option-radio" />
          <span class="opt-letter-badge">${letter}</span>
          <span class="opt-text-body">${formatQuestionText(opt)}</span>
        </label>
      `;
    });
    html += `</div>`;
    html += `<div class="question-feedback" id="feedback-${f.id}" style="display:none;"></div>`;

    block.innerHTML = html;

    // Attach listeners
    block.querySelectorAll("input[type=radio]").forEach((radio) => {
      radio.addEventListener("change", (e) => {
        structuredAnswers[f.id] = e.target.value;
        block.querySelectorAll(".option-item").forEach((it) => it.classList.remove("selected"));
        radio.closest(".option-item").classList.add("selected");
      });
    });

    container.appendChild(block);
  });
}

async function validateStructured() {
  try {
    const res = await fetch("/api/validate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        exerciseId: currentExerciseId,
        answers: structuredAnswers
      })
    });
    const data = await res.json();

    if (data.fieldResults) {
      data.fieldResults.forEach((fr) => {
        const qBlock = document.getElementById(`qblock-${fr.id}`);
        const fb = document.getElementById(`feedback-${fr.id}`);
        if (!qBlock || !fb) return;

        fb.style.display = "block";
        if (fr.correct) {
          qBlock.className = "question-block correct";
          fb.className = "question-feedback success";
          fb.innerHTML = `<strong>✔ Correto!</strong> ${escapeHtml(fr.explanation)}`;
        } else {
          qBlock.className = "question-block incorrect";
          fb.className = "question-feedback error";
          fb.innerHTML = `<strong>❌ Incorreto.</strong> Resposta esperada: <em>${escapeHtml(fr.expectedAnswer)}</em><br><br>${escapeHtml(fr.explanation)}`;
        }
      });
    }

    if (data.matched) {
      markAsSolved(currentExerciseId);
      showToast(`🎉 Item ${currentExerciseId} Concluído com Sucesso!`);
    } else {
      showToast(`Atenção: Pontuação ${data.score}. Revise os itens destacados.`);
    }
  } catch (err) {
    console.error("Erro ao validar estruturado:", err);
    showToast("Erro ao validar respostas.");
  }
}

function resetStructured() {
  if (currentExerciseMeta && currentExerciseMeta.fields) {
    renderStructuredQuestions(currentExerciseMeta.fields);
    showToast("Seleção reiniciada.");
  }
}

async function runCode() {
  const query = document.getElementById("sql-editor").value.trim();
  if (!query) {
    showToast("Escreva seu código no editor.");
    return;
  }

  document.getElementById("out-tab-result").click();
  const container = document.getElementById("result-table-container");
  container.innerHTML = `<div class="empty-state"><span class="empty-icon">⏳</span><p>Executando...</p></div>`;

  try {
    const res = await fetch("/api/execute", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ exerciseId: currentExerciseId, query })
    });
    const data = await res.json();

    document.getElementById("stats-time").innerText = `${data.elapsedMs || 0} ms`;
    document.getElementById("validation-banner").style.display = "none";

    if (!data.success) {
      container.innerHTML = `
        <div style="padding:18px; color:#f87171; background:rgba(239,68,68,0.1); border-radius:6px; font-family:var(--font-code);">
          <strong>❌ Erro de Execução:</strong><br><br>
          ${escapeHtml(data.error)}
        </div>
      `;
      document.getElementById("stats-summary").innerText = "Erro na execução";
      return;
    }

    document.getElementById("stats-summary").innerText = `${data.rowCount} resultado(s) retornado(s)`;
    renderResultTable(data.columns, data.rows);
  } catch (err) {
    console.error(err);
    showToast("Erro de comunicação com o servidor.");
  }
}

async function validateCode() {
  const query = document.getElementById("sql-editor").value.trim();
  if (!query) {
    showToast("Escreva seu código no editor para validar.");
    return;
  }

  document.getElementById("out-tab-result").click();
  const container = document.getElementById("result-table-container");
  container.innerHTML = `<div class="empty-state"><span class="empty-icon">⏳</span><p>Executando bateria de testes e validação...</p></div>`;

  try {
    const res = await fetch("/api/validate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ exerciseId: currentExerciseId, query })
    });
    const data = await res.json();

    const banner = document.getElementById("validation-banner");
    const bannerTitle = document.getElementById("banner-title");
    const bannerDesc = document.getElementById("banner-desc");
    const bannerIcon = document.getElementById("banner-icon");

    banner.style.display = "flex";

    if (data.matched) {
      banner.className = "validation-banner success";
      bannerIcon.innerText = "✔";
      bannerTitle.innerText = "Accepted! (Gabarito e Restrições 100% Corretas)";
      bannerDesc.innerText = data.diffReason || "Parabéns! Todas as validações foram atendidas.";
      markAsSolved(currentExerciseId);
      showToast(`🎉 Exercício ${currentExerciseId} Resolvido com Sucesso!`);
    } else {
      banner.className = "validation-banner error";
      bannerIcon.innerText = "⚠️";
      bannerTitle.innerText = "Divergência ou Falha de Restrição Encontrada";
      bannerDesc.innerText = data.diffReason || data.error || "A saída difere do gabarito oficial.";
    }

    if (data.testResults) {
      renderTestSuiteResults(data.testResults);
    } else if (data.execResult && data.execResult.success) {
      document.getElementById("stats-time").innerText = `${data.execResult.elapsedMs || 0} ms`;
      document.getElementById("stats-summary").innerText = `${data.execResult.rowCount} linhas retornadas`;
      renderResultTable(data.execResult.columns, data.execResult.rows);
    } else if (data.error) {
      container.innerHTML = `
        <div style="padding:18px; color:#f87171; background:rgba(239,68,68,0.1); border-radius:6px; font-family:var(--font-code);">
          <strong>❌ Erro:</strong><br><br>
          ${escapeHtml(data.error)}
        </div>
      `;
    }
  } catch (err) {
    console.error(err);
    showToast("Erro ao validar código.");
  }
}

function renderTestSuiteResults(testResults) {
  const container = document.getElementById("result-table-container");
  let html = `<div class="test-suite-list">`;
  testResults.forEach((t) => {
    html += `
      <div class="test-suite-item ${t.passed ? "pass" : "fail"}">
        <span class="test-icon">${t.passed ? "✅" : "❌"}</span>
        <div class="test-info">
          <span class="test-name">${escapeHtml(t.name)}</span>
          <span class="test-detail">${escapeHtml(t.detail)}</span>
        </div>
      </div>
    `;
  });
  html += `</div>`;
  container.innerHTML = html;
  document.getElementById("stats-summary").innerText = `${testResults.filter(t => t.passed).length} / ${testResults.length} testes aprovados`;
}

function renderExpectedCriteria() {
  const container = document.getElementById("expected-table-container");
  const title = document.getElementById("expected-info-title");

  if (currentExerciseMeta.mode === "sql_query") {
    title.innerText = "Output Sample Oficial Esperado:";
    renderResultTable(currentExerciseMeta.expectedColumns, currentExerciseMeta.expectedRows, container);
  } else if (currentExerciseMeta.mode === "sql_ddl") {
    title.innerText = "Bateria de Injeção de Falhas que seu DDL deve suportar:";
    let html = `<div class="test-suite-list">`;
    (currentExerciseMeta.ddlTests || []).forEach((tName) => {
      html += `
        <div class="test-suite-item pass">
          <span class="test-icon">🧪</span>
          <div class="test-info">
            <span class="test-name">${escapeHtml(tName)}</span>
          </div>
        </div>
      `;
    });
    html += `</div>`;
    container.innerHTML = html;
  } else if (currentExerciseMeta.mode === "sql_assertion") {
    title.innerText = "Cenários de Teste da Asserção SQL-92:";
    let html = `<div class="test-suite-list">`;
    (currentExerciseMeta.assertionTests || []).forEach((tName) => {
      html += `
        <div class="test-suite-item pass">
          <span class="test-icon">🧪</span>
          <div class="test-info">
            <span class="test-name">${escapeHtml(tName)}</span>
          </div>
        </div>
      `;
    });
    html += `</div>`;
    container.innerHTML = html;
  }
}

function renderResultTable(columns, rows, targetContainer = null) {
  const container = targetContainer || document.getElementById("result-table-container");
  if (!columns || !columns.length) {
    container.innerHTML = `<div class="empty-state"><p>Nenhum dado retornado.</p></div>`;
    return;
  }

  let html = `<table class="data-table"><thead><tr>`;
  columns.forEach((c) => {
    html += `<th>${escapeHtml(c)}</th>`;
  });
  html += `</tr></thead><tbody>`;

  rows.forEach((r) => {
    html += `<tr>`;
    r.forEach((val) => {
      html += `<td>${val === null ? "<em>NULL</em>" : escapeHtml(String(val))}</td>`;
    });
    html += `</tr>`;
  });
  html += `</tbody></table>`;
  container.innerHTML = html;
}

function renderSchemaTables(tables) {
  const container = document.getElementById("schema-tables-container");
  container.innerHTML = "";

  if (!tables || Object.keys(tables).length === 0) {
    container.innerHTML = `<div class="empty-state"><p>Nenhuma tabela persistente carregada neste exercício.</p></div>`;
    return;
  }

  for (const [tableName, tInfo] of Object.entries(tables)) {
    const block = document.createElement("div");
    block.className = "schema-table-block";

    let html = `<div class="schema-table-name">📌 Tabela: ${tableName} (${tInfo.rows.length} tuplas)</div>`;
    html += `<table class="data-table"><thead><tr>`;
    tInfo.columns.forEach((c) => {
      html += `<th>${escapeHtml(c.name)} <span style="font-weight:normal;color:#94a3b8;font-size:10px;">${c.type}${c.pk ? " (PK)" : ""}</span></th>`;
    });
    html += `</tr></thead><tbody>`;

    tInfo.rows.forEach((r) => {
      html += `<tr>`;
      r.forEach((val) => {
        html += `<td>${val === null ? "<em>NULL</em>" : escapeHtml(String(val))}</td>`;
      });
      html += `</tr>`;
    });
    html += `</tbody></table>`;

    block.innerHTML = html;
    container.appendChild(block);
  }
}

function markAsSolved(exId) {
  solvedExercises.add(exId);
  localStorage.setItem("ibd_prereq_solved", JSON.stringify([...solvedExercises]));
  updateProgressUI();

  const activeNavItem = document.getElementById(`nav-ex-${exId}`);
  if (activeNavItem) {
    const icon = activeNavItem.querySelector(".ex-status-icon");
    if (icon) icon.innerText = "✅";
  }
}

function updateProgressUI() {
  const count = solvedExercises.size;
  const total = curriculumData
    ? curriculumData.modules.reduce((acc, m) => acc + m.exercises.length, 0)
    : 48;
  const pct = Math.min(100, Math.round((count / total) * 100));
  document.getElementById("progress-text").innerText = `${count} / ${total} Concluídos`;
  document.getElementById("progress-bar-fill").style.width = `${pct}%`;
}

function showHint() {
  alert(`💡 Dica para ${currentExerciseId}:\n\nConsulte o Cheat Sheet no topo ou revise os slides de ibd-parte3 e ibd-parte4 para a sintaxe exata das restrições e consultas.`);
}

function showToast(msg) {
  const toast = document.getElementById("toast-notification");
  document.getElementById("toast-message").innerText = msg;
  toast.style.display = "flex";
  setTimeout(() => {
    toast.style.display = "none";
  }, 3500);
}

function escapeHtml(str) {
  if (typeof str !== "string") return str;
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function formatQuestionText(str) {
  if (typeof str !== "string") return "";
  let out = escapeHtml(str);
  // Highlight single-quoted identifiers/schemas like 'CARRO (placa...)' or 'R1(A, B)'
  out = out.replace(/&#039;([^&#]+?)&#039;/g, "<code class=\"inline-token\">$1</code>");
  // Highlight backtick spans if any
  out = out.replace(/`([^`]+?)`/g, "<code class=\"inline-token\">$1</code>");
  // Highlight functional dependency arrows
  out = out.replace(/\s*-&gt;\s*/g, " <strong style=\"color:#38bdf8;\">→</strong> ");
  return out;
}

function formatMarkdown(text) {
  if (!text) return "";
  let out = escapeHtml(text);

  // 1. Extract fenced code blocks ```sql ... ``` or ``` ... ```
  const codeBlocks = [];
  out = out.replace(/```(?:[a-zA-Z0-9_-]+)?\n([\s\S]*?)```/g, (_, code) => {
    const idx = codeBlocks.length;
    codeBlocks.push(`<pre class="md-code-block"><code>${code.trim()}</code></pre>`);
    return `__CODE_BLOCK_${idx}__`;
  });

  // 2. Inline bold and inline code
  out = out.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
  out = out.replace(/`([^`\n]+?)`/g, "<code>$1</code>");

  // 3. Process paragraphs & bullet/numbered lists cleanly
  const blocks = out.split(/\n\n+/);
  const renderedBlocks = blocks.map((blk) => {
    const trimmed = blk.trim();
    if (/^__CODE_BLOCK_\d+__$/.test(trimmed)) {
      return trimmed;
    }
    const lines = trimmed.split("\n");
    const isBulletList = lines.length > 1 && lines.every((l) => /^\s*-\s+/.test(l));
    if (isBulletList) {
      const items = lines
        .map((l) => `<li>${l.replace(/^\s*-\s+/, "")}</li>`)
        .join("");
      return `<ul class="md-list">${items}</ul>`;
    }
    const isNumList = lines.length > 1 && lines.every((l) => /^\s*\d+\.\s+/.test(l));
    if (isNumList) {
      const items = lines
        .map((l) => `<li>${l.replace(/^\s*\d+\.\s+/, "")}</li>`)
        .join("");
      return `<ol class="md-list">${items}</ol>`;
    }
    // Mixed block with header line + list items
    if (lines.length > 1 && lines.slice(1).some((l) => /^\s*-\s+/.test(l))) {
      let html = "";
      let inList = false;
      lines.forEach((l) => {
        if (/^\s*-\s+/.test(l)) {
          if (!inList) {
            html += `<ul class="md-list">`;
            inList = true;
          }
          html += `<li>${l.replace(/^\s*-\s+/, "")}</li>`;
        } else {
          if (inList) {
            html += `</ul>`;
            inList = false;
          }
          html += `<p class="md-para">${l}</p>`;
        }
      });
      if (inList) html += `</ul>`;
      return html;
    }
    return `<p class="md-para">${lines.join("<br>")}</p>`;
  });

  out = renderedBlocks.join("");
  codeBlocks.forEach((cb, idx) => {
    out = out.replace(`__CODE_BLOCK_${idx}__`, cb);
  });

  return out;
}

