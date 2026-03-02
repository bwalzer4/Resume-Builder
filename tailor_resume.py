import json
import os
import argparse
import subprocess
from google import genai

def get_tailored_json(company, jd_text):
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    tailored_content = None 
    
    with open('master_resume.json', 'r') as f:
        master_data = json.load(f)
    
    # We explicitly tell the AI to use the 'sections' key
    prompt = (
        f"Context: Recruiter for {company}. JD: {jd_text}\n"
        f"Task: From this Master JSON, pick the top 6 bullets and 12 skills.\n"
        f"Constraint: Return a JSON object with a 'sections' key. "
        f"Inside 'sections', use 'experience' for work and 'specialized_skills' for skills.\n"
        f"Master Data: {json.dumps(master_data)}"
    )

    try:
        response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        raw_text = response.text.strip()
        if "```json" in raw_text:
            raw_text = raw_text.split("```json")[1].split("```")[0].strip()
        tailored_content = json.loads(raw_text)
    except Exception as e:
        print(f"❌ AI Error: {e}")
        return None

    if tailored_content:
        # THE REPAIR LAYER: Force the RenderCV Schema
        # If the AI put experience at the top level, move it under 'sections'
        sections = {}
        if "sections" in tailored_content:
            sections = tailored_content["sections"]
        else:
            # Fallback: capture experience/skills if AI missed the 'sections' wrapper
            sections["experience"] = tailored_content.get("experience", [])
            sections["specialized_skills"] = tailored_content.get("specialized_skills", [])

        final_data = {
            "cv": {
                "name": "Ben Walzer",
                "location": "Falls Church, VA", # Update to your actual location
                "email": "benjamin.walzer4@gmail.com",
                "sections": sections
            },
            "settings": {
                "render_command": {
                    "design": "theme.yaml"
                }
            }
        }
        
        temp_path = f"outputs/{company.replace(' ', '_')}_tailored.json"
        with open(temp_path, 'w') as f:
            json.dump(final_data, f, indent=4)
        return temp_path
    
    return None

def render_pdf(json_path):
    if not json_path: return
    # Use 'render' command which is part of rendercv[full]
    subprocess.run(["rendercv", "render", json_path], check=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--company', required=True)
    parser.add_argument('--jd', required=True)
    args = parser.parse_args()
    
    tailored_file = get_tailored_json(args.company, args.jd)
    if tailored_file:
        render_pdf(tailored_file)
