import os
import joblib
import numpy as np
from datetime import datetime, timezone
from typing import Dict, Any, List
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix

from app.ml.dataset import generate_realistic_risk_dataset
from app.ml.feature_engineering import extract_features, FEATURE_NAMES, CLASSES

MODEL_STORAGE_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "ml_models")

def train_and_evaluate_models(num_samples: int = 700, save_best: bool = True) -> Dict[str, Any]:
    """
    Train, cross-validate, and empirically evaluate 4 classification algorithms on realistic dataset.
    Calculates actual Accuracy, Precision, Recall, F1, and Confusion Matrix.
    Persists best model to disk.
    """
    os.makedirs(MODEL_STORAGE_PATH, exist_ok=True)
    
    # 1. Dataset Generation & Splitting (70% train, 15% val, 15% test)
    df = generate_realistic_risk_dataset(num_samples=num_samples, random_state=42)
    X, y = extract_features(df)

    # First split: 70% train, 30% temp
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=0.30, random_state=42, stratify=y
    )
    # Second split: 15% val, 15% test
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.50, random_state=42, stratify=y_temp
    )

    # 2. Scaling
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_val_scaled = scaler.transform(X_val)
    X_test_scaled = scaler.transform(X_test)

    # 3. Models Definition (4 benchmark algorithms)
    models = {
        "Random Forest": RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            class_weight="balanced",
            random_state=42
        ),
        "Gradient Boosting": GradientBoostingClassifier(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            random_state=42
        ),
        "Decision Tree": DecisionTreeClassifier(
            max_depth=8,
            min_samples_split=5,
            class_weight="balanced",
            random_state=42
        ),
        "Logistic Regression": LogisticRegression(
            max_iter=1000,
            solver="lbfgs",
            random_state=42
        )
    }

    results = []
    best_model_name = None
    best_f1 = -1.0
    best_model_obj = None

    for name, model in models.items():
        # 5-fold cross validation on training set
        cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring="f1_macro")
        
        # Fit on full training set
        model.fit(X_train_scaled, y_train)

        # Predict on unseen test set
        y_pred = model.predict(X_test_scaled)

        acc = float(accuracy_score(y_test, y_pred))
        precision_macro, recall_macro, f1_macro, _ = precision_recall_fscore_support(
            y_test, y_pred, average="macro", zero_division=0
        )
        conf_mat = confusion_matrix(y_test, y_pred, labels=CLASSES).tolist()

        # Feature importances if available
        feat_importances = {}
        if hasattr(model, "feature_importances_"):
            for f_name, imp in zip(FEATURE_NAMES, model.feature_importances_):
                feat_importances[f_name] = round(float(imp), 4)
        elif hasattr(model, "coef_"):
            avg_coef = np.mean(np.abs(model.coef_), axis=0)
            for f_name, imp in zip(FEATURE_NAMES, avg_coef):
                feat_importances[f_name] = round(float(imp), 4)

        model_metrics = {
            "model_name": name,
            "model_type": name.lower().replace(" ", "_"),
            "version": "1.0.0",
            "accuracy": round(acc, 4),
            "precision": round(float(precision_macro), 4),
            "recall": round(float(recall_macro), 4),
            "f1_score": round(float(f1_macro), 4),
            "cv_f1_mean": round(float(np.mean(cv_scores)), 4),
            "confusion_matrix": conf_mat,
            "feature_importances": feat_importances,
            "is_active": False,
            "trained_at": datetime.now(timezone.utc).isoformat()
        }
        results.append(model_metrics)

        if f1_macro > best_f1:
            best_f1 = f1_macro
            best_model_name = name
            best_model_obj = model

    # Mark best model as active
    for r in results:
        if r["model_name"] == best_model_name:
            r["is_active"] = True

    # Save best model to disk
    if save_best and best_model_obj:
        save_path = os.path.join(MODEL_STORAGE_PATH, "risk_classifier.pkl")
        scaler_path = os.path.join(MODEL_STORAGE_PATH, "scaler.pkl")
        metadata_path = os.path.join(MODEL_STORAGE_PATH, "metadata.json")

        joblib.dump(best_model_obj, save_path)
        joblib.dump(scaler, scaler_path)

        import json
        with open(metadata_path, "w") as f:
            json.dump({
                "best_model_name": best_model_name,
                "version": "1.0.0",
                "trained_at": datetime.now(timezone.utc).isoformat(),
                "test_samples": len(y_test),
                "metrics": [r for r in results if r["model_name"] == best_model_name][0],
                "all_models": results
            }, f, indent=2)

    return {
        "status": "success",
        "message": f"Trained {len(models)} models successfully. Best model: {best_model_name} (F1: {round(best_f1, 4)})",
        "samples_count": len(df),
        "test_samples": len(y_test),
        "models_evaluated": results,
        "best_model_name": best_model_name,
        "best_model_accuracy": [r["accuracy"] for r in results if r["model_name"] == best_model_name][0],
        "best_model_f1": round(best_f1, 4)
    }

if __name__ == "__main__":
    train_and_evaluate_models()
