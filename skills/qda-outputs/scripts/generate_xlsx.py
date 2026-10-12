#!/usr/bin/env python3
"""
generate_xlsx.py
Generates the QDA coded corpus Excel workbook from v4 coded speech files.

Usage (run from project root):
    python skills/qda-outputs/scripts/generate_xlsx.py

Output:
    analysis/results/v4/qda_v4_coded_corpus_REGENERATED.xlsx  (comparison build; the master is qda_v4_coded_corpus_261011.xlsx)

Formatting review (2026-08-08): reworked per Juan's feedback —
  - Dimension colors now match the HTML explorer exactly (D1.1 blue / D1.2 orange /
    D1.3 red / IND gray), applied consistently to every cell fill and chart.
  - Coded Passages: columns A/B now solid-filled by dimension; new "Venue Group"
    column added.
  - Freq — By Dimension: the old 194-column per-speech crosstab and its unreadable
    stacked chart are gone (redundant with the redesigned Speech Overview sheet).
    Replaced with a compact 4-row dimension-totals table + donut + bar chart.
  - Freq — By Sub-code: fixed a real bug where the per-speech data columns started
    at column B instead of C, silently overwriting the "Sub-code" label in every
    data row with the first speech's COUNTIFS formula. Chart is now sorted
    descending by frequency and colored by dimension (matches the HTML's Code
    Frequency Ranking), instead of grouped-by-dimension order in a flat navy color.
  - Speech Overview: D1 Codes / D2 Codes / Inductive columns replaced with
    D1.1 / D1.2 / D1.3 (D2 is always 0 for this speech corpus; Inductive is
    currently always 0 corpus-wide). New "Venue Group" column added.
  - Freq — By Scope: added a sub-code frequency ranking split National vs.
    International, same ranked/colored style as the Sub-code sheet.
  - Freq — By Venue Type: the 23 raw `tipo` values are regrouped into 6
    analytically coherent venue groups (see corpus_metadata.VENUE_GROUPS_ORDER),
    making both the crosstab and the dimension-distribution chart legible.
"""

import sys
from pathlib import Path
from collections import OrderedDict, Counter, defaultdict

try:
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter, column_index_from_string
    from openpyxl.chart import BarChart, PieChart, Reference
    from openpyxl.chart.series import SeriesLabel
except ImportError:
    print("ERROR: openpyxl not found. Run: pip install openpyxl --break-system-packages")
    sys.exit(1)

sys.path.insert(0, str(Path(__file__).parent))
from corpus_metadata import (
    build_metadata_index, venue_type_categories, venue_group_categories,
    short_label, print_warnings,
)
from corpus_data import build_corpus, VALID_CODES, print_code_warnings

# ── Configuration ─────────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent  # skills/qda-outputs/scripts/ → project root
CODED_DIR    = PROJECT_ROOT / "analysis" / "coded_speeches" / "v4"
MASTER_PATH  = PROJECT_ROOT / "analysis" / "results" / "v4" / "qda_v4_coded_corpus_261011.xlsx"   # master: never overwritten
OUTPUT_PATH  = PROJECT_ROOT / "analysis" / "results" / "v4" / "qda_v4_coded_corpus_REGENERATED.xlsx"   # default target for a fresh build (comparison only)

# NOTE: speech title/venue/event-type/scope/venue_group are no longer hardcoded
# here. They are derived per-file from the master corpus CSV via
# corpus_metadata.build_metadata_index(), so new coded speeches need no script
# edits — see corpus_metadata.py for the matching/grouping logic.

# Sub-code normalized display names (underscore_key → "Display Name")
# v4: merged/renamed codes; retired codes omitted
SUBCODE_DISPLAY = {
    # D1.1
    "Anti_Casta": "Anti-Casta (Elite Frame)",
    "Anti_State_Anti_Bureaucratic": "Anti-State / Anti-Bureaucratic",
    "Delegitimization_of_Regulation": "Delegitimization of Regulation",
    "Market_Primacy": "Market Primacy",
    "Rejection_of_Multilateral_Governance": "Rejection of Multilateral Governance",
    "Sustainability_as_Ideological_or_Harmful": "Sustainability as Ideological or Harmful",
    # D1.2
    "Attack_on_Universities_and_Research_Institutions": "Attack on Universities & Research Institutions",
    "Attack_on_Experts_and_Technocrats": "Attack on Experts & Technocrats",
    "Climate_Skepticism_or_Dismissal": "Climate Skepticism or Dismissal",
    "Pseudo_Science_or_Ideological_Science": "Pseudo-Science / Ideological Science",
    "Selective_Empiricism": "Selective Empiricism",
    # D1.3
    "Civilizational_Defense": "Civilizational Defense",
    "Anti_Socialism_Anti_Collectivism": "Anti-Socialism / Anti-Collectivism",
    "Woke_Bundling": "Woke Bundling",
    # Legacy v3 keys — kept for graceful parsing of any residual v3 annotations
    "Deregulation_Benefits": "Delegitimization of Regulation [v3 legacy]",
    "Attack_on_Public_Research_Institutions": "Attack on Universities & Research Institutions [v3 legacy]",
    "Attack_on_Universities": "Attack on Universities & Research Institutions [v3 legacy]",
    "Rejection_of_Expert_Mediation": "Attack on Experts & Technocrats [v3 legacy]",
    "Neo_Marxism": "Anti-Socialism / Anti-Collectivism [v3 legacy]",
}

