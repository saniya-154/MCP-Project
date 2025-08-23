import os
import json
import csv
import requests
from serpapi import GoogleSearch
from bs4 import BeautifulSoup
import time

# -------------------
# CONFIG
# -------------------
SERPAPI_KEY = "72b7fed1869fee1158459d43656b0afd563277075a518516985073b4fb989f83"   # Replace with your API key
QUERIES = [
    # "MCP server database",
    # "MCP server SQL",
    # "MCP server LLM",
    # "MCP server Claude AI",
    # "MCP server LangChain",
    # "MCP server Docker",
    # "MCP server Notion",
    # "MCP server Slack integration",
    # "MCP server GitHub Copilot",

    "MCP servers site:medium.com",
    "MCP servers site:dev.to",
    "MCP servers site:kdnuggets.com",
    "MCP servers site:datacamp.com",
    "MCP servers site:reddit.com"
]
OUTPUT_CSV = "mcp_servers_Source_Specific.csv"
OUTPUT_JSON = "mcp_servers_Source_Specific.json"

# -------------------
# HELPER FUNCTIONS
# -------------------

def search_serpapi(query):
    """Search Google using SerpAPI and return results."""
    params = {
        "q": query,
        "api_key": SERPAPI_KEY,
        "engine": "google",
        "num": 20
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    return results.get("organic_results", [])


def scrape_github_repo(url):
    """Scrape GitHub repo page to get description if available."""
    try:
        res = requests.get(url, timeout=10)
        if res.status_code != 200:
            return None
        soup = BeautifulSoup(res.text, "html.parser")
        desc_tag = soup.find("p", {"class": "f4 my-3"})
        if desc_tag:
            return desc_tag.text.strip()
    except Exception as e:
        print(f"Error scraping {url}: {e}")
    return None


def collect_data():
    """Main function to collect data from queries."""
    dataset = []
    seen = set()

    for query in QUERIES:
        print(f"Searching for: {query}")
        results = search_serpapi(query)

        for r in results:
            title = r.get("title", "")
            link = r.get("link", "")
            snippet = r.get("snippet", "")

            if link in seen:
                continue
            seen.add(link)

            # If GitHub repo, try to scrape description
            description = snippet
            if "github.com" in link:
                repo_desc = scrape_github_repo(link)
                if repo_desc:
                    description = repo_desc

            dataset.append({
                "server_name": title,
                "description": description,
                "category": "MCP Server",
                "repo_link": link
            })

            time.sleep(1)  # avoid overloading

    return dataset


def save_dataset(dataset):
    """Save dataset into CSV and JSON."""
    # Save CSV
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["server_name", "description", "category", "repo_link"])
        writer.writeheader()
        writer.writerows(dataset)

    # Save JSON
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=4, ensure_ascii=False)

    print(f"✅ Saved {len(dataset)} entries to {OUTPUT_CSV} and {OUTPUT_JSON}")


# -------------------
# MAIN
# -------------------
if __name__ == "__main__":
    data = collect_data()
    save_dataset(data)
