"""Interactive tourism map using Folium (Leaflet.js)."""
import pandas as pd
import folium
from folium.plugins import MarkerCluster


def _prepare_map_data(df: pd.DataFrame, continent: str | None = None) -> pd.DataFrame:
    """Aggregate attractions per location for a clean, visible map."""
    data = df.copy()
    if continent and continent != "All":
        data = data[data["Continent"] == continent]

    if data.empty or "Latitude" not in data.columns or "Longitude" not in data.columns:
        return pd.DataFrame()

    return (
        data.groupby(["Continent", "Country", "Region", "Attraction", "VisitMode"], as_index=False)
        .agg(
            Rating=("Rating", "mean"),
            Visits=("UserId", "count"),
            Latitude=("Latitude", "mean"),
            Longitude=("Longitude", "mean"),
        )
    )


def _rating_color(rating: float) -> str:
    """Color markers by average rating."""
    if rating >= 4.5:
        return "#22c55e"
    if rating >= 3.5:
        return "#38bdf8"
    if rating >= 2.5:
        return "#fbbf24"
    return "#f87171"


# Default map center per continent
CONTINENT_CENTER = {
    "Asia": (34.0, 100.0, 3),
    "Africa": (8.0, 20.0, 3),
    "Europe": (54.0, 15.0, 4),
    "North America": (45.0, -100.0, 3),
    "South America": (-15.0, -60.0, 3),
    "Australia": (-25.0, 135.0, 4),
    "Antarctica": (-75.0, 0.0, 2),
}


def build_leaflet_map(df: pd.DataFrame, continent: str | None = None) -> folium.Map | None:
    """Build an interactive Leaflet map with clustered markers and popups."""
    map_df = _prepare_map_data(df, continent)
    if map_df.empty:
        return None

    if len(map_df) > 1200:
        map_df = map_df.nlargest(1200, "Visits")

    if continent and continent in CONTINENT_CENTER:
        center_lat, center_lon, zoom = CONTINENT_CENTER[continent]
    else:
        center_lat = float(map_df["Latitude"].mean())
        center_lon = float(map_df["Longitude"].mean())
        zoom = 2

    tourism_map = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=zoom,
        tiles="OpenStreetMap",
        attr="© OpenStreetMap contributors",
    )

    # Dark themed overlay option as second tile layer
    folium.TileLayer(
        tiles="CartoDB dark_matter",
        name="Dark Map",
        attr="© CartoDB",
        overlay=False,
        control=True,
    ).add_to(tourism_map)

    cluster = MarkerCluster(name="Tourist Attractions").add_to(tourism_map)

    for row in map_df.itertuples(index=False):
        color = _rating_color(row.Rating)
        radius = 6 + min(int(row.Visits) // 5, 14)

        popup_html = f"""
        <div style="font-family:Arial,sans-serif;min-width:220px;">
            <h4 style="margin:0 0 8px;color:#0ea5e9;">{row.Attraction}</h4>
            <b>Country:</b> {row.Country}<br>
            <b>Region:</b> {row.Region}<br>
            <b>Continent:</b> {row.Continent}<br>
            <b>Visit Mode:</b> {row.VisitMode}<br>
            <b>Rating:</b> ⭐ {row.Rating:.2f}<br>
            <b>Visits:</b> {row.Visits:,}
        </div>
        """

        folium.CircleMarker(
            location=[row.Latitude, row.Longitude],
            radius=radius,
            popup=folium.Popup(popup_html, max_width=320),
            tooltip=f"{row.Attraction} ({row.Rating:.1f}★)",
            color="#ffffff",
            weight=1.5,
            fill=True,
            fill_color=color,
            fill_opacity=0.85,
        ).add_to(cluster)

    # Legend
    legend_html = """
    <div style="
        position:fixed;bottom:30px;left:30px;z-index:9999;
        background:rgba(15,23,42,0.92);color:#f1f5f9;padding:12px 16px;
        border-radius:12px;border:1px solid #38bdf8;font-size:13px;
        font-family:Arial,sans-serif;">
        <b style="color:#22d3ee;">Rating Legend</b><br>
        <span style="color:#22c55e;">●</span> 4.5 – 5.0 &nbsp;
        <span style="color:#38bdf8;">●</span> 3.5 – 4.4<br>
        <span style="color:#fbbf24;">●</span> 2.5 – 3.4 &nbsp;
        <span style="color:#f87171;">●</span> 1.0 – 2.4
    </div>
    """
    tourism_map.get_root().html.add_child(folium.Element(legend_html))

    folium.LayerControl(collapsed=False).add_to(tourism_map)
    return tourism_map


def get_map_points_for_streamlit(df: pd.DataFrame, continent: str | None = None) -> pd.DataFrame:
    """Lat/lon frame for optional st.map fallback."""
    map_df = _prepare_map_data(df, continent)
    if map_df.empty:
        return map_df
    return map_df.rename(columns={"Latitude": "lat", "Longitude": "lon"})
