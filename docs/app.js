import {
  filterAndSortTools,
  formatCompactNumber,
  getScoreTier,
  getStatusLabel,
  parseParamsToState,
  serializeStateToParams,
} from "./catalog-logic.js";

const I18N = {
  en: {
    title: "Awesome Antigravity Tools",
    subtitle: "100% Google Antigravity-exclusive tools, extensions, runtime hotfixes & ACP gateways.",
    githubBtn: "GitHub ↗",
    statTools: "Curated Tools",
    statStars: "Combined Stars",
    statHealth: "Active Ratio",
    statScore: "Avg Health Score",
    allCategories: "All",
    allPlatforms: "All Platforms",
    allStatuses: "All Statuses",
    statusHealthy: "Healthy & Active",
    statusStale: "Stale (>180d)",
    sortStars: "Most Stars",
    sortScore: "Health Score",
    sortRecent: "Recently Updated",
    sortName: "Alphabetical (A-Z)",
    searchPlaceholder: "Search tools, tags, languages, ACP, quota... (Press /)",
    resetFilters: "Reset filters",
    emptyMessage: "No Antigravity-exclusive tools matched your current filters.",
    details: "Details",
    compare: "Compare",
    comparing: "Selected ✓",
    openRepo: "Open on GitHub ↗",
    copyLink: "Copy Share Link",
    copied: "Copied ✓",
    exclusivityHeading: "Why 100% Antigravity-Exclusive",
    installHeading: "Quick Install / Usage",
    copyCmd: "Copy",
    compareHeading: "Side-by-Side Tool Comparison",
    footerNote: "Backed by single-source-of-truth",
    contribute: "Contribute",
    auditReport: "Health Report",
    langToggle: "中文",
  },
  zh: {
    title: "Awesome Antigravity Tools",
    subtitle: "纯粹且极致：100% 专为 Google Antigravity 打造的扩展、底层修复与 ACP 网关。",
    githubBtn: "GitHub ↗",
    statTools: "收录专有工具",
    statStars: "生态合计 Stars",
    statHealth: "健康活跃率",
    statScore: "平均健康分",
    allCategories: "全部",
    allPlatforms: "全部平台",
    allStatuses: "全部状态",
    statusHealthy: "活跃健康",
    statusStale: "观察 (>180天)",
    sortStars: "按 Star 排序",
    sortScore: "按健康分排序",
    sortRecent: "按最近更新",
    sortName: "按名称 A-Z",
    searchPlaceholder: "搜索工具名、标签、语言、ACP、配额... (按 / 聚焦)",
    resetFilters: "重置筛选",
    emptyMessage: "当前筛选条件下未找到匹配的 Antigravity 专有工具。",
    details: "查看详情",
    compare: "对比",
    comparing: "已选 ✓",
    openRepo: "访问 GitHub ↗",
    copyLink: "复制分享链接",
    copied: "已复制 ✓",
    exclusivityHeading: "为什么 100% 专属于 Antigravity",
    installHeading: "快速安装 / 使用提示",
    copyCmd: "复制",
    compareHeading: "工具横向对比",
    footerNote: "由单一数据源驱动",
    contribute: "参与贡献",
    auditReport: "巡检报告",
    langToggle: "EN",
  },
};

const state = {
  ...parseParamsToState(window.location.search),
  bundle: null,
  compareIds: [],
  focusedIndex: -1,
};

const els = {
  searchInput: document.getElementById("searchInput"),
  platformFilter: document.getElementById("platformFilter"),
  statusFilter: document.getElementById("statusFilter"),
  sortSelect: document.getElementById("sortSelect"),
  categoryPills: document.getElementById("categoryPills"),
  resultsCount: document.getElementById("resultsCount"),
  resetFiltersBtn: document.getElementById("resetFiltersBtn"),
  emptyResetBtn: document.getElementById("emptyResetBtn"),
  toolsGrid: document.getElementById("toolsGrid"),
  emptyState: document.getElementById("emptyState"),
  langToggle: document.getElementById("langToggle"),
  themeToggle: document.getElementById("themeToggle"),
  toolDialog: document.getElementById("toolDialog"),
  dialogTitle: document.getElementById("dialogTitle"),
  dialogRepo: document.getElementById("dialogRepo"),
  dialogBody: document.getElementById("dialogBody"),
  dialogGithubLink: document.getElementById("dialogGithubLink"),
  dialogCloseBtn: document.getElementById("dialogCloseBtn"),
  dialogCopyUrlBtn: document.getElementById("dialogCopyUrlBtn"),
  compareBar: document.getElementById("compareBar"),
  compareDialog: document.getElementById("compareDialog"),
  compareBody: document.getElementById("compareBody"),
  compareCloseBtn: document.getElementById("compareCloseBtn"),
  statTotalTools: document.getElementById("statTotalTools"),
  statTotalStars: document.getElementById("statTotalStars"),
  statActiveRatio: document.getElementById("statActiveRatio"),
  statAvgScore: document.getElementById("statAvgScore"),
  lastUpdatedText: document.getElementById("lastUpdatedText"),
};

