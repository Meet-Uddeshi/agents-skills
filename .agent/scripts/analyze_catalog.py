import glob
import os
import re
import json

def analyze():
    agent_files = sorted(glob.glob(".agent/agents/*.md"))
    skill_dirs = [d for d in os.listdir(".agent/skills") if os.path.isdir(os.path.join(".agent/skills", d))]
    
    agent_catalog = []
    
    for af in agent_files:
        name = os.path.splitext(os.path.basename(af))[0]
        with open(af, "r", encoding="utf-8") as f:
            content = f.read()
        
        desc = ""
        skills = []
        
        m_desc = re.search(r"description:\s*(.*?)(?=\n[a-zA-Z0-9_-]+:|\n---)", content, re.DOTALL)
        if m_desc:
            desc = " ".join(m_desc.group(1).split())
            
        m_skills = re.search(r"skills:\s*(.*?)(?=\n[a-zA-Z0-9_-]+:|\n---)", content, re.DOTALL)
        if m_skills:
            raw_skills = " ".join(m_skills.group(1).split())
            skills = [s.strip() for s in raw_skills.split(",") if s.strip()]
            
        agent_catalog.append({
            "name": name,
            "description": desc,
            "skills": skills,
            "file": af
        })
        
    print(f"Total Agents: {len(agent_catalog)}")
    print(f"Total Skill Dirs: {len(skill_dirs)}")
    
    with open(".agent/scripts/catalog_summary.json", "w", encoding="utf-8") as out:
        json.dump({
            "agents": agent_catalog,
            "skills_count": len(skill_dirs),
            "skills": sorted(skill_dirs)
        }, out, indent=2)
    print("Catalog summary written to .agent/scripts/catalog_summary.json")

if __name__ == "__main__":
    analyze()
