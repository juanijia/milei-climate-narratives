#!/usr/bin/env python3
"""
generate_html.py
Generates the interactive QDA HTML explorer from v3 coded speech files.

Usage (run from project root):
    python skills/qda-outputs/scripts/generate_html.py

Output:
    analysis/results/qda_explorer_v3.html
"""

import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
CODED_DIR    = PROJECT_ROOT / "analysis" / "coded_speeches" / "v3"
OUTPUT_PATH  = PROJECT_ROOT / "analysis" / "results" / "qda_explorer_v3.html"

# Chronological speech metadata
SPEECH_META = {
    "2023-10-08": {"id": "debate2023",   "title": "Debate Presidencial 2023",
                   "venue": "Buenos Aires", "type": "debate"},
    "2024-01-17": {"id": "davos2024",    "title": "WEF Davos 2024",
                   "venue": "Davos", "type": "speech"},
    "2024-03-01": {"id": "apertura2024", "title": "Apertura Sesiones Ordinarias 2024 (142°)",
                   "venue": "Buenos Aires", "type": "speech"},
    "2024-09-24": {"id": "un2024",       "title": "UN General Assembly — 79th Session",
                   "venue": "New York", "type": "speech"},
    "2025-01-23": {"id": "davos2025",    "title": "WEF Davos 2025",
                   "venue": "Davos", "type": "speech"},
    "2025-03-01": {"id": "apertura2025", "title": "Apertura Sesiones Ordinarias 2025 (143°)",
                   "venue": "Buenos Aires", "type": "speech"},
    "2025-09-24": {"id": "onu2025",      "title": "UN General Assembly — 80th Session",
                   "venue": "New York", "type": "speech"},
    "2026-01-22": {"id": "davos2026",    "title": "WEF Davos 2026",
                   "venue": "Davos", "type": "speech"},
    "2026-03-01": {"id": "apertura2026", "title": "Apertura Sesiones Ordinarias 2026 (144°)",
                   "venue": "Buenos Aires", "type": "speech"},
}


# ── Parsers ───────────────────────────────────────────────────────────────────

def get_date(raw):
    m = re.search(r'^date:\s*(\d{4}-\d{2}-\d{2})', raw, re.MULTILINE)
    return m.group(1) if m else None


def parse_code_tag(tag):
    m = re.match(r'([A-Z0-9\.]+)\s*>\s*([A-Za-z_]+)', tag.strip())
    if not m:
        return None, None
    dim_raw, sub = m.group(1), m.group(2)
    return ("IND" if dim_raw == "INDUCTIVE" else dim_raw), sub


def clean_line(line):
    line = re.sub(r'\*\*\[([^\]]+)\]\*\*:\s*', r'[\1]: ', line)
    line = re.sub(r'\*\*([^*]+)\*\*', r'\1', line)
    line = re.sub(r'\*([^*]+)\*', r'\1', line)
    return ' '.join(line.split()).strip()


def is_skip(line):
    s = line.strip()
    if not s or s.startswith('---') or s.startswith('#'): return True
    if re.match(r'^\*\[', s) or re.match(r'^\[Not coded', s): return True
    return False


