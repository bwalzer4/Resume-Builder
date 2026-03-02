import json
import os
import argparse
import subprocess
import google.generativeai as genai

# Stage 1: The AI Selector
def get_tailored_json(company, jd_text):
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    with open('master_resume.json', 'r') as f:
        master_data = json.load(f)
    
    prompt = f"Act as a recruiter for {company}. Use this JD: {jd_text} to filter this Master JSON: {json.dumps(master_data)}. Return ONLY a valid JSON with the top 6 relevant bullets and 12 skills. Keep the exact same structure."
    
    response = model.generate_content(prompt)
    # Clean AI output and save to temp file
    temp_path = f"outputs/{company}_tailored.json"
    os.makedirs('outputs', exist_ok=True)
    with open(temp_path, 'w') as f:
        f.write(response.text.replace("```json", "").replace("```", "").strip())
    return temp_path

# Stage 2: The LaTeX Renderer
def render_pdf(json_path):
    print(f"--- Printing PDF from {json_path} ---")
    # RenderCV is a CLI tool, so we call it via subprocess
    subprocess.run(["rendercv", "render", json_path, "--design", "theme.yaml"], check=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--company', required=True)
    parser.add_argument('--jd', required=True)
    args = parser.parse_args()
    
    tailored_file = get_tailored_json(args.company, args.jd)
    render_pdf(tailored_file)
