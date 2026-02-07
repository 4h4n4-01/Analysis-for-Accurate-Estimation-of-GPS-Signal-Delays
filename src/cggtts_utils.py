from __future__ import annotations

import re
from pathlib import Path
import pandas as pd

MJD0 = pd.Timestamp("1858-11-17")


def parse_datetime(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # --- Normalize headers to avoid Windows/Mac/Excel quirks ---
    # e.g. "sttime ", " STTIME", "StTime" -> "STTIME"
    df.columns = [str(c).strip().upper() for c in df.columns]

    # Must-have columns check (we can skip file if missing)
    if "MJD" not in df.columns or "REFSYS" not in df.columns or "STTIME" not in df.columns:
        return pd.DataFrame()

    # Ensure numeric for key fields (coerce junk to NaN)
    df["MJD"] = pd.to_numeric(df["MJD"], errors="coerce")
    df["REFSYS"] = pd.to_numeric(df["REFSYS"], errors="coerce")

    # --- Clean STTIME: remove repeated header rows / junk values ---
    # STTIME should be HHMMSS (e.g., 103400). Some files contain repeated header strings like "STTIME".
    st_raw = df["STTIME"].astype(str).str.strip()
    st_raw = st_raw.str.replace(r"\.0$", "", regex=True)

    # Keep only rows where STTIME is digits
    mask_st = st_raw.str.fullmatch(r"\d+")
    if not mask_st.any():
        return pd.DataFrame()

    df = df.loc[mask_st].copy()
    st = st_raw.loc[mask_st].str.zfill(6)

    # Convert HHMMSS -> timedeltas
    hh = st.str[0:2].astype(int)
    mm = st.str[2:4].astype(int)
    ss = st.str[4:6].astype(int)

    # Build datetime from MJD + STTIME
    df["date"] = MJD0 + pd.to_timedelta(df["MJD"], unit="D")
    df["time"] = (
        pd.to_timedelta(hh, unit="h")
        + pd.to_timedelta(mm, unit="m")
        + pd.to_timedelta(ss, unit="s")
    )
    df["datetime"] = df["date"] + df["time"]

    # Drop any rows that still ended up invalid
    df = df.dropna(subset=["datetime", "REFSYS", "MJD"])

    return df


def month_from_filename(name: str) -> str:
    # e.g. "Feb_CGGTTS_Data Set 1.xlsx" -> "Feb"
    m = re.match(r"([A-Za-z]+)_", name.strip())
    return m.group(1) if m else "Unknown"


def dataset_from_filename(name: str) -> str:
    # Data Set 1 / 2
    m = re.search(r"Data Set\s*(\d+)", name)
    return f"Set {m.group(1)}" if m else "Set ?"


def load_all_excels(data_dir: str | Path) -> pd.DataFrame:
    data_dir = Path(data_dir)
    files = sorted(data_dir.glob("*.xlsx"))
    all_df: list[pd.DataFrame] = []

    for fp in files:
        try:
            df = pd.read_excel(fp)
        except Exception as e:
            print(f"Skipping unreadable file {fp.name}: {e}")
            continue

        # Skip completely empty sheets
        if df is None or df.empty:
            print(f"Skipping empty sheet: {fp.name}")
            continue

        df = parse_datetime(df)

        # If parse_datetime decided it's not a valid CGGTTS-like sheet
        if df.empty:
            print(f"Skipping file (missing/invalid columns or STTIME): {fp.name}")
            continue

        df["month"] = month_from_filename(fp.name)
        df["dataset"] = dataset_from_filename(fp.name)
        df["source_file"] = fp.name

        # Keep only what we need
        keep = [
            "datetime", "MJD", "STTIME", "SAT", "ELV", "AZTH", "REFSYS",
            "month", "dataset", "source_file"
        ]
        df = df[[c for c in keep if c in df.columns]]

        # Final safety
        df = df.dropna(subset=["datetime", "REFSYS"])

        all_df.append(df)

    return pd.concat(all_df, ignore_index=True) if all_df else pd.DataFrame()
