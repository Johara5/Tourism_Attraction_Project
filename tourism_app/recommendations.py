"""Collaborative and content-based recommendation engines."""
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
def _popular_fallback(df: pd.DataFrame, top_n: int) -> pd.DataFrame:
    popular = (
        df.groupby("Attraction")
        .agg(AvgRating=("Rating", "mean"), Visits=("UserId", "count"))
        .reset_index()
        .sort_values(["AvgRating", "Visits"], ascending=False)
        .head(top_n)
    )
    popular["Method"] = "Popular (fallback)"
    popular["Score"] = popular["AvgRating"]
    return popular


def collaborative_recommendations(
    df: pd.DataFrame, user_id: int, top_n: int = 8
) -> pd.DataFrame:
    """User-based collaborative filtering via cosine similarity on ratings matrix."""
    pivot = df.pivot_table(
        index="UserId", columns="Attraction", values="Rating", aggfunc="mean"
    ).fillna(0)

    if user_id not in pivot.index:
        return _popular_fallback(df, top_n)

    sim = cosine_similarity(pivot)
    user_idx = pivot.index.get_loc(user_id)
    similar_users = np.argsort(sim[user_idx])[::-1][1:6]

    seen = set(df[df["UserId"] == user_id]["Attraction"])
    scores: dict[str, list[float]] = {}

    for s_idx in similar_users:
        similar_uid = pivot.index[s_idx]
        weight = sim[user_idx][s_idx]
        user_ratings = pivot.iloc[s_idx]
        for attraction, rating in user_ratings.items():
            if rating > 0 and attraction not in seen:
                scores.setdefault(attraction, []).append(rating * weight)

    if not scores:
        return _popular_fallback(df, top_n)

    recs = [
        {"Attraction": a, "Score": np.mean(v), "Method": "Collaborative Filtering"}
        for a, v in scores.items()
    ]
    rec_df = pd.DataFrame(recs).sort_values("Score", ascending=False).head(top_n)
    meta = df.groupby("Attraction").agg(
        AvgRating=("Rating", "mean"),
        Continent=("Continent", "first"),
        AttractionType=("AttractionType", "first"),
    )
    return rec_df.merge(meta, on="Attraction", how="left")


def content_based_recommendations(
    df: pd.DataFrame,
    continent: str,
    attraction_type: str,
    visit_mode: str,
    top_n: int = 8,
) -> pd.DataFrame:
    """Recommend attractions similar in content profile to user preferences."""
    profile = df[
        (df["Continent"] == continent)
        & (df["AttractionType"] == attraction_type)
        & (df["VisitMode"] == visit_mode)
    ]
    if profile.empty:
        profile = df[df["Continent"] == continent]
    if profile.empty:
        profile = df

    attraction_features = (
        profile.groupby("Attraction")
        .agg(
            AvgRating=("Rating", "mean"),
            Continent=("Continent", lambda x: x.mode().iloc[0]),
            Region=("Region", lambda x: x.mode().iloc[0]),
            AttractionType=("AttractionType", lambda x: x.mode().iloc[0]),
            VisitMode=("VisitMode", lambda x: x.mode().iloc[0]),
            Visits=("UserId", "count"),
        )
        .reset_index()
    )

    # Build simple content vectors
    type_dummies = pd.get_dummies(attraction_features["AttractionType"], prefix="type")
    mode_dummies = pd.get_dummies(attraction_features["VisitMode"], prefix="mode")
    matrix = pd.concat(
        [
            attraction_features[["AvgRating", "Visits"]].astype(float),
            type_dummies,
            mode_dummies,
        ],
        axis=1,
    ).fillna(0)

    seed = matrix.iloc[0:1] if len(matrix) else matrix
    sims = cosine_similarity(matrix, seed).flatten()
    attraction_features["Score"] = sims
    attraction_features["Method"] = "Content-Based Filtering"

    return (
        attraction_features.sort_values("Score", ascending=False)
        .head(top_n)[
            [
                "Attraction",
                "Score",
                "AvgRating",
                "Continent",
                "Region",
                "AttractionType",
                "VisitMode",
                "Method",
            ]
        ]
    )
