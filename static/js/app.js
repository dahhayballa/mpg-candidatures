/* ══════════════════════════════════════════
   I18N
   ══════════════════════════════════════════ */
const TRANSLATIONS = {
  fr: {
    subtitle:"Candidatures 2025–2026",
    nav_section:"Navigation",
    nav_dashboard:"Tableau de bord",
    nav_candidats:"Candidats",
    nav_evaluation:"Évaluation",
    nav_statistiques:"Statistiques",
    deadline_label:"Date limite :",
    btn_export:"⬇ Exporter CSV",
    stat_total:"Candidats recevables", stat_total_sub:"dans les délais",
    stat_hd:"Hors délai", stat_hd_sub:"après le 31/03 14h",
    stat_complet:"Dossiers complets", stat_complet_sub:"4 pièces présentes",
    stat_partiel:"Partiels", stat_partiel_sub:"pièces manquantes",
    stat_eval:"Évalués", stat_eval_sub:"note saisie",
    stat_reste:"À évaluer", stat_reste_sub:"en attente",
    ring_eval:"Taux d'évaluation", ring_complet:"Dossiers complets", ring_excellent:"Candidats excellents",
    specialty_repartition:"Répartition par filière",
    mentions_results:"Résultats de la notation",
    mention_excellent:"Excellent (prioritaire)", mention_bon:"Bon candidat",
    mention_moyen:"Moyen (à discuter)", mention_non_retenu:"Non retenu",
    search_ph:"Rechercher par nom, e-mail, filière…",
    all_statuts:"Tous les statuts", all_filieres:"Toutes les filières",
    all_mentions:"Toutes les mentions", all_eval:"Tous",
    a_evaluer:"À évaluer", evalues:"Déjà évalués",
    complet:"✅ Complet", partiel:"🟡 Partiel", incomplet:"❌ Incomplet", vide:"⚪ Vide",
    col_nom:"Nom", col_filiere:"Filière", col_pieces:"Pièces",
    col_dossier:"Dossier", col_note:"Note /100", col_mention:"Mention", col_date:"Date",
    eval_select_title:"Sélectionner un candidat",
    eval_select_sub:"Allez dans la page Candidats et cliquez sur une ligne pour commencer l'évaluation.",
    eval_go_candidats:"Voir les candidats →",
    scoring_grid:"Grille d'évaluation — /100 points",
    crit_niveau:"Niveau d'études", crit_niveau_desc:"Correspondance avec la filière, niveau minimum requis, pertinence",
    crit_exp:"Expérience", crit_exp_desc:"Stages, expériences professionnelles ou pratiques liées au domaine",
    crit_motiv:"Lettre de motivation", crit_motiv_desc:"Clarté, coherence, motivation réelle, projet professionnel",
    crit_adeq:"Adéquation au profil", crit_adeq_desc:"Compatibilité avec la formation, aptitudes techniques, logique",
    crit_dossier:"Qualité du dossier", crit_dossier_desc:"CV (2.5) + Lettre motivation (2.5) + CIN (2.5) + Diplômes (2.5)",
    crit_dispo:"Disponibilité", crit_dispo_desc:"Capacité à suivre toute la formation (3 à 6 mois, temps plein)",
    total_note:"Note totale", total_note_sub:"sur 100 points",
    note_ph:"Observations de l'évaluateur (facultatif)…",
    btn_annuler:"Annuler", btn_save:"💾 Enregistrer la note",
    toast_saved:"✅ Note enregistrée avec succès !",
    topbar_sub_dashboard:"Vue d'ensemble des candidatures",
    topbar_sub_candidats:"Liste et फيلتر",
    topbar_sub_evaluation:"Grille de notation",
    topbar_sub_statistiques:"Analyses détaillées",
    info_filiere:"Filière demandée",info_emails:"E-mails envoyés",
    info_first:"Première candidature",info_last:"Dernière candidature",
    docs_cv:"CV",docs_lettre:"Lettre de motivation",docs_cin:"Pièce d'identité",docs_diplome:"Diplômes",
    stats_loading:"Chargement…",
    badge_complet:"✅ Complet",badge_partiel:"🟡 Partiel",badge_incomplet:"❌ Incomplet",badge_vide:"⚪ Vide",
    badge_excellent:"🏆 Excellent",badge_bon:"✅ Bon",badge_moyen:"🟡 Moyen",badge_non_retenu:"❌ Non retenu",
    badge_pending:"À évaluer",
    stat_page_title:"Statistiques détaillées",
  },
  ar: {
    subtitle:"الترشحات 2025–2026",
    nav_section:"القائمة",
    nav_dashboard:"لوحة التحكم",
    nav_candidats:"المترشحون",
    nav_evaluation:"التقييم",
    nav_statistiques:"الإحصائيات",
    deadline_label:"الموعد النهائي :",
    btn_export:"⬇ تصدير CSV",
    stat_total:"المترشحون المقبولون", stat_total_sub:"في الوقت المحدد",
    stat_hd:"خارج الموعد", stat_hd_sub:"بعد 31/03 الساعة 14:00",
    stat_complet:"ملفات مكتملة", stat_complet_sub:"4 وثائق موجودة",
    stat_partiel:"ملفات جزئية", stat_partiel_sub:"وثائق ناقصة",
    stat_eval:"تم تقييمهم", stat_eval_sub:"تم إدخال الدرجة",
    stat_reste:"لم يُقيَّموا", stat_reste_sub:"في الانتظار",
    ring_eval:"نسبة التقييم", ring_complet:"الملفات المكتملة", ring_excellent:"المترشحون الممتازون",
    specialty_repartition:"التوزيع حسب التخصص",
    mentions_results:"نتائج التقييم",
    mention_excellent:"ممتاز (أولوية)", mention_bon:"جيد",
    mention_moyen:"متوسط (للمناقشة)", mention_non_retenu:"مرفوض",
    search_ph:"ابحث بالاسم أو البريد أو التخصص…",
    all_statuts:"جميع الحالات", all_filieres:"جميع التخصصات",
    all_mentions:"جميع التقديرات", all_eval:"الكل",
    a_evaluer:"لم يُقيَّم بعد", evalues:"تم تقييمهم",
    complet:"✅ مكتمل", partiel:"🟡 جزئي", incomplet:"❌ ناقص", vide:"⚪ فارغ",
    col_nom:"الاسم", col_filiere:"التخصص", col_pieces:"الوثائق",
    col_dossier:"الملف", col_note:"الدرجة /100", col_mention:"التقدير", col_date:"التاريخ",
    eval_select_title:"اختر مترشحاً",
    eval_select_sub:"انتقل إلى صفحة المترشحين وانقر على أي صف لبدء التقييم.",
    eval_go_candidats:"→ عرض المترشحين",
    scoring_grid:"شبكة التقييم — /100 نقطة",
    crit_niveau:"المستوى الدراسي", crit_niveau_desc:"التوافق مع التخصص المختار، الحد الأدنى المطلوب",
    crit_exp:"الخبرة", crit_exp_desc:"تدريبات، خبرات مهنية أو تطبيقية في المجال",
    crit_motiv:"رسالة التحفيز", crit_motiv_desc:"الوضوح، التماسك، الدافعية الحقيقية، المشروع المهني",
    crit_adeq:"التوافق مع المتطلبات", crit_adeq_desc:"التوافق مع التكوين، الكفاءات التقنية، المنطق",
    crit_dossier:"جودة الملف", crit_dossier_desc:"السيرة (2.5) + الرسالة (2.5) + بطاقة التعريف (2.5) + الشهادات (2.5)",
    crit_dispo:"التفرغ", crit_dispo_desc:"القدرة على متابعة التكوين بالكامل (3 إلى 6 أشهر)",
    total_note:"الدرجة الإجمالية", total_note_sub:"من 100 نقطة",
    note_ph:"ملاحظات المقيِّم (اختياري)…",
    btn_annuler:"إلغاء", btn_save:"💾 حفظ الدرجة",
    toast_saved:"✅ تم حفظ الدرجة بنجاح!",
    topbar_sub_dashboard:"نظرة عامة على الترشحات",
    topbar_sub_candidats:"القائمة والفلاتر",
    topbar_sub_evaluation:"شبكة التنقيط",
    topbar_sub_statistiques:"تحليلات مفصلة",
    info_filiere:"التخصص المطلوب",info_emails:"عدد الرسائل",
    info_first:"أول ترشح",info_last:"آخر ترشح",
    docs_cv:"السيرة الذاتية",docs_lettre:"رسالة التحفيز",docs_cin:"بطاقة التعريف",docs_diplome:"الشهادات",
    stats_loading:"جارٍ التحميل…",
    badge_complet:"✅ مكتمل",badge_partiel:"🟡 جزئي",badge_incomplet:"❌ ناقص",badge_vide:"⚪ فارغ",
    badge_excellent:"🏆 ممتاز",badge_bon:"✅ جيد",badge_moyen:"🟡 متوسط",badge_non_retenu:"❌ مرفوض",
    badge_pending:"لم يُقيَّم",
    stat_page_title:"إحصائيات مفصلة",
  }
};