DIM_FULL = {
    "D1.1": "D1.1 — State Intervention & Governance",
    "D1.2": "D1.2 — Public Science & Expertise",
    "D1.3": "D1.3 — Cultural Backlash",
    "IND":  "Inductive",
}

DIMS_ORDER = ['D1.1', 'D1.2', 'D1.3', 'IND']

# Dimension colors — must match the HTML explorer exactly (skills/qda-outputs/
# scripts/generate_html.py's DIM_COLOR constant) so a reader moving between the
# two deliverables sees the same visual language. Hex, no '#'.
DIM_CHART_COLORS = {
    'D1.1': '3B82F6',  # blue
    'D1.2': 'F59E0B',  # orange
    'D1.3': 'EF4444',  # red
    'IND':  '9CA3AF',  # gray
}

SCOPE_CATEGORIES = ["National", "International"]

# VENUE_TYPES/VENUE_GROUPS are no longer fixed lists — computed at runtime in
# main() from whichever values actually appear in the coded corpus, so sheets
# scale automatically as more speeches are coded.

# Column letters in Coded Passages sheet (A-M layout, with Venue Group added)
TYPE_COL         = "K"   # col 11 — Type (raw venue tipo label)
VENUE_GROUP_COL  = "L"   # col 12 — Venue Group (6-category grouping)
SCOPE_COL        = "M"   # col 13 — Scope (National / International)


# ── Parsing ───────────────────────────────────────────────────────────────────
# All parsing (frontmatter, `[CODE: ...]` tags, passage buffering) lives in
# corpus_data.py (parse_speech_segments / flatten_segments / build_corpus), which
# generate_html.py also consumes — this eliminates the risk of the two output
# scripts silently diverging on what counts as a "passage" or a valid code.


def _canonical_subcode_lists():
    """(dim, [display names]) pairs in v4 codebook order, derived from
    corpus_data.VALID_CODES — the single source for 'ensure all known sub-codes
    are present' logic."""
    result = []
    for dim in ('D1.1', 'D1.2', 'D1.3'):
        subs = [SUBCODE_DISPLAY.get(k, k.replace('_', ' ')) for k in VALID_CODES.get(dim, [])]
        result.append((dim, subs))
    result.append(('IND', []))
    return result


def _canonical_subcode_keys():
    """(dim, sub_key, display_name) triples in v4 codebook order — used to seed
    zero-count sub-codes into ranking tables so they still appear."""
    result = []
    for dim in ('D1.1', 'D1.2', 'D1.3'):
        for key in VALID_CODES.get(dim, []):
            result.append((dim, key, SUBCODE_DISPLAY.get(key, key.replace('_', ' '))))
    return result


# ── Excel builder ─────────────────────────────────────────────────────────────

def thin_border():
    s = Side(style='thin', color='CCCCCC')
    return Border(left=s, right=s, top=s, bottom=s)

TITLE_FONT   = Font(name='Calibri', bold=True, size=11, color='FFFFFF')
HEADER_FONT  = Font(name='Calibri', bold=True, size=10, color='FFFFFF')
DATA_FONT    = Font(name='Calibri', size=10)
WRAP_ALIGN   = Alignment(wrap_text=True, vertical='top')
CENTER_ALIGN = Alignment(horizontal='center', vertical='center')


def dim_fill(dim):
    return PatternFill('solid', fgColor=DIM_CHART_COLORS.get(dim, '6B7280'))


def dim_header_cell(ws, row, col, dim, label=None):
    """Writes a dimension label into (row, col), solid-filled with that
    dimension's color and bold white text — the shared 'colored dimension chip'
    look used across Coded Passages, Freq sheets, and Speech Overview headers."""
    cell = ws.cell(row, col, label if label is not None else dim)
    cell.font = Font(bold=True, color='FFFFFF')
    cell.fill = dim_fill(dim)
    cell.alignment = CENTER_ALIGN
    return cell


def color_pie(chart, colors):
    for series in chart.series:
        for j, point in enumerate(series.dPt):
            if j < len(colors):
                point.spPr.solidFill = colors[j]


