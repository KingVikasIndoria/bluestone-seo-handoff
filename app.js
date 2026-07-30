// ── Bluestone SEO Dashboard Logic ──

let appData = null;
let currentTab = "post_july16";
let currentSortField = "raw_date";
let currentSortOrder = "desc";
let dailyChart = null;
let rankingChart = null;

document.addEventListener("DOMContentLoaded", () => {
  fetchDashboardData();
  setupEventListeners();
});

async function fetchDashboardData() {
  try {
    const res = await fetch("dashboard_data.json");
    if (!res.ok) throw new Error("Failed to load dashboard_data.json");
    appData = await res.json();
    
    // Update Sync Badge
    const syncBadge = document.getElementById("syncBadge");
    if (syncBadge && appData.metadata) {
      syncBadge.innerHTML = `<i class="fa-solid fa-circle-check"></i> Last Synced: ${appData.metadata.generated_at}`;
    }

    // Populate Tab Counts
    if (document.getElementById("countPostJuly16")) {
      document.getElementById("countPostJuly16").innerText = (appData.post_july16_blogs || []).length;
    }
    if (document.getElementById("countPreJuly16")) {
      document.getElementById("countPreJuly16").innerText = (appData.pre_july16_blogs || []).length;
    }
    if (document.getElementById("countAll")) {
      document.getElementById("countAll").innerText = (appData.all_blogs || []).length;
    }
    if (document.getElementById("countTop100")) {
      document.getElementById("countTop100").innerText = (appData.top_100_performing || []).length;
    }
    if (document.getElementById("countStriking")) {
      document.getElementById("countStriking").innerText = (appData.striking_distance || []).length;
    }

    // Render Strategy Comparison Metrics
    renderStrategyBanner();

    // Render KPIs & Charts
    renderKpiCards();
    renderDailyTrendChart();
    renderRankingDistChart();

    // Render Table
    renderTable();

  } catch (err) {
    console.error("Error loading dashboard data:", err);
    document.getElementById("syncBadge").innerHTML = `<i class="fa-solid fa-triangle-exclamation" style="color:#dc2626"></i> Error loading data`;
    document.getElementById("blogsTableBody").innerHTML = `
      <tr>
        <td colspan="10" class="text-center" style="padding: 40px; color: #dc2626;">
          <i class="fa-solid fa-triangle-exclamation fa-2x"></i><br><br>
          Failed to load <code>dashboard_data.json</code>.<br>
          Run <code>python3 scripts/generate_dashboard_dataset.py</code> to build the dataset.
        </td>
      </tr>
    `;
  }
}

function renderStrategyBanner() {
  if (!appData || !appData.post_july16_blogs || !appData.pre_july16_blogs) return;

  const postBlogs = appData.post_july16_blogs;
  const preBlogs = appData.pre_july16_blogs;

  // Post July 16
  const postPublished = postBlogs.length;
  const postIndexed = postBlogs.filter(b => b.impressions > 0).length;
  const postClicks = postBlogs.reduce((acc, b) => acc + b.clicks, 0);
  const postImpressions = postBlogs.reduce((acc, b) => acc + b.impressions, 0);
  const postIndexedPct = postPublished ? ((postIndexed / postPublished) * 100).toFixed(1) : "0.0";

  document.getElementById("stratNewPublished").innerText = postPublished;
  document.getElementById("stratNewIndexed").innerText = postIndexed;
  document.getElementById("stratNewIndexedPct").innerText = `${postIndexedPct}% indexed`;
  document.getElementById("stratNewClicks").innerText = postClicks.toLocaleString();
  document.getElementById("stratNewImpressions").innerText = postImpressions.toLocaleString();

  // Pre July 16
  const prePublished = preBlogs.length;
  const preIndexed = preBlogs.filter(b => b.impressions > 0).length;
  const preClicks = preBlogs.reduce((acc, b) => acc + b.clicks, 0);
  const preImpressions = preBlogs.reduce((acc, b) => acc + b.impressions, 0);
  const preIndexedPct = prePublished ? ((preIndexed / prePublished) * 100).toFixed(1) : "0.0";

  document.getElementById("stratLegacyPublished").innerText = prePublished.toLocaleString();
  document.getElementById("stratLegacyIndexed").innerText = preIndexed.toLocaleString();
  document.getElementById("stratLegacyIndexedPct").innerText = `${preIndexedPct}% indexed`;
  document.getElementById("stratLegacyClicks").innerText = preClicks.toLocaleString();
  document.getElementById("stratLegacyImpressions").innerText = preImpressions.toLocaleString();
}

