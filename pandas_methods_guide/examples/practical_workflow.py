from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
input_path = BASE_DIR / "sales.csv"
output_dir = BASE_DIR / "output"
output_dir.mkdir(exist_ok=True)


df = pd.read_csv(input_path)

print("head")
print(df.head())
print("shape", df.shape)
print("dtypes")
print(df.dtypes)

df["date"] = pd.to_datetime(df["date"])

print("missing")
print(df.isna().sum())

df = df.dropna(subset=["date", "store", "price"])
df["quantity"] = df["quantity"].fillna(0)
df = df.assign(amount=df["quantity"] * df["price"])

store_summary = (
    df.groupby("store")
    .agg(
        total_amount=("amount", "sum"),
        avg_price=("price", "mean"),
        row_count=("amount", "count"),
    )
    .reset_index()
    .sort_values("total_amount", ascending=False)
)

monthly = (
    df.set_index("date")
    .resample("ME")["amount"]
    .sum()
    .reset_index(name="monthly_amount")
)
monthly["rolling_3m"] = monthly["monthly_amount"].rolling(window=3).mean()

store_summary.to_csv(output_dir / "store_summary.csv", index=False)
try:
    monthly.to_excel(output_dir / "monthly_summary.xlsx", index=False)
except ModuleNotFoundError as exc:
    if exc.name != "openpyxl":
        raise
    monthly.to_csv(output_dir / "monthly_summary.csv", index=False)
    print("openpyxl is not installed; wrote monthly_summary.csv instead.")

print("store_summary")
print(store_summary)
print("monthly")
print(monthly)
