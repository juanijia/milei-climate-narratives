# %%
"""
Dimension 2 — Phase 2.1: Institutional budget layer
Argentina under Milei — 2023 vs 2025

Purpose
-------
Build a reproducible institutional-level budget panel for the paper's
Section 5.2.1 (Budgetary retrenchment), using SAFs as the main longitudinal
institutional unit and explicit activity/programme rules where institutional
reclassification makes a SAF-only comparison misleading.

Design choices follow the D2 methodology proposal:
- Measure: credito_devengado for closed years
- Comparison: 2025 vs 2023
- Base year: 2023
- Universe: Administración Nacional
- Deflator: INDEC CPI, national/general level, annual average
- Main indicators: real change, budget share, RRI, priority ratio,
  execution rate, and reallocation rate

Important:
-----------
This script is deliberately an ANALYTICAL PIPELINE, not a paper-writing
script. It exports clean CSVs for inspection in VS Code/Data Wrangler.

It does NOT yet attempt to:
- construct the legal/decree concordance for every institutional change;
- estimate FNECBN as a separate programme (reserved for Phase 3);
- include national universities in the aggregate public-science total;
- infer institutional "erosion" solely from spending changes.

Those are documented as separate analytical tasks.
"""

# %%
from __future__ import annotations

import json
import re
import ssl
import urllib.request
import zipfile
from pathlib import Path

import pandas as pd


# =============================================================================
# 1. PROJECT PATHS AND CONFIGURATION
# =============================================================================

PROJECT_DIR = Path(__file__).resolve().parent
RAW_DIR = PROJECT_DIR / "data" / "raw"
PROCESSED_DIR = PROJECT_DIR / "data" / "processed"
OUTPUT_DIR = PROJECT_DIR / "outputs"

for directory in (RAW_DIR, PROCESSED_DIR, OUTPUT_DIR):
    directory.mkdir(parents=True, exist_ok=True)

YEARS = [2023, 2025]
BASE_YEAR = 2023
TARGET_YEAR = 2025

EXPECTED_UNIVERSE = "Administración Nacional"

# Tolerances are deliberately explicit.
# 2023 is expected to reproduce FARN's Table 2 very closely.
FARN_2023_TOLERANCE_PCT = 0.10
FARN_2025_REPORT_TOLERANCE_PCT = 1.00

# The current Phase 2 perimeter intentionally does not aggregate universities
# into "public science", because their scale can dominate the category.
# They are exported separately and can be switched on later.
INCLUDE_UNIVERSITIES = False

pd.set_option("display.max_columns", 100)
pd.set_option("display.width", 220)
pd.set_option("display.float_format", lambda x: f"{x:,.3f}")


# =============================================================================
# 2. HTTP / DOWNLOAD UTILITIES
# =============================================================================

HEADERS = {
    "User-Agent": "Mozilla/5.0 (academic research; reproducible public-budget analysis)"
}


def fetch(url: str, timeout: int = 300) -> bytes:
    """
    Download a public resource.

    SSL verification is kept ON by default. If a government endpoint fails
    certificate validation on the researcher's machine, fix the local
    certificate chain rather than silently disabling verification.
    """
    context = ssl.create_default_context()
    request = urllib.request.Request(url, headers=HEADERS)

    with urllib.request.urlopen(request, context=context, timeout=timeout) as response:
        return response.read()


# =============================================================================
# 3. PRESUPUESTO ABIERTO DATASET DISCOVERY
# =============================================================================

CATALOG_URL = (
    "https://www.presupuestoabierto.gob.ar/"
    "sici/rest-api/catalog/site"
)


def discover_datasets(
    name_contains: str = "ejecución detallada - agrupación anual",
) -> pd.DataFrame:
    """Read the Presupuesto Abierto catalogue and return matching datasets."""
    payload = json.loads(fetch(CATALOG_URL).decode("utf-8"))

    rows = []
    for distribution in payload["distribuciones"]:
        resource_name = distribution["nombreRecurso"]

        if name_contains.lower() in resource_name.lower():
            rows.append(
                {
                    "ejercicios": distribution["ejercicios"],
                    "recurso": resource_name,
                    "actualizado": distribution["fechaDeActualizacion"],
                    "registros": distribution["cantidadDeRegistros"],
                    "url": distribution["urlArchivo"],
                }
            )

    if not rows:
        raise RuntimeError(
            "No matching Presupuesto Abierto dataset was found. "
            "Inspect the catalogue manually."
        )

    return pd.DataFrame(rows)


catalogue = discover_datasets()