function getActiveDataset() {
  if (!appData) return [];
  if (currentTab === "post_july16") return appData.post_july16_blogs || [];
  if (currentTab === "pre_july16") return appData.pre_july16_blogs || [];
  if (currentTab === "top100") return appData.top_100_performing || [];
  if (currentTab === "striking") return appData.striking_distance || [];
  if (currentTab === "all") return appData.all_blogs || [];
  return appData.post_july16_blogs || [];
}

function renderKpiCards() {
  if (!appData) return;
  const allBlogs = appData.all_blogs || [];
  const stratComp = (appData.metadata && appData.metadata.strategy_comparison) ? appData.metadata.strategy_comparison : {};

  let thisWeek = stratComp.published_this_week || 0;
  let lastWeek = stratComp.published_last_week || 0;

  // Dynamic fallback calculation directly from blog post timestamps
  if (!thisWeek && allBlogs.length) {
    let latestMs = 0;
    allBlogs.forEach(b => {
      if (b.raw_date) {
        const ms = new Date(b.raw_date).getTime();
        if (!isNaN(ms) && ms > latestMs) latestMs = ms;
      }
    });
    if (!latestMs) latestMs = Date.now();

    const sevenDaysMs = 7 * 24 * 60 * 60 * 1000;
    const fourteenDaysMs = 14 * 24 * 60 * 60 * 1000;

    allBlogs.forEach(b => {
      if (b.raw_date) {
        const ms = new Date(b.raw_date).getTime();
        if (!isNaN(ms)) {
          const diff = latestMs - ms;
          if (diff >= 0 && diff <= sevenDaysMs) {
            thisWeek++;
          } else if (diff > sevenDaysMs && diff <= fourteenDaysMs) {
            lastWeek++;
          }
        }
      }
    });
  }

  if (document.getElementById("kpiWeeklyVol")) {
    document.getElementById("kpiWeeklyVol").innerText = thisWeek.toLocaleString();
  }
  if (document.getElementById("kpiWeeklyVolSub")) {
    const isUp = thisWeek >= lastWeek;
    const iconClass = isUp ? "fa-arrow-trend-up text-success" : "fa-arrow-trend-down text-muted";
    document.getElementById("kpiWeeklyVolSub").innerHTML = `<i class="fa-solid ${iconClass}"></i> <strong>This Week: ${thisWeek}</strong> vs <strong>Last Week: ${lastWeek}</strong>`;
  }

  let totalClicks = 0;
  let totalImpressions = 0;
  let ctrs = [];
  let positions = [];
  let indexedCount = 0;

  allBlogs.forEach(b => {
    totalClicks += b.clicks;
    totalImpressions += b.impressions;
    if (b.impressions > 0) {
      ctrs.push(b.ctr);
      indexedCount++;
    }
    if (b.position > 0) {
      positions.push(b.position);
    }
  });

  const avgCtr = ctrs.length ? (ctrs.reduce((a,b)=>a+b,0)/ctrs.length).toFixed(2) : "0.00";
  const avgPos = positions.length ? (positions.reduce((a,b)=>a+b,0)/positions.length).toFixed(1) : "0.0";
  const indexingRate = allBlogs.length ? ((indexedCount / allBlogs.length) * 100).toFixed(1) : "0.0";

  if (document.getElementById("kpiClicks")) document.getElementById("kpiClicks").innerText = totalClicks.toLocaleString();
  if (document.getElementById("kpiImpressions")) document.getElementById("kpiImpressions").innerText = totalImpressions.toLocaleString();
  if (document.getElementById("kpiCtr")) document.getElementById("kpiCtr").innerText = `${avgCtr}%`;
  if (document.getElementById("kpiIndexing")) document.getElementById("kpiIndexing").innerText = `${indexingRate}%`;
  if (document.getElementById("kpiIndexingSub")) document.getElementById("kpiIndexingSub").innerText = `${indexedCount} / ${allBlogs.length} total blogs active`;
}

