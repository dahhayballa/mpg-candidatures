/* ══════════════════════════════════════════
   I18N & GLOBALS
   ══════════════════════════════════════════ */
const TRANSLATIONS = {
  fr: {
    subtitle: "Candidatures 2025–2026",
    nav_section: "Navigation",
    nav_dashboard: "Tableau de bord",
    nav_candidats: "Candidats",
    nav_evaluation: "Évaluation",
    nav_statistiques: "Statistiques",
    deadline_label: "Date limite :",
    btn_export: "⬇ Exporter CSV",
    stat_total: "Candidats recevables", stat_total_sub: "dans les délais",
    stat_hd: "Hors délai", stat_hd_sub: "après le 31/03 14h",
    stat_complet: "Dossiers complets", stat_complet_sub: "4 pièces présentes",
    stat_partiel: "Partiels", stat_partiel_sub: "pièces manquantes",
    stat_eval: "Évaluations", stat_eval_sub: "note saisie",
    stat_reste: "À évaluer", stat_reste_sub: "en attente",
    ring_eval: "Taux d'évaluation", ring_complet: "Dossiers complets", ring_excellent: "Candidats excellents",
    specialty_repartition: "Répartition par filière",
    mentions_results: "Résultats de la notation",
    mention_excellent: "Excellent (prioritaire)", mention_bon: "Bon candidat",
    mention_moyen: "Moyen (à discuter)", mention_non_retenu: "Non retenu",
    search_ph: "Rechercher par nom, e-mail, filière…",
    all_statuts: "Tous les statuts", all_filieres: "Toutes les filières",
    all_mentions: "Toutes les mentions", all_eval: "Tous",
    a_evaluer: "À évaluer", evalues: "Déjà évalués",
    complet: "✅ Complet", partiel: "🟡 Partiel", incomplet: "❌ Incomplet", vide: "⚪ Vide",
    col_nom: "Nom", col_filiere: "Filière", col_pieces: "Pièces",
    col_dossier: "Dossier", col_note: "Note /100", col_mention: "Mention", col_date: "Date",
    eval_select_title: "Sélectionner un candidat",
    eval_select_sub: "Allez dans la page Candidats et cliquez sur une ligne pour commencer l'évaluation.",
    eval_go_candidats: "Voir les candidats →",
    scoring_grid: "Grille d'évaluation — /100 points",
    crit_niveau: "Niveau d'études", crit_niveau_desc: "Correspondance avec la filière, niveau minimum requis, pertinence",
    crit_exp: "Expérience", crit_exp_desc: "Stages, expériences professionnelles ou pratiques liées au domaine",
    crit_motiv: "Lettre de motivation", crit_motiv_desc: "Clarté, coherence, motivation réelle, projet professionnel",
    crit_adeq: "Adéquation au profil", crit_adeq_desc: "Compatibilité avec la formation, aptitudes techniques, logique",
    crit_dossier: "Qualité du dossier", crit_dossier_desc: "CV (2.5) + Lettre motivation (2.5) + CIN (2.5) + Diplômes (2.5)",
    crit_dispo: "Disponibilité", crit_dispo_desc: "Capacité à suivre toute la formation (3 à 6 mois, temps plein)",
    total_note: "Note totale", total_note_sub: "sur 100 points",
    note_ph: "Observations de l'évaluateur (facultatif)…",
    btn_annuler: "Annuler", btn_save: "💾 Enregistrer la note",
    toast_saved: "✅ Note enregistrée avec succès !",
    topbar_sub_dashboard: "Vue d'ensemble des candidatures",
    topbar_sub_candidats: "Liste et filtres",
    topbar_sub_evaluation: "Grille de notation",
    topbar_sub_statistiques: "Analyses détaillées",
    info_filiere: "Filière demandée", info_emails: "E-mails envoyés",
    info_first: "Première candidature", info_last: "Dernière candidature",
    docs_cv: "CV", docs_lettre: "Lettre de motivation", docs_cin: "Pièce d'identité", docs_diplome: "Diplômes",
    stats_loading: "Chargement…",
    badge_complet: "✅ Complet", badge_partiel: "🟡 Partiel", badge_incomplet: "❌ Incomplet", badge_vide: "⚪ Vide",
    badge_excellent: "🏆 Excellent", badge_bon: "✅ Bon", badge_moyen: "🟡 Moyen", badge_non_retenu: "❌ Non retenu",
    badge_pending: "À évaluer",
    stat_page_title: "Statistiques détaillées",
    audit_trail: "Journal d'activité récent",
    verify_required: "⚠️ À vérifier",
    all_verify: "Tous",
    needs_verify: "تطلب تحقق يدوي"
  },
  ar: {
    subtitle: "الترشحات 2025–2026",
    nav_section: "القائمة",
    nav_dashboard: "لوحة التحكم",
    nav_candidats: "المترشحون",
    nav_evaluation: "التقييم",
    nav_statistiques: "الإحصائيات",
    deadline_label: "الموعد النهائي :",
    btn_export: "⬇ تصدير CSV",
    stat_total: "المترشحون المقبولون", stat_total_sub: "في الوقت المحدد",
    stat_hd: "خارج الموعد", stat_hd_sub: "بعد 31/03 الساعة 14:00",
    stat_complet: "ملفات مكتملة", stat_complet_sub: "4 وثائق موجودة",
    stat_partiel: "ملفات جزئية", stat_partiel_sub: "وثائق ناقصة",
    stat_eval: "تقييمات", stat_eval_sub: "تم إدخال الدرجة",
    stat_reste: "لم يُقيَّموا", stat_reste_sub: "في الانتظار",
    ring_eval: "نسبة التقييم", ring_complet: "الملفات المكتملة", ring_excellent: "المترشحون الممتازون",
    specialty_repartition: "التوزيع حسب التخصص",
    mentions_results: "نتائج التقييم",
    mention_excellent: "ممتاز (أولوية)", mention_bon: "جيد",
    mention_moyen: "متوسط (للمناقشة)", mention_non_retenu: "مرفوض",
    search_ph: "ابحث بالاسم أو البريد أو التخصص…",
    all_statuts: "جميع الحالات", all_filieres: "جميع التخصصات",
    all_mentions: "جميع التقديرات", all_eval: "الكل",
    a_evaluer: "لم يُقيَّم بعد", evalues: "تم تقييمهم",
    complet: "✅ مكتمل", partiel: "🟡 جزئي", incomplet: "❌ ناقص", vide: "⚪ فارغ",
    col_nom: "الاسم", col_filiere: "التخصص", col_pieces: "الوثائق",
    col_dossier: "الملف", col_note: "الدرجة /100", col_mention: "التقدير", col_date: "التاريخ",
    eval_select_title: "اختر مترشحاً",
    eval_select_sub: "انتقل إلى صفحة المترشحين وانقر على أي صف لبدء التقييم.",
    eval_go_candidats: "→ عرض المترشحين",
    scoring_grid: "شبكة التقييم — /100 نقطة",
    crit_niveau: "المستوى الدراسي", crit_niveau_desc: "التوافق مع التخصص المختار، الحد الأدنى المطلوب",
    crit_exp: "الخبرة", crit_exp_desc: "تدريبات، خبرات مهنية أو تطبيقية في المجال",
    crit_motiv: "رسالة التحفيز", crit_motiv_desc: "الوضوح، التماسك، الدافعية الحقيقية، المشروع المهني",
    crit_adeq: "التوافق مع المتطلبات", crit_adeq_desc: "التوافق مع التكوين، الكفاءات التقنية، المنطق",
    crit_dossier: "جودة الملف", crit_dossier_desc: "السيرة (2.5) + الرسالة (2.5) + بطاقة التعريف (2.5) + الشهادات (2.5)",
    crit_dispo: "التفرغ", crit_dispo_desc: "القدرة على متابعة التكوين بالكامل (3 إلى 6 أشهر)",
    total_note: "الدرجة الإجمالية", total_note_sub: "من 100 نقطة",
    note_ph: "ملاحظات المقيِّم (اختياري)…",
    btn_annuler: "إلغاء", btn_save: "💾 حفظ الدرجة",
    toast_saved: "✅ تم حفظ الدرجة بنجاح!",
    topbar_sub_dashboard: "نظرة عامة على الترشحات",
    topbar_sub_candidats: "القائمة والفلاتر",
    topbar_sub_evaluation: "شبكة التنقيط",
    topbar_sub_statistiques: "تحليلات مفصلة",
    info_filiere: "التخصص المطلوب", info_emails: "عدد الرسائل",
    info_first: "أول ترشح", info_last: "آخر ترشح",
    docs_cv: "السيرة الذاتية", docs_lettre: "رسالة التحفيز", docs_cin: "بطاقة التعريف", docs_diplome: "الشهادات",
    stats_loading: "جارٍ التحميل…",
    badge_complet: "✅ مكتمل", badge_partiel: "🟡 جزئي", badge_incomplet: "❌ ناقص", badge_vide: "⚪ فارغ",
    badge_excellent: "🏆 ممتاز", badge_bon: "✅ جيد", badge_moyen: "🟡 متوسط", badge_non_retenu: "❌ مرفوض",
    badge_pending: "لم يُقيَّم",
    stat_page_title: "إحصائيات مفصلة",
    audit_trail: "سجل النشاط الأخير",
    verify_required: "⚠️ يتطلب تحقق",
    all_verify: "الكل",
    needs_verify: "تطلب تحقق يدوي"
  }
};