catalogue_relevant = catalogue[
    catalogue["ejercicios"].map(lambda x: bool(set(x) & set(YEARS)))
].copy()

catalogue_relevant.to_csv(
    PROCESSED_DIR / "dataset_provenance_catalogue.csv",
    index=False,
)

print("Relevant Presupuesto Abierto datasets:")
print(catalogue_relevant.to_string(index=False))


# =============================================================================
# 4. DOWNLOAD / LOAD ANNUAL MICRODATA
# =============================================================================

MEASURES = [
    "credito_presupuestado",
    "credito_vigente",
    "credito_devengado",
]

USECOLS = [
    "ejercicio_presupuestario",
    "subsector_desc",
    "caracter_desc",
    "jurisdiccion_id",
    "jurisdiccion_desc",
    "entidad_id",
    "entidad_desc",
    "servicio_id",
    "servicio_desc",
    "programa_id",
    "programa_desc",
    "actividad_id",
    "actividad_desc",
    "finalidad_id",
    "funcion_id",
    "funcion_desc",
    "inciso_id",
    "inciso_desc",
] + MEASURES


def dataset_url_for_year(year: int) -> str:
    """
    Resolve the annual dataset URL from the official catalogue.

    This avoids relying on a hard-coded repository path if the government
    changes the storage URL.
    """
    matches = catalogue[
        catalogue["ejercicios"].map(lambda years: year in years)
    ]

    if matches.empty:
        raise RuntimeError(
            f"No annual budget dataset found in catalogue for {year}."
        )

    # Prefer the resource explicitly matching "ejecución detallada".
    return matches.iloc[0]["url"]


def parse_budget_number(series: pd.Series, column_name: str) -> pd.Series:
    """
    Parse Presupuesto Abierto numeric fields.

    Historical files use decimal commas and no thousands separators.
    Example: 48645,776825 -> 48645.776825.
    """
    if pd.api.types.is_numeric_dtype(series):
        return pd.to_numeric(series, errors="raise")

    raw = series.astype("string").str.strip()

    # Fail loudly if a future file introduces thousands separators or a new
    # number convention. Silent parsing is dangerous here.
    suspicious = raw.str.contains(r"\.", regex=True, na=False)
    if suspicious.any():
        examples = raw[suspicious].head(5).tolist()
        raise ValueError(
            f"Unexpected '.' found in {column_name}. "
            f"Check the source format. Examples: {examples}"
        )

    cleaned = raw.str.replace(",", ".", regex=False)
    return pd.to_numeric(cleaned, errors="raise")


def load_credito(year: int) -> pd.DataFrame:
    """Download, cache, extract and load one annual expenditure file."""

    zip_path = RAW_DIR / f"credito-anual-{year}.zip"

    if not zip_path.exists():
        url = dataset_url_for_year(year)
        print(f"Downloading {year}: {url}")
        zip_path.write_bytes(fetch(url))

    # Extract only if the expected CSV is not already present.
    candidate_csvs = list(RAW_DIR.glob(f"*{year}*.csv"))

    if not candidate_csvs:
        with zipfile.ZipFile(zip_path) as archive:
            archive.extractall(RAW_DIR)

        candidate_csvs = list(RAW_DIR.glob(f"*{year}*.csv"))

    if not candidate_csvs:
        raise FileNotFoundError(
            f"Could not find an extracted CSV for {year} in {RAW_DIR}."
        )

    # Prefer the file whose name contains "credito".
    credito_candidates = [
        p for p in candidate_csvs if "credito" in p.name.lower()
    ]

    csv_path = credito_candidates[0] if credito_candidates else candidate_csvs[0]

    print(f"Loading {year}: {csv_path.name}")

    df = pd.read_csv(
        csv_path,
        usecols=USECOLS,
        low_memory=False,
    )

    missing = [column for column in USECOLS if column not in df.columns]
    if missing:
        raise ValueError(
            f"{year}: required columns missing from source file: {missing}"
        )

    for column in MEASURES:
        df[column] = parse_budget_number(df[column], column)

    df["anio"] = year

    return df


credito = {year: load_credito(year) for year in YEARS}


# =============================================================================
# 5. SOURCE / UNIVERSE VALIDATION
# =============================================================================

