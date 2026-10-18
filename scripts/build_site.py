"""Build a standalone, dependency-light copy of the dashboard for static hosting (GitHub Pages).

Usage: python scripts/build_site.py
Reads dashboard/index.html and data/sample_data.csv, writes docs/index.html (served by GitHub Pages).
"""

import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
page = open(os.path.join(ROOT, "dashboard", "index.html"), encoding="utf-8").read()
csv = open(os.path.join(ROOT, "data", "sample_data.csv"), encoding="utf-8").read()
# keep the CSV safe inside a <script> block
csv = csv.replace("</", "<\\/")

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI-Powered Sales Analytics · HarpalSinh Jhala</title>
<meta name="description" content="An AI-powered sales analytics dashboard built end to end on a Microsoft Fabric lakehouse by HarpalSinh Jhala.">
<meta name="author" content="HarpalSinh Jhala">
<meta property="og:title" content="AI-Powered Sales Analytics · HarpalSinh Jhala">
<meta property="og:description" content="Microsoft Fabric lakehouse to interactive dashboard, built with AI-assisted analytics engineering.">
<script>try { var t = localStorage.getItem('sd-theme'); if (t) document.documentElement.dataset.theme = t; } catch (e) {}</script>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%23111'/%3E%3Cpath d='M8 22l5-6 4 3 7-9' fill='none' stroke='%23fff' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Newsreader:opsz,wght@6..72,400&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.9.0/d3.min.js"></script>
<style>
:root {
  color-scheme: light;
  --font-anthropic-sans: "Inter", system-ui, -apple-system, "Segoe UI", sans-serif;
  --font-anthropic-serif: "Newsreader", Georgia, "Times New Roman", serif;
  --color-bg: #f7f7f5; --color-panel: #ffffff; --color-fg: #18181b; --color-fg-muted: #71717a;
  --color-border-line: #e7e7e4; --color-ok: #15803d; --color-warn: #b45309; --color-bad: #c2410c;
  --series-1: #4f5bd5;
  --cds-chart-grid: #ececea; --cds-chart-axis: #a1a1aa; --cds-chart-reference: #a1a1aa; --cds-chart-muted: #c9c9c6; --cds-chart-status-critical: #dc2626;
  --cds-surface-popover: #ffffff; --cds-border: #e4e4e7; --cds-shadow-popover: 0 8px 24px rgba(0,0,0,.08), 0 1px 3px rgba(0,0,0,.06);
  --cds-text-secondary: #71717a;
  --cds-font-size-caption: 12px; --cds-font-size-body: 14px; --cds-font-size-heading: 15px; --cds-font-size-title: 30px;
  --cds-font-weight-medium: 500;
  --cds-gap-xs: 4px; --cds-gap-sm: 8px; --cds-gap-md: 14px; --cds-gap-lg: 20px; --cds-gap-xl: 32px;
  --cds-pad-xs: 6px; --cds-pad-sm: 10px; --cds-pad-md: 14px; --cds-pad-lg: 20px; --cds-pad-xl: 28px;
  --cds-radius: 12px; --cds-dur-slow: 220ms; --cds-ease-out: cubic-bezier(.2,.7,.2,1);
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    color-scheme: dark;
    --color-bg: #0f0f11; --color-panel: #17171a; --color-fg: #f4f4f5; --color-fg-muted: #a1a1aa;
    --color-border-line: #26262b; --color-ok: #4ade80; --color-warn: #fbbf24; --color-bad: #fb923c;
    --series-1: #8b94ff;
    --cds-chart-grid: #232328; --cds-chart-axis: #52525b; --cds-chart-reference: #63636b; --cds-chart-muted: #3f3f46; --cds-chart-status-critical: #f87171;
    --cds-surface-popover: #1d1d21; --cds-border: #2e2e34; --cds-shadow-popover: 0 8px 24px rgba(0,0,0,.4);
    --cds-text-secondary: #a1a1aa;
  }
}
:root[data-theme="dark"] {
  color-scheme: dark;
  --color-bg: #0f0f11; --color-panel: #17171a; --color-fg: #f4f4f5; --color-fg-muted: #a1a1aa;
  --color-border-line: #26262b; --color-ok: #4ade80; --color-warn: #fbbf24; --color-bad: #fb923c;
  --series-1: #8b94ff;
  --cds-chart-grid: #232328; --cds-chart-axis: #52525b; --cds-chart-reference: #63636b; --cds-chart-muted: #3f3f46; --cds-chart-status-critical: #f87171;
  --cds-surface-popover: #1d1d21; --cds-border: #2e2e34; --cds-shadow-popover: 0 8px 24px rgba(0,0,0,.4);
  --cds-text-secondary: #a1a1aa;
}
@media (max-width: 600px) { :root { --cds-font-size-title: 26px; } }
* { box-sizing: border-box; }
html, body { margin: 0; }
body { background: var(--color-bg); color: var(--color-fg); font-family: var(--font-anthropic-sans); -webkit-font-smoothing: antialiased; }
#dash-root { padding: clamp(16px, 4vw, 48px) clamp(16px, 4vw, 40px) 40px; }
.dash-skeleton { color: transparent !important; position: relative; }
.dash-skeleton::after { content: ""; position: absolute; inset: 20% 0; max-width: 6rem; border-radius: 6px; background: var(--cds-chart-grid); }
html { scroll-behavior: smooth; }
@media (prefers-reduced-motion: reduce) { html { scroll-behavior: auto; } }

/* Top bar */
.tb { position: sticky; top: 0; z-index: 20; background: color-mix(in srgb, var(--color-bg) 78%, transparent);
  -webkit-backdrop-filter: saturate(160%) blur(14px); backdrop-filter: saturate(160%) blur(14px);
  border-bottom: 1px solid color-mix(in srgb, var(--color-border-line) 85%, transparent); }