let lang = 'fr';
const t = k => TRANSLATIONS[lang][k] || TRANSLATIONS.fr[k] || k;

function setLang(l) {
  lang = l;
  const h = document.documentElement;
  h.setAttribute('lang', l);
  h.setAttribute('dir', l === 'ar' ? 'rtl' : 'ltr');
  document.getElementById('lang-fr').classList.toggle('active', l === 'fr');
  document.getElementById('lang-ar').classList.toggle('active', l === 'ar');
  applyTranslations();
  loadTable();
}

function applyTranslations() {
  document.querySelectorAll('[data-i18n]').forEach(el => el.textContent = t(el.getAttribute('data-i18n')));
  document.querySelectorAll('[data-i18n-ph]').forEach(el => el.placeholder = t(el.getAttribute('data-i18n-ph')));
  updateTopbar();
}

/* ══════════════════════════════════════════
   NAVIGATION
   ══════════════════════════════════════════ */
let currentPage = 'dashboard';
const pageMeta = {
  dashboard: { title: 'nav_dashboard', sub: 'topbar_sub_dashboard' },
  candidats: { title: 'nav_candidats', sub: 'topbar_sub_candidats' },
  evaluation: { title: 'nav_evaluation', sub: 'topbar_sub_evaluation' },
  verification: { title: 'nav_verification', sub: '' },
  quotas: { title: 'nav_quotas', sub: '' },
  statistiques: { title: 'nav_statistiques', sub: 'topbar_sub_statistiques' },
};