def validate_source(df: pd.DataFrame, year: int) -> None:
    """Run basic integrity checks before analysis."""

    if df.empty:
        raise ValueError(f"{year}: source dataset is empty.")

    if df["credito_devengado"].isna().any():
        raise ValueError(f"{year}: missing values in credito_devengado.")

    if df["credito_vigente"].isna().any():
        raise ValueError(f"{year}: missing values in credito_vigente.")

    if df["credito_presupuestado"].isna().any():
        raise ValueError(f"{year}: missing values in credito_presupuestado.")

    universes = sorted(df["subsector_desc"].dropna().astype(str).unique())

    print(f"\n{year}")
    print(f"Rows: {len(df):,}")
    print(f"Universe labels: {universes}")
    print(f"Devengado total: {df.credito_devengado.sum():,.0f} million pesos")

    # We do not silently filter if the source contains another universe.
    # The researcher must see this before proceeding.
    if EXPECTED_UNIVERSE not in universes:
        raise ValueError(
            f"{year}: expected '{EXPECTED_UNIVERSE}' not found. "
            f"Actual labels: {universes}"
        )

    unexpected = [
        value for value in universes if value != EXPECTED_UNIVERSE
    ]

    if unexpected:
        raise ValueError(
            f"{year}: dataset contains universes other than "
            f"'{EXPECTED_UNIVERSE}': {unexpected}. "
            "Do not proceed until the universe is resolved."
        )


for year, df in credito.items():
    validate_source(df, year)


# =============================================================================
# 6. CPI DEFLATOR
# =============================================================================

CPI_URL = (
    "https://apis.datos.gob.ar/series/api/series/"
    "?ids=148.3_INIVELNAL_DICI_M_26"
    "&format=json&limit=5000&start_date=2016-12"
)


def indec_cpi_annual_average() -> pd.Series:
    """Retrieve monthly INDEC CPI and calculate annual averages."""
    payload = json.loads(fetch(CPI_URL).decode("utf-8"))

    series = pd.DataFrame(
        payload["data"],
        columns=["fecha", "ipc"],
    )

    series["fecha"] = pd.to_datetime(series["fecha"])
    series["ipc"] = pd.to_numeric(series["ipc"], errors="raise")

    series = series[
        series["fecha"].dt.year.isin(YEARS)
    ].copy()

    counts = series.groupby(series["fecha"].dt.year).size()

    for year in YEARS:
        if counts.get(year, 0) != 12:
            raise ValueError(
                f"INDEC CPI does not contain exactly 12 observations for {year}: "
                f"{counts.get(year, 0)}"
            )

    annual = (
        series
        .assign(anio=series["fecha"].dt.year)
        .groupby("anio")["ipc"]
        .mean()
    )

    return annual


CPI = indec_cpi_annual_average()

cpi_table = CPI.rename("ipc_annual_average").reset_index()
cpi_table.to_csv(
    PROCESSED_DIR / "deflator_indec_cpi_annual_average.csv",
    index=False,
)

DEFLATOR = CPI[TARGET_YEAR] / CPI[BASE_YEAR]

print("\nINDEC annual-average CPI:")
print(cpi_table.to_string(index=False))
print(
    f"\n2023→2025 cumulative inflation using annual averages: "
    f"{DEFLATOR - 1:.1%}"
)


# =============================================================================
# 7. FARN FINALIDAD VALIDATION
# =============================================================================

# FARN 2026, Table 2.
# Values are nominal executed spending in million pesos.
FARN_FINALIDAD = {
    1: (2_349_060, 6_652_753, -0.376),
    2: (1_710_842, 6_075_017, -0.217),
    3: (24_845_207, 90_257_189, -0.199),
    4: (5_647_579, 9_539_839, -0.628),
    5: (3_472_801, 10_352_974, -0.343),
}

FARN_TOTAL = (38_025_489, 122_877_771, -0.288)


def build_farn_validation() -> pd.DataFrame:
    all_data = pd.concat(credito.values(), ignore_index=True)

    ours = (
        all_data
        .groupby(["anio", "finalidad_id"])["credito_devengado"]
        .sum()
        .unstack("anio")
    )

    rows = []

    for finalidad, (f23, f25, f_real) in FARN_FINALIDAD.items():
        o23 = ours.loc[finalidad, BASE_YEAR]
        o25 = ours.loc[finalidad, TARGET_YEAR]

        rows.append(
            {
                "finalidad_id": finalidad,
                "ours_2023": o23,
                "farn_2023": f23,
                "diff_2023_pct": (o23 / f23 - 1) * 100,
                "ours_2025": o25,
                "farn_2025": f25,
                "diff_2025_pct": (o25 / f25 - 1) * 100,
                "farn_real_change": f_real,
            }
        )

    total23 = all_data.loc[
        all_data.anio == BASE_YEAR,
        "credito_devengado",
    ].sum()

    total25 = all_data.loc[
        all_data.anio == TARGET_YEAR,
        "credito_devengado",
    ].sum()

    rows.append(
        {
            "finalidad_id": "TOTAL",
            "ours_2023": total23,
            "farn_2023": FARN_TOTAL[0],
            "diff_2023_pct": (total23 / FARN_TOTAL[0] - 1) * 100,
            "ours_2025": total25,
            "farn_2025": FARN_TOTAL[1],
            "diff_2025_pct": (total25 / FARN_TOTAL[1] - 1) * 100,
            "farn_real_change": FARN_TOTAL[2],
        }
    )

    return pd.DataFrame(rows)