def add_dimension_pie(ws, labels_ref, data_ref, colors, anchor_cell, title):
    pie = PieChart()
    pie.title = title
    pie.width = 13
    pie.height = 12
    pie.add_data(data_ref)
    pie.set_categories(labels_ref)
    color_pie(pie, colors)
    ws.add_chart(pie, anchor_cell)


def add_colored_vbar(ws, labels_ref, data_ref, colors, anchor_cell, title, y_title):
    chart = BarChart()
    chart.type = "col"
    chart.grouping = "clustered"
    chart.title = title
    chart.y_axis.title = y_title
    chart.width = 15
    chart.height = 12
    chart.legend = None
    chart.add_data(data_ref)
    chart.set_categories(labels_ref)
    color_pie(chart, colors)  # dPt coloring works identically for bar series
    ws.add_chart(chart, anchor_cell)


def add_ranked_hbar(ws, labels_ref, data_ref, colors, anchor_cell, title, n_rows):
    """Horizontal bar chart for a frequency ranking: colored per-row by dimension,
    with the highest value at the TOP (Excel's default for a 'bar' chart type
    puts the first data row at the bottom of the category axis, so we flip the
    axis orientation to match the sorted-descending row order)."""
    chart = BarChart()
    chart.type = "bar"
    chart.grouping = "clustered"
    chart.title = title
    chart.x_axis.title = "Count"
    chart.width = 20
    chart.height = max(10, n_rows * 0.55)
    chart.legend = None
    chart.add_data(data_ref)
    chart.set_categories(labels_ref)
    color_pie(chart, colors)
    chart.y_axis.scaling.orientation = "maxMin"  # highest count at top
    chart.x_axis.crosses = "max"
    ws.add_chart(chart, anchor_cell)


