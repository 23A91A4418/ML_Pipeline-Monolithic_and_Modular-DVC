import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score, f1_score
import joblib
import json
import os

def main():
    # Create output directories
    os.makedirs('metrics', exist_ok=True)
    os.makedirs('models', exist_ok=True)

    # Load data
    df = pd.read_csv('data/adult.csv')

    # Clean data
    df.replace(' ?', np.nan, inplace=True)
    df.dropna(inplace=True)

    # Encode categorical columns
    le = LabelEncoder()
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = le.fit_transform(df[col].astype(str))

    # Split features and target
    X = df.drop('income', axis=1)
    y = df['income']

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    # Train model
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42
    )

    model.fit(X_train, y_train)

    # Predictions
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]

    # Metrics
    metrics = {
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "auc": float(roc_auc_score(y_test, y_pred_proba)),
        "f1_macro": float(f1_score(y_test, y_pred, average="macro"))
    }

    # Save metrics
    with open('metrics/metrics.json', 'w') as f:
        json.dump(metrics, f, indent=4)

    # Save model
    joblib.dump(model, 'models/model.joblib')

    print("Model saved to: models/model.joblib")
    print("Metrics saved to: metrics/metrics.json")

if __name__ == "__main__":
    main()