import json
import pandas as pd

files = [
    "mcp_servers_general.json",
    "mcp_servers_Category_Specific.json",
    "mcp_servers_Source_Specific.json"
]

all_data = []

# Load all files
for f in files:
    with open(f, "r", encoding="utf-8") as file:
        all_data.extend(json.load(file))

# Convert to DataFrame
df = pd.DataFrame(all_data)

# Normalize server_name (remove : and ...)
df["server_name"] = df["server_name"].str.split(":").str[0].str.strip()

# Remove duplicates by repo_link
df.drop_duplicates(subset=["repo_link"], inplace=True)

# Save master file
df.to_csv("mcp_servers_master.csv", index=False)
df.to_json("mcp_servers_master.json", orient="records", indent=2)

print(f"✅ Final merged dataset saved: {len(df)} entries")
