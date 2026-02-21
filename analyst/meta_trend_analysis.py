import pandas as pd

df = pd.read_csv("../ml_core/data/processed/cleaned.csv")

df["date"] = pd.to_datetime(df["date"])
df["month"] = df["date"].dt.to_period("M")

monthly_winrate = df.groupby("month")["winner"].mean()

monthly_winrate.to_csv("monthly_meta_trend.csv")

print(monthly_winrate)