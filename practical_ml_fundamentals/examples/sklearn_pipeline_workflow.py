from __future__ import annotations

from _shared import DATA_DIR, make_one_hot_encoder, require_dependencies


np, pd = require_dependencies()

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


RANDOM_STATE = 42


def main() -> None:
    df = pd.read_csv(DATA_DIR / "customer_churn.csv")

    numeric_features = ["tenure_months", "monthly_spend", "support_tickets"]
    categorical_features = ["plan", "region"]
    target = "churned"

    X = df[numeric_features + categorical_features]
    y = df[target]

    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("one_hot", make_one_hot_encoder()),
        ]
    )
    preprocess = ColumnTransformer(
        transformers=[
            ("numeric", numeric_pipeline, numeric_features),
            ("categorical", categorical_pipeline, categorical_features),
        ]
    )
    workflow = Pipeline(
        steps=[
            ("preprocess", preprocess),
            ("model", LogisticRegression(random_state=RANDOM_STATE, max_iter=1000)),
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.33,
        random_state=RANDOM_STATE,
        stratify=y,
    )
    workflow.fit(X_train, y_train)
    predictions = workflow.predict(X_test)

    new_customers = pd.DataFrame(
        [
            {
                "tenure_months": 4,
                "monthly_spend": 41,
                "support_tickets": 4,
                "plan": "basic",
                "region": "north",
            },
            {
                "tenure_months": 34,
                "monthly_spend": 88,
                "support_tickets": 0,
                "plan": "premium",
                "region": "west",
            },
        ]
    )
    churn_probability = workflow.predict_proba(new_customers)[:, 1]

    print("scikit-learn pipeline workflow")
    print(f"Holdout accuracy: {accuracy_score(y_test, predictions):.3f}")
    print("New customer churn probabilities")
    print(new_customers.assign(churn_probability=np.round(churn_probability, 3)))


if __name__ == "__main__":
    main()