let lang = 'fr';
function t(k){ return TRANSLATIONS[lang][k] || TRANSLATIONS.fr[k] || k }

function setLang(l){
  lang = l;
  const html = document.getElementById('html-root');
  html.setAttribute('lang', l);
  html.setAttribute('dir', l==='ar'?'rtl':'ltr');
  document.getElementById('lang-fr').classList.toggle('active', l==='fr');
  document.getElementById('lang-ar').classList.toggle('active', l==='ar');
  applyTranslations();
}

function applyTranslations(){
  document.querySelectorAll('[data-i18n]').forEach(el=>{
    const k = el.getAttribute('data-i18n');
    el.textContent = t(k);
  });
  document.querySelectorAll('[data-i18n-ph]').forEach(el=>{
    el.placeholder = t(el.getAttribute('data-i18n-ph'));
  });
  updateTopbar();
}

/* ══════════════════════════════════════════
   NAVIGATION
   ══════════════════════════════════════════ */
let currentPage = 'dashboard';
const pageMeta = {
  dashboard:    { title:'nav_dashboard',  sub:'topbar_sub_dashboard' },
  candidats:    { title:'nav_candidats',  sub:'topbar_sub_candidats' },
  evaluation:   { title:'nav_evaluation', sub:'topbar_sub_evaluation' },
  statistiques: { title:'nav_statistiques',sub:'topbar_sub_statistiques' },
};