def build_workbook(entries, speech_list, venue_groups):
    wb = openpyxl.Workbook()

    # ── Sheet 1: Coded Passages ────────────────────────────────────────────────
    # Columns A-M (13 total):
    #   A:#  B:Dimension  C:Sub-dimension  D:Dimension(Full)  E:Sub-code(Full)
    #   F:Quoted Passage  G:Analytical Memo  H:Speech  I:Date
    #   J:Venue  K:Type  L:Venue Group  M:Scope
    ws = wb.active
    ws.title = 'Coded Passages'

    ws.merge_cells('A1:M1')
    ws['A1'] = "Milei Climate Narratives — v4 Coded Passages  ·  Data source for all summary sheets"
    ws['A1'].font = Font(name='Calibri', bold=True, size=12, color='111827')
    ws['A1'].fill = PatternFill('solid', fgColor='E0F2FE')
    ws['A1'].alignment = Alignment(horizontal='left', vertical='center')
    ws.row_dimensions[1].height = 22

    headers    = ['#', 'Dimension', 'Sub-dimension', 'Dimension (Full)', 'Sub-code (Full)',
                  'Quoted Passage', 'Analytical Memo', 'Speech', 'Date',
                  'Venue', 'Type', 'Venue Group', 'Scope']
    col_widths = [5, 8, 30, 34, 34, 55, 60, 25, 12, 22, 18, 28, 14]

    for ci, (h, w) in enumerate(zip(headers, col_widths), 1):
        cell = ws.cell(2, ci, h)
        cell.font = HEADER_FONT
        cell.fill = PatternFill('solid', fgColor='1E3A5F')
        cell.alignment = CENTER_ALIGN
        ws.column_dimensions[get_column_letter(ci)].width = w
    ws.row_dimensions[2].height = 16

    for i, e in enumerate(entries, 1):
        r = i + 2
        sub_display = SUBCODE_DISPLAY.get(e['sub_key'], e['sub_key'].replace('_', ' '))
        dim_full    = DIM_FULL.get(e['dim'], e['dim'])
        row_vals = [
            i, e['dim'], sub_display, dim_full, sub_display,
            e['passage'], e['memo'], e['speech'], e['date'],
            e['venue'], e['event_type'], e.get('venue_group', 'Unclassified'), e['scope'],
        ]
        for ci, v in enumerate(row_vals, 1):
            cell = ws.cell(r, ci, v)
            cell.font = DATA_FONT
            cell.alignment = WRAP_ALIGN
        # Columns A and B: solid dimension color, bold white text — the
        # requested "colouring format applied per coded passage".
        dim_header_cell(ws, r, 1, e['dim'], label=i)
        ws.cell(r, 1).alignment = Alignment(horizontal='center', vertical='top')
        dim_header_cell(ws, r, 2, e['dim'])
        ws.cell(r, 2).alignment = Alignment(horizontal='center', vertical='top', wrap_text=True)
        ws.row_dimensions[r].height = 60

    ws.freeze_panes = 'A3'

    # ── Sheet 2: Freq — By Dimension (redesigned: compact totals, not a
    #    194-column per-speech crosstab — that view now lives properly in
    #    'Speech Overview') ─────────────────────────────────────────────────
    wd = wb.create_sheet('Freq — By Dimension')
    wd.merge_cells('A1:D1')
    wd['A1'] = "Dimension Totals  —  values update automatically from 'Coded Passages'"
    wd['A1'].font = Font(bold=True, size=11)
    wd['A1'].fill = PatternFill('solid', fgColor='E0F2FE')

    dim_headers = ['Dimension', 'Dimension (Full)', 'Total', '% of Corpus']
    for ci, h in enumerate(dim_headers, 1):
        cell = wd.cell(2, ci, h)
        cell.font = HEADER_FONT
        cell.fill = PatternFill('solid', fgColor='1E3A5F')
        cell.alignment = CENTER_ALIGN
    wd.column_dimensions['A'].width = 12
    wd.column_dimensions['B'].width = 40
    wd.column_dimensions['C'].width = 12
    wd.column_dimensions['D'].width = 14

    DATA_START_ROW_DIM = 3
    for i, dim in enumerate(DIMS_ORDER):
        r = DATA_START_ROW_DIM + i
        dim_header_cell(wd, r, 1, dim)
        wd.cell(r, 2, DIM_FULL.get(dim, dim))
        wd.cell(r, 3).value = f"=COUNTIFS('Coded Passages'!$B:$B,$A{r})"
    DATA_END_ROW_DIM = DATA_START_ROW_DIM + len(DIMS_ORDER) - 1

    tr_dim = DATA_END_ROW_DIM + 1
    for r in range(DATA_START_ROW_DIM, DATA_END_ROW_DIM + 1):
        wd.cell(r, 4).value = f"=C{r}/$C${tr_dim}"
        wd.cell(r, 4).number_format = '0.0%'

    wd.cell(tr_dim, 1, 'TOTAL').font = Font(bold=True)
    wd.cell(tr_dim, 2, 'All Dimensions').font = Font(bold=True)
    wd.cell(tr_dim, 3).value = f"=SUM(C{DATA_START_ROW_DIM}:C{DATA_END_ROW_DIM})"
    wd.cell(tr_dim, 3).font = Font(bold=True)
    wd.cell(tr_dim, 4).value = f"=SUM(D{DATA_START_ROW_DIM}:D{DATA_END_ROW_DIM})"
    wd.cell(tr_dim, 4).font = Font(bold=True)
    wd.cell(tr_dim, 4).number_format = '0.0%'

    dim_counts = Counter(e['dim'] for e in entries)
    colors_in_order = [DIM_CHART_COLORS[d] for d in DIMS_ORDER]
    labels_ref = Reference(wd, min_col=1, max_col=1, min_row=DATA_START_ROW_DIM, max_row=DATA_END_ROW_DIM)
    data_ref   = Reference(wd, min_col=3, max_col=3, min_row=DATA_START_ROW_DIM, max_row=DATA_END_ROW_DIM)
    add_dimension_pie(wd, labels_ref, data_ref, colors_in_order,
                       f"A{tr_dim + 2}", "Dimension Share of Total Annotations")
    add_colored_vbar(wd, labels_ref, data_ref, colors_in_order,
                      f"F{tr_dim + 2}", "Dimension Totals", "Annotations")

    # ── Sheet 3: Freq — By Sub-code ───────────────────────────────────────────
    # Rows are sorted globally by descending frequency (matches the HTML's
    # "Code Frequency Ranking"), not grouped by dimension order.
    ws2 = wb.create_sheet('Freq — By Sub-code')
    ws2.merge_cells('A1:L1')
    ws2['A1'] = "Code Frequency by Sub-code × Speech  —  values update automatically from 'Coded Passages'"
    ws2['A1'].font = Font(bold=True, size=11)
    ws2['A1'].fill = PatternFill('solid', fgColor='E0F2FE')

    n_sp = len(speech_list)
    # FIX (2026-08-08): speech data columns must start at column C (col 3), not B —
    # column B holds the "Sub-code" label. The previous version used
    # get_column_letter(i + 2), which put the first speech in column B and
    # silently clobbered the label with a COUNTIFS formula in every data row.
    sp_cols_sc = {s: get_column_letter(i + 3) for i, s in enumerate(speech_list)}
    total_col_num_sc = n_sp + 3
    total_col_ltr_sc = get_column_letter(total_col_num_sc)

    for ci, h in enumerate((['Dim', 'Sub-code'] + speech_list + ['TOTAL']), 1):
        cell = ws2.cell(2, ci, h)
        cell.font = HEADER_FONT
        cell.fill = PatternFill('solid', fgColor='1E3A5F')
        cell.alignment = CENTER_ALIGN
    ws2.column_dimensions['A'].width = 7
    ws2.column_dimensions['B'].width = 42
    for col in sp_cols_sc.values():
        ws2.column_dimensions[col].width = 20
    ws2.column_dimensions[total_col_ltr_sc].width = 10

    # Global frequency count per (dim, sub_key) to sort rows descending.
    sub_counts = Counter((e['dim'], e['sub_key']) for e in entries)
    ordered_subs = list(_canonical_subcode_keys())  # ensures zero-count codes appear
    seen = {(d, k) for d, k, _ in ordered_subs}
    for e in entries:
        k = (e['dim'], e['sub_key'])
        if k not in seen:
            seen.add(k)
            ordered_subs.append((e['dim'], e['sub_key'],
                                  SUBCODE_DISPLAY.get(e['sub_key'], e['sub_key'].replace('_', ' '))))
    ordered_subs.sort(key=lambda t: sub_counts.get((t[0], t[1]), 0), reverse=True)

    DATA_START_ROW_SC = 3
    sr = DATA_START_ROW_SC
    for dim, sub_key, sub_display in ordered_subs:
        dim_header_cell(ws2, sr, 1, dim)
        ws2.cell(sr, 2, sub_display).font = DATA_FONT
        for sp, col in sp_cols_sc.items():
            ci = column_index_from_string(col)
            ws2.cell(sr, ci).value = (
                f"=COUNTIFS('Coded Passages'!$B:$B,$A{sr},"
                f"'Coded Passages'!$E:$E,$B{sr},"
                f"'Coded Passages'!$H:$H,{col}$2)"
            )
        ws2.cell(sr, total_col_num_sc).value = (
            f"=SUM(C{sr}:{get_column_letter(total_col_num_sc - 1)}{sr})"
        )
        sr += 1

    DATA_END_ROW_SC = sr - 1

    ws2.cell(sr, 1, 'TOTAL').font = Font(bold=True)
    ws2.cell(sr, 2, 'All Sub-codes').font = Font(bold=True)
    for ci in range(3, total_col_num_sc + 1):
        col = get_column_letter(ci)
        ws2.cell(sr, ci).value = f"=SUM({col}{DATA_START_ROW_SC}:{col}{DATA_END_ROW_SC})"
        ws2.cell(sr, ci).font = Font(bold=True)

    sc_colors = [DIM_CHART_COLORS.get(d, '6B7280') for d, _, _ in ordered_subs]
    sc_labels_ref = Reference(ws2, min_col=2, max_col=2, min_row=DATA_START_ROW_SC, max_row=DATA_END_ROW_SC)
    sc_data_ref   = Reference(ws2, min_col=total_col_num_sc, max_col=total_col_num_sc,
                               min_row=DATA_START_ROW_SC, max_row=DATA_END_ROW_SC)
    CHART_ANCHOR_ROW_SC = sr + 2
    add_ranked_hbar(ws2, sc_labels_ref, sc_data_ref, sc_colors,
                     f"A{CHART_ANCHOR_ROW_SC}", "Code Frequency Ranking (all sub-codes, corpus-wide)",
                     DATA_END_ROW_SC - DATA_START_ROW_SC + 1)

    # ── Sheet 4: Speech Overview ───────────────────────────────────────────────
    ws3 = wb.create_sheet('Speech Overview')
    ws3.merge_cells('A1:K1')
    ws3['A1'] = "Speech-Level Overview  --  D1.1 / D1.2 / D1.3 counts update automatically from 'Coded Passages'"
    ws3['A1'].font = Font(bold=True, size=11)
    ws3['A1'].fill = PatternFill('solid', fgColor='E0F2FE')

    ov_headers = ['Speech', 'Date', 'Venue', 'Type', 'Venue Group', 'Scope',
                  'D1.1', 'D1.2', 'D1.3', 'Total', 'Notes']
    for ci, h in enumerate(ov_headers, 1):
        cell = ws3.cell(2, ci, h)
        cell.font = HEADER_FONT
        cell.fill = PatternFill('solid', fgColor='1E3A5F')
        cell.alignment = CENTER_ALIGN
    ws3.column_dimensions['A'].width = 30
    ws3.column_dimensions['B'].width = 12
    ws3.column_dimensions['C'].width = 22
    ws3.column_dimensions['D'].width = 18
    ws3.column_dimensions['E'].width = 26
    ws3.column_dimensions['F'].width = 14
    # Color the D1.1/D1.2/D1.3 header cells to match the dimension palette.
    for ci, dim in zip((7, 8, 9), ('D1.1', 'D1.2', 'D1.3')):
        c = ws3.cell(2, ci)
        c.fill = dim_fill(dim)
        c.font = Font(bold=True, color='FFFFFF')

    speech_meta = {}
    for e in entries:
        speech_meta.setdefault(e['speech'], (e['date'], e['venue'], e['event_type'],
                                              e.get('venue_group', 'Unclassified'), e['scope']))
    for si, sp in enumerate(speech_list, 3):
        meta = speech_meta.get(sp, ("", "", "", "Unclassified", ""))
        date, venue, event_type, venue_group, scope = meta
        ws3.cell(si, 1, sp)
        ws3.cell(si, 2, date)
        ws3.cell(si, 3, venue)
        ws3.cell(si, 4, event_type.title() if event_type else "")
        ws3.cell(si, 5, venue_group)
        ws3.cell(si, 6, scope)
        ws3.cell(si, 7).value  = f"=COUNTIFS('Coded Passages'!$H:$H,$A{si},'Coded Passages'!$B:$B,\"D1.1\")"
        ws3.cell(si, 8).value  = f"=COUNTIFS('Coded Passages'!$H:$H,$A{si},'Coded Passages'!$B:$B,\"D1.2\")"
        ws3.cell(si, 9).value  = f"=COUNTIFS('Coded Passages'!$H:$H,$A{si},'Coded Passages'!$B:$B,\"D1.3\")"
        ws3.cell(si, 10).value = f"=G{si}+H{si}+I{si}"

    tr_ov = len(speech_list) + 3
    ws3.cell(tr_ov, 1, 'TOTAL').font = Font(bold=True)
    for ci in range(7, 11):
        col = get_column_letter(ci)
        ws3.cell(tr_ov, ci).value = f"=SUM({col}3:{col}{tr_ov - 1})"
        ws3.cell(tr_ov, ci).font = Font(bold=True)

    # ── Sheet 5: Freq — By Scope ──────────────────────────────────────────────
    build_scope_sheet(wb, len(speech_list), entries)
    # ── Sheet 6: Freq — By Venue Type (regrouped into 6 categories) ──────────
    build_venue_type_sheet(wb, len(speech_list), venue_groups)

    return wb