farn_validation = build_farn_validation()

farn_validation.to_csv(
    PROCESSED_DIR / "validation_farn_finalidad.csv",
    index=False,
)

print("\nFARN finalidades validation:")
print(farn_validation.to_string(index=False))

# 2023 is the hard validation checkpoint.
max_2023_gap = farn_validation["diff_2023_pct"].abs().max()

if max_2023_gap > FARN_2023_TOLERANCE_PCT:
    raise AssertionError(
        f"2023 FARN validation failed. Maximum gap = {max_2023_gap:.3f}%. "
        "Stop and investigate universe, source vintage, units, or parsing."
    )

# 2025 is reported as a diagnostic rather than an automatic failure because
# the methodology proposal already anticipates post-publication source revisions.
max_2025_gap = farn_validation["diff_2025_pct"].abs().max()

print(
    f"\nPASS: 2023 FARN validation within "
    f"{FARN_2023_TOLERANCE_PCT:.2f} percentage points."
)
print(
    f"2025 maximum gap versus FARN: {max_2025_gap:.3f}%. "
    "Inspect the validation table rather than silently harmonising it."
)


# =============================================================================
# 8. JURISDICTION CONCORDANCE
# =============================================================================

def jurisdiction_table(year: int) -> pd.DataFrame:
    df = credito[year]

    return (
        df.groupby(
            ["jurisdiccion_id", "jurisdiccion_desc"],
            dropna=False,
        )["credito_devengado"]
        .sum()
        .reset_index()
        .rename(columns={"credito_devengado": "devengado"})
    )


j23 = jurisdiction_table(BASE_YEAR)
j25 = jurisdiction_table(TARGET_YEAR)

jurisdiction_crosswalk = j23.merge(
    j25,
    on="jurisdiccion_id",
    how="outer",
    suffixes=("_2023", "_2025"),
)

def jurisdiction_status(row) -> str:
    a = row["jurisdiccion_desc_2023"]
    b = row["jurisdiccion_desc_2025"]

    if pd.isna(a):
        return "NEW_IN_2025"
    if pd.isna(b):
        return "ABSENT_IN_2025"
    if a == b:
        return "UNCHANGED"
    return "RENAMED_OR_RESTRUCTURED"


jurisdiction_crosswalk["status"] = jurisdiction_crosswalk.apply(
    jurisdiction_status,
    axis=1,
)

jurisdiction_crosswalk.to_csv(
    PROCESSED_DIR / "crosswalk_jurisdiction_2023_2025.csv",
    index=False,
)


# =============================================================================
# 9. SAF CONCORDANCE
# =============================================================================

def saf_table(year: int) -> pd.DataFrame:
    df = credito[year]

    return (
        df.groupby(
            ["servicio_id", "servicio_desc", "jurisdiccion_id", "jurisdiccion_desc"],
            dropna=False,
        )
        .agg(
            devengado=("credito_devengado", "sum"),
            vigente=("credito_vigente", "sum"),
            inicial=("credito_presupuestado", "sum"),
        )
        .reset_index()
    )


saf23 = saf_table(BASE_YEAR)
saf25 = saf_table(TARGET_YEAR)

saf_crosswalk = saf23.merge(
    saf25,
    on="servicio_id",
    how="outer",
    suffixes=("_2023", "_2025"),
)

def saf_status(row) -> str:
    a = row["servicio_desc_2023"]
    b = row["servicio_desc_2025"]

    if pd.isna(a):
        return "NEW_IN_2025"
    if pd.isna(b):
        return "ABSENT_IN_2025"
    if a == b and row["jurisdiccion_id_2023"] == row["jurisdiccion_id_2025"]:
        return "UNCHANGED"
    return "SAME_SAF_RESTRUCTURED"


saf_crosswalk["status"] = saf_crosswalk.apply(
    saf_status,
    axis=1,
)

