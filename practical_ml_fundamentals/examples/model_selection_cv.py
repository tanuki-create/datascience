from __future__ import annotations

from _shared import DATA_DIR, make_one_hot_encoder, require_dependencies


np, pd = require_dependencies()

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


RANDOM_STATE = 42


def build_pipeline() -> Pipeline:
    numeric_features = ["tenure_months", "monthly_spend", "support_tickets"]
    categorical_features = ["plan", "region"]

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
            ("model", LogisticRegression(random_state=RANDOM_STATE, max_iter=1000)),
        ]
    )


def main() -> None:
    df = pd.read_csv(DATA_DIR / "customer_churn.csv")

    features = ["tenure_months", "monthly_spend", "support_tickets", "plan", "region"]
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

    cv = StratifiedKFold(n_splits=4, shuffle=True, random_state=RANDOM_STATE)
    search = GridSearchCV(
        estimator=build_pipeline(),
        param_grid={
            "model__C": [0.1, 1.0, 10.0],
            "model__class_weight": [None, "balanced"],
        },
        scoring="accuracy",
        cv=cv,
        n_jobs=1,
        return_train_score=True,
    )
    search.fit(X_train, y_train)

    results = pd.DataFrame(search.cv_results_)[
        ["param_model__C", "param_model__class_weight", "mean_test_score", "std_test_score"]
    ].sort_values("mean_test_score", ascending=False)
    holdout_predictions = search.predict(X_test)

    print("Model selection with cross-validation")
    print(f"Best parameters: {search.best_params_}")
    print(f"Best mean CV accuracy: {search.best_score_:.3f}")
    print(f"Holdout accuracy: {accuracy_score(y_test, holdout_predictions):.3f}")
    print("CV results")
    print(results.to_string(index=False))


if __name__ == "__main__":
    main()