function gotoPage(p) {
  currentPage = p;
  document.querySelectorAll('.page').forEach(el => el.classList.remove('active'));
  document.getElementById(`page-${p}`).classList.add('active');
  document.querySelectorAll('.sb-nav a').forEach(a => a.classList.remove('active'));
  document.getElementById(`nav-${p}`).classList.add('active');
  updateTopbar();
  if (p === 'candidats' && !tableLoaded) loadTable();
  if (p === 'verification') loadVerifyTable();
  if (p === 'quotas') loadQuotasTable();
  if (p === 'dashboard') loadStats();
  if (p === 'statistiques') loadStatsPage();
}

function updateTopbar() {
  const m = pageMeta[currentPage];
  if (!m) return;
  const titleEl = document.getElementById('topbar-title');
  const subEl = document.getElementById('topbar-sub');
  if (titleEl) titleEl.textContent = t(m.title);
  if (subEl) subEl.textContent = t(m.sub);
}

/* ══════════════════════════════════════════
   CHARTS & STATS
   ══════════════════════════════════════════ */
let charts = {};

function initCharts(data) {
  const ctxTrend = document.getElementById('trendChart')?.getContext('2d');
  const ctxSpec = document.getElementById('specialtyChart')?.getContext('2d');
  const ctxMent = document.getElementById('mentionsChart')?.getContext('2d');

  // Destroy existing to avoid overlap
  Object.values(charts).forEach(c => c && c.destroy());

  // 1. Trend Chart (Area)
  if (ctxTrend) {
    const trendLabels = data.daily_stats.map(s => s.day);
    const trendData = data.daily_stats.map(s => s.cnt);
    const gradient = ctxTrend.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, 'rgba(99, 102, 241, 0.4)');
    gradient.addColorStop(1, 'rgba(99, 102, 241, 0)');

    charts.trend = new Chart(ctxTrend, {
      type: 'line',
      data: {
        labels: trendLabels,
        datasets: [{
          label: 'Candidatures',
          data: trendData,
          fill: true,
          backgroundColor: gradient,
          borderColor: '#6366F1',
          borderWidth: 3,
          tension: 0.4,
          pointRadius: 4,
          pointBackgroundColor: '#6366F1'
        }]
      },
      options: {
        responsive: true, maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          x: { grid: { display: false }, ticks: { font: { size: 10 } } },
          y: { beginAtZero: true, grid: { color: 'rgba(0,0,0,0.05)' } }
        }
      }
    });
  }

  // 2. Specialty (Doughnut)
  if (ctxSpec) {
    charts.spec = new Chart(ctxSpec, {
      type: 'doughnut',
      data: {
        labels: data.by_specialty.map(s => s.specialty || 'Non spécifié'),
        datasets: [{
          data: data.by_specialty.map(s => s.cnt),
          backgroundColor: ['#6366F1', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#3B82F6', '#64748B'],
          borderWidth: 4,
          borderColor: '#ffffff'
        }]
      },
      options: {
        responsive: true, maintainAspectRatio: false,
        plugins: {
          legend: { position: lang === 'ar' ? 'left' : 'right', labels: { boxWidth: 12, font: { size: 11, weight: '600' } } }
        },
        cutout: '65%'
      }
    });
  }

  // 3. Mentions
  if (ctxMent) {
    charts.ment = new Chart(ctxMent, {
      type: 'bar',
      data: {
        labels: [t('mention_excellent'), t('mention_bon'), t('mention_moyen'), t('mention_non_retenu')],
        datasets: [{
          data: [data.excellent, data.bon, data.moyen, data.non_retenu],
          backgroundColor: ['#10B981', '#6366F1', '#F59E0B', '#EF4444'],
          barThickness: 24,
          borderRadius: 12
        }]
      },
      options: {
        responsive: true, maintainAspectRatio: false,
        indexAxis: 'y',
        plugins: { legend: { display: false } },
        scales: {
          x: { display: false },
          y: { grid: { display: false }, ticks: { font: { weight: '700' } } }
        }
      }
    });
  }
}

async function loadStats() {
  const r = await fetch('/api/stats');
  const d = await r.json();

  setText('s-total', fmt(d.total));
  setText('s-complet', fmt(d.complet));

  // Distinguish evaluations
  const totalEval = (d.eval_ia || 0) + (d.eval_human || 0);
  setText('s-eval', fmt(totalEval));
  const evalSub = document.getElementById('s-eval-sub');
  if (evalSub) {
    evalSub.innerHTML = `<i data-lucide="cpu" style="width:10px;height:10px;"></i> ${fmt(d.eval_ia || 0)} IA • <i data-lucide="user" style="width:10px;height:10px;"></i> ${fmt(d.eval_human || 0)} Manuel`;
  }

  setText('s-verify', d.verify || 0);
  setText('nb-count', fmt(d.total || 0));

  const nvBadge = document.getElementById('nb-verify');
  if (nvBadge) {
    if (d.verify > 0) { nvBadge.style.display = 'inline-flex'; nvBadge.textContent = d.verify; }
    else { nvBadge.style.display = 'none'; }
  }

  initCharts(d);
  renderAudit(d.audit);
  startCountdown('2026-03-31 14:00');

  setTimeout(() => { if (window.lucide) lucide.createIcons(); }, 100);
}