# These columns are intentionally blank: they are the manual/legal research
# fields to be populated from the Boletín Oficial in the administrative layer.
saf_crosswalk["decree_reference"] = ""
saf_crosswalk["institutional_change_note"] = ""

saf_crosswalk = saf_crosswalk.sort_values(
    ["status", "devengado_2023"],
    ascending=[True, False],
)

saf_crosswalk.to_csv(
    PROCESSED_DIR / "crosswalk_SAF_2023_2025.csv",
    index=False,
)


# =============================================================================
# 10. FOCAL SAF DIAGNOSTIC
# =============================================================================

FOCAL_SAF = [
    317,  # Environment / former MAyDS
    107,  # APN
    103,  # CONICET
    336,  # Science and Technology
    106,  # CONAE
    173,  # Agencia I+D+i
    105,  # CNEA
    606,  # INTA
    608,  # INTI
    452,  # SMN
    321,  # INDEC
    330,  # Universities (reported separately)
    302,  # SIDE
]

focal_saf = saf_crosswalk[
    saf_crosswalk["servicio_id"].isin(FOCAL_SAF)
].copy()

focal_saf.to_csv(
    PROCESSED_DIR / "crosswalk_SAF_focal.csv",
    index=False,
)


# =============================================================================
# 11. ACTIVITY-LEVEL FIRE CROSSWALK
# =============================================================================

FIRE_PATTERN = re.compile(
    r"Servicio Nacional de Manejo del Fuego|^Manejo del Fuego",
    flags=re.IGNORECASE,
)


def fire_activity_detail(year: int) -> pd.DataFrame:
    df = credito[year].copy()

    mask = df["actividad_desc"].fillna("").str.contains(
        FIRE_PATTERN.pattern,
        case=False,
        regex=True,
    )

    subset = df.loc[mask].copy()

    result = (
        subset.groupby(
            [
                "jurisdiccion_id",
                "jurisdiccion_desc",
                "servicio_id",
                "servicio_desc",
                "programa_id",
                "programa_desc",
                "actividad_id",
                "actividad_desc",
            ],
            dropna=False,
        )["credito_devengado"]
        .sum()
        .reset_index()
        .sort_values("credito_devengado", ascending=False)
    )

    result["anio"] = year

    return result


fire_details = pd.concat(
    [fire_activity_detail(year) for year in YEARS],
    ignore_index=True,
)

fire_details.to_csv(
    PROCESSED_DIR / "fire_activity_crosswalk_2023_2025.csv",
    index=False,
)


# =============================================================================
# 12. EXPLICIT ANALYTICAL PERIMETER
# =============================================================================

# Rule format:
# ("saf", SAF_ID)
# ("saf_programa", SAF_ID, PROGRAMA_ID)
# ("actividad", REGEX)

PERIMETER = {
    # -------------------------------------------------------------------------
    # Environment
    # -------------------------------------------------------------------------
    "Ambiente (ex-MAyDS, SAF 317)": {
        "class": "Environment",
        "rules": [("saf", 317)],
        "note": "Core environmental administration; FNECBN not separately isolated here.",
    },

    "Parques Nacionales (APN)": {
        "class": "Environment",
        "rules": [("saf", 107)],
        "note": "APN; its own fire-management activity remains included in this SAF total.",
    },

    "Servicio Nacional de Manejo del Fuego": {
        "class": "Environment",
        "rules": [("actividad", FIRE_PATTERN.pattern)],
        "note": "Constant functional perimeter across the 2023→2025 transfer.",
    },

    "Cuenca Matanza-Riachuelo (ACUMAR)": {
        "class": "Environment",
        "rules": [
            ("saf_programa", 364, 44),
            ("saf_programa", 377, 44),
        ],
        "note": "Programme-level identification; must be checked against FARN aggregation.",
    },

    # -------------------------------------------------------------------------
    # Public science / knowledge infrastructure
    # -------------------------------------------------------------------------
    "CONICET": {
        "class": "Public science",
        "rules": [("saf", 103)],
        "note": "Core public research institution.",
    },

    "Ciencia y Tecnología (SAF 336)": {
        "class": "Public science",
        "rules": [("saf", 336)],
        "note": "Secretariat-level science and technology administration.",
    },

    "Agencia I+D+i (ANPCyT)": {
        "class": "Public science",
        "rules": [("saf", 173)],
        "note": "Research funding agency.",
    },

    "CONAE": {
        "class": "Public science",
        "rules": [("saf", 106)],
        "note": "Public scientific/technical infrastructure.",
    },

    "CNEA": {
        "class": "Public science",
        "rules": [("saf", 105)],
        "note": "Public scientific/technical infrastructure.",
    },

    "INTA": {
        "class": "Public science",
        "rules": [("saf", 606)],
        "note": "Agricultural research; reported individually because it is embedded in another policy function.",
    },

    "INTI": {
        "class": "Public science",
        "rules": [("saf", 608)],
        "note": "Industrial research/technical infrastructure.",
    },

    "Servicio Meteorológico Nacional": {
        "class": "Public science",
        "rules": [("saf", 452)],
        "note": "Climate/weather knowledge and monitoring infrastructure.",
    },

    "INDEC": {
        "class": "Public science",
        "rules": [("saf", 321)],
        "note": "Statistical knowledge infrastructure; not environmental-specific.",
    },

    "National universities": {
        "class": "Public science — separate",
        "rules": [("saf_programa", 330, 26)],
        "note": "Reported separately by default because aggregate university transfers are large.",
    },

    # -------------------------------------------------------------------------
    # Comparators
    # -------------------------------------------------------------------------
    "Ministerio de Salud (SAF 310)": {
        "class": "Comparator",
        "rules": [("saf", 310)],
        "note": "Comparator; not intended to represent the entire health function.",
    },

    "Inteligencia (SIDE / AFI, SAF 302)": {
        "class": "Comparator",
        "rules": [("saf", 302)],
        "note": "Comparator highlighted in FARN.",
    },

    "Armed forces": {
        "class": "Comparator",
        "rules": [
            ("saf", 374),
            ("saf", 379),
            ("saf", 381),
        ],
        "note": "Selected armed-forces SAFs.",
    },
}

