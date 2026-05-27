from __future__ import annotations

from _shared import DATA_DIR, require_dependencies


np, pd = require_dependencies()

from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


RANDOM_STATE = 42


def rmse(y_true, y_pred) -> float:
    return float(np.sqrt(mean_squared_error(y_true, y_pred)))


def print_metrics(name: str, y_true, y_pred) -> None:
    print(
        f"{name}: "
        f"MAE={mean_absolute_error(y_true, y_pred):.1f} "
        f"RMSE={rmse(y_true, y_pred):.1f} "
        f"R2={r2_score(y_true, y_pred):.3f}"
    )


def main() -> None:
    df = pd.read_csv(DATA_DIR / "rentals.csv")

    features = ["sqft", "bedrooms", "age_years", "distance_km"]
    target = "rent"
    X = df[features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.33,
        random_state=RANDOM_STATE,
    )

    mean_baseline = DummyRegressor(strategy="mean")
    mean_baseline.fit(X_train, y_train)
    baseline_predictions = mean_baseline.predict(X_test)

    model = LinearRegression()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    print("Regression baseline: monthly rent")
    print(f"Rows: train={len(X_train)} test={len(X_test)}")
    print_metrics("Mean baseline", y_test, baseline_predictions)
    print_metrics("Linear regression", y_test, predictions)

    coefficients = pd.Series(model.coef_, index=features).sort_values(key=np.abs, ascending=False)
    print("Linear coefficients")
    print(coefficients.round(2))


if __name__ == "__main__":
    main()
