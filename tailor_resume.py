import json
import os
import argparse
import subprocess
import datetime
from google import genai

def clean_date(date_str):
    if not date_str or "Present" in date_str.lower():
        return "present"
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
    
    prompt = (
        f"Context: Recruiter for {company}. JD: {jd_text}\n"
        f"Task: Create a tailored resume JSON.\n"
        f"Structure required:\n"
        f"1. 'summary': A 2-sentence professional profile.\n"
        f"2. 'experience': Top 6 bullets from NASA/USMC. Use keys: 'company', 'position', 'location', 'start_date', 'highlights'.\n"
        f"3. 'skills': An array of skill groups. Example: [{{'name': 'Technical Skills', 'details': 'Python, SQL, AWS'}}].\n"
        f"Master Data: {json.dumps(master_data)}"
    )

    try:
        response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        raw_text = response.text.strip()
        if "```json" in raw_text:
            raw_text = raw_text.split("```json")[1].split("```")[0].strip()
        
        ai_data = json.loads(raw_text)

        # Map AI response to RenderCV 'Sections'
        sections = {
            "summary": ai_data.get("summary", ""),
            "experience": ai_data.get("experience", []),
            "skills": ai_data.get("skills", [])
        }

        # Date Sanitization
        for entry in sections["experience"]:
            entry["start_date"] = clean_date(entry.get("start_date", ""))
            if "end_date" in entry:
                entry["end_date"] = clean_date(entry["end_date"])

        final_data = {
            "cv": {
                "name": "Ben Walzer",
                "location": "Falls Church, VA",
                "email": "benjamin.walzer4@gmail.com", # Update this!
                "phone": "757-374-1691",            # Update this!
                "sections": sections
            },
            "design": {"theme": "classic"}
        }

        temp_path = f"outputs/{company.replace(' ', '_')}_tailored.json"
        with open(temp_path, 'w') as f:
            json.dump(final_data, f, indent=4)
        return temp_path
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def render_pdf(json_path):
    if not json_path: return
    # Use 'render' command
    subprocess.run(["rendercv", "render", json_path], check=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--company', required=True)
    parser.add_argument('--jd', required=True)
    args = parser.parse_args()
    
    tailored_file = get_tailored_json(args.company, args.jd)
    if tailored_file:
        render_pdf(tailored_file)
