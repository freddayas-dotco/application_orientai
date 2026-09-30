/* OrientAI v2 — logique front (espace, questionnaire, explorateur, résultats, dashboard) */
"use strict";

// ── Utilitaires ─────────────────────────────────────────────────────────────
const $ = (sel, root = document) => root.querySelector(sel);

const store = {
  get(key) {
    try { return JSON.parse(sessionStorage.getItem(key)); } catch { return null; }
  },
  set(key, value) {
    try { sessionStorage.setItem(key, JSON.stringify(value)); } catch { /* stockage indisponible */ }
  },
  remove(key) {
    try { sessionStorage.removeItem(key); } catch { /* stockage indisponible */ }
  },
};

function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, (c) => (
    { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]
  ));
}

async function api(path, body) {
  const res = await fetch(path, {
    method: body === undefined ? "GET" : "POST",
    headers: body === undefined ? {} : { "Content-Type": "application/json" },
    body: body === undefined ? undefined : JSON.stringify(body),
    credentials: "same-origin",
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const detail = Array.isArray(data.detail) ? data.detail.map((d) => d.msg).join(" ") : data.detail;
    const err = new Error(detail || `Erreur ${res.status}`);
    err.status = res.status;
    throw err;
  }
  return data;
}

function showAlert(el, message, kind = "error") {
  el.className = `alert alert-${kind}`;
  el.textContent = message;
  el.hidden = false;
}

const LETTERS = ["A", "B", "C", "D"];
const MODES = {
  eleve: { label: "Élève", icon: "🎓", public: "Collège · Lycée", classe: "Classe", classeHint: "Ex : 3e B, Terminale générale" },
  adulte: { label: "Adulte", icon: "💼", public: "Étudiant·e · Professionnel·le · Reconversion", classe: "Profession", classeHint: "Ex : Infirmière, Chargé de projet" },
};
const RESULT_KEY = "orientai_resultats";
const identiteKey = (mode) => `orientai_identite_${mode}`;
const getMode = () => (new URLSearchParams(location.search).get("mode") === "adulte" ? "adulte" : "eleve");

// ── Page espace (identité puis choix du parcours) ──────────────────────────
function initEspace() {
  const param = new URLSearchParams(window.location.search).get("mode");
  const mode = param === "adulte" ? "adulte" : "eleve";
  const cfg = MODES[mode];
  const adulte = mode === "adulte";
  console.log("[espace] mode URL =", param, "→", mode);

  document.title = `Espace ${cfg.label} · OrientAI`;
  $("#espace-icon").textContent = cfg.icon;
  $("#espace-title").textContent = `Espace ${cfg.label}`;
  $("#espace-subtitle").textContent = cfg.public;
  $("#espace-intro").textContent = adulte
    ? "Présentez-vous, puis passez le questionnaire soft skills ou explorez librement les métiers."
    : "Présente-toi, puis passe le questionnaire soft skills ou explore librement les métiers.";
  $("#classe-label").firstChild.textContent = cfg.classe + " ";
  $("#classe").placeholder = cfg.classeHint;

  const identite = store.get(identiteKey(mode));
  if (identite) {
    $("#prenom").value = identite.prenom || "";
    $("#nom").value = identite.nom || "";
    $("#classe").value = identite.classe || "";
  }

  $("#espace-form").addEventListener("submit", (ev) => {
    ev.preventDefault();
    const data = {
      prenom: $("#prenom").value.trim(),
      nom: $("#nom").value.trim(),
      classe: $("#classe").value.trim(),
    };
    if (!data.prenom || !data.nom) {
      showAlert($("#espace-error"), adulte
        ? "Indiquez votre prénom et votre nom pour continuer."
        : "Indique ton prénom et ton nom pour continuer.");
      (data.prenom ? $("#nom") : $("#prenom")).focus();
      return;
    }
    store.set(identiteKey(mode), data);
    const cible = ev.submitter && ev.submitter.value === "explorateur" ? "explorateur" : "questionnaire";
    location.href = `/${cible}?mode=${mode}`;
  });
}

// ── Page questionnaire ──────────────────────────────────────────────────────
async function initQuestionnaire() {
  const mode = getMode();
  const cfg = MODES[mode];
  const stateKey = `orientai_quiz_${mode}`;

  const introView = $("#intro");
  const quizView = $("#quiz");
  const loadingView = $("#loading");
  const errorBox = $("#quiz-error");

  $("#mode-label").textContent = cfg.label;
  $("#classe-label").firstChild.textContent = cfg.classe + " ";
  $("#classe").placeholder = cfg.classeHint;

  let questions = [];
  try {
    questions = (await api(`/api/questions?mode=${mode}`)).questions;
  } catch (e) {
    showAlert($("#intro-error"), "Impossible de charger le questionnaire. Réessayez dans un instant.");
    return;
  }

  const saved = store.get(stateKey);
  const state = saved && Array.isArray(saved.answers) && saved.answers.length === questions.length
    ? saved
    : { identite: { prenom: "", nom: "", classe: "" }, answers: Array(questions.length).fill(null), idx: 0, started: false };

  const persist = () => store.set(stateKey, state);

  // Identité déjà saisie sur la page espace : on passe directement aux questions
  const identite = store.get(identiteKey(mode));
  if (identite) {
    state.identite = { prenom: identite.prenom || "", nom: identite.nom || "", classe: identite.classe || "" };
    state.started = true;
    persist();
  }

  // Pré-remplissage du formulaire
  $("#prenom").value = state.identite.prenom;
  $("#nom").value = state.identite.nom;
  $("#classe").value = state.identite.classe;
  if (state.started) $("#resume-hint").hidden = false;

  $("#intro-form").addEventListener("submit", (ev) => {
    ev.preventDefault();
    state.identite = {
      prenom: $("#prenom").value.trim(),
      nom: $("#nom").value.trim(),
      classe: $("#classe").value.trim(),
    };
    state.started = true;
    persist();
    introView.hidden = true;
    quizView.hidden = false;
    render();
    $("#question-text").focus();
  });

  const optionsEl = $("#options");
  let advanceTimer = null;

  function render() {
    const q = questions[state.idx];
    const answered = state.answers.filter((a) => a !== null).length;
    $("#q-count").textContent = `Question ${state.idx + 1} / ${questions.length}`;
    $("#q-section").textContent = q.section;
    $("#progress-bar").style.width = `${(answered / questions.length) * 100}%`;
    $("#progress").setAttribute("aria-valuenow", String(answered));
    $("#question-text").textContent = q.q;

    optionsEl.innerHTML = q.opts.map((opt, i) => `
      <button type="button" class="option" role="radio" data-i="${i}"
              aria-checked="${state.answers[state.idx] === i}">
        <span class="option-letter">${LETTERS[i]}</span>
        <span class="option-text">${escapeHtml(opt)}</span>
      </button>`).join("");

    const isLast = state.idx === questions.length - 1;
    $("#btn-prev").disabled = state.idx === 0;
    const next = $("#btn-next");
    next.textContent = isLast ? "Voir mes résultats" : "Suivant →";
    next.disabled = isLast ? state.answers.some((a) => a === null) : state.answers[state.idx] === null;
  }

  function choose(i) {
    state.answers[state.idx] = i;
    persist();
    render();
    clearTimeout(advanceTimer);
    if (state.idx < questions.length - 1) {
      advanceTimer = setTimeout(() => go(1), 280);
    }
  }

  function go(delta) {
    clearTimeout(advanceTimer);
    const target = state.idx + delta;
    if (target < 0 || target >= questions.length) return;
    state.idx = target;
    persist();
    render();
  }

  async function finish() {
    const missing = state.answers.findIndex((a) => a === null);
    if (missing !== -1) {
      state.idx = missing;
      render();
      showAlert(errorBox, `Il reste des questions sans réponse (question ${missing + 1}).`);
      return;
    }
    errorBox.hidden = true;
    quizView.hidden = true;
    loadingView.hidden = false;
    try {
      const payload = { ...state.identite, mode, answers: state.answers };
      const result = await api("/api/resultats", payload);
      store.set(RESULT_KEY, { payload, result });
      store.remove(stateKey);
      location.href = "/resultats";
    } catch (e) {
      loadingView.hidden = true;
      quizView.hidden = false;
      showAlert(errorBox, `Le calcul a échoué : ${e.message}`);
    }
  }

  optionsEl.addEventListener("click", (ev) => {
    const btn = ev.target.closest(".option");
    if (btn) choose(Number(btn.dataset.i));
  });
  $("#btn-prev").addEventListener("click", () => go(-1));
  $("#btn-next").addEventListener("click", () => {
    if (state.idx === questions.length - 1) finish();
    else go(1);
  });

  document.addEventListener("keydown", (ev) => {
    if (quizView.hidden || ev.ctrlKey || ev.metaKey || ev.altKey) return;
    const letter = LETTERS.indexOf(ev.key.toUpperCase());
    if (letter !== -1) { ev.preventDefault(); choose(letter); }
    else if (ev.key === "ArrowLeft") go(-1);
    else if (ev.key === "ArrowRight" && state.answers[state.idx] !== null) go(1);
  });

  if (identite) {
    introView.hidden = true;
    quizView.hidden = false;
    render();
  }
}

// ── Page résultats ──────────────────────────────────────────────────────────
async function initResultats() {
  const saved = store.get(RESULT_KEY);
  if (!saved || !saved.result) {
    $("#no-result").hidden = false;
    return;
  }
  $("#content").hidden = false;

  const { payload, result } = saved;
  const prenom = payload.prenom;
  $("#title").textContent = prenom ? `${prenom}, voici ton profil` : "Voici ton profil";
  if (payload.mode === "adulte") {
    $("#title").textContent = prenom ? `${prenom}, voici votre profil` : "Voici votre profil";
  }

  // Profil soft skills
  const LEVELS = { 1: "À développer", 2: "Intermédiaire", 3: "Très développée" };
  $("#skills").innerHTML = result.profil.map((s) => `
    <div class="skill-row">
      <div class="skill-top">
        <span class="skill-name">${escapeHtml(s.label)}</span>
        <span class="skill-level">${LEVELS[s.niveau]}</span>
      </div>
      <div class="meter" role="img" aria-label="${escapeHtml(s.label)} : niveau ${s.niveau} sur 3">
        ${[1, 2, 3].map((n) => `<span class="${n <= s.niveau ? "on" : ""}"></span>`).join("")}
      </div>
    </div>`).join("");

  // Filtres
  const secteurSel = $("#filtre-secteur");
  const niveauSel = $("#filtre-niveau");
  try {
    const filtres = await api("/api/metiers/filtres");
    secteurSel.insertAdjacentHTML("beforeend",
      filtres.secteurs.map((s) => `<option>${escapeHtml(s)}</option>`).join(""));
    niveauSel.insertAdjacentHTML("beforeend",
      filtres.niveaux_etudes.map((n) => `<option>${escapeHtml(n)}</option>`).join(""));
  } catch { /* filtres indisponibles : la liste reste utilisable */ }

  // Niveau requis par métier sur les 8 soft skills (gris / orange clair / orange foncé)
  const JOB_SS_CLASS = { "Peu nécessaire": "ss-low", "Nécessaire": "ss-mid", "Absolument nécessaire": "ss-high" };
  function jobSkills(softSkills) {
    if (!softSkills) return "";
    return `
      <h4 class="job-ss-title">Soft skills requises pour ce métier</h4>
      <ul class="job-ss">
        ${Object.entries(softSkills).map(([nom, niveau]) => `
          <li><span>${escapeHtml(nom)}</span><span class="job-ss-level ${JOB_SS_CLASS[niveau] || ""}">${escapeHtml(niveau || "–")}</span></li>`).join("")}
      </ul>`;
  }

  // Résultats calculés avant l'ajout des soft skills par métier : on les recalcule
  if (result.metiers.length && !result.metiers[0].soft_skills) {
    try {
      Object.assign(result, await api("/api/resultats", payload));
      store.set(RESULT_KEY, { ...saved, result });
    } catch { /* on garde l'affichage sans le détail des soft skills */ }
  }

  const list = $("#jobs");
  function renderJobs() {
    const secteur = secteurSel.value;
    const niveau = niveauSel.value;
    const filtered = result.metiers.filter((m) =>
      (!secteur || m.secteurs.includes(secteur)) && (!niveau || m.niveau_etudes === niveau));
    const top = filtered.slice(0, 10);
    $("#jobs-count").textContent = filtered.length
      ? `${Math.min(10, filtered.length)} sur ${filtered.length} métiers correspondants`
      : "";
    $("#jobs-empty").hidden = top.length > 0;
    list.innerHTML = top.map((m, i) => {
      const secteurs = m.secteurs.slice(0, 2);
      return `
      <li class="job">
        <details>
          <summary>
            <span class="job-rank">${i + 1}</span>
            <div>
              <div class="job-title">${escapeHtml(m.metier)}</div>
              <div class="job-meta">
                ${secteurs.map((s) => `<span class="chip">${escapeHtml(s)}</span>`).join("")}
                <span class="chip chip-strong">${escapeHtml(m.niveau_etudes)}</span>
              </div>
            </div>
            <div class="job-score" aria-label="Compatibilité ${m.score} %">
              <strong>${m.score}%</strong>
              <div class="bar"><i style="width:${m.score}%"></i></div>
            </div>
            <span class="job-chevron" aria-hidden="true">▼</span>
          </summary>
          <div class="job-details">
            ${jobSkills(m.soft_skills)}
            ${m.descriptif && m.descriptif !== "nan" ? `<p>${escapeHtml(m.descriptif)}</p>` : ""}
            <dl>
              ${m.diplomes && m.diplomes !== "nan" ? `<dt>Formation</dt><dd>${escapeHtml(m.diplomes)}</dd>` : ""}
              ${m.salaire && m.salaire !== "nan" ? `<dt>Salaire</dt><dd>${escapeHtml(m.salaire)}</dd>` : ""}
              ${m.niveau && m.niveau !== "nan" ? `<dt>Poste</dt><dd>${escapeHtml(m.niveau)}</dd>` : ""}
              ${m.secteurs.length > 2 ? `<dt>Secteurs</dt><dd>${escapeHtml(m.secteurs.join(", "))}</dd>` : ""}
            </dl>
            <p style="margin:12px 0 0"><a class="metier-link" href="${ficheUrl(m.metier)}" target="_blank" rel="noopener">Fiche ONISEP ↗</a></p>
          </div>
        </details>
      </li>`;
    }).join("");
  }
  secteurSel.addEventListener("change", renderJobs);
  niveauSel.addEventListener("change", renderJobs);
  $("#reset-filtres").addEventListener("click", () => {
    secteurSel.value = "";
    niveauSel.value = "";
    renderJobs();
  });
  renderJobs();

  // Sauvegarde
  $("#save-prenom").value = payload.prenom || "";
  $("#save-nom").value = payload.nom || "";
  $("#save-classe").value = payload.classe || "";
  $("#save-classe-label").firstChild.textContent = MODES[payload.mode].classe + " ";
  const saveMsg = $("#save-msg");
  const saveBtn = $("#btn-save");
  if (saved.saved) {
    saveBtn.disabled = true;
    showAlert(saveMsg, "Résultats déjà enregistrés.", "success");
  }
  $("#save-form").addEventListener("submit", async (ev) => {
    ev.preventDefault();
    const body = {
      ...payload,
      prenom: $("#save-prenom").value.trim(),
      nom: $("#save-nom").value.trim(),
      classe: $("#save-classe").value.trim(),
    };
    if (!body.prenom || !body.nom) {
      showAlert(saveMsg, "Indique ton prénom et ton nom pour enregistrer.");
      return;
    }
    saveBtn.disabled = true;
    saveBtn.textContent = "Enregistrement…";
    try {
      const res = await api("/api/sauvegarde", body);
      store.set(RESULT_KEY, { ...saved, payload: body, saved: true });
      showAlert(saveMsg, res.google_ok
        ? "Résultats enregistrés. Ton conseiller pourra les consulter."
        : "Résultats enregistrés localement (Google Sheets indisponible).", "success");
      saveBtn.textContent = "Enregistré";
    } catch (e) {
      saveBtn.disabled = false;
      saveBtn.textContent = "Enregistrer mes résultats";
      showAlert(saveMsg, e.message);
    }
  });

  const pdfBtn = $("#btn-pdf");
  pdfBtn.addEventListener("click", async () => {
    pdfBtn.disabled = true;
    pdfBtn.textContent = "Génération du PDF…";
    try {
      // Résultats obtenus avant l'ajout de l'analyse détaillée : on les recalcule
      if (!result.analyse) {
        Object.assign(result, await api("/api/resultats", payload));
        store.set(RESULT_KEY, { ...store.get(RESULT_KEY), result });
      }
      await exportRapportPdf({
        prenom: $("#save-prenom").value.trim() || payload.prenom || "",
        nom: $("#save-nom").value.trim() || payload.nom || "",
        mode: payload.mode,
        result,
        levels: LEVELS,
      });
    } catch (e) {
      alert(`Le PDF n'a pas pu être généré : ${e.message}`);
    } finally {
      pdfBtn.disabled = false;
      pdfBtn.textContent = "Télécharger mon profil PDF";
    }
  });

  $("#btn-restart").addEventListener("click", () => {
    store.remove(RESULT_KEY);
    location.href = `/questionnaire?mode=${payload.mode}`;
  });
}

// ── Rapport PDF (jsPDF + html2canvas, généré dans le navigateur) ────────────
const PDF_LEVEL_COLORS = { 1: "#E53E3E", 2: "#DD6B20", 3: "#38A169" };
const PDF_PAGE_H = 1123;          // hauteur A4 en px à 96 dpi (largeur 794)
const PDF_BOTTOM_RESERVE = 90;    // marge basse laissée libre pour le pied de page
// Styles en ligne des cellules : html2canvas les applique de façon fiable, le texte reste dans sa cellule
const TD = "white-space:normal; word-break:break-word; overflow-wrap:break-word; word-wrap:break-word; overflow:hidden;";

// Radar Chart.js dessiné hors écran puis converti en image
function radarImage(host, profil) {
  const canvas = document.createElement("canvas");
  canvas.width = 900;
  canvas.height = 760;
  host.appendChild(canvas);
  const chart = new Chart(canvas, {
    type: "radar",
    data: {
      labels: profil.map((s) => s.label),
      datasets: [{
        data: profil.map((s) => s.niveau),
        backgroundColor: "rgba(232, 103, 74, .22)",
        borderColor: "#E8674A",
        borderWidth: 3,
        pointBackgroundColor: profil.map((s) => PDF_LEVEL_COLORS[s.niveau]),
        pointBorderColor: "#fff",
        pointRadius: 8,
      }],
    },
    options: {
      responsive: false,
      animation: false,
      devicePixelRatio: 1,
      plugins: { legend: { display: false }, tooltip: { enabled: false } },
      scales: {
        r: {
          min: 0, max: 3,
          ticks: { stepSize: 1, backdropColor: "transparent", color: "#6B7280", font: { family: "Inter", size: 16 } },
          pointLabels: { color: "#1F2328", font: { family: "Inter", size: 22, weight: "600" } },
          grid: { color: "#E5E0DA" },
          angleLines: { color: "#E5E0DA" },
        },
      },
    },
  });
  const url = canvas.toDataURL("image/png");
  chart.destroy();
  canvas.remove();
  return url;
}

async function exportRapportPdf({ prenom, nom, mode, result, levels }) {
  if (!window.jspdf || !window.html2canvas || typeof Chart === "undefined") {
    throw new Error("les modules PDF n'ont pas pu être chargés, vérifiez votre connexion");
  }
  const host = document.createElement("div");
  host.className = "pdf-host";
  document.body.appendChild(host);
  try {
    const pages = [];
    const newPage = (cls = "") => {
      const page = document.createElement("section");
      page.className = `pdf-page ${cls}`;
      host.appendChild(page);
      pages.push(page);
      return page;
    };
    const badge = (n) => `<span class="pdf-badge" style="background:${PDF_LEVEL_COLORS[n]}">${escapeHtml(levels[n])}</span>`;
    const nomComplet = `${prenom} ${nom}`.trim();
    const date = new Date().toLocaleDateString("fr-FR", { day: "numeric", month: "long", year: "numeric" });

    // Page 1 — couverture
    newPage("pdf-cover").innerHTML = `
      <div class="pdf-cover-mark">✦</div>
      <h1>OrientAI — Mon profil soft skills</h1>
      <p class="pdf-cover-name">${escapeHtml(nomComplet || "Profil anonyme")}</p>
      <p class="pdf-cover-date">${escapeHtml(date)}</p>
      <p class="pdf-cover-meta">OrientAI v2 · ${mode === "adulte" ? "Parcours adulte" : "Parcours élève"} · Questionnaire de 48 questions</p>`;

    // Page 2 — profil en un coup d'œil
    const radar = radarImage(host, result.profil);
    newPage().innerHTML = `
      <h2>1. Votre profil en un coup d'œil</h2>
      <table class="pdf-table">
        <thead><tr><th>Soft skill</th><th class="pdf-right">Niveau</th></tr></thead>
        <tbody>${result.profil.map((s, i) => `
          <tr><td style="${TD}">${escapeHtml(result.analyse[i].nom)}</td><td class="pdf-right" style="${TD}">${badge(s.niveau)}</td></tr>`).join("")}
        </tbody>
      </table>
      <div class="pdf-radar"><img alt="" src="${radar}"></div>`;

    // Page 3 — top 15 métiers
    newPage().innerHTML = `
      <h2>2. Métiers recommandés</h2>
      <p class="pdf-muted">Les 15 métiers dont les exigences en soft skills sont les plus proches de votre profil.</p>
      <table class="pdf-table">
        <colgroup><col style="width:8%"><col style="width:45%"><col style="width:12%"><col style="width:35%"></colgroup>
        <thead><tr><th>Rang</th><th>Métier</th><th>Score</th><th>Secteur</th></tr></thead>
        <tbody>${result.metiers.slice(0, 15).map((m, i) => {
          const secteur = m.secteurs.join(", ");
          const secteurCourt = secteur.length > 40 ? secteur.substring(0, 40) + '...' : secteur;
          return `
          <tr>
            <td class="pdf-rank" style="${TD}">${i + 1}</td>
            <td style="${TD}"><strong>${escapeHtml(m.metier)}</strong></td>
            <td class="pdf-score" style="${TD}">${m.score}%</td>
            <td style="${TD}" title="${escapeHtml(secteur)}">${escapeHtml(secteurCourt)}</td>
          </tr>`;
        }).join("")}
        </tbody>
      </table>`;

    // Pages 4+ — analyse détaillée, nouvelle page dès qu'un bloc déborde
    let page = newPage();
    page.innerHTML = `<h2>3. Analyse détaillée de vos soft skills</h2>`;
    result.analyse.forEach((skill, i) => {
      const niveau = result.profil[i].niveau;
      const block = document.createElement("div");
      block.className = "pdf-skill";
      block.innerHTML = `
        <div class="pdf-skill-head" style="background:${PDF_LEVEL_COLORS[niveau]}">
          <span>${escapeHtml(skill.nom)}</span><span>${escapeHtml(levels[niveau])}</span>
        </div>
        <table class="pdf-table">
          <colgroup><col width="35%" style="width:35%"><col width="65%" style="width:65%"></colgroup>
          <thead><tr><th>Sous-compétence</th><th>Ce que vos réponses révèlent</th></tr></thead>
          <tbody>${skill.items.map((it) => `
            <tr><td style="${TD} width:35%; max-width:0;"><strong>${escapeHtml(it.sous_competence)}</strong></td><td style="${TD} width:65%; max-width:0;">${escapeHtml(it.texte)}</td></tr>`).join("")}
          </tbody>
        </table>`;
      page.appendChild(block);
      if (block.offsetTop + block.offsetHeight > PDF_PAGE_H - PDF_BOTTOM_RESERVE && page.children.length > 1) {
        page = newPage();
        page.appendChild(block);
      }
    });

    await Promise.all([...host.querySelectorAll("img")].map((img) => img.decode().catch(() => {})));

    const pdf = new window.jspdf.jsPDF({ unit: "mm", format: "a4" });
    for (const [i, el] of pages.entries()) {
      const canvas = await window.html2canvas(el, {
        scale: 2,
        backgroundColor: "#ffffff",
        // Le conteneur est hors écran : on le ramène dans le cadre sur la copie capturée
        onclone: (doc) => { doc.querySelector(".pdf-host").style.left = "0"; },
      });
      if (i > 0) pdf.addPage();
      pdf.addImage(canvas.toDataURL("image/jpeg", 0.92), "JPEG", 0, 0, 210, 297);
      pdf.setFont("helvetica", "normal");
      pdf.setFontSize(8);
      pdf.setTextColor(107, 114, 128);
      pdf.text("Données issues de l'ONISEP · Rapport généré par OrientAI v2", 105, 289, { align: "center" });
      pdf.text(`${i + 1} / ${pages.length}`, 195, 289, { align: "right" });
    }

    const slug = `${prenom}-${nom}`.normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[^A-Za-z0-9]+/g, "-").replace(/^-|-$/g, "");
    pdf.save(`rapport-orientai${slug ? `-${slug}` : ""}.pdf`);
  } finally {
    host.remove();
  }
}

