"""Application configuration and paths."""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

DATA_PATH = os.path.join(PROJECT_ROOT, "Tourism_Project", "final_data.csv")
ENRICHED_CACHE = os.path.join(BASE_DIR, "enriched_dataset.csv")
USERS_FILE = os.path.join(BASE_DIR, "users.json")
MODELS_DIR = os.path.join(BASE_DIR, "models")

APP_TITLE = "Tourism Analytics & Recommendation System"
PAGE_ICON = "🌍"

# Chart catalog for Live Graphs dropdown
CHART_OPTIONS = {
    "1. Animated Bar Chart": "animated_bar",
    "2. Horizontal Bar Chart": "horizontal_bar",
    "3. Top 10 Countries Bar Chart": "top_countries",
    "4. Visit Modes Pie Chart": "visit_mode_pie",
    "5. Ratings Histogram": "rating_histogram",
    "6. Ratings Box Plot by Visit Mode": "rating_box",
    "7. Attraction Ratings Scatter": "rating_scatter",
    "8. Attraction Types Treemap": "attraction_treemap",
    "9. Rating Violin by Visit Mode": "rating_violin",
    "10. Monthly Activity Line Chart": "monthly_line",
    "11. Tourism Growth Area Chart": "growth_area",
    "12. Visit Mode Stacked Bar by Continent": "stacked_visit_mode",
    "13. Regional Ratings Strip Plot": "rating_strip",
    "14. Correlation Heatmap": "correlation_heatmap",
    "15. Pair Plot / Scatter Matrix": "pair_plot",
}

REGRESSION_MODEL_FILES = {
    "Linear Regression": "linear_regression_model.pkl",
    "Random Forest": "random_forest_model.pkl",
    "XGBoost": "xgboost_model.pkl",
}

CLASSIFICATION_MODEL_FILES = {
    "Logistic Regression": "logistic_regression_model.pkl",
    "Random Forest Classifier": "random_forest_classifier.pkl",
    "XGBoost Classifier": "xgboost_classifier.pkl",
}