.tb-in { max-width: calc(1240px + 2 * clamp(16px, 4vw, 40px)); margin: 0 auto; padding: 10px clamp(16px, 4vw, 40px); display: flex; align-items: center; gap: 16px; }
.tb-brand { display: flex; align-items: center; gap: 10px; color: var(--color-fg); text-decoration: none; font-size: 14px; font-weight: 500; white-space: nowrap; }
.tb-mark { width: 28px; height: 28px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 600; letter-spacing: .03em; color: var(--color-panel);
  background: linear-gradient(135deg, var(--series-1), color-mix(in srgb, var(--series-1) 45%, var(--color-fg))); }
.tb-nav { margin-left: auto; display: flex; gap: 2px; }
.tb-nav a { font-size: 13px; color: var(--color-fg-muted); text-decoration: none; padding: 6px 11px; border-radius: 999px; transition: background var(--cds-dur-slow), color var(--cds-dur-slow); }
.tb-nav a:hover { color: var(--color-fg); background: color-mix(in srgb, var(--color-fg) 6%, transparent); }
.tb-nav a.on { color: var(--color-fg); background: color-mix(in srgb, var(--color-fg) 8%, transparent); }
.tb-theme { all: unset; cursor: pointer; width: 32px; height: 32px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; color: var(--color-fg); border: 1px solid var(--color-border-line); flex: none; transition: background var(--cds-dur-slow); }
.tb-theme:hover { background: color-mix(in srgb, var(--color-fg) 6%, transparent); }
.tb-theme:focus-visible { outline: 2px solid var(--color-fg-muted); outline-offset: 2px; }
.tb-theme svg { width: 16px; height: 16px; }
@media (max-width: 760px) { .tb-nav { display: none; } .tb-theme { margin-left: auto; } }
</style>
</head>
<body>
<script type="text/csv" id="sd-data">__CSV__</script>
<script>
/* Minimal stand-in for the dashboard runtime: one embedded dataset and derived calcs. */
window.dash = (function () {
  const rows = d3.csvParse(document.getElementById('sd-data').textContent);
  const cache = { sample_data: rows }, calcs = {}, subs = [];
  const api = {
    colors: ['var(--series-1)'],
    calc(id, o) { calcs[id] = o; },
    data(id) {
      if (!(id in cache) && calcs[id]) cache[id] = calcs[id].fn(...calcs[id].inputs.map(i => api.data(i).data));
      if (!(id in cache)) return { status: 'missing', data: [], columns: [] };
      const d = cache[id];
      return { status: 'ok', data: d, refreshing: false, meta: [], columns: Array.isArray(d) && d.length ? Object.keys(d[0]) : [] };
    },
    onData(fn) { subs.push(fn); queueMicrotask(fn); },
    refresh() {}, params() { return {}; }, setParams() {}, resetParams() {}, setLink() {}
  };
  let w = window.innerWidth, t;
  window.addEventListener('resize', () => {
    if (window.innerWidth === w) return;
    w = window.innerWidth; clearTimeout(t); t = setTimeout(() => subs.forEach(f => f()), 120);
  });
  return api;
})();
</script>
<header class="tb">
  <div class="tb-in">
    <a class="tb-brand" href="#overview"><span class="tb-mark" aria-hidden="true">HJ</span>HarpalSinh Jhala</a>
    <nav class="tb-nav" aria-label="Sections">
      <a href="#headline">Overview</a>
      <a href="#insights">Insights</a>
      <a href="#trends">Trends</a>
      <a href="#deep-dive">Deep dive</a>
      <a href="#data">Data</a>
    </nav>
    <button class="tb-theme" type="button" aria-label="Switch theme"></button>
  </div>
</header>
<main id="dash-root">
__PAGE__
</main>
<script>
(function () {
  const SUN = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" aria-hidden="true"><circle cx="8" cy="8" r="3"/><path d="M8 1.5v1.5M8 13v1.5M1.5 8H3M13 8h1.5M3.4 3.4l1 1M11.6 11.6l1 1M3.4 12.6l1-1M11.6 4.4l1-1"/></svg>';
  const MOON = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round" aria-hidden="true"><path d="M13.5 9.5A5.5 5.5 0 0 1 6.5 2.5a5.5 5.5 0 1 0 7 7z"/></svg>';
  const html = document.documentElement, btn = document.querySelector('.tb-theme');
  const current = () => html.dataset.theme || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  const paint = () => {
    const dark = current() === 'dark';
    btn.innerHTML = dark ? SUN : MOON;
    btn.setAttribute('aria-label', dark ? 'Switch to light mode' : 'Switch to dark mode');
  };
  btn.addEventListener('click', () => {
    const next = current() === 'dark' ? 'light' : 'dark';
    html.dataset.theme = next;
    try { localStorage.setItem('sd-theme', next); } catch (e) {}
    paint();
  });
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', paint);
  paint();

  // highlight the section in view
  const links = [...document.querySelectorAll('.tb-nav a')];
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(entries => entries.forEach(e => {
      if (e.isIntersecting) links.forEach(a => a.classList.toggle('on', a.getAttribute('href') === '#' + e.target.id));
    }), { rootMargin: '-40% 0px -55% 0px' });
    links.forEach(a => { const s = document.querySelector(a.getAttribute('href')); if (s) io.observe(s); });
  }
})();
</script>
</body>
</html>
"""

out = TEMPLATE.replace("__CSV__", csv).replace("__PAGE__", page)
os.makedirs(os.path.join(ROOT, "docs"), exist_ok=True)
with open(os.path.join(ROOT, "docs", "index.html"), "w", encoding="utf-8") as f:
    f.write(out)
print("wrote docs/index.html", len(out), "bytes")