// ── Page explorateur de métiers ─────────────────────────────────────────────
const PAGE_SIZE = 60;
const ficheUrl = (metier) => `https://www.onisep.fr/recherche?context=metier&text=${encodeURIComponent(metier)}`;
const CATALOGUE_MAX = 2000;   // limite serveur : couvre tout le catalogue

// Centres d'intérêt → valeurs de la colonne « Domaine » du CSV métiers
const CENTRES_INTERET = {
  "Communiquer / Informer": ["Communication", "Marketing", "Traduction", "Accueil et service client"],
  "Aider / Accompagner": ["Médical", "Relation sociale", "Services à la personne", "Soins esthétiques et beauté", "Recrutement et mobilité"],
  "Concevoir / Innover": ["Ingénierie et conception technique", "Développement et ingénierie informatique", "Conception graphique et esthétique"],
  "Créer / Fabriquer": ["Production et fabrication", "Conception artistique", "Cuisine et gastronomie"],
  "Organiser / Gérer": ["Gestion de projet", "Administratif", "Logistique", "Transport", "Stratégie", "Finance", "Comptabilité"],
  "Analyser / Rechercher": ["Étude et expertise", "Scientifique", "Audit et contrôle de gestion", "Qualité - conformité", "Conseil - consulting"],
  "Enseigner / Former": ["Formation - coaching", "Activité sportive"],
  "Vendre / Négocier": ["Commercial", "Achats et approvisionnement"],
  "Protéger / Sécuriser": ["Sécurité", "Juridique"],
  "Construire / Réparer": ["Installation et/ou maintenance", "Entretien et nettoyage"],
};

