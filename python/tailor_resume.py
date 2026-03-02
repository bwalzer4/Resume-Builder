import json
import os
import google.generativeai as genai

# Setup API Key (Stored in GitHub Secrets for security)
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def tailor_resume(job_description_text):
    master_data = load_json('master_resume.json')
    
    prompt = f"""
    You are an expert technical recruiter. I will provide a Job Description and my Master Resume JSON.
    
    TASK:
    1. Select the 6 most relevant bullet points from the 'experience' section that match the JD.
    2. Select the top 12 most relevant skills.
    3. Rewrite the 'profile' text to align with the specific goals of this role while remaining truthful.
    4. Maintain the EXACT same JSON structure as the master file.

    JOB DESCRIPTION:
    {job_description_text}

    MASTER RESUME DATA:
    {json.dumps(master_data)}
    
    RETURN ONLY THE NEW TAILORED JSON.
    """
    
    response = model.generate_content(prompt)
    
    # Save the tailored version
    with open('tailored_resume.json', 'w') as f:
        f.write(response.text)
    print("Tailored resume JSON generated successfully!")

if __name__ == "__main__":
    # In a real workflow, this JD would be passed as a command-line argument
    jd_input = input("Paste the Job Description here: ")
    tailor_resume(jd_input)
