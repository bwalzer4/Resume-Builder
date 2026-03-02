import json
import os
import argparse
import subprocess
from google import genai  # Use the modern SDK

# Stage 1: The AI Selector
def get_tailored_json(company, jd_text):
    # The client automatically picks up GEMINI_API_KEY from the environment
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    tailored_data = None
    
    with open('master_resume.json', 'r') as f:
        master_data = json.load(f)
    
    prompt = (
        f"You are a recruiter for {company}. Use this Job Description: \n\n{jd_text}\n\n"
        f"Filter the following Master Resume JSON to pick the top 6 most relevant bullets "
        f"and top 12 skills. Return ONLY the valid JSON, keeping the exact same structure.\n\n"
        f"MASTER DATA: {json.dumps(master_data)}"
    )
    
    try:
        # Modern syntax for content generation
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        
        # Strip potential markdown backticks from AI response
        raw_text = response.text.strip()
        if raw_text.startswith("```json"):
            raw_text = raw_text.replace("```json", "", 1).rsplit("```", 1)[0].strip()
        elif raw_text.startswith("```"):
            raw_text = raw_text.replace("```", "", 1).rsplit("```", 1)[0].strip()

        # Save the tailored JSON
        os.makedirs('outputs', exist_ok=True)
        temp_path = f"outputs/{company.replace(' ', '_')}_tailored.json"

        if os.path.exists(temp_path):
            print(f"✅ Success: {temp_path} created.")
        else:
            print(f"❌ Error: {temp_path} was NOT created.")
        
        # Validate that the response is actual JSON before saving
        tailored_data = json.loads(raw_text)
        # 1. Ensure 'cv' is the top-level container
        # If the AI didn't wrap it in 'cv', we do it manually
        if "cv" in tailored_data:
            final_data = tailored_data
        else:
            final_data = {"cv": tailored_data}

        # 2. Inject your Personal Info (AI often forgets this part)
        # Pull this from your master_resume.json or hardcode it
        final_data["cv"]["name"] = "Your Full Name"
        final_data["cv"]["location"] = "Your City, State"
        final_data["cv"]["email"] = "your.email@example.com"
                
        # Inject the settings RenderCV is looking for
        final_data["settings"] = {
            "render_command": {
                "design": "theme.yaml"
            }
        }
        
        # Save the modified JSON
        with open(temp_path, 'w') as f:
            json.dump(final_data, f, indent=4)
            
        return temp_path
        
    except Exception as e:
        print(f"Error during AI generation: {e}")
        return None

# Stage 2: The LaTeX Renderer
def render_pdf(json_path):
    if not json_path: return
    # Get the absolute path to the directory where THIS script lives
    current_dir = os.path.dirname(os.path.abspath(__file__))
    theme_path = os.path.join(current_dir, "theme.yaml")
    
    print(f"--- Printing PDF using theme at {theme_path} ---")
    
    # Pass the full path to ensure RenderCV finds it
    subprocess.run([
        "rendercv", "render", json_path, 
        "--design", theme_path
    ], check=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--company', required=True)
    parser.add_argument('--jd', required=True)
    args = parser.parse_args()
    
    tailored_file = get_tailored_json(args.company, args.jd)
    if tailored_file:
        render_pdf(tailored_file)
