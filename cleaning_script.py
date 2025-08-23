import json
import pandas as pd

with open("mcp_servers_master.json", "r", encoding="utf-8") as f:
    data = json.load(f)

cleaned = []

for entry in data:
    name = entry.get("server_name", "").split(":")[0].strip()
    desc = entry.get("description", "").strip() or "No description available"
    link = entry.get("repo_link", "").strip()

    # Skip irrelevant links
    if not any(domain in link for domain in ["github.com", "gitlab.com", "mcp", ".io", ".org"]):
        continue

    # Categorization rules
    if any(word in name.lower() or word in desc.lower() for word in ["sql", "database"]):
        category = "Database"
    elif any(word in name.lower() or word in desc.lower() for word in ["claude", "chat", "llm", "gpt"]):
        category = "LLM"
    elif "docker" in name.lower() or "docker" in desc.lower():
        category = "DevOps"
    elif any(word in name.lower() or word in desc.lower() for word in ["slack", "notion", "integration"]):
        category = "Productivity"
    else:
        category = "General MCP"

    cleaned.append({
        "server_name": name,
        "description": desc,
        "category": category,
        "repo_link": link,
        "text_for_embedding": f"{name} - {desc}"
    })

# Save cleaned dataset
df = pd.DataFrame(cleaned).drop_duplicates(subset=["repo_link"])
df.to_csv("mcp_servers_cleaned.csv", index=False)
df.to_json("mcp_servers_cleaned.json", orient="records", indent=2)

print(f"✅ Cleaned dataset saved: {len(df)} entries")