function gotoPage(p){
  currentPage = p;
  document.querySelectorAll('.page').forEach(el=>el.classList.remove('active'));
  document.getElementById(`page-${p}`).classList.add('active');
  document.querySelectorAll('.sb-nav a').forEach(a=>a.classList.remove('active'));
  document.getElementById(`nav-${p}`).classList.add('active');
  updateTopbar();
  if(p==='candidats' && !tableLoaded) loadTable();
  if(p==='statistiques') loadStatsPage();
}

function updateTopbar(){
  const m = pageMeta[currentPage];
  if(!m) return;
  document.getElementById('topbar-title').textContent = t(m.title);
  document.getElementById('topbar-sub').textContent   = t(m.sub);
}

let tableLoaded = false;

/* ══════════════════════════════════════════
   STATS — PAGE DASHBOARD
   ══════════════════════════════════════════ */
let statsData = null;

async function loadStats(){
  const r = await fetch('/api/stats');
  statsData = await r.json();
  const d = statsData;

  setText('s-total',  fmt(d.total));
  setText('s-hd',     fmt(d.hors_delai));
  setText('s-complet',fmt(d.complet));
  setText('s-partiel',fmt(d.partiel));
  setText('s-eval',   fmt(d.evalues));
  setText('s-reste',  fmt(d.total - d.evalues));
  setText('nb-count', fmt(d.total));

  // Anneaux
  animRing('ring-eval',     d.evalues / Math.max(d.total,1) * 100, 'ring-eval-pct');
  animRing('ring-complet',  d.complet / Math.max(d.total,1) * 100, 'ring-complet-pct');
  animRing('ring-excellent',d.excellent / Math.max(d.evalues,1) * 100, 'ring-excellent-pct');

  // Barres spécialités
  const sb = document.getElementById('d-specialty-bars');
  const mx = Math.max(...d.by_specialty.map(s=>s.cnt), 1);
  sb.innerHTML = d.by_specialty.map(s=>`
    <div class="sp-row">
      <div class="sp-hd"><span>${esc(s.specialty||'Non spécifié')}</span><span>${s.cnt}</span></div>
      <div class="sp-bg"><div class="sp-fill" style="width:${Math.round(s.cnt/mx*100)}%"></div></div>
    </div>`).join('');

  // Barres mentions
  const mb = document.getElementById('d-mention-bars');
  const ev = Math.max(d.evalues, 1);
  const ms = [
    {cls:'m-ex',l:t('mention_excellent'), v:d.excellent},
    {cls:'m-bo',l:t('mention_bon'),       v:d.bon},
    {cls:'m-mo',l:t('mention_moyen'),     v:d.moyen},
    {cls:'m-nr',l:t('mention_non_retenu'),v:d.non_retenu},
  ];
  mb.innerHTML = d.evalues > 0
    ? ms.map(m=>`<div class="mention-row ${m.cls}">
        <span class="mention-lbl">${m.l}</span>
        <div class="mbar-bg"><div class="mbar-fill" style="width:${Math.round(m.v/ev*100)}%"></div></div>
        <span class="mention-cnt">${m.v}</span>
      </div>`).join('')
    : `<div style="color:var(--dim);font-size:.78rem">${lang==='ar'?'لم يتم إجراء أي تقييم بعد':'Aucune évaluation encore saisie.'}</div>`;
}