def _context_sheet(wb, sheet_name, categories, col_letter, col_label, n_sp, category_labels=None):
    """
    Generic cross-tab sheet: Dimension/Sub-code × context categories.
    col_letter: the column in 'Coded Passages' to filter on (L or M)
    col_label:  a short label for the title
    n_sp:       number of speech columns in Coded Passages (used to set column widths)
    categories: raw values as stored in the Coded Passages column (used in COUNTIFS formulas)
    category_labels: optional display labels (same length/order as categories) for headers —
        defaults to categories itself when not given.

    Returns the row number immediately after the sheet's content, so callers can
    append additional sections (see build_scope_sheet's ranked-by-scope charts).
    """
    if category_labels is None:
        category_labels = categories
    SUBCODES_V4 = _canonical_subcode_lists()

    n_cats = len(categories)
    total_col_num = n_cats + 3           # A=Dim/Sub, B=Full, C..=cats, then TOTAL
    total_col_ltr = get_column_letter(total_col_num)

    ws = wb.create_sheet(sheet_name)
    ws.merge_cells(f"A1:{total_col_ltr}1")
    ws["A1"] = f"Code Frequency by {col_label}  —  values update automatically from 'Coded Passages'"
    ws["A1"].font = Font(bold=True, size=11)
    ws["A1"].fill = PatternFill("solid", fgColor="E0F2FE")

    hdrs = ["Dimension", "Dimension (Full)"] + category_labels + ["TOTAL"]
    for ci, h in enumerate(hdrs, 1):
        cell = ws.cell(2, ci, h)
        cell.font = HEADER_FONT
        cell.fill = PatternFill("solid", fgColor="1E3A5F")
        cell.alignment = CENTER_ALIGN
    ws.column_dimensions["A"].width = 8
    ws.column_dimensions["B"].width = 34
    for ci in range(3, n_cats + 3):
        ws.column_dimensions[get_column_letter(ci)].width = 24
    ws.column_dimensions[total_col_ltr].width = 10

    # ── Section 1: Dimension totals ───────────────────────────────────────────
    DIM_START = 3
    for dr_off, dim in enumerate(DIMS_ORDER):
        dr = DIM_START + dr_off
        dim_header_cell(ws, dr, 1, dim)
        ws.cell(dr, 2, DIM_FULL.get(dim, dim))
        for ci, cat in enumerate(categories, 3):
            ws.cell(dr, ci).value = (
                f"=COUNTIFS('Coded Passages'!$B:$B,$A{dr},"
                f"'Coded Passages'!${col_letter}:${col_letter},\"{cat}\")"
            )
        ws.cell(dr, total_col_num).value = (
            f"=SUM(C{dr}:{get_column_letter(total_col_num-1)}{dr})"
        )

    DIM_END = DIM_START + len(DIMS_ORDER) - 1

    tr_dim = DIM_END + 1
    ws.cell(tr_dim, 1, "TOTAL").font = Font(bold=True)
    ws.cell(tr_dim, 2, "All Dimensions").font = Font(bold=True)
    for ci in range(3, total_col_num + 1):
        col = get_column_letter(ci)
        ws.cell(tr_dim, ci).value = f"=SUM({col}{DIM_START}:{col}{DIM_END})"
        ws.cell(tr_dim, ci).font = Font(bold=True)

    # ── Dimension grouped-bar chart ───────────────────────────────────────────
    dim_chart = BarChart()
    dim_chart.type = "col"
    dim_chart.grouping = "clustered"
    dim_chart.title = f"Dimension Distribution by {col_label}"
    dim_chart.y_axis.title = "Annotations"
    dim_chart.width  = 28
    dim_chart.height = 14

    data_ref = Reference(ws, min_col=3, max_col=n_cats + 2,
                         min_row=DIM_START, max_row=DIM_END)
    dim_chart.add_data(data_ref, from_rows=True)

    dim_labels = ["D1.1 — State/Gov.", "D1.2 — Science/Expertise",
                  "D1.3 — Cultural Backlash", "Inductive"]
    for i, label in enumerate(dim_labels[:len(dim_chart.series)]):
        dim_chart.series[i].title = SeriesLabel(v=label)
        dim_chart.series[i].graphicalProperties.solidFill = DIM_CHART_COLORS[DIMS_ORDER[i]]

    cats_ref = Reference(ws, min_col=3, max_col=n_cats + 2, min_row=2, max_row=2)
    dim_chart.set_categories(cats_ref)
    ws.add_chart(dim_chart, f"A{tr_dim + 2}")

    # ── Section 2: Sub-code detail ────────────────────────────────────────────
    SC_HEADER_ROW = tr_dim + 22   # below chart
    ws.merge_cells(f"A{SC_HEADER_ROW}:{total_col_ltr}{SC_HEADER_ROW}")
    ws[f"A{SC_HEADER_ROW}"] = f"Sub-code Detail × {col_label}"
    ws[f"A{SC_HEADER_ROW}"].font = Font(bold=True, size=11)
    ws[f"A{SC_HEADER_ROW}"].fill = PatternFill("solid", fgColor="F0FDF4")

    sc_hdrs = ["Dim", "Sub-code"] + category_labels + ["TOTAL"]
    for ci, h in enumerate(sc_hdrs, 1):
        cell = ws.cell(SC_HEADER_ROW + 1, ci, h)
        cell.font = HEADER_FONT
        cell.fill = PatternFill("solid", fgColor="374151")
        cell.alignment = CENTER_ALIGN

    sr = SC_HEADER_ROW + 2
    SC_DATA_START = sr
    for dim, subs in SUBCODES_V4:
        for sub in subs:
            dim_header_cell(ws, sr, 1, dim)
            ws.cell(sr, 2, sub).font = DATA_FONT
            for ci, cat in enumerate(categories, 3):
                ws.cell(sr, ci).value = (
                    f"=COUNTIFS('Coded Passages'!$B:$B,$A{sr},"
                    f"'Coded Passages'!$E:$E,$B{sr},"
                    f"'Coded Passages'!${col_letter}:${col_letter},\"{cat}\")"
                )
            ws.cell(sr, total_col_num).value = (
                f"=SUM(C{sr}:{get_column_letter(total_col_num-1)}{sr})"
            )
            sr += 1
    SC_DATA_END = sr - 1

    ws.cell(sr, 1, "TOTAL").font = Font(bold=True)
    ws.cell(sr, 2, "All Sub-codes").font = Font(bold=True)
    for ci in range(3, total_col_num + 1):
        col = get_column_letter(ci)
        ws.cell(sr, ci).value = f"=SUM({col}{SC_DATA_START}:{col}{SC_DATA_END})"
        ws.cell(sr, ci).font = Font(bold=True)

    return ws, sr + 1


