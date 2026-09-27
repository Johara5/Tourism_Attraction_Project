"""Machine learning: training, evaluation, prediction, and model persistence."""
import os
from dataclasses import dataclass

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    mean_squared_error,
    precision_score,
    r2_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier, XGBRegressor

from config import MODELS_DIR, REGRESSION_MODEL_FILES, CLASSIFICATION_MODEL_FILES


@dataclass
class ModelBundle:
    regression: dict
    classification: dict
    encoders: dict
    regression_metrics: dict
    classification_metrics: dict


def _ensure_models_dir() -> None:
    os.makedirs(MODELS_DIR, exist_ok=True)


def _encode_features(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    encoders = {}
    encoded = pd.DataFrame()
    for col in ["Continent", "Region", "AttractionType", "VisitMode"]:
        le = LabelEncoder()
        encoded[col] = le.fit_transform(df[col].astype(str))
        encoders[col] = le
    encoded["VisitTime"] = df["VisitTime"]
    encoded["Year"] = df["Year"]
    encoded["Month"] = df["Month"]
    return encoded, encoders


def train_all_models(df: pd.DataFrame, sample_size: int = 25000) -> ModelBundle:
    """Train regression, classification models and save with joblib."""
    _ensure_models_dir()
    data = df.sample(min(sample_size, len(df)), random_state=42).reset_index(drop=True)

    features, encoders = _encode_features(data)
    y_rating = data["Rating"].values
    y_visit = data["VisitMode"].values

    X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(
        features, y_rating, test_size=0.2, random_state=42
    )
    X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(
        features.drop(columns=["VisitMode"]), y_visit, test_size=0.2, random_state=42
    )

    regressors = {
        "Linear Regression": LinearRegression(),
        "Random Forest": RandomForestRegressor(n_estimators=80, random_state=42, n_jobs=-1),
        "XGBoost": XGBRegressor(
            n_estimators=80, max_depth=6, learning_rate=0.1, random_state=42, verbosity=0
        ),
    }

    classifiers = {
        "Logistic Regression": LogisticRegression(max_iter=500, random_state=42),
        "Random Forest Classifier": RandomForestClassifier(
            n_estimators=80, random_state=42, n_jobs=-1
        ),
        "XGBoost Classifier": XGBClassifier(
            n_estimators=80, max_depth=6, learning_rate=0.1, random_state=42, verbosity=0
        ),
    }

    regression_models = {}
    regression_metrics = {}
    for name, model in regressors.items():
        model.fit(X_train_r, y_train_r)
        preds = model.predict(X_test_r)
        regression_metrics[name] = {
            "R² Score": round(r2_score(y_test_r, preds), 4),
            "Mean Squared Error": round(mean_squared_error(y_test_r, preds), 4),
        }
        regression_models[name] = model
        fname = REGRESSION_MODEL_FILES[name]
        joblib.dump(model, os.path.join(MODELS_DIR, fname))

    classification_models = {}
    classification_metrics = {}
    visit_encoder = LabelEncoder()
    y_train_enc = visit_encoder.fit_transform(y_train_c)
    y_test_enc = visit_encoder.transform(y_test_c)

    for name, model in classifiers.items():
        model.fit(X_train_c, y_train_enc)
        preds = model.predict(X_test_c)
        classification_metrics[name] = {
            "Accuracy": round(accuracy_score(y_test_enc, preds), 4),
            "Precision": round(precision_score(y_test_enc, preds, average="weighted", zero_division=0), 4),
            "Recall": round(recall_score(y_test_enc, preds, average="weighted", zero_division=0), 4),
            "F1 Score": round(f1_score(y_test_enc, preds, average="weighted", zero_division=0), 4),
        }
        classification_models[name] = model
        fname = CLASSIFICATION_MODEL_FILES[name]
        joblib.dump(model, os.path.join(MODELS_DIR, fname))

    joblib.dump(encoders, os.path.join(MODELS_DIR, "feature_encoders.pkl"))
    joblib.dump(visit_encoder, os.path.join(MODELS_DIR, "visit_mode_label_encoder.pkl"))
    joblib.dump(regression_metrics, os.path.join(MODELS_DIR, "regression_metrics.pkl"))
    joblib.dump(classification_metrics, os.path.join(MODELS_DIR, "classification_metrics.pkl"))

    return ModelBundle(
        regression=regression_models,
        classification=classification_models,
        encoders=encoders,
        regression_metrics=regression_metrics,
        classification_metrics=classification_metrics,
    )


def models_exist() -> bool:
    required = list(REGRESSION_MODEL_FILES.values()) + list(CLASSIFICATION_MODEL_FILES.values())
    return all(os.path.exists(os.path.join(MODELS_DIR, f)) for f in required)


def load_models() -> ModelBundle:
    """Load trained models from disk."""
    regression = {}
    for name, fname in REGRESSION_MODEL_FILES.items():
        regression[name] = joblib.load(os.path.join(MODELS_DIR, fname))

    classification = {}
    for name, fname in CLASSIFICATION_MODEL_FILES.items():
        classification[name] = joblib.load(os.path.join(MODELS_DIR, fname))

    encoders = joblib.load(os.path.join(MODELS_DIR, "feature_encoders.pkl"))
    reg_path = os.path.join(MODELS_DIR, "regression_metrics.pkl")
    cls_path = os.path.join(MODELS_DIR, "classification_metrics.pkl")
    reg_metrics = joblib.load(reg_path) if os.path.exists(reg_path) else {}
    cls_metrics = joblib.load(cls_path) if os.path.exists(cls_path) else {}
    return ModelBundle(
        regression=regression,
        classification=classification,
        encoders=encoders,
        regression_metrics=reg_metrics,
        classification_metrics=cls_metrics,
    )


def get_or_train_models(df: pd.DataFrame, force_retrain: bool = False) -> ModelBundle:
    if not force_retrain and models_exist():
        return load_models()
    return train_all_models(df)


def build_feature_row(
    continent: str,
    region: str,
    attraction_type: str,
    visit_mode: str,
    visit_time: int,
    year: int,
    month: int,
    encoders: dict,
) -> pd.DataFrame:
    row = {
        "Continent": encoders["Continent"].transform([continent])[0],
        "Region": encoders["Region"].transform([region])[0],
        "AttractionType": encoders["AttractionType"].transform([attraction_type])[0],
        "VisitMode": encoders["VisitMode"].transform([visit_mode])[0],
        "VisitTime": visit_time,
        "Year": year,
        "Month": month,
    }
    return pd.DataFrame([row])


def predict_rating(model_name: str, features: pd.DataFrame, bundle: ModelBundle) -> float:
    model = bundle.regression[model_name]
    return float(np.clip(model.predict(features)[0], 1, 5))


def predict_visit_mode(model_name: str, features: pd.DataFrame, bundle: ModelBundle) -> str:
    visit_encoder = joblib.load(os.path.join(MODELS_DIR, "visit_mode_label_encoder.pkl"))
    model = bundle.classification[model_name]
    X = features.drop(columns=["VisitMode"], errors="ignore")
    pred = model.predict(X)[0]
    return visit_encoder.inverse_transform([pred])[0]
