import json
import os
import argparse
import subprocess
import datetime
from google import genai

def clean_date(date_str):
    if not date_str or "present" in str(date_str).lower():
        return "present"
    # Ensure it's a string
    date_str = str(date_str)
    for fmt in ("%b %Y", "%B %Y", "%m/%Y", "%Y-%m-%d"):
        try:
            return datetime.datetime.strptime(date_str, fmt).strftime("%Y-%m")
        except:
            continue
    return date_str

def get_tailored_json(company, jd_text):
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    
    with open('master_resume.json', 'r') as f:
        master_data = json.load(f)
    
    # We use double braces {{ }} for literal brackets in f-strings
    prompt = (
        f"Context: Recruiter for {company}. JD: {jd_text}\n"
        f"Task: Create a tailored resume JSON.\n"
        f"Structure required:\n"
        f"1. 'summary': A 2-sentence professional profile string.\n"
        f"2. 'experience': Top 6 bullets from NASA/USMC. Use keys: 'company', 'position', 'location', 'start_date', 'highlights'.\n"
        f"3. 'skills': An array of skill groups. Example: [{{'name': 'Technical Skills', 'details': 'Python, SQL, AWS'}}].\n"
        f"Master Data: {json.dumps(master_data)}"
    )

    try:
        response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        raw_text = response.text.strip()
        
        # Strip Markdown if present
        if "```json" in raw_text:
            raw_text = raw_text.split("```json")[1].split("```")[0].strip()
        elif "```" in raw_text:
             raw_text = raw_text.split("```")[1].split("```")[0].strip()
        
        ai_data = json.loads(raw_text)

        # --- FIX 1: Format Summary as a list of strings ---
        raw_summary = ai_data.get("summary", "")
        formatted_summary = [raw_summary] if isinstance(raw_summary, str) else raw_summary

        # --- FIX 2: Standardize Experience Entries ---
        raw_experience = ai_data.get("experience", [])
        for entry in raw_experience:
            entry["start_date"] = clean_date(entry.get("start_date", ""))
            if "end_date" in entry:
                entry["end_date"] = clean_date(entry["end_date"])
            # Ensure highlights is a list
            if isinstance(entry.get("highlights"), str):
                entry["highlights"] = [entry["highlights"]]

        # --- FIX 3: Robust Skills Mapping ---
        raw_skills = ai_data.get("skills", [])
        formatted_skills = []
        
        if isinstance(raw_skills, list):
            # If AI gave us a list of dicts, rename 'name' to 'label'
            for item in raw_skills:
                if isinstance(item, dict):
                    label = item.get("label", item.get("name", "Technical Skills"))
                    details = item.get("details", "")
                    formatted_skills.append({"label": label, "details": details})
                elif isinstance(item, str):
                    if not formatted_skills:
                        formatted_skills.append({"label": "Skills", "details": item})
                    else:
                        formatted_skills[0]["details"] += f", {item}"
        
        # Assemble Final Sections
        sections = {
            "summary": formatted_summary,
            "experience": raw_experience,
            "skills": formatted_skills
        }

        final_data = {
            "cv": {
                "name": "Ben Walzer",
                "location": "Falls Church, VA",
                "email": "benjamin.walzer4@gmail.com",
                "phone": "+1 757-374-1691",
                "sections": sections
            },
            "design": {
                "theme": "engineering",
                # We use the theme name as the key for its specific options
                "engineering": {
                    "font": "latin-modern",
                    "page_size": "us-letter",
                    "header_font_size": "24 pt",
                    "margins": {
                        "top": "1.5 cm",
                        "bottom": "1.5 cm",
                        "left": "1.5 cm",
                        "right": "1.5 cm"
                    }
                }
            }
        }

        os.makedirs('outputs', exist_ok=True)
        temp_path = f"outputs/{company.replace(' ', '_')}_tailored.json"
        with open(temp_path, 'w') as f:
            json.dump(final_data, f, indent=4)
        return temp_path
        
    except Exception as e:
        print(f"❌ Error during AI generation or processing: {e}")
        return None

def render_pdf(json_path):
    if not json_path: return
    print(f"--- Rendering PDF from {json_path} ---")
    try:
        subprocess.run(["rendercv", "render", json_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ RenderCV failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--company', required=True)
    parser.add_argument('--jd', required=True)
    args = parser.parse_args()
    
    tailored_file = get_tailored_json(args.company, args.jd)
    if tailored_file:
        render_pdf(tailored_file)