async function initExplorateur() {
  const params = new URLSearchParams(location.search);
  const mode = params.get("mode");
  if (MODES[mode]) {
    $("#back-link").href = `/espace?mode=${mode}`;
    $("#back-link").textContent = `Espace ${MODES[mode].label}`;
    const identite = store.get(identiteKey(mode));
    if (identite && identite.prenom) {
      $("#title").textContent = mode === "adulte"
        ? `${identite.prenom}, explorez les métiers`
        : `${identite.prenom}, explore les métiers`;
    }
  }

  const qInput = $("#q");
  const secteurSel = $("#filtre-secteur");
  const niveauSel = $("#filtre-niveau");
  const interetSel = $("#filtre-interet");
  const resultsEl = $("#results");
  const moreBtn = $("#btn-more");
  const errorBox = $("#search-error");

  try {
    const filtres = await api("/api/metiers/filtres");
    secteurSel.insertAdjacentHTML("beforeend",
      filtres.secteurs.map((s) => `<option>${escapeHtml(s)}</option>`).join(""));
    niveauSel.insertAdjacentHTML("beforeend",
      filtres.niveaux_etudes.map((n) => `<option>${escapeHtml(n)}</option>`).join(""));
  } catch { /* filtres indisponibles : la recherche texte reste utilisable */ }

  // Recherche restaurée depuis l'URL (retour arrière, lien partagé)
  qInput.value = params.get("q") || "";
  secteurSel.value = params.get("secteur") || "";
  niveauSel.value = params.get("niveau") || "";
  interetSel.value = CENTRES_INTERET[params.get("interet")] ? params.get("interet") : "";

  let limit = PAGE_SIZE;
  let controller = null;
  let debounce = null;

  function card(m) {
    return `
      <article class="card metier-card">
        <h3 class="job-title">${escapeHtml(m.metier)}</h3>
        <div class="job-meta">
          ${m.secteurs.slice(0, 2).map((s) => `<span class="chip" title="${escapeHtml(s)}">${escapeHtml(s)}</span>`).join("")}
          <span class="chip chip-strong">${escapeHtml(m.niveau_etudes)}</span>
        </div>
        ${m.descriptif ? `<p class="metier-desc">${escapeHtml(m.descriptif)}</p>` : ""}
        <div class="metier-foot">
          <span class="muted">${escapeHtml(m.salaire)}</span>
          <a class="metier-link" href="${ficheUrl(m.metier)}" target="_blank" rel="noopener">Fiche ONISEP ↗</a>
        </div>
      </article>`;
  }

  async function search() {
    const query = { q: qInput.value.trim(), secteur: secteurSel.value, niveau: niveauSel.value };
    const interet = interetSel.value;
    const url = new URL(location.href);
    Object.entries({ ...query, interet }).forEach(([k, v]) => (v ? url.searchParams.set(k, v) : url.searchParams.delete(k)));
    history.replaceState(null, "", url);

    // Annule la requête précédente pour éviter qu'une réponse lente écrase la plus récente
    if (controller) controller.abort();
    controller = new AbortController();
    let data;
    try {
      // Centre d'intérêt filtré côté client : on récupère alors tous les résultats du serveur
      const serverLimit = interet ? CATALOGUE_MAX : limit;
      const res = await fetch(`/api/metiers/search?${new URLSearchParams({ ...query, limit: serverLimit })}`, { signal: controller.signal });
      if (!res.ok) throw new Error(`Erreur ${res.status}`);
      data = await res.json();
    } catch (e) {
      if (e.name === "AbortError") return;
      showAlert(errorBox, `Recherche impossible : ${e.message}`);
      return;
    }
    errorBox.hidden = true;
    if (interet) {
      const domaines = CENTRES_INTERET[interet];
      const filtres = data.metiers.filter((m) => domaines.includes(m.domaine));
      data = { total: filtres.length, metiers: filtres.slice(0, limit) };
    }
    resultsEl.innerHTML = data.metiers.map(card).join("");
    $("#results-count").textContent = data.total
      ? `${data.total} métier${data.total > 1 ? "s" : ""}${data.total > data.metiers.length ? ` · ${data.metiers.length} affichés` : ""}`
      : "";
    $("#results-empty").hidden = data.total > 0;
    moreBtn.hidden = data.total <= data.metiers.length;
  }

  const relancer = () => { limit = PAGE_SIZE; search(); };
  qInput.addEventListener("input", () => { clearTimeout(debounce); debounce = setTimeout(relancer, 200); });
  secteurSel.addEventListener("change", relancer);
  niveauSel.addEventListener("change", relancer);
  interetSel.addEventListener("change", relancer);
  moreBtn.addEventListener("click", () => { limit += PAGE_SIZE; search(); });
  $("#reset-filtres").addEventListener("click", () => {
    qInput.value = "";
    secteurSel.value = "";
    niveauSel.value = "";
    interetSel.value = "";
    relancer();
    qInput.focus();
  });
  search();
}

