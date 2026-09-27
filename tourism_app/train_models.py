"""Standalone script to train and save all ML models."""
from data_loader import load_data
from ml_models import train_all_models


def main() -> None:
    print("Loading tourism data...")
    df = load_data()
    print(f"Records: {len(df):,}")
    print("Training models (this may take a minute)...")
    bundle = train_all_models(df)
    print("\n=== Regression Metrics ===")
    for name, metrics in bundle.regression_metrics.items():
        print(f"{name}: {metrics}")
    print("\n=== Classification Metrics ===")
    for name, metrics in bundle.classification_metrics.items():
        print(f"{name}: {metrics}")
    print("\nModels saved to tourism_app/models/")


if __name__ == "__main__":
    main()
