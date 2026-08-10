#!/usr/bin/env python3
"""
generate_html.py
Generates the interactive QDA HTML explorer from v4 coded speech files.

Usage (run from project root):
    python skills/qda-outputs/scripts/generate_html.py

Output:
    analysis/results/v4/qda_explorer_v4.html
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from corpus_metadata import (
    build_metadata_index, venue_group_categories, short_group_label,
    VENUE_GROUP_PALETTE, print_warnings,
)
from corpus_data import build_corpus, print_code_warnings

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
CODED_DIR    = PROJECT_ROOT / "analysis" / "coded_speeches" / "v4"
OUTPUT_PATH  = PROJECT_ROOT / "analysis" / "results" / "v4" / "qda_explorer_v4.html"

# NOTE: speech title/venue/event-type/scope are no longer hardcoded here. They are
# derived per-file from the master corpus CSV via corpus_metadata.build_metadata_index()
# (see corpus_metadata.py), so new coded speeches need no script edits and are never
# silently skipped — the old SPEECH_META / SPEECH_META_BY_FILE dicts used to drop any
# file with no matching entry.


# ── Parsing ───────────────────────────────────────────────────────────────────
# All parsing (frontmatter, `[CODE: ...]` tags, passage buffering) now lives in
# corpus_data.py (parse_speech_segments / build_corpus), which generate_xlsx.py
# also consumes — this is the single canonical parse both outputs project from,
# instead of each script maintaining its own regex-based parser that could
# silently diverge from the other's counts.

# ── JavaScript CORPUS builder ─────────────────────────────────────────────────

def js_str(s):
    return (s.replace('\\', '\\\\')
             .replace('"', '\\"')
             .replace('\n', ' ')
             .replace('\r', ''))


def build_corpus_js(files):
    """
    Build the CORPUS JavaScript array string from the already-parsed corpus
    (corpus_data.build_corpus() output, passed in from main()). Every coded file
    is included — files with no CSV match still get an entry (fallback metadata
    from corpus_metadata), they are never silently dropped.
    """
    corpus_parts = []
    total_codes = 0

    for f in files:
        segments = f['segments']
        file_codes = sum(len(s.get('codes', [])) for s in segments if s['type'] == 'coded')
        total_codes += file_codes
        print(f"  {f['filename']}: {len(segments)} segments, {file_codes} code annotations")

        seg_parts = []
        for seg in segments:
            if seg['type'] == 'plain':
                seg_parts.append(f'      {{type:"plain",text:"{js_str(seg["text"])}"}}'  )
            else:
                codes_js = ','.join(
                    f'{{dim:"{c["dim"]}",sub:"{c["sub"]}",memo:"{js_str(c["memo"])}"}}'
                    for c in seg['codes']
                )
                seg_parts.append(
                    f'      {{type:"coded",text:"{js_str(seg["text"])}",codes:[{codes_js}]}}'
                )

        segs_str = ',\n'.join(seg_parts)
        stem = Path(f['filename']).stem
        corpus_parts.append(
            f'  {{id:"{js_str(stem)}",date:"{f["date"]}",'
            f'title:"{js_str(f["speech"])}",'
            f'venue:"{js_str(f["venue"])}",type:"speech",scope:"{f["scope"]}",'
            f'eventType:"{js_str(f["event_type"])}",venueGroup:"{js_str(f.get("venue_group", "Unclassified"))}",\n'
            f'    segments:[\n{segs_str}\n    ]}}'
        )

    print(f"\nTotal code annotations in HTML: {total_codes}")
    return 'const CORPUS = [\n' + ',\n'.join(corpus_parts) + '\n];'


# ── HTML template ─────────────────────────────────────────────────────────────

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Milei Climate Narratives — QDA Explorer v4</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<style>
  :root{--bg:#0f1117;--surface:#1a1d27;--surface2:#22263a;--border:#2e3349;--text:#e2e8f0;--text-muted:#8892aa;--accent:#6366f1;--c-d11:#3B82F6;--c-d12:#F59E0B;--c-d13:#EF4444;--c-ind:#9CA3AF;}
  *{box-sizing:border-box;margin:0;padding:0;}
  body{background:var(--bg);color:var(--text);font-family:'Segoe UI',system-ui,sans-serif;font-size:14px;height:100vh;display:flex;flex-direction:column;overflow:hidden;}
  header{background:var(--surface);border-bottom:1px solid var(--border);padding:0 20px;display:flex;align-items:center;gap:20px;height:52px;flex-shrink:0;}
  header h1{font-size:13px;font-weight:700;color:var(--text-muted);letter-spacing:.05em;text-transform:uppercase;white-space:nowrap;}
  .v4-badge{background:#059669;color:#fff;font-size:10px;font-weight:800;padding:2px 7px;border-radius:4px;}
  nav{display:flex;gap:4px;}
  nav button{background:none;border:none;color:var(--text-muted);padding:6px 14px;border-radius:6px;cursor:pointer;font-size:13px;font-weight:500;transition:all .15s;}
  nav button:hover{background:var(--surface2);color:var(--text);}
  nav button.active{background:var(--accent);color:#fff;}
  .badge{background:var(--surface2);color:var(--text-muted);font-size:10px;padding:1px 6px;border-radius:10px;margin-left:4px;}
  .tab{display:none;flex:1;overflow:hidden;}
  .tab.active{display:flex;}
  /* BROWSE */
  #tab-browse{flex-direction:row;}
  .speech-list{width:220px;flex-shrink:0;background:var(--surface);border-right:1px solid var(--border);display:flex;flex-direction:column;overflow:hidden;}
  .speech-list h2{font-size:11px;font-weight:700;color:var(--text-muted);letter-spacing:.08em;text-transform:uppercase;padding:14px 16px 8px;}
  .speech-list ul{list-style:none;overflow-y:auto;flex:1;}
  .speech-list li{padding:10px 16px;cursor:pointer;border-left:3px solid transparent;transition:all .1s;}
  .speech-list li:hover{background:var(--surface2);}
  .speech-list li.active{background:var(--surface2);border-left-color:var(--accent);}
  .speech-list li .s-date{font-size:10px;color:var(--text-muted);}
  .speech-list li .s-title{font-size:12px;font-weight:600;line-height:1.3;margin-top:2px;}
  .speech-list li .s-meta{display:flex;gap:5px;margin-top:4px;flex-wrap:wrap;}
  .tag{font-size:9px;padding:1px 5px;border-radius:3px;font-weight:700;text-transform:uppercase;letter-spacing:.04em;}
  .reader-toolbar{display:flex;gap:8px;align-items:center;padding:8px 20px;background:var(--surface);border-bottom:1px solid var(--border);flex-wrap:wrap;flex-shrink:0;}
  .toolbar-sep{width:1px;height:20px;background:var(--border);margin:0 4px;}
  .toolbar-label{font-size:11px;color:var(--text-muted);font-weight:600;}
  .filter-chip{border:none;border-radius:20px;padding:3px 10px;font-size:11px;font-weight:700;cursor:pointer;opacity:.4;transition:opacity .15s;}
  .filter-chip.on{opacity:1;}
  .view-toggle{display:flex;background:var(--surface2);border-radius:8px;padding:2px;gap:2px;margin-left:auto;}
  .view-btn{border:none;background:none;color:var(--text-muted);padding:4px 12px;border-radius:6px;cursor:pointer;font-size:11px;font-weight:600;transition:all .15s;white-space:nowrap;}
  .view-btn.active{background:var(--accent);color:#fff;}
  .reader-wrap{flex:1;display:flex;overflow:hidden;}
  .reader{flex:1;overflow-y:auto;padding:24px 32px;line-height:1.8;}
  .reader h2{font-size:16px;font-weight:700;margin-bottom:4px;}
  .reader .meta-row{font-size:11px;color:var(--text-muted);margin-bottom:24px;display:flex;gap:14px;}
  .reader.view-excerpts .plain-block{display:none;}
  .reader.view-full .plain-block{display:block;}
  .plain-block{margin-bottom:14px;color:#9aa3b8;font-size:13.5px;}
  .plain-block.speaker-label{font-size:11px;color:var(--text-muted);font-style:italic;margin-bottom:4px;}
  .coded-block{position:relative;margin-bottom:16px;}
  .coded-block .passage{border-radius:6px;padding:10px 14px;cursor:pointer;transition:filter .15s;line-height:1.7;font-size:13.5px;}
  .coded-block .passage:hover{filter:brightness(1.18);}
  .coded-block.all-filtered .passage{background:rgba(255,255,255,.03)!important;border-left-color:var(--border)!important;cursor:default;}
  .coded-block.all-filtered .passage:hover{filter:none;}
  .reader.view-excerpts .coded-block.all-filtered{display:none;}
  .code-pills{display:flex;gap:5px;flex-wrap:wrap;margin-top:6px;}
  .pill{font-size:9px;font-weight:800;padding:2px 7px;border-radius:10px;letter-spacing:.04em;text-transform:uppercase;color:#fff;}
  .memo-panel{width:310px;flex-shrink:0;background:var(--surface);border-left:1px solid var(--border);display:flex;flex-direction:column;overflow:hidden;}
  .memo-panel .mp-header{padding:14px 16px;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:8px;}
  .memo-panel .mp-header h3{font-size:12px;font-weight:700;color:var(--text-muted);text-transform:uppercase;letter-spacing:.06em;flex:1;}
  .mp-body{overflow-y:auto;flex:1;padding:12px 16px;}
  .memo-item{margin-bottom:14px;}
  .memo-item .mi-code{font-size:10px;font-weight:800;padding:2px 8px;border-radius:4px;color:#fff;display:inline-block;margin-bottom:5px;}
  .memo-item .mi-text{font-size:12px;color:#b0bbd4;line-height:1.6;}
  .memo-placeholder{color:var(--text-muted);font-size:12px;padding:20px 0;text-align:center;}
  .legend{padding:14px 16px;border-top:1px solid var(--border);}
  .legend h4{font-size:10px;font-weight:700;color:var(--text-muted);text-transform:uppercase;margin-bottom:8px;}
  .legend-item{display:flex;align-items:center;gap:7px;margin-bottom:5px;font-size:11px;color:var(--text-muted);}
  .legend-dot{width:10px;height:10px;border-radius:3px;flex-shrink:0;}
  .legend-note{margin-top:10px;font-size:10px;color:var(--text-muted);line-height:1.5;}
  /* PATTERNS */
  #tab-patterns{flex-direction:column;overflow-y:auto;padding:24px 28px;gap:24px;}
  .panel{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:20px;}
  .panel h2{font-size:13px;font-weight:700;margin-bottom:4px;}
  .panel p.sub{font-size:11px;color:var(--text-muted);margin-bottom:16px;}
  .heatmap-wrap{overflow-x:auto;}
  table.heatmap{border-collapse:collapse;font-size:11px;min-width:600px;}
  table.heatmap th{font-size:10px;font-weight:700;color:var(--text-muted);padding:6px 10px;text-align:center;white-space:nowrap;}
  table.heatmap th.row-h{text-align:left;max-width:220px;}
  table.heatmap td{width:44px;height:32px;text-align:center;border:1px solid var(--border);font-size:12px;font-weight:700;}
  table.heatmap td.row-label{text-align:left;padding:0 10px;font-size:11px;color:var(--text-muted);white-space:nowrap;width:220px;}
  .co-occur-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:10px;}
  .co-item{background:var(--surface2);border-radius:6px;padding:10px 12px;}
  .co-item .count{font-size:22px;font-weight:800;}
  .co-item .speeches{font-size:10px;color:var(--text-muted);margin-top:2px;}
  .rank-list{display:flex;flex-direction:column;gap:6px;}
  .rank-row{display:flex;align-items:center;gap:10px;}
  .rank-label{font-size:11px;color:var(--text-muted);width:240px;flex-shrink:0;text-align:right;}
  .rank-bar-wrap{flex:1;background:var(--surface2);border-radius:4px;height:22px;overflow:hidden;}
  .rank-bar{height:100%;border-radius:4px;display:flex;align-items:center;padding-left:8px;font-size:11px;font-weight:800;color:#fff;transition:width .4s;}
  .rank-n{width:28px;font-size:13px;font-weight:800;text-align:right;flex-shrink:0;}
  /* VIZ */
  #tab-viz{flex-direction:column;overflow-y:auto;padding:24px 28px;gap:24px;}
  .viz-grid{display:grid;grid-template-columns:1fr 1fr;gap:20px;}
  .chart-wrap{position:relative;height:320px;}
  .chart-wrap-tall{position:relative;height:420px;}
  .dim-bars{display:flex;gap:16px;margin-top:8px;}
  .dim-bar-item{flex:1;background:var(--surface2);border-radius:8px;padding:14px;text-align:center;}
  .dim-bar-item .db-label{font-size:10px;font-weight:700;text-transform:uppercase;color:var(--text-muted);letter-spacing:.05em;}
  .dim-bar-item .db-n{font-size:36px;font-weight:800;margin:6px 0;}
  .dim-bar-item .db-pct{font-size:12px;color:var(--text-muted);}
  .timeline-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:8px;margin-top:8px;}
  .tl-col{background:var(--surface2);border-radius:6px;padding:10px 8px;}
  .tl-col h4{font-size:9px;font-weight:700;color:var(--text-muted);text-align:center;margin-bottom:8px;line-height:1.3;}
  .tl-dot{border-radius:4px;margin-bottom:3px;padding:2px 5px;font-size:9px;font-weight:700;color:#fff;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
  /* GLOBAL FILTER BAR */
  .global-filter-bar{display:flex;align-items:center;gap:8px;padding:7px 20px;background:var(--surface2);border-bottom:1px solid var(--border);flex-shrink:0;flex-wrap:wrap;}
  .gf-label{font-size:11px;color:var(--text-muted);font-weight:700;letter-spacing:.04em;white-space:nowrap;}
  .gf-sep{width:1px;height:18px;background:var(--border);margin:0 4px;}
  .gf-chip{border:1px solid var(--border);border-radius:20px;padding:3px 11px;font-size:11px;font-weight:700;cursor:pointer;transition:all .15s;background:transparent;color:var(--text-muted);}
  .gf-chip.on{background:var(--chip-c,#555);color:#fff;border-color:transparent;}
  .gf-chip:not(.on){opacity:.4;}
  ::-webkit-scrollbar{width:6px;height:6px;}
  ::-webkit-scrollbar-track{background:transparent;}
  ::-webkit-scrollbar-thumb{background:var(--border);border-radius:3px;}
</style>
</head>
<body>
<header>
  <h1>Milei Climate Narratives · QDA Explorer <span class="v4-badge">V4</span></h1>
  <nav>
    <button class="active" onclick="switchTab('browse',this)">📖 Corpus Browser <span class="badge" id="corpus-badge">—</span></button>
    <button onclick="switchTab('patterns',this)">🔗 Pattern Analysis</button>
    <button onclick="switchTab('viz',this)">📊 Visualizations</button>
  </nav>
</header>
<div class="global-filter-bar">
  <span class="gf-label">Scope:</span>
  <button class="gf-chip on" style="--chip-c:#0f766e" data-scope="National" onclick="toggleGlobalScope(this)">&#127963; National</button>
  <button class="gf-chip on" style="--chip-c:#1d4ed8" data-scope="International" onclick="toggleGlobalScope(this)">&#127760; International</button>
  <div class="gf-sep"></div>
  <span class="gf-label">Venue group:</span>
  <span id="vg-chip-container"></span>
</div>

<div id="tab-browse" class="tab active">
  <div class="speech-list"><h2>Speeches</h2><ul id="speech-nav"></ul></div>
  <div style="flex:1;display:flex;flex-direction:column;overflow:hidden;">
    <div class="reader-toolbar">
      <span class="toolbar-label">Show:</span>
      <button class="filter-chip on" style="background:var(--c-d11);color:#fff" data-dim="D1.1" onclick="toggleFilter(this)">D1.1 Gov/State</button>
      <button class="filter-chip on" style="background:var(--c-d12);color:#fff" data-dim="D1.2" onclick="toggleFilter(this)">D1.2 Science/Experts</button>
      <button class="filter-chip on" style="background:var(--c-d13);color:#fff" data-dim="D1.3" onclick="toggleFilter(this)">D1.3 Cultural</button>
      <button class="filter-chip on" style="background:var(--c-ind);color:#fff" data-dim="IND" onclick="toggleFilter(this)">Inductive</button>
      <div class="toolbar-sep"></div>
      <div class="view-toggle">
        <button class="view-btn active" id="btn-excerpts" onclick="setView('excerpts')">✦ Excerpts</button>
        <button class="view-btn" id="btn-full" onclick="setView('full')">📜 Full Speech</button>
      </div>
    </div>
    <div class="reader-wrap">
      <div class="reader view-excerpts" id="reader-content">
        <p style="color:var(--text-muted);margin-top:40px;text-align:center;">← Select a speech to begin reading</p>
      </div>
      <div class="memo-panel">
        <div class="mp-header"><h3>Annotation</h3><span id="memo-count" style="font-size:10px;color:var(--text-muted)"></span></div>
        <div class="mp-body" id="memo-body"><p class="memo-placeholder">Click a highlighted passage to see coding memos</p></div>
        <div class="legend">
          <h4>Colour key — v4</h4>
          <div class="legend-item"><div class="legend-dot" style="background:var(--c-d11)"></div>D1.1 — State/Governance</div>
          <div class="legend-item"><div class="legend-dot" style="background:var(--c-d12)"></div>D1.2 — Science/Experts</div>
          <div class="legend-item"><div class="legend-dot" style="background:var(--c-d13)"></div>D1.3 — Cultural Backlash</div>
          <div class="legend-item"><div class="legend-dot" style="background:var(--c-ind)"></div>Inductive</div>
          <div class="legend-note">D2 codes excluded from speech corpus (v4 — speech corpus only).</div>
        </div>
      </div>
    </div>
  </div>
</div>

<div id="tab-patterns" class="tab">
  <div class="panel"><h2>Code Frequency Ranking</h2><p class="sub">Coded passages per sub-code across the full corpus</p><div class="rank-list" id="rank-list"></div></div>
  <div class="panel"><h2>Venue Group × Code Heatmap</h2><p class="sub">Coded passages per venue group × sub-code. Darker = more occurrences — shows where each rhetorical move concentrates.</p><div class="heatmap-wrap"><table class="heatmap" id="heatmap"></table></div></div>
  <div class="panel"><h2>Code Co-occurrence</h2><p class="sub">Pairs of codes appearing in the same passage — indicates rhetorical bundling</p><div class="co-occur-grid" id="co-occur"></div></div>
</div>

<div id="tab-viz" class="tab">
  <div class="dim-bars" id="dim-summary"></div>
  <div class="viz-grid">
    <div class="panel"><h2>D1.1 Sub-code Composition</h2><p class="sub">Share of the 6 governance/state sub-codes (D1.1 only)</p><div class="chart-wrap"><canvas id="chart-d11-donut"></canvas></div></div>
    <div class="panel"><h2>Dimension Composition by Quarter</h2><p class="sub">100% stacked — D1.1 / D1.2 / D1.3 / IND share per quarter, tracks how the rhetorical register shifts over time</p><div class="chart-wrap"><canvas id="chart-quarterly"></canvas></div></div>
  </div>
  <div class="viz-grid">
    <div class="panel"><h2>Rhetorical Register by Venue Group (%)</h2><p class="sub">D1.1 / D1.2 / D1.3 share (%) across venue groups — how rhetoric shifts by institutional context</p><div class="chart-wrap"><canvas id="chart-venue"></canvas></div></div>
    <div class="panel"><h2>Venue Group — Annotation Counts</h2><p class="sub">Absolute counts per dimension across venue groups</p><div class="chart-wrap"><canvas id="chart-vtype"></canvas></div></div>
  </div>
  <div class="panel"><h2>National vs International — Annotation Counts</h2><p class="sub">Total D1.1 / D1.2 / D1.3 / IND annotations: speeches delivered domestically vs abroad</p><div class="chart-wrap"><canvas id="chart-scope"></canvas></div></div>
</div>

<script>
const DIM_COLOR={"D1.1":"#3B82F6","D1.2":"#F59E0B","D1.3":"#EF4444","IND":"#9CA3AF"};
const DIM_BG={"D1.1":"rgba(59,130,246,0.18)","D1.2":"rgba(245,158,11,0.18)","D1.3":"rgba(239,68,68,0.18)","IND":"rgba(156,163,175,0.14)"};

%%CORPUS_JS%%

%%VENUE_GROUPS_JS%%

function allCoded(){return filteredCorpus().flatMap(sp=>sp.segments.filter(s=>s.type==='coded').flatMap(s=>s.codes.map(c=>({speechId:sp.id,...c}))));}
function codesBySpeech(){const m={};filteredCorpus().forEach(sp=>{m[sp.id]={};sp.segments.forEach(s=>{if(s.type==='coded')s.codes.forEach(c=>{const k=c.dim+'>'+c.sub;m[sp.id][k]=(m[sp.id][k]||0)+1;});});});return m;}
function codesByVenueGroup(){const m={};filteredCorpus().forEach(sp=>{const g=sp.venueGroup;if(!m[g])m[g]={};sp.segments.forEach(s=>{if(s.type==='coded')s.codes.forEach(c=>{const k=c.dim+'>'+c.sub;m[g][k]=(m[g][k]||0)+1;});});});return m;}
function totalFreq(){const f={};allCoded().forEach(c=>{const k=c.dim+'>'+c.sub;f[k]=(f[k]||0)+1;});return f;}
function coOccurrences(){const pairs={};filteredCorpus().forEach(sp=>sp.segments.forEach(s=>{if(s.type==='coded'&&s.codes.length>1){for(let i=0;i<s.codes.length;i++)for(let j=i+1;j<s.codes.length;j++){const a=s.codes[i].dim+'>'+s.codes[i].sub,b=s.codes[j].dim+'>'+s.codes[j].sub;const key=[a,b].sort().join(' + ');if(!pairs[key])pairs[key]={count:0,speeches:new Set()};pairs[key].count++;pairs[key].speeches.add(sp.title);}}}));return pairs;}

let activeSpeech=null,activeFilters=new Set(["D1.1","D1.2","D1.3","IND"]),currentView='excerpts';
let scopeFilter=new Set(["National","International"]);
// venueGroupFilter starts with every venue group present in the corpus "on" — VENUE_GROUPS
// is injected above (corpus_metadata.venue_group_categories) and reflects the 6-category
// grouping of the master CSV's `tipo` values, so this scales automatically without a
// hardcoded list to maintain, and stays legible as a filter/chart axis (vs. the raw
// 23 `tipo` values previously used here).
let venueGroupFilter=new Set(VENUE_GROUPS.map(v=>v.key));
function filteredCorpus(){return CORPUS.filter(sp=>scopeFilter.has(sp.scope)&&venueGroupFilter.has(sp.venueGroup));}

function initVenueGroupChips(){
  const c=document.getElementById('vg-chip-container');
  c.innerHTML=VENUE_GROUPS.map(vg=>`<button class="gf-chip on" style="--chip-c:#${vg.color}" data-vg="${escAttr(vg.key)}" onclick="toggleGlobalVenueGroup(this)">${escAttr(vg.short)}</button>`).join('');
}
function escAttr(s){return String(s).replace(/&/g,'&amp;').replace(/"/g,'&quot;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}

function switchTab(name,btn){document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));document.querySelectorAll('nav button').forEach(b=>b.classList.remove('active'));document.getElementById('tab-'+name).classList.add('active');btn.classList.add('active');if(name==='patterns')buildPatterns();if(name==='viz')buildViz();}
function toggleGlobalScope(btn){const sc=btn.dataset.scope;if(scopeFilter.has(sc)){if(scopeFilter.size===1)return;scopeFilter.delete(sc);btn.classList.remove('on');}else{scopeFilter.add(sc);btn.classList.add('on');}rebuildAll();}
function toggleGlobalVenueGroup(btn){const vg=btn.dataset.vg;if(venueGroupFilter.has(vg)){if(venueGroupFilter.size===1)return;venueGroupFilter.delete(vg);btn.classList.remove('on');}else{venueGroupFilter.add(vg);btn.classList.add('on');}rebuildAll();}
function rebuildAll(){buildNav();const at=document.querySelector('.tab.active');if(at){const id=at.id;if(id==='tab-patterns')buildPatterns();else if(id==='tab-viz')buildViz();}}
function setView(v){currentView=v;document.getElementById('btn-excerpts').classList.toggle('active',v==='excerpts');document.getElementById('btn-full').classList.toggle('active',v==='full');const r=document.getElementById('reader-content');r.classList.toggle('view-excerpts',v==='excerpts');r.classList.toggle('view-full',v==='full');if(activeSpeech!==null)applyFilters();}
function toggleFilter(btn){const dim=btn.dataset.dim;if(activeFilters.has(dim)){activeFilters.delete(dim);btn.classList.remove('on');}else{activeFilters.add(dim);btn.classList.add('on');}if(activeSpeech!==null)applyFilters();}

function applyFilters(){document.querySelectorAll('.coded-block').forEach(block=>{const dims=block.dataset.dims.split(',');const hasVis=dims.some(d=>activeFilters.has(d));block.classList.toggle('all-filtered',!hasVis);block.querySelectorAll('.pill').forEach(p=>{p.style.opacity=activeFilters.has(p.dataset.dim)?'1':'0.25';});if(hasVis){const fd=dims.find(d=>activeFilters.has(d));const ps=block.querySelector('.passage');ps.style.background=DIM_BG[fd]||'rgba(255,255,255,.05)';ps.style.borderLeftColor=DIM_COLOR[fd]||'#888';}});}

function buildNav(){
  const ul=document.getElementById('speech-nav');
  ul.innerHTML='';
  const fc=filteredCorpus();
  const fcIds=new Set(fc.map(sp=>sp.id));
  if(activeSpeech!==null&&!fcIds.has(CORPUS[activeSpeech].id)){
    activeSpeech=null;
    document.getElementById('reader-content').innerHTML='<p style="color:var(--text-muted);margin-top:40px;text-align:center;">← Select a speech to begin reading</p>';
    clearMemo();
  }
  fc.forEach(sp=>{
    const i=CORPUS.indexOf(sp);
    const li=document.createElement('li');
    const total=sp.segments.filter(s=>s.type==='coded').reduce((a,s)=>a+s.codes.length,0);
    const d11=sp.segments.flatMap(s=>s.type==='coded'?s.codes:[]).filter(c=>c.dim==='D1.1').length;
    const scopeTag=sp.scope==='National'?'<span class="tag" style="background:rgba(15,118,110,.3);color:#5eead4">Local</span>':'<span class="tag" style="background:rgba(29,78,216,.3);color:#93c5fd">Intl</span>';
    li.innerHTML=`<div class="s-date">${sp.date}</div><div class="s-title">${sp.title}</div><div class="s-meta"><span class="tag" style="background:rgba(59,130,246,.2);color:#93c5fd">D1:${total}</span><span class="tag" style="background:rgba(99,102,241,.2);color:#a5b4fc">D1.1:${d11}</span>${scopeTag}</div>`;
    if(activeSpeech===i)li.classList.add('active');
    li.onclick=()=>{document.querySelectorAll('.speech-list li').forEach(l=>l.classList.remove('active'));li.classList.add('active');activeSpeech=i;renderSpeech(i);};
    ul.appendChild(li);
  });
  const total=allCoded().length;
  document.getElementById('corpus-badge').textContent=fc.length+' speeches · '+total+' codes';
}

function renderSpeech(idx){
  const sp=CORPUS[idx];
  const reader=document.getElementById('reader-content');
  clearMemo();
  let html=`<h2>${sp.title}</h2><div class="meta-row"><span>📅 ${sp.date}</span><span>📍 ${sp.venue}</span><span>🗂 ${sp.eventType}</span><span style="color:${sp.scope==='National'?'#5eead4':'#93c5fd'}">${sp.scope==='National'?'🏛 Nacional':'🌐 Internacional'}</span></div>`;
  let si=0;
  sp.segments.forEach(seg=>{
    if(seg.type==='plain'){const isLabel=seg.text.startsWith('[')&&seg.text.includes(']:');html+=`<p class="plain-block${isLabel?' speaker-label':''}">${esc(seg.text)}</p>`;return;}
    const dims=[...new Set(seg.codes.map(c=>c.dim))];
    const hasVis=dims.some(d=>activeFilters.has(d));
    const fd=dims.find(d=>activeFilters.has(d))||dims[0];
    const bg=hasVis?(DIM_BG[fd]||'rgba(255,255,255,.05)'):'rgba(255,255,255,.03)';
    const bc=hasVis?(DIM_COLOR[fd]||'#888'):'var(--border)';
    const pills=seg.codes.map(c=>`<span class="pill" style="background:${DIM_COLOR[c.dim]};opacity:${activeFilters.has(c.dim)?1:.25}" data-dim="${c.dim}">${c.dim}·${c.sub.replace(/_/g,' ')}</span>`).join('');
    html+=`<div class="coded-block${hasVis?'':' all-filtered'}" data-dims="${dims.join(',')}" data-seg="${si}" data-sp="${idx}"><div class="passage" style="background:${bg};border-left:3px solid ${bc}" onclick="showMemo(${si},${idx})">${esc(seg.text)}</div><div class="code-pills">${pills}</div></div>`;
    si++;
  });
  reader.innerHTML=html;
  reader.classList.toggle('view-excerpts',currentView==='excerpts');
  reader.classList.toggle('view-full',currentView==='full');
  const nc=sp.segments.filter(s=>s.type==='coded').reduce((a,s)=>a+s.codes.length,0);
  document.getElementById('memo-count').textContent=nc+' codes · '+sp.segments.filter(s=>s.type==='coded').length+' passages';
}
function esc(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function showMemo(si,spi){
  const sp=CORPUS[spi];let ci=0,seg=null;
  for(const s of sp.segments){if(s.type==='coded'){if(ci===si){seg=s;break;}ci++;}}
  if(!seg)return;
  const body=document.getElementById('memo-body');
  const vis=seg.codes.filter(c=>activeFilters.has(c.dim));
  if(!vis.length){body.innerHTML='<p class="memo-placeholder">No visible codes (check filters)</p>';return;}
  body.innerHTML=vis.map(c=>`<div class="memo-item"><span class="mi-code" style="background:${DIM_COLOR[c.dim]||'#888'}">${c.dim}·${c.sub.replace(/_/g,' ')}</span><p class="mi-text">${esc(c.memo)}</p></div>`).join('<hr style="border-color:var(--border);margin:10px 0">');
}
function clearMemo(){document.getElementById('memo-body').innerHTML='<p class="memo-placeholder">Click a highlighted passage to see coding memos</p>';document.getElementById('memo-count').textContent='';}

function buildPatterns(){
  const freq=totalFreq(),sorted=Object.entries(freq).sort((a,b)=>b[1]-a[1]),max=sorted[0]?.[1]||1;
  document.getElementById('rank-list').innerHTML=sorted.map(([k,n])=>{const[d,s]=k.split('>');const c=DIM_COLOR[d]||'#888';return`<div class="rank-row"><div class="rank-label">${d}·${s.replace(/_/g,' ')}</div><div class="rank-bar-wrap"><div class="rank-bar" style="width:${Math.round(n/max*100)}%;background:${c}">${n}</div></div><div class="rank-n" style="color:${c}">${n}</div></div>`;}).join('');
  const allCodes=Object.keys(freq).sort(),byGroup=codesByVenueGroup();
  const groupsPresent=VENUE_GROUPS.map(v=>v.key).filter(g=>venueGroupFilter.has(g)&&byGroup[g]);
  let h='<thead><tr><th class="row-h">Venue Group</th>';
  allCodes.forEach(k=>{const[d,s]=k.split('>');h+=`<th style="color:${DIM_COLOR[d]}" title="${k}">${s.replace(/_/g,' ').substring(0,12)}</th>`;});
  h+='</tr></thead><tbody>';
  groupsPresent.forEach(g=>{h+=`<tr><td class="row-label">${g}</td>`;allCodes.forEach(k=>{const n=byGroup[g]?.[k]||0,[d]=k.split('>');const c=DIM_COLOR[d]||'#888',a=n===0?0:.1+Math.min(n,20)/20*.7,bg=n===0?'transparent':hRgba(c,a);h+=`<td style="background:${bg};color:${n>0?c:'var(--border)'}">${n||''}</td>`;});h+='</tr>';});
  h+='</tbody>';document.getElementById('heatmap').innerHTML=h;
  const pairs=coOccurrences(),top=Object.entries(pairs).sort((a,b)=>b[1].count-a[1].count).slice(0,12);
  document.getElementById('co-occur').innerHTML=top.map(([pair,data])=>{const[a,b]=pair.split(' + ');const da=a.split('>')[0],db=b.split('>')[0];return`<div class="co-item"><div style="font-size:10px;margin-bottom:4px"><span style="color:${DIM_COLOR[da]}">${a.replace('>','·').replace(/_/g,' ')}</span><span style="color:var(--text-muted)"> + </span><span style="color:${DIM_COLOR[db]}">${b.replace('>','·').replace(/_/g,' ')}</span></div><div class="count" style="color:${DIM_COLOR[da]}">${data.count}</div><div class="speeches">${[...data.speeches].join(', ')}</div></div>`;}).join('');
}

let charts={};
function buildViz(){
  const coded=allCoded(),total=coded.length;
  const cnts={D1_1:0,D1_2:0,D1_3:0,IND:0};
  coded.forEach(c=>{if(c.dim==='D1.1')cnts.D1_1++;else if(c.dim==='D1.2')cnts.D1_2++;else if(c.dim==='D1.3')cnts.D1_3++;else cnts.IND++;});

  // ── KPI summary ──────────────────────────────────────────────────────────
  document.getElementById('dim-summary').innerHTML=[
    {l:'Total Coded',n:total,c:'var(--text)',p:'100%'},
    {l:'D1.1 — State/Gov',n:cnts.D1_1,c:'#3B82F6',p:pct(cnts.D1_1,total)},
    {l:'D1.2 — Science/Experts',n:cnts.D1_2,c:'#F59E0B',p:pct(cnts.D1_2,total)},
    {l:'D1.3 — Cultural Backlash',n:cnts.D1_3,c:'#EF4444',p:pct(cnts.D1_3,total)},
    {l:'Inductive',n:cnts.IND,c:'#9CA3AF',p:pct(cnts.IND,total)},
  ].map(i=>`<div class="dim-bar-item"><div class="db-label">${i.l}</div><div class="db-n" style="color:${i.c}">${i.n}</div><div class="db-pct">${i.p}</div></div>`).join('');

  // ── Chart 2: D1.1 sub-code composition donut ─────────────────────────────
  // (Chart 1, a corpus-wide sub-code frequency bar, was removed 2026-08-08 — it
  // duplicated the Pattern Analysis tab's "Code Frequency Ranking" panel exactly.)
  const freq=totalFreq();
  const d11subs=Object.entries(freq)
    .filter(([k])=>k.startsWith('D1.1'))
    .sort((a,b)=>b[1]-a[1]);
  const donutColors=['#1d4ed8','#2563eb','#3b82f6','#60a5fa','#93c5fd','#bfdbfe','#dbeafe'];
  if(charts.donut)charts.donut.destroy();
  charts.donut=new Chart(document.getElementById('chart-d11-donut'),{
    type:'doughnut',
    data:{
      labels:d11subs.map(([k])=>k.split('>')[1].replace(/_/g,' ')),
      datasets:[{data:d11subs.map(([,n])=>n),
        backgroundColor:donutColors.slice(0,d11subs.length),
        borderColor:'#1a1d27',borderWidth:2}]},
    options:{responsive:true,maintainAspectRatio:false,cutout:'55%',
      plugins:{legend:{position:'right',labels:{color:'#aab',font:{size:10},boxWidth:12,padding:8}},
               tooltip:{callbacks:{label:ctx=>` ${ctx.label}: ${ctx.raw} (${Math.round(ctx.raw/cnts.D1_1*100)}% of D1.1)`}}}}});

  // ── Chart 3: Venue-group comparison grouped bar (% share) ────────────────
  // Categories come from VENUE_GROUPS (injected from the actual corpus — see
  // corpus_metadata.venue_group_categories: 6 analytically coherent groups,
  // replacing the previous 23-raw-`tipo` version which was unreadable as a
  // chart axis).
  const VG_ORDER=VENUE_GROUPS.map(v=>v.key).filter(g=>venueGroupFilter.has(g));
  const VG_SHORT=Object.fromEntries(VENUE_GROUPS.map(v=>[v.key,v.short]));
  const VG_MAP={};
  filteredCorpus().forEach(sp=>{if(!VG_MAP[sp.venueGroup])VG_MAP[sp.venueGroup]=[];VG_MAP[sp.venueGroup].push(sp);});
  const bySpeech=codesBySpeech();
  const dims=['D1.1','D1.2','D1.3','IND'];
  const dNames={'D1.1':'D1.1 Gov/State','D1.2':'D1.2 Science','D1.3':'D1.3 Cultural','IND':'Inductive'};
  const venueLabels=VG_ORDER.map(vg=>VG_SHORT[vg]);
  if(charts.venue)charts.venue.destroy();
  charts.venue=new Chart(document.getElementById('chart-venue'),{
    type:'bar',
    data:{
      labels:venueLabels,
      datasets:dims.map(dim=>({
        label:dNames[dim],
        data:VG_ORDER.map(vg=>{
          const speeches=VG_MAP[vg]||[];
          const tot=speeches.reduce((a,sp)=>a+Object.entries(bySpeech[sp.id]||{}).filter(([k])=>k.startsWith(dim)).reduce((s,[,n])=>s+n,0),0);
          const allTot=speeches.reduce((a,sp)=>a+Object.values(bySpeech[sp.id]||{}).reduce((s,n)=>s+n,0),0);
          return allTot>0?Math.round(tot/allTot*100):0;
        }),
        backgroundColor:DIM_COLOR[dim]+'bb',borderColor:DIM_COLOR[dim],borderWidth:1}))},
    options:{responsive:true,maintainAspectRatio:false,
      plugins:{legend:{labels:{color:'#aab'}},
               tooltip:{callbacks:{label:ctx=>` ${ctx.dataset.label}: ${ctx.raw}%`}}},
      scales:{x:{grid:{color:'#2e3349'},ticks:{color:'#8892aa',font:{size:10}}},
              y:{grid:{color:'#2e3349'},max:100,ticks:{color:'#8892aa',callback:v=>v+'%'},
                 title:{display:true,text:'% of annotations in venue group',color:'#8892aa'}}}}});

  // ── Chart 4: Dimension composition by quarter ─────────────────────────────
  // Replaces the old per-speech 100%-stacked chart (194 bars was unreadable).
  // Binning by quarter keeps it legible while still answering the underlying
  // question — how the D1.1/D1.2/D1.3 mix evolves over the corpus's timespan
  // (directly the codebook's own "rhetoric evolution 2023–2026" question).
  const qMap={};
  filteredCorpus().forEach(sp=>{
    if(!sp.date)return;
    const parts=sp.date.split('-');if(parts.length<2)return;
    const y=parts[0],m=parseInt(parts[1],10);
    const key=y+'-Q'+(Math.floor((m-1)/3)+1);
    if(!qMap[key])qMap[key]={};
    sp.segments.forEach(s=>{if(s.type==='coded')s.codes.forEach(c=>{qMap[key][c.dim]=(qMap[key][c.dim]||0)+1;});});
  });
  const qKeys=Object.keys(qMap).sort();
  if(charts.quarterly)charts.quarterly.destroy();
  charts.quarterly=new Chart(document.getElementById('chart-quarterly'),{
    type:'bar',
    data:{
      labels:qKeys,
      datasets:dims.map(dim=>({
        label:dNames[dim],
        data:qKeys.map(qk=>{
          const tot=Object.values(qMap[qk]||{}).reduce((a,n)=>a+n,0);
          const dTot=(qMap[qk]||{})[dim]||0;
          return tot>0?Math.round(dTot/tot*100):0;
        }),
        backgroundColor:DIM_COLOR[dim]+'bb',borderColor:DIM_COLOR[dim],borderWidth:1}))},
    options:{responsive:true,maintainAspectRatio:false,
      plugins:{legend:{labels:{color:'#aab',font:{size:10}}},
               tooltip:{callbacks:{label:ctx=>` ${ctx.dataset.label}: ${ctx.raw}%`}}},
      scales:{x:{stacked:true,grid:{color:'#2e3349'},ticks:{color:'#8892aa',font:{size:10}}},
              y:{stacked:true,max:100,grid:{color:'#2e3349'},
                 ticks:{color:'#8892aa',callback:v=>v+'%'},
                 title:{display:true,text:'% share of annotations',color:'#8892aa'}}}}});

  // ── Chart 5: National vs International counts ─────────────────────────────
  const fc5=filteredCorpus();const scopeGroups={'National':fc5.filter(sp=>sp.scope==='National'),'International':fc5.filter(sp=>sp.scope==='International')};
  const scopeLabels=['National','International'];
  if(charts.scope)charts.scope.destroy();
  charts.scope=new Chart(document.getElementById('chart-scope'),{
    type:'bar',
    data:{
      labels:scopeLabels,
      datasets:dims.map(dim=>({label:dNames[dim],
        data:scopeLabels.map(sc=>{const speeches=scopeGroups[sc]||[];
          return speeches.reduce((a,sp)=>a+Object.entries(bySpeech[sp.id]||{}).filter(([k])=>k.startsWith(dim)).reduce((s,[,n])=>s+n,0),0);}),
        backgroundColor:DIM_COLOR[dim]+'bb',borderColor:DIM_COLOR[dim],borderWidth:1}))},
    options:{responsive:true,maintainAspectRatio:false,
      plugins:{legend:{labels:{color:'#aab'}},tooltip:{callbacks:{label:ctx=>` ${ctx.dataset.label}: ${ctx.raw}`}}},
      scales:{x:{grid:{color:'#2e3349'},ticks:{color:'#8892aa'}},
              y:{grid:{color:'#2e3349'},ticks:{color:'#8892aa'},title:{display:true,text:'Annotation count',color:'#8892aa'}}}}});

  // ── Chart 6: Venue group absolute counts ─────────────────────────────────
  if(charts.vtype)charts.vtype.destroy();
  charts.vtype=new Chart(document.getElementById('chart-vtype'),{
    type:'bar',
    data:{
      labels:venueLabels,
      datasets:dims.map(dim=>({label:dNames[dim],
        data:VG_ORDER.map(vg=>{const speeches=VG_MAP[vg]||[];
          return speeches.reduce((a,sp)=>a+Object.entries(bySpeech[sp.id]||{}).filter(([k])=>k.startsWith(dim)).reduce((s,[,n])=>s+n,0),0);}),
        backgroundColor:DIM_COLOR[dim]+'bb',borderColor:DIM_COLOR[dim],borderWidth:1}))},
    options:{responsive:true,maintainAspectRatio:false,
      plugins:{legend:{labels:{color:'#aab'}},tooltip:{callbacks:{label:ctx=>` ${ctx.dataset.label}: ${ctx.raw}`}}},
      scales:{x:{grid:{color:'#2e3349'},ticks:{color:'#8892aa',font:{size:10}}},
              y:{grid:{color:'#2e3349'},ticks:{color:'#8892aa'},title:{display:true,text:'Annotation count',color:'#8892aa'}}}}});
}

function pct(n,t){return Math.round(n/t*100)+'%';}
function hRgba(hex,a){const r=parseInt(hex.slice(1,3),16),g=parseInt(hex.slice(3,5),16),b=parseInt(hex.slice(5,7),16);return`rgba(${r},${g},${b},${a})`;}

initVenueGroupChips();
buildNav();
</script>
</body>
</html>"""