// ── Page dashboard ──────────────────────────────────────────────────────────
const CHART_COLORS = {
  single: "#E8674A",
  grid: "#ECE7E1",
  ink: "#6B7280",
};

const GAUGE_COLORS = { low: "#E53E3E", mid: "#DD6B20", high: "#38A169" };
const gaugeColor = (avg) => (avg < 1.5 ? GAUGE_COLORS.low : avg > 2.5 ? GAUGE_COLORS.high : GAUGE_COLORS.mid);

async function initDashboard() {
  const loginView = $("#login");
  const dashView = $("#dash");
  const charts = {};
  let data = null;

  async function load() {
    try {
      data = await api("/api/dashboard/data");
      console.log("[dashboard] données reçues :", data.rows.length, "lignes", data);
    } catch (e) {
      if (e.status === 401) {
        loginView.hidden = false;
        dashView.hidden = true;
        $("#password").focus();
        return;
      }
      loginView.hidden = true;
      dashView.hidden = false;
      showAlert($("#dash-error"), `Chargement impossible : ${e.message}`);
      return;
    }
    loginView.hidden = true;
    dashView.hidden = false;
    $("#btn-logout").hidden = false;
    setupFilters();
    render();
  }

  $("#login-form").addEventListener("submit", async (ev) => {
    ev.preventDefault();
    const btn = $("#login-btn");
    btn.disabled = true;
    try {
      await api("/dashboard/login", { password: $("#password").value });
      $("#password").value = "";
      $("#login-error").hidden = true;
      await load();
    } catch (e) {
      showAlert($("#login-error"), e.status === 401 ? "Mot de passe incorrect." : e.message);
    } finally {
      btn.disabled = false;
    }
  });

  $("#btn-logout").addEventListener("click", async () => {
    await api("/dashboard/logout", {}).catch(() => {});
    location.reload();
  });

  const isEleve = (mode) => ["lycee", "eleve", "élève"].includes(String(mode || "").toLowerCase());

  function setupFilters() {
    const classes = [...new Set(data.rows.map((r) => r.classe).filter(Boolean))].sort((a, b) => String(a).localeCompare(String(b), "fr"));
    $("#f-classe").innerHTML = `<option value="">Toutes les classes</option>` +
      classes.map((c) => `<option>${escapeHtml(c)}</option>`).join("");
    ["#f-search", "#f-classe", "#f-mode"].forEach((sel) => $(sel).addEventListener("input", render));
  }

  function filteredRows() {
    const q = $("#f-search").value.trim().toLowerCase();
    const classe = $("#f-classe").value;
    const mode = $("#f-mode").value;
    return data.rows.filter((r) =>
      (!classe || String(r.classe) === classe) &&
      (!mode || (mode === "eleve" ? isEleve(r.mode) : !isEleve(r.mode))) &&
      (!q || `${r.prenom} ${r.nom} ${r.classe} ${r.top1_metier}`.toLowerCase().includes(q)));
  }

  function render() {
    const rows = filteredRows();

    // KPIs
    $("#kpi-total").textContent = rows.length;
    $("#kpi-eleves").textContent = rows.filter((r) => isEleve(r.mode)).length;
    $("#kpi-adultes").textContent = rows.filter((r) => !isEleve(r.mode)).length;
    $("#kpi-classes").textContent = new Set(rows.map((r) => r.classe).filter(Boolean)).size;

    renderSkillsGauges(rows);
    renderJobsChart(rows);
    renderTable(rows);
    $("#dash-empty").hidden = rows.length > 0;
  }

  function baseOptions() {
    return {
      indexAxis: "y",
      responsive: true,
      maintainAspectRatio: false,
      animation: { duration: 250 },
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: "#1F2328", padding: 10, cornerRadius: 8,
          titleFont: { family: "Inter", weight: "600" }, bodyFont: { family: "Inter" },
        },
      },
      scales: {
        x: { grid: { color: CHART_COLORS.grid }, border: { display: false }, ticks: { color: CHART_COLORS.ink, font: { family: "Inter", size: 11 } } },
        y: { grid: { display: false }, border: { display: false }, ticks: { color: "#1F2328", font: { family: "Inter", size: 12 } } },
      },
    };
  }

  function renderSkillsGauges(rows) {
    const box = $("#skills-gauges");
    if (!box) { console.error("[dashboard] #skills-gauges introuvable dans la page"); return; }
    console.log("[dashboard] jauges :", rows.length, "profils, clés", data.ss_keys, "1re ligne", rows[0]);
    box.innerHTML = data.ss_keys.map((k, i) => {
      const vals = rows.map((r) => Number(r[k])).filter((v) => v >= 1 && v <= 3);
      const label = escapeHtml(data.ss_labels[i]);
      if (!vals.length) {
        return `<li class="gauge empty"><span class="gauge-name">${label}</span><span class="gauge-track"></span><span class="gauge-value">–</span></li>`;
      }
      const avg = vals.reduce((sum, v) => sum + v, 0) / vals.length;
      const pct = Math.round(((avg - 1) / 2) * 100);   // échelle 1 → 3
      return `<li class="gauge" title="${label} : ${avg.toFixed(2)} / 3">
        <span class="gauge-name">${label}</span>
        <span class="gauge-track" role="meter" aria-label="${label}" aria-valuemin="1" aria-valuemax="3" aria-valuenow="${avg.toFixed(1)}"><span class="gauge-fill" data-avg="${avg}" style="width:${Math.max(pct, 3)}%"></span></span>
        <span class="gauge-value">${avg.toFixed(1)}</span>
      </li>`;
    }).join("");
    box.querySelectorAll(".gauge-fill").forEach((bar) => {
      bar.style.backgroundColor = gaugeColor(Number(bar.dataset.avg));
    });
  }

  function renderJobsChart(rows) {
    const counts = new Map();
    rows.forEach((r) => [1, 2, 3].forEach((i) => {
      const m = r[`top${i}_metier`];
      if (m) counts.set(m, (counts.get(m) || 0) + 1);
    }));
    const top = [...counts.entries()].sort((a, b) => b[1] - a[1]).slice(0, 10);
    const maxLen = document.getElementById("chart-jobs").parentElement.clientWidth < 420 ? 20 : 32;
    const opts = baseOptions();
    opts.plugins.tooltip.callbacks = { title: (items) => top[items[0].dataIndex][0] };
    opts.scales.x.ticks.precision = 0;
    opts.plugins.tooltip.callbacks.label = (c) => ` ${c.raw} profil${c.raw > 1 ? "s" : ""}`;
    draw("jobs", "chart-jobs", {
      type: "bar",
      data: {
        labels: top.map(([m]) => (m.length > maxLen ? `${m.slice(0, maxLen - 1)}…` : m)),
        datasets: [{
          data: top.map(([, n]) => n),
          backgroundColor: CHART_COLORS.single,
          borderRadius: { topRight: 4, bottomRight: 4 },
          borderSkipped: false,
          barThickness: 18,
        }],
      },
      options: opts,
    });
  }

  function draw(key, canvasId, config) {
    if (typeof Chart === "undefined") return;
    if (charts[key]) charts[key].destroy();
    charts[key] = new Chart(document.getElementById(canvasId), config);
  }

  function renderTable(rows) {
    const LEVEL_SHORT = { 1: "1", 2: "2", 3: "3" };
    $("#table-body").innerHTML = rows.slice().reverse().map((r) => `
      <tr>
        <td>${escapeHtml(r.date)}</td>
        <td>${escapeHtml(`${r.prenom ?? ""} ${r.nom ?? ""}`.trim())}</td>
        <td>${escapeHtml(r.classe)}</td>
        <td>${isEleve(r.mode) ? "Élève" : "Adulte"}</td>
        <td>${escapeHtml(r.top1_metier)}</td>
        <td class="num">${r.top1_score != null && r.top1_score !== "" ? `${escapeHtml(r.top1_score)} %` : ""}</td>
        ${data.ss_keys.map((k) => `<td class="num">${r[k] != null ? LEVEL_SHORT[r[k]] ?? "" : ""}</td>`).join("")}
      </tr>`).join("");
  }

  load();
}

// ── Aiguillage ──────────────────────────────────────────────────────────────
({
  espace: initEspace,
  questionnaire: initQuestionnaire,
  explorateur: initExplorateur,
  resultats: initResultats,
  dashboard: initDashboard,
}[document.body.dataset.page] || (() => {}))();