def build_scope_sheet(wb, n_sp, entries):
    ws, next_row = _context_sheet(wb, "Freq — By Scope",
                                   SCOPE_CATEGORIES, SCOPE_COL, "Scope", n_sp)

    # ── Section 3: Sub-code frequency ranking, split by scope ────────────────
    # Directly addresses the codebook's own analytical question of whether
    # specific sub-codes cluster by where a speech is delivered.
    header_row = next_row + 1
    ws.merge_cells(f"A{header_row}:F{header_row}")
    ws[f"A{header_row}"] = "Sub-code Frequency Ranking — National vs. International"
    ws[f"A{header_row}"].font = Font(bold=True, size=11)
    ws[f"A{header_row}"].fill = PatternFill("solid", fgColor="F0FDF4")

    by_scope = defaultdict(Counter)
    for e in entries:
        by_scope[e['scope']][(e['dim'], e['sub_key'])] += 1

    canonical = _canonical_subcode_keys()

    table_start = header_row + 2
    anchors = {}
    for col_offset, scope in enumerate(SCOPE_CATEGORIES):
        base_col = 1 + col_offset * 4   # National -> A-D, International -> E-H
        c_dim, c_sub, c_total = base_col, base_col + 1, base_col + 2

        counts = by_scope.get(scope, Counter())
        ordered = sorted(canonical, key=lambda t: counts.get((t[0], t[1]), 0), reverse=True)

        ws.cell(table_start - 1, c_dim, scope).font = Font(bold=True, size=10)
        ws.cell(table_start - 1, c_sub, "Sub-code").font = Font(bold=True, size=10)
        ws.cell(table_start - 1, c_total, "Count").font = Font(bold=True, size=10)
        ws.column_dimensions[get_column_letter(c_sub)].width = 40
        ws.column_dimensions[get_column_letter(c_total)].width = 10

        for i, (dim, sub_key, sub_display) in enumerate(ordered):
            r = table_start + i
            dim_header_cell(ws, r, c_dim, dim)
            ws.cell(r, c_sub, sub_display).font = DATA_FONT
            ws.cell(r, c_total).value = counts.get((dim, sub_key), 0)
        table_end = table_start + len(ordered) - 1
        anchors[scope] = (c_dim, c_sub, c_total, table_start, table_end,
                           [DIM_CHART_COLORS.get(d, '6B7280') for d, _, _ in ordered])

    chart_row = max(a[4] for a in anchors.values()) + 3
    for col_offset, scope in enumerate(SCOPE_CATEGORIES):
        c_dim, c_sub, c_total, t_start, t_end, colors = anchors[scope]
        labels_ref = Reference(ws, min_col=c_sub, max_col=c_sub, min_row=t_start, max_row=t_end)
        data_ref   = Reference(ws, min_col=c_total, max_col=c_total, min_row=t_start, max_row=t_end)
        anchor_col_letter = get_column_letter(1 + col_offset * 7)
        add_ranked_hbar(ws, labels_ref, data_ref, colors,
                         f"{anchor_col_letter}{chart_row}",
                         f"Sub-code Ranking — {scope}", t_end - t_start + 1)