function animRing(id, pct, textId){
  const circ = 182.2;
  const el = document.getElementById(id);
  if(!el) return;
  const offset = circ - (circ * Math.min(pct,100) / 100);
  setTimeout(()=>{ el.style.strokeDashoffset = offset; }, 200);
  document.getElementById(textId).textContent = Math.round(pct) + '%';
}

/* ══════════════════════════════════════════
   TABLE — PAGE CANDIDATS
   ══════════════════════════════════════════ */
let page=1, sort='last_date', order='desc', totalPages=1;

async function loadTable(reset=true){
  tableLoaded = true;
  if(reset) page = 1;
  const q   = document.getElementById('searchInput').value;
  const st  = document.getElementById('statusFilter').value;
  const sp  = document.getElementById('specialtyFilter').value;
  const mn  = document.getElementById('mentionFilter').value;
  const ev  = document.getElementById('evalueFilter').value;
  const params = new URLSearchParams({q,status:st,specialty:sp,mention:mn,evalue:ev,page,per_page:50,sort,order});

  const tbody = document.getElementById('tableBody');
  tbody.innerHTML = `<tr><td colspan="8" class="loading-td"><div class="spinner"></div></td></tr>`;

  const r = await fetch('/api/candidates?' + params);
  const d = await r.json();
  totalPages = d.pages || 1;
  document.getElementById('resultCount').textContent = `${fmt(d.total)} ${lang==='ar'?'مترشح':'candidat(s)'}`;

  if(!d.data.length){
    tbody.innerHTML = `<tr><td colspan="8"><div class="empty-state"><p>🔍</p><p>${lang==='ar'?'لا توجد نتائج':'Aucun résultat'}</p></div></td></tr>`;
    renderPagination(d.total); return;
  }

  tbody.innerHTML = d.data.map(c=>{
    const scoreHtml = c.score_total !== null
      ? `<div class="score-wrap"><span class="score-num" style="color:${scoreColor(c.score_total)}">${c.score_total}</span><div class="score-bar-bg"><div class="score-bar-fill" style="width:${c.score_total}%;background:${scoreColor(c.score_total)}"></div></div></div>`
      : `<span style="color:var(--dim);font-size:.73rem">—</span>`;
    return `<tr onclick="selectCandidat(${c.id})">
      <td class="td-name">${esc(c.name)}</td>
      <td class="td-email">${esc(c.email_addr)}</td>
      <td style="font-size:.73rem">${esc(c.specialty||'—')}</td>
      <td><div class="chks">
        <span class="chk ${c.has_cv?'ck-ok':'ck-no'}">📄</span>
        <span class="chk ${c.has_motivation?'ck-ok':'ck-no'}">✉</span>
        <span class="chk ${c.has_id?'ck-ok':'ck-no'}">🪪</span>
        <span class="chk ${c.has_diplomas?'ck-ok':'ck-no'}">🎓</span>
      </div></td>
      <td>${statusBadge(c.status)}</td>
      <td style="text-align:center">${scoreHtml}</td>
      <td>${mentionBadge(c.mention)}</td>
      <td style="font-size:.69rem;font-family:monospace;color:var(--dim)">${c.last_date||'—'}</td>
    </tr>`;
  }).join('');

  renderPagination(d.total);
  updateSortIcons();
}

