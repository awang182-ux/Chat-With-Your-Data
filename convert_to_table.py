import json
import pandas as pd

with open("model_eval_results.json") as f:
    data = json.load(f)

df = pd.DataFrame(data)

# Keep only useful columns
df = df[["model", "dataset", "question", "success"]]

# Save to CSV
df.to_csv("model_results_table.csv", index=False)

print("Saved as model_results_table.csv")