def build_venue_type_sheet(wb, n_sp, venue_groups):
    """venue_groups: ordered list of the 6 venue-group category names actually
    present in the corpus (corpus_metadata.venue_group_categories()) — replaces
    the previous 23-raw-`tipo`-value version, which was too granular to read
    as a chart or crosstab."""
    return _context_sheet(wb, "Freq — By Venue Type",
                          venue_groups, VENUE_GROUP_COL, "Venue Group", n_sp,
                          category_labels=venue_groups)

# -- Main --

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

    all_entries = []
    for f in files:
        print(f"  {f['filename']}: {len(f['flat_entries'])} code annotations")
        all_entries.extend(f['flat_entries'])

    print(f"\nTotal code annotations: {len(all_entries)}")

    # Chronological order falls out naturally: coded_files is sorted alphabetically
    # (filenames are YYYY-MM-DD-prefixed), so first-occurrence order in all_entries
    # already matches chronological order — no hardcoded SPEECH_ORDER needed.
    present_speeches = []
    for e in all_entries:
        if e['speech'] not in present_speeches:
            present_speeches.append(e['speech'])

    venue_groups = venue_group_categories(meta_index)
    print(f"Venue groups present in corpus: {venue_groups}")
    print(f"Speeches in workbook: {present_speeches}")

    # Guard: the master workbook (qda_v4_coded_corpus_261011.xlsx) is edited by hand and carries
    # collaborator notes, comment columns and a pivot table that this script cannot reproduce.
    # NEVER write over it. To build a fresh workbook from the .md files for comparison, pass
    # --out <path> pointing to a different file.
    out = OUTPUT_PATH
    if '--out' in sys.argv:
        out = Path(sys.argv[sys.argv.index('--out') + 1]).resolve()
    if out == MASTER_PATH or (out.exists() and out.name == MASTER_PATH.name):
        print("\nABORTED: refusing to overwrite the master workbook "
              f"({MASTER_PATH.name}). Edit it directly and use sync_xlsx_to_md.py; "
              "to regenerate a fresh workbook for comparison use: generate_xlsx.py --out <other_path>.xlsx")
        sys.exit(3)

    out.parent.mkdir(parents=True, exist_ok=True)
    wb = build_workbook(all_entries, present_speeches, venue_groups)
    wb.save(out)
    print(f"\nSaved: {out}")
    print(f"  Sheets: {wb.sheetnames}")
    print(f"  Coded Passages rows: {len(all_entries)}")


if __name__ == '__main__':
    main()
