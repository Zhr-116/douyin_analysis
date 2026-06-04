import pandas as pd
df = pd.read_csv("src/core/processed/cleaned_data.csv")
print(df.head(10).to_string())