function renderPagination(total){
  const pg = document.getElementById('pagination');
  if(totalPages <= 1){ pg.innerHTML=''; return; }
  const start = Math.max(1, page-2), end = Math.min(totalPages, page+2);
  let h = `<button class="pg-btn" ${page===1?'disabled':''} onclick="goPage(${page-1})">‹</button>`;
  if(start>1) h += `<button class="pg-btn" onclick="goPage(1)">1</button><span class="pg-info">…</span>`;
  for(let i=start;i<=end;i++) h += `<button class="pg-btn ${i===page?'active':''}" onclick="goPage(${i})">${i}</button>`;
  if(end<totalPages) h += `<span class="pg-info">…</span><button class="pg-btn" onclick="goPage(${totalPages})">${totalPages}</button>`;
  h += `<button class="pg-btn" ${page===totalPages?'disabled':''} onclick="goPage(${page+1})">›</button>`;
  h += `<span class="pg-info">${fmt(total)}</span>`;
  pg.innerHTML = h;
}
function goPage(p){ page=p; loadTable(false); }
function setSort(f){ if(sort===f) order=order==='asc'?'desc':'asc'; else{sort=f;order='desc';} loadTable(); }
function updateSortIcons(){
  document.querySelectorAll('th[onclick]').forEach(th=>{
    th.classList.remove('active');
    const si = th.querySelector('.si');
    if(si) si.textContent='↕';
    if(th.getAttribute('onclick')?.includes(`'${sort}'`)){
      th.classList.add('active');
      if(si) si.textContent = order==='asc'?'↑':'↓';
    }
  });
}

/* ══════════════════════════════════════════
   ÉVALUATION
   ══════════════════════════════════════════ */
let currentCandidatId = null;

async function selectCandidat(id){
  currentCandidatId = id;
  gotoPage('evaluation');

  const r = await fetch(`/api/candidate/${id}`);
  const c = await r.json();

  // Initiales avatar
  const initials = c.name.split(' ').map(w=>w[0]).join('').substring(0,2).toUpperCase();
  setText('ev-avatar', initials);
  setText('ev-name', c.name);
  setText('ev-email', c.email_addr);

  // Infos
  document.getElementById('ev-info-rows').innerHTML = [
    {l:t('info_filiere'), v:c.specialty||'—'},
    {l:t('info_emails'),  v:`${c.num_emails} e-mail${c.num_emails>1?'s':''}`},
    {l:t('info_first'),   v:c.first_date||'—'},
    {l:t('info_last'),    v:c.last_date||'—'},
  ].map(r=>`<div class="info-row"><span class="ir-lbl">${r.l}</span><span class="ir-val">${esc(r.v)}</span></div>`).join('');

  // Docs
  document.getElementById('ev-docs').innerHTML = [
    {k:'has_cv',l:t('docs_cv')}, {k:'has_motivation',l:t('docs_lettre')},
    {k:'has_id',l:t('docs_cin')},{k:'has_diplomas',l:t('docs_diplome')},
  ].map(d=>`<div class="doc-chip ${c[d.k]?'doc-ok':'doc-no'}">${c[d.k]?'✓':'✗'} ${d.l}</div>`).join('');

  // Pré-remplir curseurs
  ['niveau','experience','motivation','adequation','dossier','disponibilite'].forEach(k=>{
    const val = c[`score_${k}`] ?? 0;
    document.getElementById(`sl-${k}`).value = val;
    document.getElementById(`v-${k}`).textContent = val;
  });
  document.getElementById('note-field').value = c.note_evaluateur || '';
  liveScore();

  document.getElementById('eval-empty').style.display  = 'none';
  document.getElementById('eval-layout').style.display = 'grid';
}

