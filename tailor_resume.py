import json
import os
import argparse
import subprocess
from google import genai

def get_tailored_json(company, jd_text):
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    
    with open('master_resume.json', 'r') as f:
        master_data = json.load(f)
    
    # We tell the AI EXACTLY what keys to use for Experience entries
    prompt = (
        f"Context: Recruiter for {company}. JD: {jd_text}\n"
        f"Task: Select the most relevant experience entries from the Master JSON.\n"
        f"IMPORTANT: Each experience entry MUST have: 'company', 'position', 'location', 'start_date', and 'highlights' (a list of strings).\n"
        f"Return ONLY a JSON with a 'sections' key containing 'experience'.\n"
        f"Master Data: {json.dumps(master_data)}"
    )

    try:
        response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        raw_text = response.text.strip()
        if "```json" in raw_text:
            raw_text = raw_text.split("```json")[1].split("```")[0].strip()
        tailored_content = json.loads(raw_text)
        
        # Pull sections from AI response
        sections = tailored_content.get("sections", tailored_content)

        # FINAL SCHEMA WRAPPER
        final_data = {
            "cv": {
                "name": "Brian Walzer",
                "location": "Arlington, VA",
                "email": "bwalzer@example.com",
                "sections": sections
            },
            "design": {
                "theme": "classic",
                "font": "Latin Modern",
                "page_size": "us-letter"
            }
        }
        
        # Notice we removed the 'settings' block that points to theme.yaml
        # and replaced it with a 'design' block directly in the JSON.
        # This removes the need for the external theme.yaml file!

        temp_path = f"outputs/{company.replace(' ', '_')}_tailored.json"
        with open(temp_path, 'w') as f:
            json.dump(final_data, f, indent=4)
        return temp_path
        
    except Exception as e:
        print(f"❌ AI/JSON Error: {e}")
        return None

def render_pdf(json_path):
    if not json_path: return
    print(f"--- Rendering PDF for {json_path} ---")
    # No --design flag needed because it's now inside the JSON!
    subprocess.run(["rendercv", "render", json_path], check=True)True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--company', required=True)
    parser.add_argument('--jd', required=True)
    args = parser.parse_args()
    
    tailored_file = get_tailored_json(args.company, args.jd)
    if tailored_file:
        render_pdf(tailored_file)
