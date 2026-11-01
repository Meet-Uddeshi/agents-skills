import json

def main():
    with open(".agent/scripts/catalog_summary.json", encoding="utf-8") as f:
        data = json.load(f)
    agents = data["agents"]
    print(f"Total Agents: {len(agents)}")
    for a in agents:
        name = a["name"]
        skills = ", ".join(a["skills"][:4])
        desc = a["description"][:70]
        print(f"{name:26} | {len(a['skills']):2d} skills | {desc}")

if __name__ == "__main__":
    main()