async function loadStatsPage() {
  const r = await fetch('/api/stats');
  const d = await r.json();

  const totalEval = (d.eval_ia || 0) + (d.eval_human || 0);
  const specComp = d.specialty_comparison || [];
  const avgScore = specComp.reduce((a, b) => a + (b.avg_score * b.count), 0) / (d.total || 1) || 0;

  setText('s-total-stat', fmt(d.total + d.hors_delai));
  setText('s-hors-delai-stat', fmt(d.hors_delai || 0));
  setText('s-comp-stat', fmt(d.complet || 0));
  setText('s-partiel-stat', fmt(d.partiel || 0));
  setText('s-vide-stat', fmt(d.vide || 0));

  setText('st-avg-score', avgScore.toFixed(1) + '/100');
  setText('st-admission-rate', d.total ? (((d.excellent || 0) + (d.bon || 0)) / d.total * 100).toFixed(1) + '%' : '0%');
  setText('st-retenu-count', fmt(d.retenu_count || 0));
  setText('st-ia-count', fmt(d.eval_ia || 0));
  setText('st-verify-count', fmt(d.verify || 0));

  // Funnel Chart
  const ctxFunnel = document.getElementById('funnelChart')?.getContext('2d');
  if (ctxFunnel) {
    if (charts.funnel) charts.funnel.destroy();
    charts.funnel = new Chart(ctxFunnel, {
      type: 'bar',
      data: {
        labels: ['Total', 'Dans les délais', 'Complets', 'Évalués'],
        datasets: [{
          data: [d.total + d.hors_delai, d.total, d.complet, totalEval],
          backgroundColor: ['#6366F1', '#8B5CF6', '#10B981', '#F59E0B'],
          borderRadius: 10,
          barThickness: 50
        }]
      },
      options: {
        responsive: true, maintainAspectRatio: false,
        indexAxis: 'y',
        plugins: { legend: { display: false } },
        scales: { x: { grid: { display: false } }, y: { grid: { display: false } } }
      }
    });
  }

  // Distribution Chart
  const ctxDist = document.getElementById('scoreDistributionChart')?.getContext('2d');
  if (ctxDist) {
    if (charts.dist) charts.dist.destroy();
    charts.dist = new Chart(ctxDist, {
      type: 'bar',
      data: {
        labels: d.score_distribution.map(s => `${s.range}-${s.range + 10}`),
        datasets: [{
          label: 'Candidats',
          data: d.score_distribution.map(s => s.cnt),
          backgroundColor: '#6366F1',
          borderRadius: 5
        }]
      },
      options: {
        responsive: true, maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: { x: { grid: { display: false } }, y: { grid: { display: false } } }
      }
    });
  }

  const tbody = document.getElementById('spec-stats-body');
  if (tbody) {
    tbody.innerHTML = d.specialty_comparison.map(s => `
        <tr>
            <td style="font-weight:700;">${esc(s.specialty || 'Non spécifié')}</td>
            <td>${fmt(s.count)}</td>
            <td>
                <div style="display:flex; align-items:center; gap:0.5rem">
                    <div style="flex:1; height:6px; background:#f1f5f9; border-radius:3px; overflow:hidden;">
                        <div style="width:${s.complet_pct}%; height:100%; background:var(--success)"></div>
                    </div>
                    <span style="font-size:0.75rem; font-weight:700;">${s.complet_pct}%</span>
                </div>
            </td>
            <td style="font-weight:800; color:var(--success)">${fmt(s.retenu_count || 0)}</td>
            <td style="font-weight:800; color:var(--accent)">${s.avg_score || 0}</td>
        </tr>
      `).join('');
  }
  lucide.createIcons();
}

function startCountdown(targetDate) {
  const timer = document.getElementById('deadline-timer');
  if (!timer) return;
  function update() {
    const now = new Date().getTime();
    const dist = new Date(targetDate).getTime() - now;
    if (dist < 0) { timer.textContent = "CLÔTURÉ"; return; }
    const d = Math.floor(dist / (1000 * 60 * 60 * 24)), h = Math.floor((dist % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)), m = Math.floor((dist % (1000 * 60 * 60)) / (1000 * 60));
    timer.textContent = `${d}j ${h}h ${m}m`;
  }
  update(); setInterval(update, 60000);
}