PERIMETER_JURISDICTION = {
    "Servicio de la Deuda Pública": {
        "class": "Comparator",
        "jurisdiccion_id": 90,
        "note": "Jurisdiction-level comparator.",
    },
    "Seguridad (jurisdicción 41)": {
        "class": "Comparator",
        "jurisdiccion_id": 41,
        "note": "Jurisdiction-level comparator.",
    },
}


# =============================================================================
# 13. PERIMETER AUDIT — DETECT OVERLAPPING RULES
# =============================================================================

def select_rule(df: pd.DataFrame, rule) -> pd.Series:
    kind = rule[0]

    if kind == "saf":
        return df["servicio_id"].eq(rule[1])

    if kind == "saf_programa":
        return (
            df["servicio_id"].eq(rule[1])
            & df["programa_id"].eq(rule[2])
        )

    if kind == "actividad":
        return df["actividad_desc"].fillna("").str.contains(
            rule[1],
            case=False,
            regex=True,
        )

    raise ValueError(f"Unknown rule type: {kind}")


def select_rules(df: pd.DataFrame, rules) -> pd.Series:
    mask = pd.Series(False, index=df.index)

    for rule in rules:
        mask |= select_rule(df, rule)

    return mask


def audit_perimeter_overlaps(year: int) -> pd.DataFrame:
    df = credito[year]

    memberships = []

    for group, config in PERIMETER.items():
        mask = select_rules(df, config["rules"])

        memberships.append(
            pd.DataFrame(
                {
                    "row_index": df.index[mask],
                    "group": group,
                }
            )
        )

    membership = pd.concat(memberships, ignore_index=True)

    overlap_counts = (
        membership.groupby("row_index")["group"]
        .agg(["count", list])
        .reset_index()
        .rename(columns={"count": "n_groups", "list": "groups"})
    )

    overlap_counts = overlap_counts[
        overlap_counts["n_groups"] > 1
    ].copy()

    overlap_counts["anio"] = year

    return overlap_counts


overlap_2023 = audit_perimeter_overlaps(2023)
overlap_2025 = audit_perimeter_overlaps(2025)

overlap_report = pd.concat(
    [overlap_2023, overlap_2025],
    ignore_index=True,
)

overlap_report.to_csv(
    PROCESSED_DIR / "perimeter_overlap_audit.csv",
    index=False,
)

print(
    f"\nPerimeter overlap audit: "
    f"{len(overlap_report):,} overlapping source rows."
)
print(
    "This is not automatically an error: SNMF intentionally overlaps "
    "with institutional totals such as SAF 317 because it is analysed "
    "as a constant functional activity. Do not sum perimeter groups."
)


# =============================================================================
# 14. BUILD INSTITUTIONAL PANEL
# =============================================================================

