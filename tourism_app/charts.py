"""Fifteen interactive Plotly visualizations for the tourism dashboard."""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

COLOR_SCALE = "Turbo"
PLOTLY_TEMPLATE = "plotly_dark"
CHART_COLORS = ["#22d3ee", "#a78bfa", "#f472b6", "#34d399", "#fbbf24", "#fb7185"]


def _base_layout(fig, height: int = 480) -> go.Figure:
    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        height=height,
        margin=dict(l=48, r=48, t=70, b=48),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15,23,42,0.4)",
        font=dict(family="DM Sans, sans-serif", color="#e2e8f0", size=13),
        title=dict(font=dict(size=16, color="#22d3ee"), x=0.02, xanchor="left"),
        colorway=CHART_COLORS,
        hoverlabel=dict(bgcolor="#1e293b", font_size=13, font_family="DM Sans"),
    )
    fig.update_xaxes(gridcolor="rgba(148,163,184,0.15)", zeroline=False)
    fig.update_yaxes(gridcolor="rgba(148,163,184,0.15)", zeroline=False)
    return fig


def chart_animated_bar(df: pd.DataFrame) -> go.Figure:
    """User Distribution Across Continents Over Different Years."""
    agg = (
        df.groupby(["Year", "Continent"])
        .size()
        .reset_index(name="Users")
    )
    fig = px.bar(
        agg,
        x="Continent",
        y="Users",
        color="Continent",
        animation_frame="Year",
        title="User Distribution Across Continents Over Different Years",
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    return _base_layout(fig, 520)


def chart_horizontal_bar(df: pd.DataFrame) -> go.Figure:
    """Regional Tourism Participation Trend Over Time."""
    agg = (
        df.groupby(["Year", "Region"])
        .size()
        .reset_index(name="Visits")
        .sort_values("Visits", ascending=True)
    )
    fig = px.bar(
        agg,
        x="Visits",
        y="Region",
        color="Year",
        orientation="h",
        title="Regional Tourism Participation Trend Over Time",
        color_continuous_scale=COLOR_SCALE,
    )
    return _base_layout(fig)


def chart_top_countries(df: pd.DataFrame) -> go.Figure:
    """Top 10 Countries Contributing to Tourism Activities."""
    top = df["Country"].value_counts().head(10).reset_index()
    top.columns = ["Country", "Activities"]
    fig = px.bar(
        top,
        x="Country",
        y="Activities",
        title="Top 10 Countries Contributing to Tourism Activities",
        color="Activities",
        color_continuous_scale="Viridis",
    )
    return _base_layout(fig)


def chart_visit_mode_pie(df: pd.DataFrame) -> go.Figure:
    """Distribution of Visit Modes Among Tourists."""
    fig = px.pie(
        df,
        names="VisitMode",
        title="Distribution of Visit Modes Among Tourists",
        hole=0.35,
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )
    return _base_layout(fig)


def chart_rating_histogram(df: pd.DataFrame) -> go.Figure:
    """Overall Distribution of User Ratings Across Attractions."""
    fig = px.histogram(
        df,
        x="Rating",
        nbins=5,
        title="Overall Distribution of User Ratings Across Attractions",
        color_discrete_sequence=["#38bdf8"],
    )
    return _base_layout(fig)


def chart_rating_box(df: pd.DataFrame) -> go.Figure:
    """Comparison of User Ratings Based on Visit Modes."""
    fig = px.box(
        df,
        x="VisitMode",
        y="Rating",
        color="VisitMode",
        title="Comparison of User Ratings Based on Visit Modes",
    )
    return _base_layout(fig)


def chart_rating_scatter(df: pd.DataFrame) -> go.Figure:
    """Average Attraction Ratings Across Continents."""
    agg = df.groupby("Continent", as_index=False)["Rating"].mean()
    fig = px.scatter(
        agg,
        x="Continent",
        y="Rating",
        size="Rating",
        color="Continent",
        title="Average Attraction Ratings Across Continents",
    )
    return _base_layout(fig)


def chart_attraction_treemap(df: pd.DataFrame) -> go.Figure:
    """Popularity of Different Attraction Types Based on User Ratings."""
    agg = (
        df.groupby("AttractionType")
        .agg(Count=("Rating", "count"), AvgRating=("Rating", "mean"))
        .reset_index()
    )
    fig = px.treemap(
        agg,
        path=["AttractionType"],
        values="Count",
        color="AvgRating",
        color_continuous_scale="RdYlGn",
        title="Popularity of Different Attraction Types Based on User Ratings",
    )
    return _base_layout(fig, 520)


def chart_rating_violin(df: pd.DataFrame) -> go.Figure:
    """Rating Variability Across Different Visit Modes Over Years."""
    fig = px.violin(
        df,
        x="VisitMode",
        y="Rating",
        color="VisitMode",
        animation_frame="Year",
        box=True,
        points="outliers",
        title="Rating Variability Across Different Visit Modes Over Years",
    )
    return _base_layout(fig, 520)


def chart_monthly_line(df: pd.DataFrame) -> go.Figure:
    """Monthly Tourism Activity Trend Across Years."""
    agg = (
        df.groupby(["Year", "MonthName"])
        .size()
        .reset_index(name="Activity")
    )
    month_order = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
    ]
    agg["MonthName"] = pd.Categorical(agg["MonthName"], categories=month_order, ordered=True)
    agg = agg.sort_values(["Year", "MonthName"])
    fig = px.line(
        agg,
        x="MonthName",
        y="Activity",
        color="Year",
        markers=True,
        title="Monthly Tourism Activity Trend Across Years",
    )
    return _base_layout(fig)