function renderAudit(logs) {
  const container = document.getElementById('audit-logs');
  if (!container) return;
  if (!logs || logs.length === 0) { container.innerHTML = '<p style="text-align:center;color:var(--text-dim);">Aucune activité.</p>'; return; }
  container.innerHTML = logs.map(l => `
        <div style="background:rgba(255,255,255,0.4); border:1px solid var(--glass-border); border-radius:16px; padding:1rem; margin-bottom:0.75rem; display:flex; justify-content:space-between; align-items:center;">
            <div>
                <div style="font-weight:700; font-size:0.9rem;">${esc(l.detail)}</div>
                <div style="font-size:0.75rem; color:var(--text-dim); margin-top:0.25rem;">${l.created_at} • ${esc(l.evaluateur)}</div>
            </div>
            <i data-lucide="chevron-right" style="width:16px; opacity:0.3"></i>
        </div>
    `).join('');
}

/* ══════════════════════════════════════════
   CANDIDATES
   ══════════════════════════════════════════ */
let page = 1, sort = 'score_total', order = 'desc', totalPages = 1, tableLoaded = false;

async function loadTable(reset = true) {
  tableLoaded = true;
  if (reset) page = 1;
  const q = document.getElementById('searchInput')?.value || '';
  const st = document.getElementById('statusFilter')?.value || '';
  const sp = document.getElementById('specialtyFilter')?.value || '';
  const vr = document.getElementById('verifyFilter')?.value || '';
  const mn = document.getElementById('mentionFilter')?.value || '';

  const params = new URLSearchParams({ q, status: st, specialty: sp, verification_required: vr, mention: mn, page, per_page: 50, sort, order });
  const tbody = document.getElementById('tableBody');
  if (!tbody) return;

  tbody.innerHTML = `<tr><td colspan="7" style="text-align:center;padding:5rem;"><div style="width:40px;height:40px;border:4px solid var(--accent-light);border-top-color:var(--accent);border-radius:50%;animation:spin 1s linear infinite;margin:0 auto;"></div></td></tr>`;

  const r = await fetch('/api/candidates?' + params);
  const d = await r.json();
  totalPages = d.pages || 1;
  const countEl = document.getElementById('resultCount');
  if (countEl) countEl.textContent = `${fmt(d.total)} entries`;

  if (!d.data.length) {
    tbody.innerHTML = `<tr><td colspan="7" style="text-align:center;padding:5rem;color:var(--text-dim);">Aucun résultat trouvé.</td></tr>`;
    renderPagination(0); return;
  }

  tbody.innerHTML = d.data.map(c => `
    <tr onclick="selectCandidat(${c.id})" style="cursor:pointer">
      <td>
        <div style="font-weight:800; color:var(--primary);">${esc(c.name)}</div>
        <div style="font-size:0.7rem; color:var(--text-dim);">${esc(c.email_addr)}</div>
      </td>
      <td>${esc(c.specialty || '—')}</td>
      <td><div style="display:flex;gap:4px;">${['cv', 'motivation', 'id', 'diplomas'].map(k => `<span style="opacity:${c['has_' + k] ? 1 : 0.1}">●</span>`).join('')}</div></td>
      <td>${statusBadge(c.status)}${c.verification_required ? ' <span class="badge" style="background:var(--danger);color:white">⚠️</span>' : ''}</td>
      <td style="text-align:center;font-weight:800;color:${scoreColor(c.score_total)}">${c.score_total || '—'}</td>
      <td>${mentionBadge(c.mention)}</td>
      <td style="font-size:0.75rem; color:var(--text-dim)">${c.last_date || '—'}</td>
    </tr>
  `).join('');

  renderPagination(d.total);
  lucide.createIcons();
}

function renderPagination(total) {
  const pg = document.getElementById('pagination');
  if (!pg) return;
  if (totalPages <= 1) { pg.innerHTML = ''; return; }

  let h = `<button class="btn btn-glass" onclick="goPage(${page - 1})" ${page === 1 ? 'disabled' : ''}>‹</button>`;
  h += `<span class="page-num">${page} / ${totalPages}</span>`;
  h += `<button class="btn btn-glass" onclick="goPage(${page + 1})" ${page === totalPages ? 'disabled' : ''}>›</button>`;
  pg.innerHTML = h;
}
function goPage(p) { page = p; loadTable(false); }
function setSort(f) { if (sort === f) order = order === 'asc' ? 'desc' : 'asc'; else { sort = f; order = 'desc'; } loadTable(); }

function resetFilters() {
  document.getElementById('searchInput').value = '';
  document.getElementById('statusFilter').value = '';
  document.getElementById('specialtyFilter').value = '';
  document.getElementById('verifyFilter').value = '';
  document.getElementById('mentionFilter').value = '';
  loadTable();
}

/* ══════════════════════════════════════════
   VERIFICATION & QUOTAS
   ══════════════════════════════════════════ */
