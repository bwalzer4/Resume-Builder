import json, os, argparse
from jinja2 import Template
from weasyprint import HTML
from google import genai

def get_tailored_resume(company, jd_text):
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    
    with open('master_resume.json', 'r') as f:
        master_data = json.load(f)

    prompt = (
        f"Tailor a resume for {company} using this JD: {jd_text}\n"
        f"Return ONLY a JSON object with these keys: "
        f"'summary' (string), 'experience' (list of objects with company, location, position, start_date, end_date, highlights), "
        f"'skills' (list of objects with label, details).\n"
        f"Master Data: {json.dumps(master_data)}"
    )
    
    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
    raw_json = response.text.strip().replace('```json', '').replace('```', '')
    data = json.loads(raw_json)

    # 1. Prepare Data for Template
    context = {
        "cv": {
            "name": "Ben Walzer",
            "location": "Falls Church, VA",
            "phone": "757-374-1691",
            "email": "benjamin.walzer4@gmail.com"
        },
        "sections": data
    }

    # 2. Render HTML
    with open('resume_template.html', 'r') as f:
        template = Template(f.read())
    html_out = template.render(context)

    # 3. Create PDF
    os.makedirs('outputs', exist_ok=True)
    output_filename = f"outputs/{company.replace(' ', '_')}_Resume.pdf"
    HTML(string=html_out).write_pdf(output_filename)
    print(f"✅ Success! PDF created at {output_filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--company', required=True)
    parser.add_argument('--jd', required=True)
    args = parser.parse_args()
    get_tailored_resume(args.company, args.jd)