function t(key) {
  return (I18N[state.lang] && I18N[state.lang][key]) || I18N.en[key] || key;
}

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined && text !== null) node.textContent = String(text);
  return node;
}

// Theme toggle following modern-web-guidance `dark-mode-toggle`
function initThemeToggle() {
  const meta = document.querySelector('meta[name="color-scheme"]');
  const getSystemDark = () => window.matchMedia("(prefers-color-scheme: dark)").matches;

  function applySchemeFromStorage() {
    try {
      const saved = localStorage.getItem("color-scheme");
      meta.content = saved === "light" || saved === "dark" ? saved : "light dark";
    } catch {
      meta.content = "light dark";
    }
  }

  els.themeToggle.addEventListener("click", () => {
    let saved = null;
    try {
      saved = localStorage.getItem("color-scheme");
    } catch {}
    const sysDark = getSystemDark();
    const currentlyDark = saved ? saved === "dark" : sysDark;
    const target = currentlyDark ? "light" : "dark";
    const matchesSystem = (target === "dark") === sysDark;

    try {
      if (matchesSystem) {
        localStorage.removeItem("color-scheme");
      } else {
        localStorage.setItem("color-scheme", target);
      }
    } catch {}
    meta.content = matchesSystem ? "light dark" : target;
  });

  window.addEventListener("storage", (e) => {
    if (e.key === "color-scheme") applySchemeFromStorage();
  });
}

// Safari fallback for `closedby="any"` following modern-web-guidance `light-dismiss-a-dialog`
function attachDialogLightDismissFallback(dialog) {
  if (!("closedBy" in HTMLDialogElement.prototype)) {
    dialog.addEventListener("click", (event) => {
      if (event.target !== dialog) return;
      const rect = dialog.getBoundingClientRect();
      const inside =
        rect.top <= event.clientY &&
        event.clientY <= rect.top + rect.height &&
        rect.left <= event.clientX &&
        event.clientX <= rect.left + rect.width;
      if (!inside) dialog.close();
    });
  }
}

function syncUrl() {
  const params = serializeStateToParams(state);
  const qs = params.toString();
  const nextUrl = qs ? `${window.location.pathname}?${qs}` : window.location.pathname;
  window.history.replaceState(null, "", nextUrl);
}

function applyI18n() {
  document.documentElement.lang = state.lang === "zh" ? "zh-CN" : "en";
  for (const node of document.querySelectorAll("[data-i18n]")) {
    const key = node.getAttribute("data-i18n");
    if (key) node.textContent = t(key);
  }
  els.searchInput.placeholder = t("searchPlaceholder");
  els.langToggle.textContent = t("langToggle");
}

function renderSummary() {
  const s = state.bundle.summary;
  els.statTotalTools.textContent = String(s.total_tools);
  els.statTotalStars.textContent = formatCompactNumber(s.total_stars);
  els.statActiveRatio.textContent = `${s.healthy_tools}/${s.total_tools} (${s.health_ratio_pct}%)`;
  els.statAvgScore.textContent = s.average_health_score !== null ? `${s.average_health_score}/100` : "—";
  els.lastUpdatedText.textContent =
    state.lang === "zh"
      ? `最近巡检：${state.bundle.generated_at.replace("T", " ").replace("Z", " UTC")}`
      : `Last audited: ${state.bundle.generated_at.replace("T", " ").replace("Z", " UTC")}`;
}

function populatePlatformSelect() {
  const current = state.platform;
  while (els.platformFilter.options.length > 1) {
    els.platformFilter.remove(1);
  }
  const platforms = state.bundle.summary.by_platform || [];
  for (const p of platforms) {
    const opt = document.createElement("option");
    opt.value = p.name;
    opt.textContent = `${p.name} (${p.count})`;
    els.platformFilter.append(opt);
  }
  els.platformFilter.value = current;
}

