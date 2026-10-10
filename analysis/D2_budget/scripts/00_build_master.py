"""
Dimension 2 · Step 0 — build the master budget extract.

WHAT THIS IS
------------
The single parsing path for the whole D2 analysis. It downloads the annual
expenditure microdata from Presupuesto Abierto once per year, parses it once,
validates it, and writes one canonical file per year to `processed/`.

Every downstream notebook reads those files. Nothing else in the project parses
raw CSV, so there is exactly one place where a parsing decision is made and
exactly one place a parsing bug could live.

RUN IT
------
    python 00_build_master.py            # build any missing years
    python 00_build_master.py --force    # re-download and rebuild everything

First run downloads ~14 MB of zips and expands ~420 MB of CSV into `raw/`;
afterwards it reads the cache. Building all four years takes a couple of minutes.

WHAT IT PRODUCES
----------------
    processed/master_2023.parquet   (or .csv.gz if pyarrow is unavailable)
    processed/master_2024.parquet
    processed/master_2025.parquet
    processed/master_2026.parquet
    processed/master_manifest.csv   provenance + integrity record

READ IT
-------
    import pandas as pd
    df = pd.read_parquet("processed/master_2023.parquet")

SOURCE
------
Presupuesto de gastos y su ejecución detallada — agrupación anual.
DGSIAF / Secretaría de Hacienda, Ministerio de Economía. CC-BY 4.0.
Portal:  https://www.presupuestoabierto.gob.ar/sici/datos-abiertos
Fields:  https://dgsiaf-repo.mecon.gob.ar/repository/pa/credito-anual.pdf

No API token is required. The download URLs come from the portal's own
catalogue endpoint, which this script queries so that the *vintage* of each file
is recorded rather than assumed — the publisher revises past years, so two runs
months apart can legitimately produce different numbers. The manifest is how you
tell.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import ssl
import time
import sys
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------

HERE = Path(__file__).resolve().parent
RAW_DIR = HERE.parent / "raw"
OUT_DIR = HERE.parent / "processed"

YEARS = [2023, 2024, 2025, 2026]

CATALOGUE_URL = "https://www.presupuestoabierto.gob.ar/sici/rest-api/catalog/site"
RECURSO = "Presupuesto de gastos y su ejecución detallada - agrupación anual"

# The five credit stages. Stored as floats, in millones de pesos corrientes.
MEASURES = [
    "credito_presupuestado",   # crédito inicial
    "credito_vigente",
    "credito_comprometido",
    "credito_devengado",       # the measure the analysis uses for closed years
    "credito_pagado",
]

# Classifier codes are integers in the source but are identifiers, not
# quantities — keep them as nullable integers so no arithmetic is ever
# accidentally performed on them and no code is silently coerced to float.
ID_COLS = [
    "sector_id", "subsector_id", "caracter_id", "jurisdiccion_id",
    "subjurisdiccion_id", "entidad_id", "servicio_id", "programa_id",
    "subprograma_id", "proyecto_id", "actividad_id", "obra_id",
    "finalidad_id", "funcion_id", "inciso_id", "principal_id", "parcial_id",
    "subparcial_id", "clasificador_economico_8_digitos_id",
    "ubicacion_geografica_id", "unidad_ejecutora_id", "prestamo_externo_id",
    "impacto_presupuestario_anio", "ejercicio_presupuestario",
]

SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False           # these hosts present chains Python rejects
SSL_CTX.verify_mode = ssl.CERT_NONE
HEADERS = {"User-Agent": "Mozilla/5.0 (academic research; budget analysis)"}


def fetch(url: str, timeout: int = 600, attempts: int = 4) -> bytes:
    """GET with retries — these hosts intermittently reset the connection."""
    last = None
    for i in range(attempts):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, context=SSL_CTX, timeout=timeout) as r:
                return r.read()
        except Exception as exc:                       # noqa: BLE001
            last = exc
            if i < attempts - 1:
                wait = 2 ** i
                print(f"    retry {i + 1}/{attempts - 1} in {wait}s ({exc})")
                time.sleep(wait)
    raise RuntimeError(f"could not fetch {url} after {attempts} attempts: {last}")


# --------------------------------------------------------------------------
# Provenance
# --------------------------------------------------------------------------

def catalogue_entries() -> dict[int, dict]:
    """Year -> {url, last_updated, row_count} from the portal's own catalogue.

    Recording the publisher's `fechaDeActualizacion` matters: the 2025 file was
    revised on 5 Jul 2026, after FARN's April 2026 report, which is why our 2025
    totals run ~0.5% above theirs. Without this field that difference looks like
    a methodological discrepancy instead of a data vintage.
    """
    cat = json.loads(fetch(CATALOGUE_URL).decode("utf8"))
    out: dict[int, dict] = {}
    for dist in cat["distribuciones"]:
        if dist["nombreRecurso"] != RECURSO:
            continue
        for year in dist["ejercicios"]:
            if year in YEARS:
                out[year] = {
                    "url": dist["urlArchivo"],
                    "last_updated": dist["fechaDeActualizacion"],
                    "row_count": dist["cantidadDeRegistros"],
                }
    return out


# --------------------------------------------------------------------------
# Download and parse
# --------------------------------------------------------------------------

def download(year: int, url: str, vintage: str, force: bool) -> Path:
    """Download and cache one annual zip, stamping it with the portal vintage.

    The stamp matters. The publisher revises past years, so a cached file can be
    older than what the portal currently serves. Without recording which vintage
    is actually on disk, the manifest would claim a provenance the data does not
    have. We never silently refresh: a frozen analysis must stay frozen, so a
    stale cache is reported and left alone until you pass --force.
    """
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    zip_path = RAW_DIR / f"credito-anual-{year}.zip"
    csv_path = RAW_DIR / f"credito-anual-{year}.csv"
    stamp = RAW_DIR / f"credito-anual-{year}.vintage.json"

    if force or not zip_path.exists():
        print(f"    downloading {url}")
        zip_path.write_bytes(fetch(url))
        stamp.write_text(json.dumps({"portal_last_updated": vintage,
                                     "downloaded_utc": datetime.now(timezone.utc)
                                     .strftime("%Y-%m-%d %H:%M")}))
    if force or not csv_path.exists():
        with zipfile.ZipFile(zip_path) as z:
            z.extractall(RAW_DIR)
    return csv_path


def cached_vintage(year: int) -> str:
    """The portal vintage of the file actually on disk, '' if unknown."""
    stamp = RAW_DIR / f"credito-anual-{year}.vintage.json"
    if stamp.exists():
        return json.loads(stamp.read_text()).get("portal_last_updated", "")
    return ""


def parse(csv_path: Path) -> pd.DataFrame:
    """Read one annual file with every column, correctly typed.

    THE DECIMAL-COMMA TRAP
    ----------------------
    Amounts are written `48645,776825` — decimal comma, no thousands separator.
    Pandas reads them as strings. `.sum()` on a string column CONCATENATES
    instead of adding, producing a plausible-looking but meaningless number and
    raising no error. Every conversion below is guarded by an assertion that
    there is no '.' in the raw values, so if the publisher ever switches to a
    thousands separator this fails loudly instead of silently.
    """
    df = pd.read_csv(csv_path, low_memory=False)

    for col in MEASURES:
        if pd.api.types.is_numeric_dtype(df[col]):
            continue
        raw = df[col].astype("string")
        assert not raw.str.contains(r"\.", na=False).any(), (
            f"{csv_path.name}: '.' found in {col} — the number format changed, "
            "check whether it is now a thousands separator before converting"
        )
        df[col] = raw.str.replace(",", ".", regex=False).astype(float)

    for col in ID_COLS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

    df.columns = [c.strip().lstrip("﻿") for c in df.columns]
    return df


# --------------------------------------------------------------------------
# Validation
# --------------------------------------------------------------------------

# FARN (2026), Table 2 — nominal executed spending by finalidad, millones $.
# 2023 is the hard check: it must reproduce to the peso. 2025 is expected to run
# slightly high because of the July 2026 revision, so it is reported, not asserted.
FARN_2023 = {1: 2_349_060, 2: 1_710_842, 3: 24_845_207, 4: 5_647_579, 5: 3_472_801}
FARN_TOTAL_2023 = 38_025_489


def validate(year: int, df: pd.DataFrame) -> None:
    universe = sorted(df.subsector_desc.dropna().unique())
    assert universe == ["Administración Nacional"], (
        f"{year}: unexpected universe {universe} — the analysis assumes "
        "Administración Nacional only"
    )
    assert (df.ejercicio_presupuestario == year).all(), f"{year}: mixed ejercicios"
    assert df[MEASURES].notna().all().all(), f"{year}: nulls in the measure columns"

    if year == 2023:
        by_fin = df.groupby("finalidad_id")["credito_devengado"].sum()
        for fin, expected in FARN_2023.items():
            got = by_fin.loc[fin]
            assert abs(got - expected) < 1, (
                f"2023 finalidad {fin}: {got:,.0f} != FARN {expected:,.0f}. "
                "The 2023 base must reproduce FARN exactly — investigate before "
                "using any downstream result."
            )
        total = df.credito_devengado.sum()
        assert abs(total - FARN_TOTAL_2023) < 1, f"2023 total {total:,.0f} != FARN"
        print("    validation: 2023 reproduces FARN (2026) Table 2 to the peso")


# --------------------------------------------------------------------------
# Write
# --------------------------------------------------------------------------

def write_master(df: pd.DataFrame, year: int) -> Path:
    """Parquet if pyarrow is present, gzipped CSV otherwise.

    Parquet keeps dtypes and loads roughly twenty times faster; the CSV fallback
    exists so the pipeline never hard-depends on a package the reader may not
    have. `load_master` below reads whichever exists.
    """
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    try:
        import pyarrow  # noqa: F401
        path = OUT_DIR / f"master_{year}.parquet"
        df.to_parquet(path, index=False)
    except ImportError:
        path = OUT_DIR / f"master_{year}.csv.gz"
        df.to_csv(path, index=False, compression="gzip")
        print("    (pyarrow not installed — wrote gzipped CSV instead of parquet)")
    return path


def load_master(year: int, base: Path | str = OUT_DIR) -> pd.DataFrame:
    """Read one master year. This is what downstream notebooks should call."""
    base = Path(base)
    for name in (f"master_{year}.parquet", f"master_{year}.csv.gz"):
        path = base / name
        if path.exists():
            return pd.read_parquet(path) if path.suffix == ".parquet" \
                else pd.read_csv(path, low_memory=False)
    raise FileNotFoundError(
        f"no master file for {year} in {base} — run 00_build_master.py first"
    )


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def main(force: bool = False, years: list[int] | None = None) -> pd.DataFrame:
    global YEARS
    if years:
        YEARS = years
    print("Querying the Presupuesto Abierto catalogue for current file URLs …")
    entries = catalogue_entries()
    missing = [y for y in YEARS if y not in entries]
    assert not missing, f"catalogue has no annual file for {missing}"

    manifest = []
    for year in YEARS:
        meta = entries[year]
        print(f"\n{year}  (portal vintage: {meta['last_updated']})")

        out_exists = any((OUT_DIR / f"master_{year}{ext}").exists()
                         for ext in (".parquet", ".csv.gz"))
        if out_exists and not force:
            print("    master already built — skipping (use --force to rebuild)")
            df = load_master(year)
        else:
            csv_path = download(year, meta["url"], meta["last_updated"], force)
            df = parse(csv_path)
            validate(year, df)
            path = write_master(df, year)
            print(f"    wrote {path.name}")

        have = cached_vintage(year)
        # Two independent staleness signals. The vintage stamp is definitive but
        # only exists for files downloaded by this script; the row count works
        # for any cache, because the catalogue reports data rows + 1 header.
        stale = (have != meta["last_updated"]) if have \
            else (meta["row_count"] - len(df) != 1)
        if stale:
            detail = (f"on disk = '{have}'" if have
                      else f"cached file has {len(df):,} rows, portal serves "
                           f"{meta['row_count'] - 1:,}")
            print(f"    STALE: {detail}; portal now serves "
                  f"'{meta['last_updated']}'. Kept the cached file so results stay "
                  "reproducible — rerun with --force to adopt the newer vintage.")

        zip_path = RAW_DIR / f"credito-anual-{year}.zip"
        manifest.append({
            "ejercicio": year,
            "source_url": meta["url"],
            "vintage_on_disk": have or "unstamped cache",
            "portal_vintage_now": meta["last_updated"],
            "stale_vs_portal": stale,
            "portal_row_count": meta["row_count"],
            "rows_loaded": len(df),
            "columns": df.shape[1],
            "zip_sha256": hashlib.sha256(zip_path.read_bytes()).hexdigest()[:16]
                          if zip_path.exists() else "",
            "total_credito_presupuestado": round(df.credito_presupuestado.sum(), 2),
            "total_credito_vigente": round(df.credito_vigente.sum(), 2),
            "total_credito_devengado": round(df.credito_devengado.sum(), 2),
            "built_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M"),
        })

    man = pd.DataFrame(manifest)
    man.to_csv(OUT_DIR / "master_manifest.csv", index=False)

    print("\n" + "=" * 78)
    print("MASTER EXTRACT BUILT")
    print("=" * 78)
    print(man[["ejercicio", "vintage_on_disk", "stale_vs_portal", "rows_loaded",
               "columns", "total_credito_devengado"]].to_string(
        index=False, float_format=lambda v: f"{v:,.0f}"))
    print(f"\nprovenance record: {(OUT_DIR / 'master_manifest.csv')}")
    print("Downstream notebooks should now read these files, not raw CSV.")
    return man


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--force", action="store_true",
                    help="re-download and rebuild")
    ap.add_argument("--years", type=int, nargs="+", default=None,
                    help="restrict to these ejercicios (default: all four)")
    sys.exit(0 if main(**vars(ap.parse_args())) is not None else 1)