function clearEval(){
  document.getElementById('eval-empty').style.display  = 'block';
  document.getElementById('eval-layout').style.display = 'none';
  currentCandidatId = null;
}

function liveScore(){
  const keys = ['niveau','experience','motivation','adequation','dossier','disponibilite'];
  const vals = keys.map(k=>{
    const v = parseFloat(document.getElementById(`sl-${k}`).value);
    document.getElementById(`v-${k}`).textContent = v;
    return v;
  });
  const total = vals.reduce((a,b)=>a+b,0);
  const m = getMention(total);
  setText('total-score', total.toFixed(1));
  const mb = document.getElementById('total-mention');
  mb.textContent = m.label; mb.className = `badge tb-mention ${m.cls}`;
}

function getMention(s){
  if(s>=80) return{label:t('badge_excellent'),cls:'b-excellent'};
  if(s>=65) return{label:t('badge_bon'),cls:'b-bon'};
  if(s>=50) return{label:t('badge_moyen'),cls:'b-moyen'};
  return{label:t('badge_non_retenu'),cls:'b-nonretenu'};
}

async function saveScore(){
  if(!currentCandidatId) return;
  const btn = document.getElementById('save-btn');
  btn.disabled = true; btn.textContent = '⏳…';
  try{
    const body = {
      score_niveau:      parseFloat(document.getElementById('sl-niveau').value),
      score_experience:  parseFloat(document.getElementById('sl-experience').value),
      score_motivation:  parseFloat(document.getElementById('sl-motivation').value),
      score_adequation:  parseFloat(document.getElementById('sl-adequation').value),
      score_dossier:     parseFloat(document.getElementById('sl-dossier').value),
      score_disponibilite:parseFloat(document.getElementById('sl-disponibilite').value),
      note_evaluateur:   document.getElementById('note-field').value,
    };
    const res = await fetch(`/api/candidate/${currentCandidatId}/score`,
      {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
    const d = await res.json();
    if(d.success){
      showToast(t('toast_saved'));
      loadStats();
      tableLoaded = false; // force reload when going back
    }
  } finally {
    btn.disabled=false; btn.textContent=t('btn_save');
  }
}

/* ══════════════════════════════════════════
   STATS PAGE
   ══════════════════════════════════════════ */
async function loadStatsPage(){
  if(!statsData) await loadStats();
  const d = statsData;
  const container = document.getElementById('stats-detail-content');
  const evalTotal = Math.max(d.evalues,1);

  container.innerHTML = `
    <div class="panel">
      <div class="panel-title">📊 ${t('specialty_repartition')}</div>
      ${d.by_specialty.map(s=>`
        <div class="sp-row">
          <div class="sp-hd"><span>${esc(s.specialty||'Non spécifié')}</span><span>${s.cnt}</span></div>
          <div class="sp-bg"><div class="sp-fill" style="width:${Math.round(s.cnt/Math.max(...d.by_specialty.map(x=>x.cnt),1)*100)}%"></div></div>
        </div>`).join('')}
    </div>
    <div class="panel">
      <div class="panel-title">🏆 ${t('mentions_results')}</div>
      <div style="margin-bottom:.5rem">
        <div class="mention-row m-ex"><span class="mention-lbl">${t('mention_excellent')}</span><div class="mbar-bg"><div class="mbar-fill" style="width:${Math.round(d.excellent/evalTotal*100)}%"></div></div><span class="mention-cnt">${d.excellent}</span></div>
        <div class="mention-row m-bo"><span class="mention-lbl">${t('mention_bon')}</span><div class="mbar-bg"><div class="mbar-fill" style="width:${Math.round(d.bon/evalTotal*100)}%"></div></div><span class="mention-cnt">${d.bon}</span></div>
        <div class="mention-row m-mo"><span class="mention-lbl">${t('mention_moyen')}</span><div class="mbar-bg"><div class="mbar-fill" style="width:${Math.round(d.moyen/evalTotal*100)}%"></div></div><span class="mention-cnt">${d.moyen}</span></div>
        <div class="mention-row m-nr"><span class="mention-lbl">${t('mention_non_retenu')}</span><div class="mbar-bg"><div class="mbar-fill" style="width:${Math.round(d.non_retenu/evalTotal*100)}%"></div></div><span class="mention-cnt">${d.non_retenu}</span></div>
      </div>
    </div>
    <div class="panel">
      <div class="panel-title">📋 ${lang==='ar'?'ملخص الأرقام':'Chiffres clés'}</div>
      ${[
        {l:lang==='ar'?'إجمالي الرسائل':'Total e-mails reçus', v:fmt(d.total_emails)},
        {l:lang==='ar'?'مترشحون فريدون':'Candidats uniques (dans les délais)', v:fmt(d.total)},
        {l:lang==='ar'?'خارج الموعد':'Candidatures hors délai', v:fmt(d.hors_delai)},
        {l:lang==='ar'?'رسائل مكررة':'Doublons (même personne)', v:fmt(d.duplicates)},
        {l:lang==='ar'?'ملفات مكتملة':'Dossiers complets', v:fmt(d.complet)},
        {l:lang==='ar'?'ملفات جزئية':'Dossiers partiels', v:fmt(d.partiel)},
        {l:lang==='ar'?'ملفات فارغة':'Dossiers vides', v:fmt(d.vide)},
        {l:lang==='ar'?'تم تقييمهم':'Candidats évalués', v:fmt(d.evalues)},
        {l:lang==='ar'?'يبقى لتقييم':'Reste à évaluer', v:fmt(d.total-d.evalues)},
      ].map(row=>`<div class="info-row"><span class="ir-lbl">${row.l}</span><span class="ir-val" style="font-family:'IBM Plex Mono',monospace">${row.v}</span></div>`).join('')}
    </div>`;
}

/* ══════════════════════════════════════════
   HELPERS
   ══════════════════════════════════════════ */
function debounce(fn,ms){let t;return(...a)=>{clearTimeout(t);t=setTimeout(()=>fn(...a),ms)}}
function fmt(n){return (n||0).toLocaleString('fr-FR')}
function esc(s){return String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')}
function setText(id,v){const el=document.getElementById(id);if(el)el.textContent=v}

function scoreColor(s){
  if(s>=80)return'var(--green)';if(s>=65)return'var(--blue)';
  if(s>=50)return'var(--yellow)';return'var(--red)';
}
function statusBadge(s){
  const m={Complet:`b-complet ${t('badge_complet')}`,Partiel:`b-partiel ${t('badge_partiel')}`,
           Incomplet:`b-incomplet ${t('badge_incomplet')}`,Vide:`b-vide ${t('badge_vide')}`};
  const [cls,...w]=(m[s]||`b-vide ${s}`).split(' ');
  return `<span class="badge ${cls}">${w.join(' ')}</span>`;
}
function mentionBadge(m){
  if(!m)return`<span class="badge b-pending">${t('badge_pending')}</span>`;
  const mp={Excellent:`b-excellent ${t('badge_excellent')}`,Bon:`b-bon ${t('badge_bon')}`,
            Moyen:`b-moyen ${t('badge_moyen')}`,'Non retenu':`b-nonretenu ${t('badge_non_retenu')}`};
  const [cls,...w]=(mp[m]||`b-pending ${m}`).split(' ');
  return `<span class="badge ${cls}">${w.join(' ')}</span>`;
}

function showToast(msg){
  const t=document.getElementById('toast');
  t.textContent=msg; t.classList.add('show');
  setTimeout(()=>t.classList.remove('show'), 3000);
}

function exportCSV(){ window.location='/api/export/csv' }

/* ══════════════════════════════════════════
   INIT
   ══════════════════════════════════════════ */
loadStats();
applyTranslations();
