"""Load tourism data and enrich with analytics dimensions."""
import hashlib
import os

import numpy as np
import pandas as pd

from config import DATA_PATH, ENRICHED_CACHE

# Region → representative country for analytics and maps
REGION_COUNTRY = {
    "Southeast Asia": "Indonesia",
    "East Asia": "Japan",
    "South Asia": "India",
    "Central Asia": "Kazakhstan",
    "Western Asia": "UAE",
    "North Africa": "Egypt",
    "West Africa": "Nigeria",
    "East Africa": "Kenya",
    "Southern Africa": "South Africa",
    "Central Africa": "Cameroon",
    "Western Europe": "France",
    "Eastern Europe": "Poland",
    "Northern Europe": "Norway",
    "Southern Europe": "Italy",
    "Central Europe": "Germany",
    "United States": "United States",
    "Canada": "Canada",
    "Mexico": "Mexico",
    "Central America": "Panama",
    "Caribbean": "Jamaica",
    "Brazil": "Brazil",
    "Argentina": "Argentina",
    "Chile": "Chile",
    "Peru": "Peru",
    "Colombia": "Colombia",
    "Venezuela": "Venezuela",
    "Antarctic Peninsula": "Antarctica",
    "East Antarctica": "Antarctica",
    "West Antarctica": "Antarctica",
    "Eastern Australia": "Australia",
    "Western Australia": "Australia",
    "Northern Territory": "Australia",
    "Queensland": "Australia",
    "New South Wales": "Australia",
}

# Approximate coordinates for map markers (lat, lon)
COUNTRY_COORDS = {
    "Indonesia": (-2.5, 118.0),
    "Japan": (36.2, 138.3),
    "India": (20.6, 78.9),
    "Kazakhstan": (48.0, 67.0),
    "UAE": (24.5, 54.4),
    "Egypt": (26.8, 30.8),
    "Nigeria": (9.1, 8.7),
    "Kenya": (-0.02, 37.9),
    "South Africa": (-30.6, 22.9),
    "Cameroon": (7.4, 12.4),
    "France": (46.2, 2.2),
    "Poland": (51.9, 19.1),
    "Norway": (60.5, 8.5),
    "Italy": (41.9, 12.6),
    "Germany": (51.2, 10.5),
    "United States": (39.8, -98.6),
    "Canada": (56.1, -106.3),
    "Mexico": (23.6, -102.6),
    "Panama": (8.5, -80.8),
    "Jamaica": (18.1, -77.3),
    "Brazil": (-14.2, -51.9),
    "Argentina": (-38.4, -63.6),
    "Chile": (-35.7, -71.5),
    "Peru": (-9.2, -75.0),
    "Colombia": (4.6, -74.1),
    "Venezuela": (6.4, -66.6),
    "Antarctica": (-82.9, 135.0),
    "Australia": (-25.3, 133.8),
}


def _stable_hash(value: str, modulo: int) -> int:
    digest = hashlib.md5(str(value).encode()).hexdigest()
    return int(digest, 16) % modulo


def enrich_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Add Year, Month, Country, City, VisitTime, and map coordinates."""
    enriched = df.copy()

    enriched["Country"] = enriched["Region"].map(REGION_COUNTRY).fillna(
        enriched["Continent"]
    )
    enriched["City"] = enriched.apply(
        lambda r: f"{r['Region'].split()[0]} City"
        if isinstance(r["Region"], str)
        else "Unknown City",
        axis=1,
    )

    enriched["Year"] = enriched["UserId"].apply(lambda u: 2018 + _stable_hash(f"y{u}", 7))
    enriched["Month"] = enriched["UserId"].apply(lambda u: 1 + _stable_hash(f"m{u}", 12))
    enriched["MonthName"] = pd.to_datetime(
        enriched["Month"].astype(str) + "-01", format="%m-%d"
    ).dt.strftime("%b")
    enriched["VisitTime"] = enriched.apply(
        lambda r: 1 + _stable_hash(f"t{r['UserId']}{r['Attraction']}", 10), axis=1
    )
    enriched["TransactionId"] = range(1, len(enriched) + 1)

    # Deterministic jitter per row for map spread
    rng = np.random.default_rng(42)
    jitter_lat = rng.normal(0, 1.2, len(enriched))
    jitter_lon = rng.normal(0, 1.2, len(enriched))
    base_lat = enriched["Country"].map(lambda c: COUNTRY_COORDS.get(c, (0, 0))[0])
    base_lon = enriched["Country"].map(lambda c: COUNTRY_COORDS.get(c, (0, 0))[1])
    enriched["Latitude"] = base_lat.values + jitter_lat
    enriched["Longitude"] = base_lon.values + jitter_lon

    return enriched


def load_data(force_refresh: bool = False) -> pd.DataFrame:
    """Load merged tourism dataset with enriched analytics columns."""
    if not force_refresh and os.path.exists(ENRICHED_CACHE):
        return pd.read_csv(ENRICHED_CACHE)

    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(
            f"Dataset not found at {DATA_PATH}. Run prepare_data.py first."
        )

    raw = pd.read_csv(DATA_PATH)
    enriched = enrich_dataset(raw)
    enriched.to_csv(ENRICHED_CACHE, index=False)
    return enriched


def filter_data(
    df: pd.DataFrame,
    continents: list | None = None,
    visit_modes: list | None = None,
    rating_range: tuple[int, int] = (1, 5),
) -> pd.DataFrame:
    """Apply sidebar filters."""
    filtered = df.copy()
    if continents:
        filtered = filtered[filtered["Continent"].isin(continents)]
    if visit_modes:
        filtered = filtered[filtered["VisitMode"].isin(visit_modes)]
    filtered = filtered[
        (filtered["Rating"] >= rating_range[0])
        & (filtered["Rating"] <= rating_range[1])
    ]
    return filtered