function renderCategoryPills() {
  els.categoryPills.textContent = "";
  const counts = {};
  for (const tool of state.bundle.tools) {
    counts[tool.category] = (counts[tool.category] || 0) + 1;
  }

  const allPill = el("button", "pill", `${t("allCategories")} (${state.bundle.tools.length})`);
  allPill.type = "button";
  allPill.role = "tab";
  allPill.setAttribute("aria-selected", String(state.category === "all"));
  allPill.addEventListener("click", () => {
    state.category = "all";
    renderAll();
  });
  els.categoryPills.append(allPill);

  for (const cat of state.bundle.categories) {
    const label = state.lang === "zh" ? cat.name_zh : cat.name_en;
    const pill = el("button", "pill", `${cat.icon} ${label} (${counts[cat.id] || 0})`);
    pill.type = "button";
    pill.role = "tab";
    pill.setAttribute("aria-selected", String(state.category === cat.id));
    pill.addEventListener("click", () => {
      state.category = cat.id;
      renderAll();
    });
    els.categoryPills.append(pill);
  }
}

function openToolDialog(tool) {
  state.openToolId = tool.id;
  syncUrl();
  const tel = tool.telemetry || {};
  els.dialogTitle.textContent = tool.name;
  els.dialogRepo.textContent = tool.repo;
  els.dialogGithubLink.href = tool.url;
  els.dialogBody.textContent = "";

  const desc = el("p", "", state.lang === "zh" ? tool.description_zh : tool.description_en);
  els.dialogBody.append(desc);

  const callout = el("div", "callout-box");
  const strong = el("strong", "", `${t("exclusivityHeading")}: `);
  const reasonText = document.createTextNode(
    state.lang === "zh" ? tool.exclusivity_reason_zh : tool.exclusivity_reason_en
  );
  callout.append(strong, reasonText);
  els.dialogBody.append(callout);

  const grid = el("div", "detail-grid");
  const kvs = [
    ["Status", getStatusLabel(tel.status, state.lang)],
    ["Health Score", tel.health_score != null ? `${tel.health_score}/100` : "—"],
    ["Stars", (tel.stars || 0).toLocaleString()],
    ["Language", tel.language || "—"],
    ["License", tel.license || "—"],
    ["Latest Release", tel.latest_release || "—"],
    ["Last Push", tel.days_inactive != null ? `${tel.days_inactive}d ago` : "—"],
    ["Added", tool.added_at || "—"],
  ];
  for (const [k, v] of kvs) {
    const box = el("div", "detail-kv");
    box.append(el("span", "", k), el("strong", "", v));
    grid.append(box);
  }
  els.dialogBody.append(grid);

  const tagsWrap = el("div", "tag-row");
  for (const p of tool.platforms || []) tagsWrap.append(el("span", "tag tag-muted", p));
  for (const tg of tool.tags || []) tagsWrap.append(el("span", "tag", tg));
  els.dialogBody.append(tagsWrap);

  if (tool.install_hint) {
    const installWrap = el("div");
    installWrap.append(el("p", "stat-label", t("installHeading")));
    const box = el("div", "install-box");
    const code = el("code", "", tool.install_hint);
    const copyBtn = el("button", "btn btn-ghost btn-sm", t("copyCmd"));
    copyBtn.type = "button";
    copyBtn.addEventListener("click", async () => {
      try {
        await navigator.clipboard.writeText(tool.install_hint);
        copyBtn.textContent = t("copied");
        setTimeout(() => (copyBtn.textContent = t("copyCmd")), 1500);
      } catch {}
    });
    box.append(code, copyBtn);
    installWrap.append(box);
    els.dialogBody.append(installWrap);
  }

  if (!els.toolDialog.open) {
    els.toolDialog.showModal();
  }
}