function renderDailyTrendChart() {
  const ctx = document.getElementById("dailyTrendChart").getContext("2d");
  if (dailyChart) dailyChart.destroy();

  const dates = appData.daily_trends.map(d => d.date.substr(5)); // MM-DD
  const clicks = appData.daily_trends.map(d => d.clicks);
  const impressions = appData.daily_trends.map(d => d.impressions);

  dailyChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: dates,
      datasets: [
        {
          label: "Clicks",
          data: clicks,
          borderColor: "#4338ca",
          backgroundColor: "rgba(67, 56, 202, 0.08)",
          fill: true,
          tension: 0.3,
          yAxisID: "yClicks"
        },
        {
          label: "Impressions",
          data: impressions,
          borderColor: "#0284c7",
          backgroundColor: "transparent",
          borderDash: [4, 4],
          tension: 0.3,
          yAxisID: "yImpressions"
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: "index", intersect: false },
      plugins: {
        legend: { labels: { color: "#475569", font: { family: "Inter", size: 12 } } }
      },
      scales: {
        x: { ticks: { color: "#64748b" }, grid: { color: "#f1f5f9" } },
        yClicks: {
          type: "linear",
          display: true,
          position: "left",
          ticks: { color: "#4338ca" },
          grid: { color: "#e2e8f0" }
        },
        yImpressions: {
          type: "linear",
          display: true,
          position: "right",
          ticks: { color: "#0284c7" },
          grid: { drawOnChartArea: false }
        }
      }
    }
  });
}

function renderRankingDistChart() {
  const ctx = document.getElementById("rankingDistChart").getContext("2d");
  if (rankingChart) rankingChart.destroy();

  const dataset = getActiveDataset();
  let top3 = 0, page1 = 0, striking = 0, lowRank = 0, unindexed = 0;

  dataset.forEach(b => {
    if (b.impressions === 0) unindexed++;
    else if (b.position > 0 && b.position <= 3) top3++;
    else if (b.position > 3 && b.position <= 10) page1++;
    else if (b.position > 10 && b.position <= 20) striking++;
    else lowRank++;
  });

  rankingChart = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: [
        `Top 3 Rank (Pos 1-3): ${top3}`,
        `Page 1 (Pos 4-10): ${page1}`,
        `Striking Dist. (Pos 11-20): ${striking}`,
        `Low Rank (Pos 21+): ${lowRank}`,
        `Non-Indexed / Pending: ${unindexed}`
      ],
      datasets: [{
        data: [top3, page1, striking, lowRank, unindexed],
        backgroundColor: [
          "#059669", // Emerald
          "#0284c7", // Sky
          "#d97706", // Amber
          "#dc2626", // Red
          "#94a3b8"  // Slate
        ],
        borderWidth: 2,
        borderColor: "#ffffff"
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { 
          position: "right", 
          labels: { 
            color: "#334155", 
            font: { family: "Inter", size: 11 },
            boxWidth: 12
          } 
        }
      },
      cutout: "65%"
    }
  });
}

