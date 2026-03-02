import json
import os
import argparse
import google.generativeai as genai

# Configure AI
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

def tailor_resume(company, jd_text):
    # 1. Load your Master Data 
    with open('master_resume.json', 'r') as f:
        master_data = json.load(f)
    
    # 2. Build the Selection Prompt
    prompt = f"""
    Acting as a recruiter for {company}, analyze this Job Description:
    {jd_text}
    
    From the provided Master Resume JSON, select the most impactful 6 bullets and 12 skills.
    Focus on achievements like {master_data['experience'][0]['bullets'][1]['text'][:50]}... if relevant. 
    
    Return ONLY the tailored JSON following the master schema.
    
    MASTER DATA:
    {json.dumps(master_data)}
    """
    
    # 3. Generate content
    response = model.generate_content(prompt)
    
    # 4. Clean up the response (remove markdown code blocks if AI adds them)
    cleaned_json = response.text.replace("```json", "").replace("```", "").strip()
    
    # 5. Save to a unique file
    os.makedirs('outputs', exist_ok=True)
    filename = f"outputs/{company.replace(' ', '_')}_Resume.json"
    
    with open(filename, 'w') as f:
        f.write(cleaned_json)
    
    print(f"Successfully saved tailored resume to {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--company', required=True)
    parser.add_argument('--jd', required=True)
    args = parser.parse_args()
    
    tailor_resume(args.company, args.jd)