function renderToolsGrid() {
  const visible = filterAndSortTools(state.bundle.tools, state);
  els.toolsGrid.textContent = "";

  const isFiltered =
    Boolean(state.query) || state.category !== "all" || state.platform !== "all" || state.status !== "all";
  els.resetFiltersBtn.hidden = !isFiltered;

  els.resultsCount.textContent =
    state.lang === "zh"
      ? `显示 ${visible.length} / ${state.bundle.tools.length} 款专有工具`
      : `Showing ${visible.length} of ${state.bundle.tools.length} exclusive tools`;

  els.emptyState.hidden = visible.length > 0;

  for (const [idx, tool] of visible.entries()) {
    const tel = tool.telemetry || {};
    const shell = el("div", "tool-card-shell");
    const card = el("article", "tool-card");
    card.dataset.toolId = tool.id;
    card.tabIndex = 0;

    const top = el("div", "card-top");
    const titleWrap = el("div", "card-title-wrap");
    const h3 = el("h3", "card-title");
    const link = el("a", "", tool.name);
    link.href = tool.url;
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    h3.append(link);
    titleWrap.append(h3, el("p", "card-repo", tool.repo));

    const metrics = el("div", "card-metrics");
    metrics.append(el("span", "badge badge-star", `★ ${formatCompactNumber(tel.stars || 0)}`));
    const tier = getScoreTier(tel.health_score);
    const scoreText = tel.health_score != null ? `${tel.health_score}` : "—";
    metrics.append(el("span", `badge badge-${tier}`, `${scoreText}/100`));

    top.append(titleWrap, metrics);

    const desc = el("p", "card-desc", state.lang === "zh" ? tool.description_zh : tool.description_en);

    const tagRow = el("div", "tag-row");
    for (const tg of tool.tags || []) tagRow.append(el("span", "tag", tg));
    if (tel.language) tagRow.append(el("span", "tag tag-muted", tel.language));

    const footer = el("div", "card-footer");
    const metaText = `${getStatusLabel(tel.status, state.lang)}${tel.license ? ` · ${tel.license}` : ""}`;
    footer.append(el("span", "", metaText));

    const actions = el("div", "card-actions");
    const isCompared = state.compareIds.includes(tool.id);
    const cmpBtn = el("button", "btn btn-ghost btn-sm", isCompared ? t("comparing") : t("compare"));
    cmpBtn.type = "button";
    cmpBtn.addEventListener("click", () => toggleCompare(tool.id));

    const detBtn = el("button", "btn btn-primary btn-sm", t("details"));
    detBtn.type = "button";
    detBtn.addEventListener("click", () => openToolDialog(tool));

    actions.append(cmpBtn, detBtn);
    footer.append(actions);

    card.append(top, desc, tagRow, footer);
    shell.append(card);
    els.toolsGrid.append(shell);
  }
}

function toggleCompare(toolId) {
  if (state.compareIds.includes(toolId)) {
    state.compareIds = state.compareIds.filter((id) => id !== toolId);
  } else if (state.compareIds.length < 3) {
    state.compareIds = [...state.compareIds, toolId];
  }
  window.dispatchEvent(new CustomEvent("aat:compare-updated"));
  renderToolsGrid();
}

function resetFilters() {
  state.query = "";
  state.category = "all";
  state.platform = "all";
  state.status = "all";
  state.sort = "stars";
  els.searchInput.value = "";
  els.platformFilter.value = "all";
  els.statusFilter.value = "all";
  els.sortSelect.value = "stars";
  renderAll();
}

function renderAll() {
  applyI18n();
  renderSummary();
  populatePlatformSelect();
  renderCategoryPills();
  renderToolsGrid();
  syncUrl();
  window.dispatchEvent(new CustomEvent("aat:rendered", { detail: { state } }));
}

function bindEvents() {
  els.searchInput.value = state.query;
  els.statusFilter.value = state.status;
  els.sortSelect.value = state.sort;

  els.searchInput.addEventListener("input", () => {
    state.query = els.searchInput.value;
    renderToolsGrid();
    syncUrl();
  });

  els.platformFilter.addEventListener("change", () => {
    state.platform = els.platformFilter.value;
    renderToolsGrid();
    syncUrl();
  });

  els.statusFilter.addEventListener("change", () => {
    state.status = els.statusFilter.value;
    renderToolsGrid();
    syncUrl();
  });

  els.sortSelect.addEventListener("change", () => {
    state.sort = els.sortSelect.value;
    renderToolsGrid();
    syncUrl();
  });

  els.langToggle.addEventListener("click", () => {
    state.lang = state.lang === "en" ? "zh" : "en";
    renderAll();
  });

  els.resetFiltersBtn.addEventListener("click", resetFilters);
  els.emptyResetBtn.addEventListener("click", resetFilters);

  els.dialogCloseBtn.addEventListener("click", () => els.toolDialog.close());
  els.compareCloseBtn.addEventListener("click", () => els.compareDialog.close());

  els.toolDialog.addEventListener("close", () => {
    state.openToolId = "";
    syncUrl();
  });

  els.dialogCopyUrlBtn.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(window.location.href);
      els.dialogCopyUrlBtn.textContent = t("copied");
      setTimeout(() => (els.dialogCopyUrlBtn.textContent = t("copyLink")), 1500);
    } catch {}
  });

  attachDialogLightDismissFallback(els.toolDialog);
  attachDialogLightDismissFallback(els.compareDialog);
}

async function boot() {
  initThemeToggle();
  bindEvents();
  try {
    const resp = await fetch("./catalog-bundle.json", { cache: "no-store" });
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    state.bundle = await resp.json();
    window.__AAT_STATE__ = state;
    renderAll();

    if (state.openToolId) {
      const target = state.bundle.tools.find((item) => item.id === state.openToolId);
      if (target) openToolDialog(target);
    }
  } catch (err) {
    els.resultsCount.textContent = `Failed to load catalog-bundle.json: ${err.message}`;
  }
}

boot();
