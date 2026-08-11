// ── Bluestone SEO Dashboard Logic ──

let appData = null;
let currentTab = "post_july16";
let currentSortField = "raw_date";
let currentSortOrder = "desc";
let dailyChart = null;
let rankingChart = null;
let indexingChart = null;

document.addEventListener("DOMContentLoaded", () => {
  fetchDashboardData();
  setupEventListeners();
});

async function fetchDashboardData() {
  try {
    const res = await fetch("dashboard_data.json?t=" + Date.now());
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

    // Render KPIs, Weekly Table & Charts
    renderKpiCards();
    renderWeeklyPublishTable();
    renderDailyTrendChart();
    renderRankBreakdownTable();
    renderIndexingTrendChart();

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
  const stratComp = (appData.metadata && appData.metadata.strategy_comparison) ? appData.metadata.strategy_comparison : null;

  // Post July 16
  const postPublished = postBlogs.length;
  const postIndexed = stratComp ? stratComp.new_strategy.indexed_count : postBlogs.filter(b => b.impressions > 0).length;
  const postClicks = postBlogs.reduce((acc, b) => acc + b.clicks, 0);
  const postImpressions = postBlogs.reduce((acc, b) => acc + b.impressions, 0);
  const postIndexedPct = stratComp ? stratComp.new_strategy.indexing_rate.toFixed(1) : (postPublished ? ((postIndexed / postPublished) * 100).toFixed(1) : "0.0");

  document.getElementById("stratNewPublished").innerText = postPublished;
  document.getElementById("stratNewIndexed").innerText = postIndexed;
  document.getElementById("stratNewIndexedPct").innerText = `${postIndexedPct}% indexed`;
  document.getElementById("stratNewClicks").innerText = postClicks.toLocaleString();
  document.getElementById("stratNewImpressions").innerText = postImpressions.toLocaleString();

  // Pre July 16
  const prePublished = preBlogs.length;
  const preIndexed = stratComp ? stratComp.legacy_strategy.indexed_count : preBlogs.filter(b => b.impressions > 0).length;
  const preClicks = preBlogs.reduce((acc, b) => acc + b.clicks, 0);
  const preImpressions = preBlogs.reduce((acc, b) => acc + b.impressions, 0);
  const preIndexedPct = stratComp ? stratComp.legacy_strategy.indexing_rate.toFixed(1) : (prePublished ? ((preIndexed / prePublished) * 100).toFixed(1) : "0.0");

  document.getElementById("stratLegacyPublished").innerText = prePublished.toLocaleString();
  document.getElementById("stratLegacyIndexed").innerText = preIndexed.toLocaleString();
  document.getElementById("stratLegacyIndexedPct").innerText = `${preIndexedPct}% indexed`;
  document.getElementById("stratLegacyClicks").innerText = preClicks.toLocaleString();
  document.getElementById("stratLegacyImpressions").innerText = preImpressions.toLocaleString();

  // Dynamically update the chart article badge
  const badge = document.getElementById("chartArticleBadge");
  if (badge) {
    badge.innerHTML = `⚡ ${postIndexed} New Articles | 📜 ${preIndexed} Old Articles`;
  }
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

  // Dynamic fallback for exact Calendar Week (Mon-Today vs Prev Mon-Sun)
  if (!thisWeek && allBlogs.length) {
    const now = new Date();
    const dayOfWeek = now.getDay(); // 0 is Sun, 1 is Mon...
    const distToMon = (dayOfWeek + 6) % 7;
    const currentMon = new Date(now.getFullYear(), now.getMonth(), now.getDate() - distToMon);
    const prevMon = new Date(currentMon.getTime() - 7 * 24 * 60 * 60 * 1000);

    allBlogs.forEach(b => {
      if (b.raw_date) {
        const parts = b.raw_date.split("T")[0].split("-");
        const dt = new Date(parseInt(parts[0]), parseInt(parts[1]) - 1, parseInt(parts[2]));
        if (!isNaN(dt.getTime())) {
          if (dt >= currentMon && dt <= now) {
            thisWeek++;
          } else if (dt >= prevMon && dt < currentMon) {
            lastWeek++;
          }
        }
      }
    });
  }

  let totalClicks = 0;
  let totalImpressions = 0;
  let ctrs = [];
  let positions = [];
  let windowIndexedCount = 0;

  allBlogs.forEach(b => {
    totalClicks += b.clicks;
    totalImpressions += b.impressions;
    if (b.impressions > 0) {
      ctrs.push(b.ctr);
      windowIndexedCount++;
    }
    if (b.position > 0) {
      positions.push(b.position);
    }
  });

  const indexedCount = stratComp && stratComp.overall ? stratComp.overall.indexed_count : windowIndexedCount;
  const avgCtr = ctrs.length ? (ctrs.reduce((a,b)=>a+b,0)/ctrs.length).toFixed(2) : "0.00";
  const avgPos = positions.length ? (positions.reduce((a,b)=>a+b,0)/positions.length).toFixed(1) : "0.0";
  const indexingRate = stratComp && stratComp.overall ? stratComp.overall.indexing_rate.toFixed(1) : (allBlogs.length ? ((indexedCount / allBlogs.length) * 100).toFixed(1) : "0.0");

  if (document.getElementById("kpiClicks")) document.getElementById("kpiClicks").innerText = totalClicks.toLocaleString();
  if (document.getElementById("kpiImpressions")) document.getElementById("kpiImpressions").innerText = totalImpressions.toLocaleString();
  if (document.getElementById("kpiCtr")) document.getElementById("kpiCtr").innerText = `${avgCtr}%`;
  if (document.getElementById("kpiIndexing")) document.getElementById("kpiIndexing").innerText = `${indexingRate}%`;
  if (document.getElementById("kpiIndexingSub")) document.getElementById("kpiIndexingSub").innerText = `${indexedCount} / ${allBlogs.length} total blogs active`;
}

function renderWeeklyPublishTable() {
  if (!appData) return;
  const tbody = document.getElementById("weeklyPublishTableBody");
  if (!tbody) return;

  const allBlogs = appData.all_blogs || [];
  const now = new Date();
  
  // Calculate start of current week (Monday)
  const dayOfWeek = now.getDay();
  const distToMon = (dayOfWeek + 6) % 7;
  const currentMon = new Date(now.getFullYear(), now.getMonth(), now.getDate() - distToMon);

  // Define 4 weekly buckets (Week 4 is current week, Week 1 is 3 weeks ago)
  const weeks = [];
  for (let i = 0; i < 4; i++) {
    const wStart = new Date(currentMon.getTime() - (3 - i) * 7 * 24 * 60 * 60 * 1000);
    const wEnd = new Date(wStart.getTime() + 6 * 24 * 60 * 60 * 1000);
    weeks.push({
      start: wStart,
      end: wEnd,
      label: `${wStart.getDate()} ${getMonthName(wStart.getMonth())} - ${wEnd.getDate()} ${getMonthName(wEnd.getMonth())}`,
      isCurrent: i === 3,
      count: 0
    });
  }

  // Count publications per week bucket
  // Parse dates using local components to avoid UTC vs local timezone mismatch
  allBlogs.forEach(b => {
    if (b.raw_date) {
      const parts = b.raw_date.split("T")[0].split("-");
      const dt = new Date(parseInt(parts[0]), parseInt(parts[1]) - 1, parseInt(parts[2]));
      if (!isNaN(dt.getTime())) {
        weeks.forEach(w => {
          if (dt >= w.start && dt <= w.end) {
            w.count++;
          }
        });
      }
    }
  });

  // Render reverse order (current week first)
  let html = "";
  weeks.reverse().forEach(w => {
    const badge = w.isCurrent ? '<span style="font-size:0.62rem; background:#4f46e5; color:#fff; padding:1px 4px; border-radius:3px; white-space:nowrap; margin-left:3px;">Now</span>' : '';
    const sameMonth = (w.start.getMonth() === w.end.getMonth());
    const shortLabel = sameMonth 
      ? `${w.start.getDate()} - ${w.end.getDate()} ${getMonthName(w.start.getMonth())}`
      : `${w.start.getDate()} ${getMonthName(w.start.getMonth())} - ${w.end.getDate()} ${getMonthName(w.end.getMonth())}`;

    html += `
      <tr style="${w.isCurrent ? 'font-weight:600; background:rgba(79,70,229,0.04);' : ''}">
        <td style="padding:2px 4px; border-bottom:1px solid #f1f5f9; white-space:nowrap;">${shortLabel} ${badge}</td>
        <td style="padding:2px 4px; text-align:right; border-bottom:1px solid #f1f5f9; font-weight:600;">${w.count}</td>
      </tr>
    `;
  });

  tbody.innerHTML = html;
}

function getMonthName(mIndex) {
  const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  return months[mIndex] || "";
}

function renderDailyTrendChart() {
  const canvas = document.getElementById("dailyTrendChart");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  if (dailyChart) dailyChart.destroy();

  const rawTrends = appData.daily_trends || [];
  if (!rawTrends.length) return;

  // Filter to last 14 days only
  const last14 = rawTrends.slice(-14);

  // Format date labels as "1 Aug", "2 Aug", "30 Jul"
  const dates = last14.map(d => {
    if (d.date_formatted) return d.date_formatted;
    const parts = d.date.split("-"); // YYYY-MM-DD
    if (parts.length === 3) {
      const day = parseInt(parts[2], 10);
      const mIdx = parseInt(parts[1], 10) - 1;
      return `${day} ${getMonthName(mIdx)}`;
    }
    return d.date;
  });

  const newClicks = last14.map(d => d.new_clicks || 0);
  const oldClicks = last14.map(d => d.old_clicks || 0);
  const totalImpressions = last14.map(d => d.impressions || 0);

  dailyChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: dates,
      datasets: [
        {
          label: "New Strategy Clicks",
          data: newClicks,
          borderColor: "#4f46e5",
          backgroundColor: "rgba(79, 70, 229, 0.12)",
          borderWidth: 3,
          pointRadius: 4,
          pointHoverRadius: 7,
          pointBackgroundColor: "#4f46e5",
          fill: true,
          tension: 0.3,
          yAxisID: "yClicks"
        },
        {
          label: "Old Strategy Clicks",
          data: oldClicks,
          borderColor: "#94a3b8",
          backgroundColor: "rgba(148, 163, 184, 0.05)",
          borderWidth: 2,
          borderDash: [3, 3],
          pointRadius: 3,
          pointHoverRadius: 6,
          pointBackgroundColor: "#94a3b8",
          fill: false,
          tension: 0.3,
          yAxisID: "yClicks"
        },
        {
          label: "Total Impressions",
          data: totalImpressions,
          borderColor: "#06b6d4",
          backgroundColor: "transparent",
          borderWidth: 2,
          borderDash: [5, 4],
          pointRadius: 2,
          pointHoverRadius: 5,
          pointBackgroundColor: "#06b6d4",
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
        legend: {
          position: "top",
          labels: { color: "#334155", font: { family: "Inter", size: 12, weight: "500" }, usePointStyle: true, boxWidth: 8 }
        }
      },
      scales: {
        x: { ticks: { color: "#64748b", font: { size: 11 } }, grid: { display: false } },
        yClicks: {
          type: "linear",
          display: true,
          position: "left",
          title: { display: true, text: "Clicks", color: "#4f46e5", font: { size: 11, weight: "600" } },
          ticks: { color: "#4f46e5", font: { size: 11 } },
          grid: { color: "#f1f5f9" }
        },
        yImpressions: {
          type: "linear",
          display: true,
          position: "right",
          title: { display: true, text: "Impressions", color: "#06b6d4", font: { size: 11, weight: "600" } },
          ticks: { color: "#06b6d4", font: { size: 11 } },
          grid: { drawOnChartArea: false }
        }
      }
    }
  });
}