def aggregate_group(df: pd.DataFrame, rules) -> dict:
    mask = select_rules(df, rules)
    subset = df.loc[mask]

    return {
        "devengado": subset["credito_devengado"].sum(),
        "vigente": subset["credito_vigente"].sum(),
        "inicial": subset["credito_presupuestado"].sum(),
        "source_rows": int(mask.sum()),
    }


rows = []

for year in YEARS:
    df = credito[year]

    # Total national budget.
    rows.append(
        {
            "anio": year,
            "group": "TOTAL Administración Nacional",
            "class": "Total",
            "devengado": df["credito_devengado"].sum(),
            "vigente": df["credito_vigente"].sum(),
            "inicial": df["credito_presupuestado"].sum(),
            "source_rows": len(df),
            "selection_note": "All source rows.",
        }
    )

    # SAF/programme/activity perimeter.
    for group, config in PERIMETER.items():
        values = aggregate_group(df, config["rules"])

        rows.append(
            {
                "anio": year,
                "group": group,
                "class": config["class"],
                **values,
                "selection_note": config["note"],
            }
        )

    # Jurisdiction-level comparators.
    for group, config in PERIMETER_JURISDICTION.items():
        mask = df["jurisdiccion_id"].eq(config["jurisdiccion_id"])
        subset = df.loc[mask]

        rows.append(
            {
                "anio": year,
                "group": group,
                "class": config["class"],
                "devengado": subset["credito_devengado"].sum(),
                "vigente": subset["credito_vigente"].sum(),
                "inicial": subset["credito_presupuestado"].sum(),
                "source_rows": int(mask.sum()),
                "selection_note": config["note"],
            }
        )


panel = pd.DataFrame(rows)

panel.to_csv(
    PROCESSED_DIR / "panel_institucional_raw.csv",
    index=False,
)


# =============================================================================
# 15. INDICATORS
# =============================================================================

wide = panel.pivot_table(
    index=["class", "group"],
    columns="anio",
    values=["devengado", "vigente", "inicial"],
)

results = pd.DataFrame(index=wide.index)

results["devengado_2023"] = wide[("devengado", 2023)]
results["devengado_2025"] = wide[("devengado", 2025)]

results["vigente_2023"] = wide[("vigente", 2023)]
results["vigente_2025"] = wide[("vigente", 2025)]

results["inicial_2023"] = wide[("inicial", 2023)]
results["inicial_2025"] = wide[("inicial", 2025)]

results["real_change_2025_vs_2023"] = (
    results["devengado_2025"] / DEFLATOR
) / results["devengado_2023"] - 1

total_2023 = results.loc[
    ("Total", "TOTAL Administración Nacional"),
    "devengado_2023",
]

total_2025 = results.loc[
    ("Total", "TOTAL Administración Nacional"),
    "devengado_2025",
]

total_real_change = (
    total_2025 / DEFLATOR
) / total_2023 - 1

results["share_2023_pct"] = (
    results["devengado_2023"] / total_2023 * 100
)

results["share_2025_pct"] = (
    results["devengado_2025"] / total_2025 * 100
)

results["RRI_pp"] = (
    results["real_change_2025_vs_2023"] - total_real_change
) * 100

results["priority_ratio"] = (
    results["share_2025_pct"] / results["share_2023_pct"]
)

results["execution_rate_2023_pct"] = (
    results["devengado_2023"] / results["vigente_2023"] * 100
)

results["execution_rate_2025_pct"] = (
    results["devengado_2025"] / results["vigente_2025"] * 100
)

results["reallocation_rate_2023_pct"] = (
    results["vigente_2023"] / results["inicial_2023"] * 100
)

results["reallocation_rate_2025_pct"] = (
    results["vigente_2025"] / results["inicial_2025"] * 100
)

results["real_change_2025_vs_2023_pct"] = (
    results["real_change_2025_vs_2023"] * 100
)

results = results.reset_index()

results = results.sort_values(
    ["class", "real_change_2025_vs_2023"],
    ascending=[True, True],
)

results.to_csv(
    PROCESSED_DIR / "panel_institucional_indicadores.csv",
    index=False,
)

print(
    f"\nTOTAL Administración Nacional real change "
    f"2025 vs 2023: {total_real_change:+.1%}"
)


# =============================================================================
# 16. FARN ENTITY VALIDATION
# =============================================================================

# FARN 2026 published real changes for these entities.
# These are validation benchmarks, NOT values substituted into our dataset.
FARN_ENTITY_BENCHMARKS = {
    "Ambiente (ex-MAyDS, SAF 317)": -0.808,
    "Parques Nacionales (APN)": -0.393,
    "Servicio Nacional de Manejo del Fuego": 0.093,
    "Servicio Meteorológico Nacional": -0.379,
    "Cuenca Matanza-Riachuelo (ACUMAR)": -0.877,
    "Inteligencia (SIDE / AFI, SAF 302)": 0.541,
    "Servicio de la Deuda Pública": -0.342,
}