function renderTable() {
  const tbody = document.getElementById("blogsTableBody");
  const dataset = getActiveDataset();
  const searchVal = document.getElementById("searchInput").value.toLowerCase().trim();
  const indexingFilter = document.getElementById("indexingFilter").value;
  const healthFilter = document.getElementById("healthFilter").value;

  // Filter
  let filtered = dataset.filter(b => {
    const matchesSearch = !searchVal || 
      b.title.toLowerCase().includes(searchVal) || 
      b.slug.toLowerCase().includes(searchVal) ||
      (b.top_queries && b.top_queries.some(q => q.query.toLowerCase().includes(searchVal)));

    let matchesIndexing = true;
    if (indexingFilter === "indexed") matchesIndexing = b.impressions > 0;
    else if (indexingFilter === "non-indexed") matchesIndexing = b.impressions === 0;

    const matchesHealth = healthFilter === "all" || b.health === healthFilter;

    return matchesSearch && matchesIndexing && matchesHealth;
  });

  // Sort
  filtered.sort((a, b) => {
    let valA = a[currentSortField];
    let valB = b[currentSortField];

    if (typeof valA === "string") valA = valA.toLowerCase();
    if (typeof valB === "string") valB = valB.toLowerCase();

    if (valA < valB) return currentSortOrder === "asc" ? -1 : 1;
    if (valA > valB) return currentSortOrder === "asc" ? 1 : -1;
    return 0;
  });

  document.getElementById("showingCount").innerText = `Showing ${filtered.length} of ${dataset.length} blogs`;

  if (filtered.length === 0) {
    tbody.innerHTML = `
      <tr>
        <td colspan="10" class="text-center" style="padding: 40px; color: #64748b;">
          <i class="fa-solid fa-folder-open fa-2x"></i><br><br>
          No matching blogs found for your filters.
        </td>
      </tr>
    `;
    return;
  }

  tbody.innerHTML = filtered.map(b => {
    const isIndexed = b.impressions > 0;
    const indexBadgeClass = isIndexed ? "badge-success" : "badge-secondary";
    const indexBadgeText = isIndexed ? "🟢 Indexed" : "⚪ Non-Indexed";

    const isPostJuly16 = b.is_post_july16;
    const stratGroupBadge = isPostJuly16 ?
      `<span class="badge-status badge-primary"><i class="fa-solid fa-rocket"></i> Post-July 16</span>` :
      `<span class="badge-status badge-secondary"><i class="fa-solid fa-clock-rotate-left"></i> Pre-July 16</span>`;

    return `
      <tr>
        <td class="blog-title-cell">
          <a href="${b.link}" target="_blank" class="blog-title-link">${escapeHtml(b.title)}</a>
          <span class="blog-slug">/${b.slug}/</span>
        </td>
        <td>${b.published_date}</td>
        <td>${stratGroupBadge}</td>
        <td><span class="badge-status ${indexBadgeClass}">${indexBadgeText}</span></td>
        <td class="text-right font-weight-bold" style="color:#0f172a;">${b.clicks.toLocaleString()}</td>
        <td class="text-right">${b.impressions.toLocaleString()}</td>
        <td class="text-right">${b.ctr.toFixed(2)}%</td>
        <td class="text-right">${b.position > 0 ? b.position.toFixed(1) : '-'}</td>
        <td>
          <span class="badge-status badge-${b.health_color}">
            ${b.health_icon} ${b.health}
          </span>
        </td>
        <td class="text-center">
          <button class="btn-inspect" onclick="openInspector('${b.slug}')">
            <i class="fa-solid fa-magnifying-glass"></i> Inspect
          </button>
        </td>
      </tr>
    `;
  }).join("");
}