function renderRankBreakdownTable() {
  const tbody = document.getElementById("rankBreakdownBody");
  if (!tbody || !appData) return;

  const rbData = (appData.metadata && appData.metadata.rank_breakdown_3w) ? appData.metadata.rank_breakdown_3w : null;

  let labels = ["3W Ago", "2W Ago", "Latest Week"];
  if (rbData && rbData.week_labels && rbData.week_labels.length === 3) {
    labels = rbData.week_labels;
  }

  if (document.getElementById("rbColW1")) document.getElementById("rbColW1").innerText = labels[0];
  if (document.getElementById("rbColW2")) document.getElementById("rbColW2").innerText = labels[1];
  if (document.getElementById("rbColW3")) document.getElementById("rbColW3").innerText = labels[2];

  let groupData = null;
  if (rbData) {
    if (currentTab === "post_july16") groupData = rbData.new_strategy;
    else if (currentTab === "pre_july16") groupData = rbData.legacy_strategy;
    else if (currentTab === "top100") groupData = rbData.top100;
    else if (currentTab === "striking") groupData = rbData.striking;
    else groupData = rbData.overall;
  }

  // Fallback if metadata not present
  if (!groupData) {
    const dataset = getActiveDataset();
    const b1 = { pos1_3: 0, pos4_10: 0, pos11_20: 0, pos21_plus: 0, unindexed: 0 };
    const b2 = { pos1_3: 0, pos4_10: 0, pos11_20: 0, pos21_plus: 0, unindexed: 0 };
    const b3 = { pos1_3: 0, pos4_10: 0, pos11_20: 0, pos21_plus: 0, unindexed: 0 };

    dataset.forEach(b => {
      const wr = b.weekly_rank || {};
      const p1 = wr.w1_pos || 0, i1 = wr.w1_imp || 0;
      if (i1 === 0) b1.unindexed++;
      else if (p1 > 0 && p1 <= 3) b1.pos1_3++;
      else if (p1 > 3 && p1 <= 10) b1.pos4_10++;
      else if (p1 > 10 && p1 <= 20) b1.pos11_20++;
      else b1.pos21_plus++;

      const p2 = wr.w2_pos || 0, i2 = wr.w2_imp || 0;
      if (i2 === 0) b2.unindexed++;
      else if (p2 > 0 && p2 <= 3) b2.pos1_3++;
      else if (p2 > 3 && p2 <= 10) b2.pos4_10++;
      else if (p2 > 10 && p2 <= 20) b2.pos11_20++;
      else b2.pos21_plus++;

      const p3 = wr.w3_pos || 0, i3 = wr.w3_imp || 0;
      if (i3 === 0) b3.unindexed++;
      else if (p3 > 0 && p3 <= 3) b3.pos1_3++;
      else if (p3 > 3 && p3 <= 10) b3.pos4_10++;
      else if (p3 > 10 && p3 <= 20) b3.pos11_20++;
      else b3.pos21_plus++;
    });
    groupData = { w1: b1, w2: b2, w3: b3 };
  }

  const w1 = groupData.w1 || {};
  const w2 = groupData.w2 || {};
  const w3 = groupData.w3 || {};

  const rows = [
    { key: "pos1_3", label: "Pos 1-3", color: "#10b981", type: "positive" },
    { key: "pos4_10", label: "Pos 4-10", color: "#06b6d4", type: "positive" },
    { key: "pos11_20", label: "Pos 11-20", color: "#f59e0b", type: "mid" },
    { key: "pos21_plus", label: "Pos 21+", color: "#ef4444", type: "lower" }
  ];

  let html = "";
  rows.forEach(r => {
    const c1 = w1[r.key] || 0;
    const c2 = w2[r.key] || 0;
    const c3 = w3[r.key] || 0;

    let trendBadge = "";
    const diff = c3 - c1;

    if (r.type === "positive") {
      if (diff > 0) {
        trendBadge = `<span style="background:#dcfce7; color:#15803d; padding:2px 6px; border-radius:4px; font-weight:600;">📈 +${diff}</span>`;
      } else if (diff === 0) {
        trendBadge = `<span style="background:#f1f5f9; color:#64748b; padding:2px 6px; border-radius:4px;">➖ Steady</span>`;
      } else {
        trendBadge = `<span style="background:#fee2e2; color:#b91c1c; padding:2px 6px; border-radius:4px; font-weight:600;">📉 ${diff}</span>`;
      }
    } else if (r.type === "mid" || r.type === "lower") {
      if (diff < 0) {
        trendBadge = `<span style="background:#dcfce7; color:#15803d; padding:2px 6px; border-radius:4px; font-weight:600;">🚀 Rank Up (${diff})</span>`;
      } else if (diff > 0) {
        trendBadge = `<span style="background:#fef3c7; color:#b45309; padding:2px 6px; border-radius:4px; font-weight:600;">+${diff}</span>`;
      } else {
        trendBadge = `<span style="background:#f1f5f9; color:#64748b; padding:2px 6px; border-radius:4px;">➖ Steady</span>`;
      }
    } else { // unindexed
      if (diff < 0) {
        trendBadge = `<span style="background:#dcfce7; color:#15803d; padding:2px 6px; border-radius:4px; font-weight:600;">⚡ Indexed (+${Math.abs(diff)})</span>`;
      } else if (diff > 0) {
        trendBadge = `<span style="background:#fef3c7; color:#b45309; padding:2px 6px; border-radius:4px;">+${diff} new</span>`;
      } else {
        trendBadge = `<span style="background:#f1f5f9; color:#64748b; padding:2px 6px; border-radius:4px;">➖ Steady</span>`;
      }
    }

    html += `
      <tr>
        <td style="padding:6px 8px; border-bottom:1px solid #f1f5f9; font-weight:500;">
          <span style="display:inline-block; width:8px; height:8px; border-radius:50%; background:${r.color}; margin-right:6px;"></span>
          ${r.label}
        </td>
        <td style="padding:6px 8px; text-align:right; border-bottom:1px solid #f1f5f9; color:#64748b;">${c1}</td>
        <td style="padding:6px 8px; text-align:right; border-bottom:1px solid #f1f5f9; color:#64748b;">${c2}</td>
        <td style="padding:6px 8px; text-align:right; border-bottom:1px solid #f1f5f9; font-weight:700; color:#0f172a;">${c3}</td>
        <td style="padding:6px 8px; text-align:right; border-bottom:1px solid #f1f5f9;">${trendBadge}</td>
      </tr>
    `;
  });

  tbody.innerHTML = html;
}