async function loadVerifyTable() {
  const tbody = document.getElementById('verifyTableBody');
  if (!tbody) return;
  tbody.innerHTML = `<tr><td colspan="5" style="text-align:center;padding:5rem;"><div class="spinner"></div></td></tr>`;

  // Filter verify = 1 + contenu manquant
  const r = await fetch('/api/candidates?verification_required=1&sort=last_date&order=desc');
  const d = await r.json();

  if (!d.data.length) {
    tbody.innerHTML = `<tr><td colspan="5" style="text-align:center;padding:5rem;color:var(--text-dim);">Aucun dossier à vérifier.</td></tr>`;
    return;
  }

  tbody.innerHTML = d.data.map(c => `
      <tr>
        <td>
          <div style="font-weight:800; color:var(--primary);">${esc(c.name)}</div>
          <div style="font-size:0.7rem; color:var(--text-dim);">${esc(c.email_addr)}</div>
        </td>
        <td>${esc(c.specialty || '—')}</td>
        <td>${statusBadge(c.status)}</td>
        <td style="font-size:0.75rem; color:var(--text-dim)">${c.last_date || '—'}</td>
        <td style="text-align:right">
            <div style="display:flex; justify-content:flex-end; gap:0.5rem">
                <button class="btn btn-glass" onclick="openFolder(${c.id})" style="padding:0.4rem 0.8rem; font-size:0.75rem">
                    <i data-lucide="folder-open" style="width:14px;height:14px"></i> Dossier
                </button>
                <button class="btn btn-primary" onclick="selectCandidat(${c.id})" style="padding:0.4rem 0.8rem; font-size:0.75rem">
                    Évaluer
                </button>
            </div>
        </td>
      </tr>
    `).join('');
  lucide.createIcons();
}

async function loadQuotasTable() {
  const rStats = await fetch('/api/quotas');
  const quotas = await rStats.json();

  const qs = document.getElementById('quotas-stats-grid');
  if (qs) {
    qs.innerHTML = quotas.map(q => `
            <div class="stat-card" style="border-top: 4px solid var(--accent); padding:1.5rem">
                <div style="font-size:0.75rem; font-weight:800; color:var(--text-dim); margin-bottom:1rem; white-space:nowrap; overflow:hidden; text-overflow:ellipsis" title="${esc(q.specialty)}">${esc(q.specialty || 'Non spécifié')}</div>
                <div style="display:flex; justify-content:space-between; align-items:flex-end;">
                    <div>
                        <div style="font-size:2rem; font-weight:900; color:var(--primary); line-height:1">${q.retenu_digital}</div>
                        <div style="font-size:0.7rem; font-weight:700; color:var(--success); margin-top:0.2rem">Retenus / ${q.total_digital}</div>
                    </div>
                    <div style="text-align:right">
                        <div style="font-size:1.25rem; font-weight:800; color:var(--text-muted); line-height:1">${q.complet_count}</div>
                        <div style="font-size:0.7rem; color:var(--text-dim); margin-top:0.2rem">Complets</div>
                    </div>
                </div>
            </div>
        `).join('');
  }

  const tbody = document.getElementById('quotasTableBody');
  if (!tbody) return;
  tbody.innerHTML = `<tr><td colspan="5" style="text-align:center;padding:5rem;"><div class="spinner"></div></td></tr>`;

  const sp = document.getElementById('quotasSpecialtyFilter')?.value || '';
  const query = new URLSearchParams({ sort: 'score_total', order: 'desc', per_page: 100 });
  if (sp) query.set('specialty', sp);
  query.set('contenu_manquant', "0");

  const r = await fetch('/api/candidates?' + query.toString());
  const d = await r.json();

  if (!d.data.length) {
    tbody.innerHTML = `<tr><td colspan="5" style="text-align:center;padding:5rem;color:var(--text-dim);">Aucun candidat pour cette sélection.</td></tr>`;
    return;
  }

  tbody.innerHTML = d.data.map(c => `
      <tr style="${c.retenu ? 'background:rgba(16, 185, 129, 0.05)' : ''}">
        <td>
          <div style="font-weight:800; color:var(--primary);">${esc(c.name)}</div>
          <div style="font-size:0.75rem; color:var(--text-dim);">${c.score_total || 0} pts • ${esc(c.mention)}</div>
        </td>
        <td style="font-size:0.85rem">${esc(c.specialty || '—')}</td>
        <td style="text-align:center"><div style="font-weight:800; color:var(--accent)">${c.score_total || '—'}</div></td>
        <td style="text-align:center"><input type="number" style="width:60px; padding:0.3rem" class="srch" placeholder="Ext."></td>
        <td style="text-align:center">
          ${c.retenu
      ? `<button class="btn btn-glass" onclick="markRetenuId(${c.id}, 0)" style="color:var(--success); border-color:var(--success); padding:0.4rem 0.8rem; font-size:0.75rem"><i data-lucide="check-circle" style="width:14px;height:14px"></i> Retenu</button>`
      : `<button class="btn btn-glass" onclick="markRetenuId(${c.id}, 1)" style="padding:0.4rem 0.8rem; font-size:0.75rem">Sélectionner</button>`
    }
        </td>
      </tr>
    `).join('');
  lucide.createIcons();
}

async function openFolder(id) {
  try {
    await fetch(`/api/candidate/${id}/open-folder`);
    showToast("Dossier ouvert dans l'explorateur");
  } catch (e) { }
}

async function markRetenuId(id, val) {
  await fetch(`/api/candidate/${id}/retenir`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ retenu: val, evaluateur: 'Commission' })
  });
  showToast(val ? "Candidat sélectionné" : "Candidat retiré");
  loadQuotasTable();
  loadStats();
}

async function markRetenu(val) {
  if (!currentCandidatId) return;
  await fetch(`/api/candidate/${currentCandidatId}/retenir`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ retenu: val, evaluateur: 'Commission' })
  });
  showToast(val ? "Candidat marqué comme retenu" : "Candidat marqué comme non retenu");
  if (currentPage === 'evaluation') {
    const r = await fetch(`/api/candidate/${currentCandidatId}`);
    const c = await r.json();
    const ev = c.evaluations[c.evaluations.length - 1] || {};
    evalUpdateUi(c, ev);
  }
}

