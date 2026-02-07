from __future__ import annotations
import re
from pathlib import Path
import pandas as pd

MJD0 = pd.Timestamp("1858-11-17")

def parse_datetime(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Ensure numeric
    df["MJD"] = pd.to_numeric(df["MJD"], errors="coerce")
    df["REFSYS"] = pd.to_numeric(df["REFSYS"], errors="coerce")

    # STTIME like 103400 -> "103400" -> 10:34:00
    st = df["STTIME"].astype(str).str.replace(r"\.0$", "", regex=True).str.zfill(6)
    hh = st.str[0:2].astype(int)
    mm = st.str[2:4].astype(int)
    ss = st.str[4:6].astype(int)

    df["date"] = MJD0 + pd.to_timedelta(df["MJD"], unit="D")
    df["time"] = pd.to_timedelta(hh, unit="h") + pd.to_timedelta(mm, unit="m") + pd.to_timedelta(ss, unit="s")
    df["datetime"] = df["date"] + df["time"]

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
    all_df = []

    for fp in files:
        df = pd.read_excel(fp)
        df = parse_datetime(df)

        df["month"] = month_from_filename(fp.name)
        df["dataset"] = dataset_from_filename(fp.name)
        df["source_file"] = fp.name

        # Keep only what we need for portfolio
        keep = ["datetime", "MJD", "STTIME", "SAT", "ELV", "AZTH", "REFSYS", "month", "dataset", "source_file"]
        df = df[[c for c in keep if c in df.columns]]

        # Drop rows where key values are missing
        df = df.dropna(subset=["datetime", "REFSYS"])
        all_df.append(df)

    return pd.concat(all_df, ignore_index=True) if all_df else pd.DataFrame()
