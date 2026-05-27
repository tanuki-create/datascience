from __future__ import annotations

from _shared import DATA_DIR, OUTPUT_DIR, make_one_hot_encoder, require_dependencies


np, pd = require_dependencies()

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


RANDOM_STATE = 7


def build_pipeline(numeric_features: list[str], categorical_features: list[str]) -> Pipeline:

    preprocess = ColumnTransformer(
        transformers=[
            (
                "numeric",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="median")),
                        ("scaler", StandardScaler()),
                    ]
                ),
                numeric_features,
            ),
            (
                "categorical",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        ("one_hot", make_one_hot_encoder()),
                    ]
                ),
                categorical_features,
            ),
        ]
    )
    return Pipeline(
        steps=[
            ("preprocess", preprocess),
            ("model", LogisticRegression(C=0.2, random_state=RANDOM_STATE, max_iter=1000)),
        ]
    )


def label_error_type(row) -> str:
    if row["y_true"] == row["y_pred"]:
        return "correct"
    if row["y_true"] == 0 and row["y_pred"] == 1:
        return "false_positive"
    return "false_negative"


def main() -> None:
    df = pd.read_csv(DATA_DIR / "customer_churn.csv")

    analysis_features = ["tenure_months", "monthly_spend", "support_tickets", "plan", "region"]
    model_numeric_features = ["support_tickets"]
    model_categorical_features = ["plan"]
    model_features = model_numeric_features + model_categorical_features
    target = "churned"
    X = df[model_features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.40,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    model = build_pipeline(model_numeric_features, model_categorical_features)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]

    report = df.loc[X_test.index, analysis_features].copy()
    report["y_true"] = y_test.to_numpy()
    report["y_pred"] = predictions
    report["churn_probability"] = np.round(probabilities, 3)
    report["confidence"] = np.round(np.where(predictions == 1, probabilities, 1 - probabilities), 3)
    report["error_type"] = report.apply(label_error_type, axis=1)

    report = report.sort_values(["error_type", "confidence"], ascending=[True, False])
    segment_summary = (
        report.assign(is_error=report["error_type"] != "correct")
        .groupby(["plan", "region"], as_index=False)
        .agg(
            rows=("is_error", "size"),
            errors=("is_error", "sum"),
            error_rate=("is_error", "mean"),
            avg_confidence=("confidence", "mean"),
        )
        .sort_values(["error_rate", "rows"], ascending=[False, False])
    )

    OUTPUT_DIR.mkdir(exist_ok=True)
    output_path = OUTPUT_DIR / "error_analysis_predictions.csv"
    report.to_csv(output_path, index=False)

    errors = report[report["error_type"] != "correct"]
    print("Error analysis template: customer churn")
    print(f"Holdout accuracy: {accuracy_score(y_test, predictions):.3f}")
    print(f"Wrote row-level prediction report: {output_path}")
    print("Highest-confidence mistakes")
    if errors.empty:
        print("No mistakes on this small holdout split. Reuse the report columns on a larger dataset.")
    else:
        print(
            errors[
                [
                    "tenure_months",
                    "monthly_spend",
                    "support_tickets",
                    "plan",
                    "region",
                    "y_true",
                    "y_pred",
                    "confidence",
                    "error_type",
                ]
            ].head(10).to_string(index=False)
        )
    print("Segment summary")
    print(segment_summary.to_string(index=False))


if __name__ == "__main__":
    main()