def parse_full_segments(path):
    """
    Parse a v3 coded speech file into a list of segments:
        {'type': 'plain', 'text': '...'} or
        {'type': 'coded', 'text': '...', 'codes': [{'dim':..., 'sub':..., 'memo':...}]}
    """
    raw = path.read_text(encoding='utf-8')
    body = re.sub(r'^---\n.*?---\n', '', raw, count=1, flags=re.DOTALL)
    body = re.sub(r'\n---\n## Coding Summary.*$', '', body, flags=re.DOTALL)
    body = re.sub(r'\n## Coding Summary.*$', '', body, flags=re.DOTALL)

    lines = body.split('\n')
    segments = []
    text_buffer = []
    pending_passage = None
    pending_codes = []

    def flush_pending():
        nonlocal pending_passage, pending_codes
        if pending_passage is not None:
            if pending_codes:
                segments.append({'type': 'coded', 'text': pending_passage,
                                  'codes': pending_codes[:]})
            else:
                segments.append({'type': 'plain', 'text': pending_passage})
        pending_passage = None
        pending_codes = []

    def flush_buffer():
        nonlocal text_buffer, pending_passage, pending_codes
        if text_buffer:
            text = ' '.join(text_buffer).strip()
            text_buffer.clear()
            if len(text) > 10:
                flush_pending()
                pending_passage = text
                pending_codes = []

    for line in lines:
        stripped = line.strip()
        m = re.match(r'`\[CODE:\s*([^\]]+)\]`\s*[—–\-]+\s*\*?(?:Memo:)?\s*(.*)', stripped)
        if m:
            if text_buffer:
                flush_buffer()
            dim, sub = parse_code_tag(m.group(1))
            memo = m.group(2).strip().strip('*').strip()
            if dim and sub and pending_passage:
                pending_codes.append({'dim': dim, 'sub': sub, 'memo': memo})
            continue
        if is_skip(line):
            flush_buffer()
            continue
        cleaned = clean_line(line)
        if cleaned and len(cleaned) > 5:
            if pending_codes:
                flush_pending()
            text_buffer.append(cleaned)

    flush_buffer()
    flush_pending()
    return segments


# ── JavaScript CORPUS builder ─────────────────────────────────────────────────

def js_str(s):
    return (s.replace('\\', '\\\\')
             .replace('"', '\\"')
             .replace('\n', ' ')
             .replace('\r', ''))