function setupEventListeners() {
  // Tabs
  document.querySelectorAll(".tab-btn").forEach(btn => {
    btn.addEventListener("click", (e) => {
      document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
      const target = e.currentTarget;
      target.classList.add("active");
      currentTab = target.getAttribute("data-tab");

      if (currentTab === "post_july16") {
        currentSortField = "raw_date";
        currentSortOrder = "desc";
      } else if (currentTab === "top100") {
        currentSortField = "clicks";
        currentSortOrder = "desc";
      } else if (currentTab === "striking") {
        currentSortField = "impressions";
        currentSortOrder = "desc";
      } else if (currentTab === "pre_july16" || currentTab === "all") {
        currentSortField = "clicks";
        currentSortOrder = "desc";
      }

      renderRankingDistChart();
      renderTable();
    });
  });

  // Search Input
  const searchInput = document.getElementById("searchInput");
  const clearBtn = document.getElementById("clearSearchBtn");

  searchInput.addEventListener("input", () => {
    clearBtn.style.display = searchInput.value ? "block" : "none";
    renderTable();
  });

  clearBtn.addEventListener("click", () => {
    searchInput.value = "";
    clearBtn.style.display = "none";
    renderTable();
  });

  // Indexing Filter
  document.getElementById("indexingFilter").addEventListener("change", () => {
    renderTable();
  });

  // Search Rank Tier Filter
  document.getElementById("healthFilter").addEventListener("change", () => {
    renderTable();
  });

  // Sortable Headers
  document.querySelectorAll(".th-sortable").forEach(th => {
    th.addEventListener("click", () => {
      const field = th.getAttribute("data-sort");
      if (currentSortField === field) {
        currentSortOrder = currentSortOrder === "asc" ? "desc" : "asc";
      } else {
        currentSortField = field;
        currentSortOrder = field === "title" ? "asc" : "desc";
      }
      renderTable();
    });
  });
}

function openInspector(slug) {
  if (!appData) return;
  const blog = appData.all_blogs.find(b => b.slug === slug);
  if (!blog) return;

  document.getElementById("modalTitle").innerText = blog.title;
  document.getElementById("modalLink").href = blog.link;
  
  const healthPill = document.getElementById("modalHealthPill");
  healthPill.className = `badge-status badge-${blog.health_color}`;
  healthPill.innerText = `${blog.health_icon} ${blog.health}`;

  document.getElementById("mClicks").innerText = blog.clicks.toLocaleString();
  document.getElementById("mImpressions").innerText = blog.impressions.toLocaleString();
  document.getElementById("mCtr").innerText = `${blog.ctr.toFixed(2)}%`;
  document.getElementById("mPosition").innerText = blog.position > 0 ? blog.position.toFixed(1) : "N/A";

  const insightTitle = document.getElementById("insightTitle");
  const insightBody = document.getElementById("insightBody");

  if (blog.position > 10 && blog.position <= 20) {
    insightTitle.innerText = "⚡ Striking Distance Opportunity!";
    insightBody.innerText = `This article is ranking on Page 2 (Position ${blog.position}). With ${blog.impressions.toLocaleString()} impressions, adding subheadings & internal links can boost it to Page 1!`;
  } else if (blog.position > 0 && blog.position <= 3) {
    insightTitle.innerText = "🏆 Top Performer!";
    insightBody.innerText = `Great job! This article holds rank #${blog.position}. Ensure links & products stay fresh.`;
  } else if (blog.impressions === 0) {
    insightTitle.innerText = "⚪ Non-Indexed / Pending Article";
    insightBody.innerText = `This URL has not yet generated search impressions on Google. We submitted it to Google Indexing API; expect indexing within 24-48 hours.`;
  } else {
    insightTitle.innerText = "💡 SEO Optimization Recommendation";
    insightBody.innerText = `Article active with ${blog.clicks} clicks and ${blog.impressions.toLocaleString()} impressions.`;
  }

  const qBody = document.getElementById("modalQueriesBody");
  if (!blog.top_queries || blog.top_queries.length === 0) {
    qBody.innerHTML = `<tr><td colspan="5" class="text-center" style="color:#64748b;">No keyword query data recorded for this page yet.</td></tr>`;
  } else {
    qBody.innerHTML = blog.top_queries.map(q => `
      <tr>
        <td class="font-weight-bold">${escapeHtml(q.query)}</td>
        <td class="text-right" style="color:#0f172a;">${q.clicks}</td>
        <td class="text-right">${q.impressions.toLocaleString()}</td>
        <td class="text-right">${q.ctr.toFixed(1)}%</td>
        <td class="text-right">${q.position.toFixed(1)}</td>
      </tr>
    `).join("");
  }

  document.getElementById("inspectorModal").classList.add("active");
}

function closeModal() {
  document.getElementById("inspectorModal").classList.remove("active");
}

function escapeHtml(str) {
  if (!str) return "";
  return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}