entity_validation = results[
    results["group"].isin(FARN_ENTITY_BENCHMARKS)
][
    [
        "group",
        "real_change_2025_vs_2023",
    ]
].copy()

entity_validation["farn_real_change"] = entity_validation["group"].map(
    FARN_ENTITY_BENCHMARKS
)

entity_validation["gap_pp"] = (
    entity_validation["real_change_2025_vs_2023"]
    - entity_validation["farn_real_change"]
) * 100

entity_validation["absolute_gap_pp"] = (
    entity_validation["gap_pp"].abs()
)

entity_validation.to_csv(
    PROCESSED_DIR / "validation_farn_entities.csv",
    index=False,
)

print("\nFARN entity validation:")
print(entity_validation.to_string(index=False))


# =============================================================================
# 17. FIRE VALIDATION
# =============================================================================

fire_result = results[
    results["group"] == "Servicio Nacional de Manejo del Fuego"
].copy()

if not fire_result.empty:
    fire_result["farn_real_change"] = 0.093
    fire_result["gap_pp"] = (
        fire_result["real_change_2025_vs_2023"]
        - fire_result["farn_real_change"]
    ) * 100

    fire_result.to_csv(
        PROCESSED_DIR / "validation_farn_fire.csv",
        index=False,
    )


# =============================================================================
# 18. RESEARCHER-READY SUMMARY TABLE
# =============================================================================

summary_groups = [
    "Ambiente (ex-MAyDS, SAF 317)",
    "Parques Nacionales (APN)",
    "Servicio Nacional de Manejo del Fuego",
    "Cuenca Matanza-Riachuelo (ACUMAR)",
    "CONICET",
    "Ciencia y Tecnología (SAF 336)",
    "Agencia I+D+i (ANPCyT)",
    "CONAE",
    "CNEA",
    "INTA",
    "INTI",
    "Servicio Meteorológico Nacional",
    "INDEC",
    "National universities",
    "Ministerio de Salud (SAF 310)",
    "Inteligencia (SIDE / AFI, SAF 302)",
    "Armed forces",
    "Servicio de la Deuda Pública",
    "Seguridad (jurisdicción 41)",
    "TOTAL Administración Nacional",
]

summary = results[
    results["group"].isin(summary_groups)
].copy()

summary = summary[
    [
        "class",
        "group",
        "devengado_2023",
        "devengado_2025",
        "real_change_2025_vs_2023_pct",
        "share_2023_pct",
        "share_2025_pct",
        "RRI_pp",
        "priority_ratio",
        "execution_rate_2023_pct",
        "execution_rate_2025_pct",
        "reallocation_rate_2023_pct",
        "reallocation_rate_2025_pct",
    ]
]

summary.to_csv(
    OUTPUT_DIR / "phase2_institutional_summary.csv",
    index=False,
)


# =============================================================================
# 19. HUMAN-READABLE VALIDATION REPORT
# =============================================================================

validation_lines = [
    "DIMENSION 2 — PHASE 2.1 VALIDATION REPORT",
    "",
    f"Base year: {BASE_YEAR}",
    f"Target year: {TARGET_YEAR}",
    f"Universe: {EXPECTED_UNIVERSE}",
    f"Total real change: {total_real_change:+.3%}",
    "",
    "FARN finalidades validation:",
    f"Maximum 2023 gap: {max_2023_gap:.4f}%",
    f"Maximum 2025 gap: {max_2025_gap:.4f}%",
    "",
    "Important methodological note:",
    "2023 is treated as the hard external-validation checkpoint.",
    "2025 differences are reported transparently because the current source",
    "vintage may post-date FARN's April 2026 publication cutoff.",
    "",
    "Perimeter overlap:",
    f"Overlapping source rows, 2023: {len(overlap_2023):,}",
    f"Overlapping source rows, 2025: {len(overlap_2025):,}",
    "Perimeter groups must NOT be summed because some groups intentionally",
    "measure sub-functions inside broader institutional totals.",
]

(OUTPUT_DIR / "phase2_validation_report.txt").write_text(
    "\n".join(validation_lines),
    encoding="utf-8",
)


print("\n" + "\n".join(validation_lines))
print(f"\nOutputs written to: {OUTPUT_DIR.resolve()}")