def build_corpus_js(coded_files):
    """
    Parse all coded files and generate the CORPUS JavaScript array string.
    """
    corpus_parts = []
    total_codes = 0

    for path in coded_files:
        raw = path.read_text(encoding='utf-8')
        date = get_date(raw) or "0000-00-00"
        meta = SPEECH_META.get(date)
        if meta is None:
            m = re.match(r'(\d{4}-\d{2}-\d{2})', path.name)
            date = m.group(1) if m else date
            meta = SPEECH_META.get(date)
        if meta is None:
            print(f"  WARNING: no metadata for {path.name} (date {date}), skipping")
            continue

        segments = parse_full_segments(path)
        file_codes = sum(len(s.get('codes', [])) for s in segments if s['type'] == 'coded')
        total_codes += file_codes
        print(f"  {path.name}: {len(segments)} segments, {file_codes} code annotations")

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
        corpus_parts.append(
            f'  {{id:"{meta["id"]}",date:"{date}",'
            f'title:"{js_str(meta["title"])}",'
            f'venue:"{meta["venue"]}",type:"{meta["type"]}",\n'
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
<title>Milei Climate Narratives — QDA Explorer v3</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<style>
  :root{--bg:#0f1117;--surface:#1a1d27;--surface2:#22263a;--border:#2e3349;--text:#e2e8f0;--text-muted:#8892aa;--accent:#6366f1;--c-d11:#3B82F6;--c-d12:#F59E0B;--c-d13:#EF4444;--c-ind:#9CA3AF;}
  *{box-sizing:border-box;margin:0;padding:0;}
  body{background:var(--bg);color:var(--text);font-family:'Segoe UI',system-ui,sans-serif;font-size:14px;height:100vh;display:flex;flex-direction:column;overflow:hidden;}
  header{background:var(--surface);border-bottom:1px solid var(--border);padding:0 20px;display:flex;align-items:center;gap:20px;height:52px;flex-shrink:0;}
  header h1{font-size:13px;font-weight:700;color:var(--text-muted);letter-spacing:.05em;text-transform:uppercase;white-space:nowrap;}
  .v3-badge{background:#6366f1;color:#fff;font-size:10px;font-weight:800;padding:2px 7px;border-radius:4px;}
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
  table.heatmap th.row-h{text-align:left;max-width:160px;}
  table.heatmap td{width:44px;height:32px;text-align:center;border:1px solid var(--border);font-size:12px;font-weight:700;}
  table.heatmap td.row-label{text-align:left;padding:0 10px;font-size:11px;color:var(--text-muted);white-space:nowrap;width:160px;}
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
  ::-webkit-scrollbar{width:6px;height:6px;}
  ::-webkit-scrollbar-track{background:transparent;}
  ::-webkit-scrollbar-thumb{background:var(--border);border-radius:3px;}
</style>
</head>
<body>
<header>
  <h1>Milei Climate Narratives · QDA Explorer <span class="v3-badge">V3</span></h1>
  <nav>
    <button class="active" onclick="switchTab('browse',this)">📖 Corpus Browser <span class="badge" id="corpus-badge">—</span></button>
    <button onclick="switchTab('patterns',this)">🔗 Pattern Analysis</button>
    <button onclick="switchTab('viz',this)">📊 Visualizations</button>
  </nav>
</header>

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
          <h4>Colour key — v3</h4>
          <div class="legend-item"><div class="legend-dot" style="background:var(--c-d11)"></div>D1.1 — State/Governance</div>
          <div class="legend-item"><div class="legend-dot" style="background:var(--c-d12)"></div>D1.2 — Science/Experts</div>
          <div class="legend-item"><div class="legend-dot" style="background:var(--c-d13)"></div>D1.3 — Cultural Backlash</div>
          <div class="legend-item"><div class="legend-dot" style="background:var(--c-ind)"></div>Inductive</div>
          <div class="legend-note">D2 codes excluded from speech corpus (v3). Re-coded as D1 where applicable.</div>
        </div>
      </div>
    </div>
  </div>
</div>

<div id="tab-patterns" class="tab">
  <div class="panel"><h2>Code Frequency Ranking</h2><p class="sub">Coded passages per sub-code across the full corpus</p><div class="rank-list" id="rank-list"></div></div>
  <div class="panel"><h2>Speech × Code Heatmap</h2><p class="sub">Coded passages per speech × sub-code. Darker = more occurrences.</p><div class="heatmap-wrap"><table class="heatmap" id="heatmap"></table></div></div>
  <div class="panel"><h2>Code Co-occurrence</h2><p class="sub">Pairs of codes appearing in the same passage — indicates rhetorical bundling</p><div class="co-occur-grid" id="co-occur"></div></div>
</div>

<div id="tab-viz" class="tab">
  <div class="dim-bars" id="dim-summary"></div>
  <div class="viz-grid">
    <div class="panel"><h2>Sub-code Frequency — Full Corpus</h2><p class="sub">Annotations per sub-code, coloured by dimension</p><div class="chart-wrap"><canvas id="chart-freq"></canvas></div></div>
    <div class="panel"><h2>D1.1 Sub-code Composition</h2><p class="sub">Share of the 7 governance/state sub-codes (D1.1 only)</p><div class="chart-wrap"><canvas id="chart-d11-donut"></canvas></div></div>
  </div>
  <div class="viz-grid">
    <div class="panel"><h2>Rhetorical Register by Venue</h2><p class="sub">D1.1 / D1.2 / D1.3 distribution across venue types — reveals how rhetoric shifts by audience</p><div class="chart-wrap"><canvas id="chart-venue"></canvas></div></div>
    <div class="panel"><h2>D1 Composition per Speech (normalised %)</h2><p class="sub">100% stacked — share of D1.1 / D1.2 / D1.3 / IND in each speech</p><div class="chart-wrap"><canvas id="chart-normalized"></canvas></div></div>
  </div>
  <div class="panel"><h2>Code Timeline</h2><p class="sub">Codes appearing in each speech — chronological repertoire</p><div class="timeline-grid" id="timeline"></div></div>
</div>

<script>
const DIM_COLOR={"D1.1":"#3B82F6","D1.2":"#F59E0B","D1.3":"#EF4444","IND":"#9CA3AF"};
const DIM_BG={"D1.1":"rgba(59,130,246,0.18)","D1.2":"rgba(245,158,11,0.18)","D1.3":"rgba(239,68,68,0.18)","IND":"rgba(156,163,175,0.14)"};

%%CORPUS_JS%%

function allCoded(){return CORPUS.flatMap(sp=>sp.segments.filter(s=>s.type==='coded').flatMap(s=>s.codes.map(c=>({speechId:sp.id,...c}))));}
function codesBySpeech(){const m={};CORPUS.forEach(sp=>{m[sp.id]={};sp.segments.forEach(s=>{if(s.type==='coded')s.codes.forEach(c=>{const k=c.dim+'>'+c.sub;m[sp.id][k]=(m[sp.id][k]||0)+1;});});});return m;}
function totalFreq(){const f={};allCoded().forEach(c=>{const k=c.dim+'>'+c.sub;f[k]=(f[k]||0)+1;});return f;}
function coOccurrences(){const pairs={};CORPUS.forEach(sp=>sp.segments.forEach(s=>{if(s.type==='coded'&&s.codes.length>1){for(let i=0;i<s.codes.length;i++)for(let j=i+1;j<s.codes.length;j++){const a=s.codes[i].dim+'>'+s.codes[i].sub,b=s.codes[j].dim+'>'+s.codes[j].sub;const key=[a,b].sort().join(' + ');if(!pairs[key])pairs[key]={count:0,speeches:new Set()};pairs[key].count++;pairs[key].speeches.add(sp.title);}}}));return pairs;}

let activeSpeech=null,activeFilters=new Set(["D1.1","D1.2","D1.3","IND"]),currentView='excerpts';

function switchTab(name,btn){document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));document.querySelectorAll('nav button').forEach(b=>b.classList.remove('active'));document.getElementById('tab-'+name).classList.add('active');btn.classList.add('active');if(name==='patterns')buildPatterns();if(name==='viz')buildViz();}
function setView(v){currentView=v;document.getElementById('btn-excerpts').classList.toggle('active',v==='excerpts');document.getElementById('btn-full').classList.toggle('active',v==='full');const r=document.getElementById('reader-content');r.classList.toggle('view-excerpts',v==='excerpts');r.classList.toggle('view-full',v==='full');if(activeSpeech!==null)applyFilters();}
function toggleFilter(btn){const dim=btn.dataset.dim;if(activeFilters.has(dim)){activeFilters.delete(dim);btn.classList.remove('on');}else{activeFilters.add(dim);btn.classList.add('on');}if(activeSpeech!==null)applyFilters();}
function applyFilters(){document.querySelectorAll('.coded-block').forEach(block=>{const dims=block.dataset.dims.split(',');const hasVis=dims.some(d=>activeFilters.has(d));block.classList.toggle('all-filtered',!hasVis);block.querySelectorAll('.pill').forEach(p=>{p.style.opacity=activeFilters.has(p.dataset.dim)?'1':'0.25';});if(hasVis){const fd=dims.find(d=>activeFilters.has(d));const ps=block.querySelector('.passage');ps.style.background=DIM_BG[fd]||'rgba(255,255,255,.05)';ps.style.borderLeftColor=DIM_COLOR[fd]||'#888';}});}

function buildNav(){
  const ul=document.getElementById('speech-nav');
  CORPUS.forEach((sp,i)=>{
    const li=document.createElement('li');
    const total=sp.segments.filter(s=>s.type==='coded').reduce((a,s)=>a+s.codes.length,0);
    const d11=sp.segments.flatMap(s=>s.type==='coded'?s.codes:[]).filter(c=>c.dim==='D1.1').length;
    li.innerHTML=`<div class="s-date">${sp.date}</div><div class="s-title">${sp.title}</div><div class="s-meta"><span class="tag" style="background:rgba(59,130,246,.2);color:#93c5fd">D1:${total}</span><span class="tag" style="background:rgba(99,102,241,.2);color:#a5b4fc">D1.1:${d11}</span><span class="tag" style="background:var(--surface2);color:var(--text-muted)">${sp.type}</span></div>`;
    li.onclick=()=>{document.querySelectorAll('.speech-list li').forEach(l=>l.classList.remove('active'));li.classList.add('active');activeSpeech=i;renderSpeech(i);};
    ul.appendChild(li);
  });
  const total=allCoded().length;
  document.getElementById('corpus-badge').textContent=CORPUS.length+' speeches · '+total+' codes';
}

function renderSpeech(idx){
  const sp=CORPUS[idx];
  const reader=document.getElementById('reader-content');
  clearMemo();
  let html=`<h2>${sp.title}</h2><div class="meta-row"><span>📅 ${sp.date}</span><span>📍 ${sp.venue}</span><span>🏷 ${sp.type}</span></div>`;
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
  const allCodes=Object.keys(freq).sort(),bySpeech=codesBySpeech();
  let h='<thead><tr><th class="row-h">Speech</th>';
  allCodes.forEach(k=>{const[d,s]=k.split('>');h+=`<th style="color:${DIM_COLOR[d]}" title="${k}">${s.replace(/_/g,' ').substring(0,12)}</th>`;});
  h+='</tr></thead><tbody>';
  CORPUS.forEach(sp=>{h+=`<tr><td class="row-label">${sp.date.substring(0,7)} ${sp.title.substring(0,18)}</td>`;allCodes.forEach(k=>{const n=bySpeech[sp.id]?.[k]||0,[d]=k.split('>');const c=DIM_COLOR[d]||'#888',a=n===0?0:.15+(n/5)*.6,bg=n===0?'transparent':hRgba(c,a);h+=`<td style="background:${bg};color:${n>0?c:'var(--border)'}">${n||''}</td>`;});h+='</tr>';});
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

  // ── Chart 1: Sub-code frequency horizontal bar ───────────────────────────
  const freq=totalFreq(),sorted=Object.entries(freq).sort((a,b)=>b[1]-a[1]);
  if(charts.freq)charts.freq.destroy();
  charts.freq=new Chart(document.getElementById('chart-freq'),{
    type:'bar',
    data:{
      labels:sorted.map(([k])=>{const[d,s]=k.split('>');return d+'·'+s.replace(/_/g,' ').substring(0,14);}),
      datasets:[{data:sorted.map(([,n])=>n),
        backgroundColor:sorted.map(([k])=>(DIM_COLOR[k.split('>')[0]]||'#888')+'cc'),
        borderColor:sorted.map(([k])=>DIM_COLOR[k.split('>')[0]]||'#888'),borderWidth:1}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,
      plugins:{legend:{display:false},tooltip:{callbacks:{label:ctx=>' n = '+ctx.raw}}},
      scales:{x:{grid:{color:'#2e3349'},ticks:{color:'#8892aa'}},
              y:{grid:{color:'#2e3349'},ticks:{color:'#aab',font:{size:10}}}}}});

  // ── Chart 2: D1.1 sub-code composition donut ─────────────────────────────
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

  // ── Chart 3: Venue-type comparison grouped bar ───────────────────────────
  // Group speeches by venue type
  const venueGroups={
    'Davos':    CORPUS.filter(sp=>sp.venue==='Davos'),
    'UN GA':    CORPUS.filter(sp=>sp.venue==='New York'),
    'Apertura': CORPUS.filter(sp=>sp.venue==='Buenos Aires'&&sp.type==='speech'),
    'Debate':   CORPUS.filter(sp=>sp.type==='debate'),
  };
  const bySpeech=codesBySpeech();
  const dims=['D1.1','D1.2','D1.3','IND'];
  const dNames={'D1.1':'D1.1 Gov/State','D1.2':'D1.2 Science','D1.3':'D1.3 Cultural','IND':'Inductive'};
  const venueLabels=Object.keys(venueGroups).filter(v=>venueGroups[v].length>0);
  if(charts.venue)charts.venue.destroy();
  charts.venue=new Chart(document.getElementById('chart-venue'),{
    type:'bar',
    data:{
      labels:venueLabels,
      datasets:dims.map(dim=>({
        label:dNames[dim],
        data:venueLabels.map(v=>{
          const speeches=venueGroups[v];
          const tot=speeches.reduce((a,sp)=>a+Object.entries(bySpeech[sp.id]||{}).filter(([k])=>k.startsWith(dim)).reduce((s,[,n])=>s+n,0),0);
          const allTot=speeches.reduce((a,sp)=>a+Object.values(bySpeech[sp.id]||{}).reduce((s,n)=>s+n,0),0);
          return allTot>0?Math.round(tot/allTot*100):0;
        }),
        backgroundColor:DIM_COLOR[dim]+'bb',borderColor:DIM_COLOR[dim],borderWidth:1}))},
    options:{responsive:true,maintainAspectRatio:false,
      plugins:{legend:{labels:{color:'#aab'}},
               tooltip:{callbacks:{label:ctx=>` ${ctx.dataset.label}: ${ctx.raw}%`}}},
      scales:{x:{grid:{color:'#2e3349'},ticks:{color:'#8892aa'}},
              y:{grid:{color:'#2e3349'},max:100,ticks:{color:'#8892aa',callback:v=>v+'%'},
                 title:{display:true,text:'% of annotations in venue',color:'#8892aa'}}}}});

  // ── Chart 4: Normalised 100% stacked per speech ───────────────────────────
  if(charts.norm)charts.norm.destroy();
  charts.norm=new Chart(document.getElementById('chart-normalized'),{
    type:'bar',
    data:{
      labels:CORPUS.map(s=>s.date.substring(0,7)),
      datasets:dims.map(dim=>({
        label:dNames[dim],
        data:CORPUS.map(sp=>{
          const spTot=Object.values(bySpeech[sp.id]||{}).reduce((a,n)=>a+n,0);
          const dimTot=Object.entries(bySpeech[sp.id]||{}).filter(([k])=>k.startsWith(dim)).reduce((a,[,n])=>a+n,0);
          return spTot>0?Math.round(dimTot/spTot*100):0;
        }),
        backgroundColor:DIM_COLOR[dim]+'bb',borderColor:DIM_COLOR[dim],borderWidth:1}))},
    options:{responsive:true,maintainAspectRatio:false,
      plugins:{legend:{labels:{color:'#aab',font:{size:10}}},
               tooltip:{callbacks:{label:ctx=>` ${ctx.dataset.label}: ${ctx.raw}%`}}},
      scales:{x:{stacked:true,grid:{color:'#2e3349'},ticks:{color:'#8892aa',font:{size:9}}},
              y:{stacked:true,max:100,grid:{color:'#2e3349'},
                 ticks:{color:'#8892aa',callback:v=>v+'%'},
                 title:{display:true,text:'% share of annotations',color:'#8892aa'}}}}});

  // ── Timeline ──────────────────────────────────────────────────────────────
  document.getElementById('timeline').innerHTML=CORPUS.map(sp=>{
    const codes=sp.segments.flatMap(s=>s.type==='coded'?s.codes:[]);
    const uniq=[...new Map(codes.map(c=>[c.dim+'>'+c.sub,c])).values()];
    return`<div class="tl-col"><h4>${sp.date.substring(0,7)}<br>${sp.title}</h4>${
      uniq.map(c=>`<div class="tl-dot" style="background:${DIM_COLOR[c.dim]}88;border-left:2px solid ${DIM_COLOR[c.dim]}">${c.sub.replace(/_/g,' ')}</div>`).join('')}</div>`;
  }).join('');
}

function pct(n,t){return Math.round(n/t*100)+'%';}
function hRgba(hex,a){const r=parseInt(hex.slice(1,3),16),g=parseInt(hex.slice(3,5),16),b=parseInt(hex.slice(5,7),16);return`rgba(${r},${g},${b},${a})`;}

buildNav();
</script>
</body>
</html>"""


def build_html(corpus_js):
    return HTML_TEMPLATE.replace('%%CORPUS_JS%%', corpus_js)


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
    corpus_js = build_corpus_js(coded_files)

    html = build_html(corpus_js)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(html, encoding='utf-8')
    print(f"\n✓ Saved: {OUTPUT_PATH}")
    print(f"  File size: {len(html):,} chars")


if __name__ == '__main__':
    main()
")]
    if not coded_files:
        print(f"ERROR: No coded speech .md files found in {CODED_DIR}")
        sys.exit(1)

    print(f"Found {len(coded_files)} coded speech files:")
    corpus_js = build_corpus_js(coded_files)

    html = build_html(corpus_js)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(html, encoding='utf-8')
    print(f"\n✓ Saved: {OUTPUT_PATH}")
    print(f"  File size: {len(html):,} chars")


if __name__ == '__main__':
    main()
gins:{legend:{labels:{color:'#aab'}},
               tooltip:{callbacks:{label:ctx=>` ${ctx.dataset.label}: ${ctx.raw}%`}}},
      scales:{x:{grid:{color:'#2e3349'},ticks:{color:'#8892aa'}},
              y:{grid:{color:'#2e3349'},max:100,ticks:{color:'#8892aa',callback:v=>v+'%'},
                 title:{display:true,text:'% of annotations in venue',color:'#8892aa'}}}}});

  // ── Chart 4: Normalised 100% stacked per speech ───────────────────────────
  if(charts.norm)charts.norm.destroy();
  charts.norm=new Chart(document.getElementById('chart-normalized'),{
    type:'bar',
    data:{
      labels:CORPUS.map(s=>s.date.substring(0,7)),
      datasets:dims.map(dim=>({
        label:dNames[dim],
        data:CORPUS.map(sp=>{
          const spTot=Object.values(bySpeech[sp.id]||{}).reduce((a,n)=>a+n,0);
          const dimTot=Object.entries(bySpeech[sp.id]||{}).filter(([k])=>k.startsWith(dim)).reduce((a,[,n])=>a+n,0);
          return spTot>0?Math.round(dimTot/spTot*100):0;
        }),
        backgroundColor:DIM_COLOR[dim]+'bb',borderColor:DIM_COLOR[dim],borderWidth:1}))},
    options:{responsive:true,maintainAspectRatio:false,
      plugins:{legend:{labels:{color:'#aab',font:{size:10}}},
               tooltip:{callbacks:{label:ctx=>` ${ctx.dataset.label}: ${ctx.raw}%`}}},
      scales:{x:{stacked:true,grid:{color:'#2e3349'},ticks:{color:'#8892aa',font:{size:9}}},
              y:{stacked:true,max:100,grid:{color:'#2e3349'},
                 ticks:{color:'#8892aa',callback:v=>v+'%'},
                 title:{display:true,text:'% share of annotations',color:'#8892aa'}}}}});

  // ── Timeline ──────────────────────────────────────────────────────────────
  document.getElementById('timeline').innerHTML=CORPUS.map(sp=>{
    const codes=sp.segments.flatMap(s=>s.type==='coded'?s.codes:[]);
    const uniq=[...new Map(codes.map(c=>[c.dim+'>'+c.sub,c])).values()];
    return`<div class="tl-col"><h4>${sp.date.substring(0,7)}<br>${sp.title}</h4>${
      uniq.map(c=>`<div class="tl-dot" style="background:${DIM_COLOR[c.dim]}88;border-left:2px solid ${DIM_COLOR[c.dim]}">${c.sub.replace(/_/g,' ')}</div>`).join('')}</div>`;
  }).join('');
}

function pct(n,t){return Math.round(n/t*100)+'%';}
function hRgba(hex,a){const r=parseInt(hex.slice(1,3),16),g=parseInt(hex.slice(3,5),16),b=parseInt(hex.slice(5,7),16);return`rgba(${r},${g},${b},${a})`;}

buildNav();
</script>
</body>
</html>"""


def build_html(corpus_js):
    return HTML_TEMPLATE.replace('%%CORPUS_JS%%', corpus_js)


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
    corpus_js = build_corpus_js(coded_files)

    html = build_html(corpus_js)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(html, encoding='utf-8')
    print(f"\n✓ Saved: {OUTPUT_PATH}")
    print(f"  File size: {len(html):,} chars")


if __name__ == '__main__':
    main()
