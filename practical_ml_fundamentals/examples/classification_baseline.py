from __future__ import annotations

from _shared import DATA_DIR, require_dependencies


np, pd = require_dependencies()

from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, precision_score, recall_score
from sklearn.model_selection import train_test_split


RANDOM_STATE = 42


def main() -> None:
    df = pd.read_csv(DATA_DIR / "customer_churn.csv")

    features = ["tenure_months", "monthly_spend", "support_tickets"]
    target = "churned"
    X = df[features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.33,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    majority_class = DummyClassifier(strategy="most_frequent")
    majority_class.fit(X_train, y_train)
    majority_predictions = majority_class.predict(X_test)

    model = LogisticRegression(random_state=RANDOM_STATE, max_iter=1000)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]

    print("Classification baseline: customer churn")
    print(f"Rows: train={len(X_train)} test={len(X_test)}")
    print(f"Majority-class accuracy: {accuracy_score(y_test, majority_predictions):.3f}")
    print(f"Logistic regression accuracy: {accuracy_score(y_test, predictions):.3f}")
    print("Confusion matrix [rows=true, cols=predicted]")
    print(confusion_matrix(y_test, predictions))
    print("Threshold trade-off")
    for threshold in [0.10, 0.50, 0.90]:
        threshold_predictions = (probabilities >= threshold).astype(int)
        print(
            f"threshold={threshold:.2f} "
            f"precision={precision_score(y_test, threshold_predictions, zero_division=0):.3f} "
            f"recall={recall_score(y_test, threshold_predictions, zero_division=0):.3f} "
            f"predicted_positive={threshold_predictions.sum()}"
        )
    print("Classification report")
    print(classification_report(y_test, predictions, target_names=["retained", "churned"]))


if __name__ == "__main__":
    main()