def build_venue_groups_js(meta_index):
    """Build the injected `const VENUE_GROUPS = [...]` array from the 6 venue-group
    categories actually present in the corpus (corpus_metadata.venue_group_categories),
    each with a short display label and a chip color. Replaces the old 23-raw-`tipo`
    version (2026-08-08 formatting review) — too granular to filter or chart legibly."""
    categories = venue_group_categories(meta_index)
    parts = []
    for g in categories:
        parts.append(
            '{key:"%s",short:"%s",color:"%s"}' % (
                js_str(g), js_str(short_group_label(g)), VENUE_GROUP_PALETTE.get(g, "6b7280"),
            )
        )
    return 'const VENUE_GROUPS = [' + ','.join(parts) + '];'


def build_html(corpus_js, venue_groups_js):
    html = HTML_TEMPLATE.replace('%%CORPUS_JS%%', corpus_js)
    return html.replace('%%VENUE_GROUPS_JS%%', venue_groups_js)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    if not CODED_DIR.exists():
        print(f"ERROR: Coded speeches directory not found: {CODED_DIR}")
        sys.exit(1)

    coded_files = sorted(CODED_DIR.glob("*.md"))
    coded_files = [f for f in coded_files if not f.name.startswith("frequency_tally")]
    if not coded_files:
        print(f"ERROR: No coded speech .md files found in {CODED_DIR}")
        sys.exit(1)

    print(f"Found {len(coded_files)} coded speech files:")

    meta_index, meta_warnings = build_metadata_index(PROJECT_ROOT, CODED_DIR)
    print_warnings(meta_warnings)

    files, code_warnings = build_corpus(CODED_DIR, meta_index)
    print_code_warnings(code_warnings)

    corpus_js = build_corpus_js(files)
    venue_groups_js = build_venue_groups_js(meta_index)

    html = build_html(corpus_js, venue_groups_js)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(html, encoding='utf-8')
    print(f"\n✓ Saved: {OUTPUT_PATH}")
    print(f"  File size: {len(html):,} chars")


if __name__ == '__main__':
    main()