function renderIndexingTrendChart() {
  const canvas = document.getElementById("indexingTrendChart");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  if (indexingChart) indexingChart.destroy();

  const rawTrend = appData.post_july16_indexing_trend || [];
  if (!rawTrend.length) return;

  // Filter to last 7 days only
  const trendData = rawTrend.slice(-7);

  const labels = trendData.map(d => d.date_formatted);
  const dailyIndexed = trendData.map(d => d.daily_indexed);
  const cumulative = trendData.map(d => d.cumulative_indexed);
  
  // Color coding: Muted slate for pre-API, Vibrant Emerald for Post-Indexing API
  const barColors = trendData.map(d => d.is_api_phase ? "#10b981" : "#94a3b8");
  const barHoverColors = trendData.map(d => d.is_api_phase ? "#059669" : "#64748b");

  indexingChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [
        {
          type: "bar",
          label: "Daily Newly Indexed Articles",
          data: dailyIndexed,
          backgroundColor: barColors,
          hoverBackgroundColor: barHoverColors,
          borderRadius: 4,
          borderSkipped: false,
          yAxisID: "yDaily"
        },
        {
          type: "line",
          label: "Cumulative Indexed Articles",
          data: cumulative,
          borderColor: "#6366f1",
          backgroundColor: "rgba(99, 102, 241, 0.08)",
          borderWidth: 2.5,
          pointRadius: 3,
          pointBackgroundColor: "#6366f1",
          tension: 0.3,
          yAxisID: "yCumulative",
          fill: true
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: "index", intersect: false },
      plugins: {
        legend: {
          position: "top",
          labels: { color: "#334155", font: { family: "Inter", size: 11, weight: "500" }, usePointStyle: true, boxWidth: 8 }
        },
        tooltip: {
          callbacks: {
            footer: (items) => {
              const idx = items[0].dataIndex;
              const item = trendData[idx];
              return item ? `Status: ${item.phase_label}` : "";
            }
          }
        }
      },
      scales: {
        x: { ticks: { color: "#64748b", font: { size: 11 } }, grid: { display: false } },
        yDaily: {
          type: "linear",
          display: true,
          position: "left",
          title: { display: true, text: "Daily Articles", color: "#10b981", font: { size: 11, weight: "600" } },
          ticks: { color: "#10b981", font: { size: 11 }, precision: 0 },
          grid: { color: "#f1f5f9" }
        },
        yCumulative: {
          type: "linear",
          display: true,
          position: "right",
          title: { display: true, text: "Total Indexed", color: "#6366f1", font: { size: 11, weight: "600" } },
          ticks: { color: "#6366f1", font: { size: 11 }, precision: 0 },
          grid: { drawOnChartArea: false }
        }
      }
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
    const isBIndexed = (b.is_indexed !== undefined) ? b.is_indexed : (b.impressions > 0);
    if (indexingFilter === "indexed") matchesIndexing = isBIndexed;
    else if (indexingFilter === "non-indexed") matchesIndexing = !isBIndexed;

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
    const isIndexed = (b.is_indexed !== undefined) ? b.is_indexed : (b.impressions > 0);
    const indexBadgeClass = isIndexed ? "badge-success" : "badge-secondary";
    const indexBadgeText = isIndexed ? "🟢 Indexed" : "⚪ Non-Indexed";

    const isPostJuly16 = b.is_new_strategy;
    const stratGroupBadge = isPostJuly16 ?
      `<span class="badge-status badge-primary"><i class="fa-solid fa-rocket"></i> New Strategy</span>` :
      `<span class="badge-status badge-secondary"><i class="fa-solid fa-clock-rotate-left"></i> Old Strategy</span>`;

    const idxDateHtml = (b.first_indexed_date && b.first_indexed_date !== "Not Indexed Yet") ?
      `<div style="font-size: 0.73rem; margin-top:3px; color: #16a34a; font-weight:600;" title="Date first indexed on Google Search Console"><i class="fa-solid fa-bolt"></i> ${b.first_indexed_date}</div>` :
      `<div style="font-size: 0.72rem; margin-top:3px; color: #94a3b8;"><i class="fa-solid fa-hourglass-start"></i> Pending Index</div>`;

    return `
      <tr>
        <td class="blog-title-cell">
          <a href="${b.link}" target="_blank" class="blog-title-link">${escapeHtml(b.title)}</a>
          <span class="blog-slug">/${b.slug}/</span>
        </td>
        <td>
          <div style="font-weight: 500;">${b.published_date}</div>
          ${idxDateHtml}
        </td>
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

      renderRankBreakdownTable();
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
  
  if (document.getElementById("mPubDate")) {
    document.getElementById("mPubDate").innerText = blog.published_date || "N/A";
  }
  if (document.getElementById("mIdxDate")) {
    const idxStr = blog.first_indexed_date || "Not Indexed Yet";
    let idxLabel = idxStr;
    if (blog.indexing_lag_days !== null && blog.indexing_lag_days !== undefined && idxStr !== "Not Indexed Yet") {
      idxLabel += ` (${blog.indexing_lag_days === 0 ? 'Same Day' : blog.indexing_lag_days + ' day' + (blog.indexing_lag_days === 1 ? '' : 's') + ' lag'})`;
    }
    document.getElementById("mIdxDate").innerText = idxLabel;
  }
  
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