/* ══════════════════════════════════════════
   EVALUATION
   ══════════════════════════════════════════ */
let currentCandidatId = null;
async function selectCandidat(id) {
  currentCandidatId = id;
  const r = await fetch(`/api/candidate/${id}`);
  const c = await r.json();
  gotoPage('evaluation');

  setText('ev-avatar', c.name.split(' ').map(w => w[0]).join('').substring(0, 2).toUpperCase());
  setText('ev-name', c.name);
  setText('ev-email', c.email_addr);

  // Update Evaluator Badge
  const b = document.getElementById('ev-evaluator-badge');
  if (b) {
    const isIA = (c.evaluateur || '').startsWith('IA');
    b.textContent = isIA ? "💡 Suggestion IA" : "👤 Validé Humain";
    b.className = `badge ${isIA ? 'b-bon' : 'b-excellent'}`;
  }

  // AI Inspector & Missing Warning
  const box = document.getElementById('ev-ai-inspector-box');
  const ocr = document.getElementById('ev-ocr-text');
  const mw = document.getElementById('ev-missing-warning');

  if (mw) {
    if (c.status === 'Vide' || c.status === 'Incomplet' || c.status === 'Partiel') mw.style.display = 'block';
    else mw.style.display = 'none';
  }

  if (box && ocr) {
    const emailTxt = (c.email_body_full || '').trim();
    const attTxt = (c.att_text || '').trim();

    if (emailTxt || attTxt) {
      let h = '';
      if (emailTxt) h += `<div style="color:var(--accent); font-weight:800; margin-bottom:0.25rem; font-size:0.65rem; opacity:0.8;">[Texte de l'E-mail]</div>${emailTxt}\n\n`;
      if (attTxt) h += `<div style="color:var(--success); font-weight:800; margin-bottom:0.25rem; font-size:0.65rem; opacity:0.8;">[Contenu des Documents (OCR)]</div>${attTxt}`;
      ocr.innerHTML = h;
      box.style.display = 'block';
    } else {
      box.style.display = 'none';
    }
  }

  // Render clickable attachments
  const att = document.getElementById('ev-attachments');
  if (att) {
    if (!c.attachment_names || c.attachment_names.length === 0) {
      att.innerHTML = '<div style="font-size:0.75rem; color:var(--text-dim); font-style:italic">Aucun fichier trouvé.</div>';
    } else {
      att.innerHTML = c.attachment_names.map(f => {
        let path = c.folder_path ? `${c.folder_path}/${f}` : f;
        // Normalisation: enlever "pieces_jointes/" si déjà présent et corriger les slashes
        path = path.replace(/\\/g, '/').replace(/^pieces_jointes\//, '');
        return `
                <a href="/pieces_jointes/${path}" target="_blank" class="btn btn-glass" style="display:flex; align-items:center; gap:0.5rem; text-decoration:none; text-align:left; font-size:0.8rem; padding:0.6rem 1rem;">
                    <i data-lucide="file-text" style="width:14px;height:14px;color:var(--accent)"></i>
                    <span style="overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">${f}</span>
                </a>
              `;
      }).join('');
    }
  }

  const infoRows = document.getElementById('ev-info-rows');
  if (infoRows) {
    infoRows.innerHTML = [
      { l: t('info_filiere'), v: c.specialty || '—', i: 'briefcase' },
      { l: t('info_emails'), v: c.num_emails, i: 'mail' },
      { l: t('info_first'), v: c.first_date, i: 'calendar' }
    ].map(r => `
      <div style="display:flex; justify-content:space-between; padding:0.75rem 0; border-bottom:1px solid var(--glass-border); font-size:0.85rem">
        <span style="color:var(--text-dim); display:flex; align-items:center; gap:0.5rem"><i data-lucide="${r.i}" style="width:14px;height:14px;"></i> ${r.l}</span>
        <span style="font-weight:700; color:var(--primary)">${r.v}</span>
      </div>
    `).join('');
  }

  const docsEl = document.getElementById('ev-docs');
  if (docsEl) {
    const docs = [{ l: t('docs_cv'), v: c.has_cv }, { l: t('docs_lettre'), v: c.has_motivation }, { l: t('docs_cin'), v: c.has_id }, { l: t('docs_diplome'), v: c.has_diplomas }];
    docsEl.innerHTML = docs.map(d => `
      <div style="background:${d.v ? 'var(--accent-light)' : '#f1f5f9'}; color:${d.v ? 'var(--accent)' : 'var(--text-dim)'}; padding:0.5rem; border-radius:8px; font-size:0.7rem; font-weight:700; text-align:center; border:1px solid ${d.v ? 'var(--accent)' : 'transparent'}; opacity:${d.v ? 1 : 0.6}">
          ${d.l}
      </div>
    `).join('');
  }

  // Load data from latest evaluation if exists
  const lastEval = c.evaluations && c.evaluations.length > 0 ? c.evaluations[c.evaluations.length - 1] : {};

  ['niveau', 'experience', 'motivation', 'adequation', 'dossier', 'disponibilite'].forEach(k => {
    const v = lastEval[`score_${k}`] ?? 0, sl = document.getElementById(`sl-${k}`), vl = document.getElementById(`v-${k}`);
    if (sl) sl.value = v; if (vl) vl.textContent = v;
    const justifEl = document.getElementById(`j-${k}`);
    if (justifEl) {
      if (lastEval[`justif_${k}`]) justifEl.innerHTML = `<span style="font-weight:700">Justification:</span> ${esc(lastEval[`justif_${k}`])}`;
      else justifEl.innerHTML = '';
    }
  });

  const nf = document.getElementById('note-field');
  const ng = lastEval.note_globale ? `🤖[IA]: ${lastEval.note_globale}\n\n` : '';
  if (nf) nf.value = ng + (lastEval.note || '');

  if (c.retenu) {
    const b = document.getElementById('ev-evaluator-badge');
    if (b) {
      b.textContent = "✅ Retenu";
      b.className = "badge b-success";
    }
  }

  liveScore();

  const ee = document.getElementById('eval-empty'), el = document.getElementById('eval-layout');
  if (ee) ee.style.display = 'none'; if (el) el.style.display = 'grid';
  setTimeout(() => lucide.createIcons(), 50);
}

function evalUpdateUi(c, ev) {
  // Update badge immediately upon Retenu click without reloading the full form
  if (c.retenu) {
    const b = document.getElementById('ev-evaluator-badge');
    if (b) {
      b.textContent = "✅ Retenu";
      b.className = "badge b-success";
    }
  } else {
    const b = document.getElementById('ev-evaluator-badge');
    if (b) {
      b.textContent = "❌ Non Retenu";
      b.className = "badge b-danger";
    }
  }
}

function liveScore() {
  const keys = ['niveau', 'experience', 'motivation', 'adequation', 'dossier', 'disponibilite'];
  let total = 0;
  keys.forEach(k => {
    const el = document.getElementById(`sl-${k}`);
    if (el) {
      total += parseFloat(el.value);
      const valEl = document.getElementById(`v-${k}`);
      if (valEl) valEl.textContent = el.value;
    }
  });
  setText('total-score', total.toFixed(1));
  const m = getMention(total);
  const mb = document.getElementById('total-mention');
  if (mb) { mb.textContent = m.label; mb.className = `badge tb-mention ${m.cls}`; }
}

async function saveScore() {
  if (!currentCandidatId) return;
  const body = {
    score_niveau: parseFloat(document.getElementById('sl-niveau').value),
    score_experience: parseFloat(document.getElementById('sl-experience').value),
    score_motivation: parseFloat(document.getElementById('sl-motivation').value),
    score_adequation: parseFloat(document.getElementById('sl-adequation').value),
    score_dossier: parseFloat(document.getElementById('sl-dossier').value),
    score_disponibilite: parseFloat(document.getElementById('sl-disponibilite').value),
    note_evaluateur: document.getElementById('note-field').value,
    evaluateur: "Admin"
  };
  await fetch(`/api/candidate/${currentCandidatId}/evaluate`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
  showToast(t('toast_saved'));
  loadStats();
}

/* ══════════════════════════════════════════
   HELPERS & INIT
   ══════════════════════════════════════════ */
function fmt(n) { return (n || 0).toLocaleString('fr-FR'); }
function esc(s) { return String(s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
function setText(id, v) { const el = document.getElementById(id); if (el) el.textContent = v; }
function showToast(msg) {
  const t = document.getElementById('toast'); if (!t) return;
  t.innerHTML = `<i data-lucide="check-circle" style="width:20px;height:20px;"></i> ${msg}`;
  lucide.createIcons(); t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 3000);
}
function scoreColor(s) { if (s >= 80) return '#10B981'; if (s >= 65) return '#6366F1'; if (s >= 50) return '#F59E0B'; return '#EF4444'; }
function statusBadge(s) {
  const m = { Complet: 'b-complet', Partiel: 'b-partiel', Incomplet: 'b-incomplet', Vide: 'b-vide' };
  return `<span class="badge ${m[s] || 'b-vide'}">${t(s.toLowerCase())}</span>`;
}
function mentionBadge(m) {
  if (!m) return `<span class="badge">${t('badge_pending')}</span>`;
  const map = { Excellent: 'b-excellent', Bon: 'b-bon', Moyen: 'b-moyen', 'Non retenu': 'b-nonretenu' };
  return `<span class="badge ${map[m] || ''}">${t('badge_' + m.toLowerCase().replace(' ', '_'))}</span>`;
}
function getMention(s) {
  if (s >= 80) return { label: t('badge_excellent'), cls: 'b-excellent' };
  if (s >= 65) return { label: t('badge_bon'), cls: 'b-bon' };
  if (s >= 50) return { label: t('badge_moyen'), cls: 'b-moyen' };
  return { label: t('badge_non_retenu'), cls: 'b-nonretenu' };
}
function debounce(fn, ms) { let t; return (...a) => { clearTimeout(t); t = setTimeout(() => fn(...a), ms) } }
function exportCSV() { window.location = '/api/export/csv' }

document.addEventListener('DOMContentLoaded', () => {
  loadStats();
  applyTranslations();
  lucide.createIcons();
});