def chart_growth_area(df: pd.DataFrame) -> go.Figure:
    """Overall Growth Trend in Tourism Visits."""
    agg = df.groupby("Year").size().reset_index(name="Visits")
    fig = px.area(
        agg,
        x="Year",
        y="Visits",
        title="Overall Growth Trend in Tourism Visits",
        color_discrete_sequence=["#a78bfa"],
    )
    fig.update_traces(fill="tozeroy")
    return _base_layout(fig)


def chart_stacked_visit_mode(df: pd.DataFrame) -> go.Figure:
    """Visit Mode Preferences Across Continents."""
    agg = (
        df.groupby(["Continent", "VisitMode"])
        .size()
        .reset_index(name="Count")
    )
    fig = px.bar(
        agg,
        x="Continent",
        y="Count",
        color="VisitMode",
        title="Visit Mode Preferences Across Continents",
        barmode="stack",
    )
    return _base_layout(fig)


def chart_rating_strip(df: pd.DataFrame) -> go.Figure:
    """Regional Distribution of User Ratings."""
    sample = df.sample(min(3000, len(df)), random_state=42)
    fig = px.strip(
        sample,
        x="Region",
        y="Rating",
        color="VisitMode",
        title="Regional Distribution of User Ratings",
    )
    fig.update_xaxes(tickangle=45)
    return _base_layout(fig, 520)


def chart_correlation_heatmap(df: pd.DataFrame) -> go.Figure:
    """Correlation Analysis Between Numerical Tourism Features."""
    numeric = df[["Rating", "Year", "Month", "VisitTime", "UserId"]].copy()
    corr = numeric.corr()
    fig = px.imshow(
        corr,
        text_auto=".2f",
        color_continuous_scale="RdBu_r",
        title="Correlation Analysis Between Numerical Tourism Features",
        aspect="auto",
    )
    return _base_layout(fig)


def chart_pair_plot(df: pd.DataFrame) -> go.Figure:
    """Pairwise Relationship Between Visit Time, Rating, and Visit Mode."""
    sample = df.sample(min(2000, len(df)), random_state=42)
    fig = px.scatter_matrix(
        sample,
        dimensions=["VisitTime", "Rating", "Year"],
        color="VisitMode",
        title="Pairwise Relationship Between Visit Time, Rating, and Visit Mode",
    )
    fig.update_layout(height=600)
    return _base_layout(fig, 600)


CHART_BUILDERS = {
    "animated_bar": chart_animated_bar,
    "horizontal_bar": chart_horizontal_bar,
    "top_countries": chart_top_countries,
    "visit_mode_pie": chart_visit_mode_pie,
    "rating_histogram": chart_rating_histogram,
    "rating_box": chart_rating_box,
    "rating_scatter": chart_rating_scatter,
    "attraction_treemap": chart_attraction_treemap,
    "rating_violin": chart_rating_violin,
    "monthly_line": chart_monthly_line,
    "growth_area": chart_growth_area,
    "stacked_visit_mode": chart_stacked_visit_mode,
    "rating_strip": chart_rating_strip,
    "correlation_heatmap": chart_correlation_heatmap,
    "pair_plot": chart_pair_plot,
}


def build_chart(chart_key: str, df: pd.DataFrame) -> go.Figure:
    builder = CHART_BUILDERS.get(chart_key)
    if builder is None:
        raise ValueError(f"Unknown chart: {chart_key}")
    return builder(df)


def model_comparison_bar(metrics: dict, metric_name: str, title: str) -> go.Figure:
    """Animated-style bar comparison for model metrics."""
    names = list(metrics.keys())
    values = list(metrics.values())
    fig = go.Figure(
        data=[
            go.Bar(
                x=names,
                y=values,
                marker=dict(
                    color=values,
                    colorscale="Turbo",
                    line=dict(width=1, color="#38bdf8"),
                ),
            )
        ]
    )
    fig.update_layout(title=title, yaxis_title=metric_name)
    return _base_layout(fig, 420)
