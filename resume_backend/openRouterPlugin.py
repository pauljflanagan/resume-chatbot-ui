import requests
import json
from pypdf import PdfReader
import os

# Replace with your actual API key from https://openrouter.ai
API_KEY = os.get("OPENROUTER_API_KEY")

# Endpoint for OpenRouter completions
url = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}


def read_resume_pdf(pdf_path):
    """Extract text content from the resume PDF"""
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text.strip()


def read_json_format(json_path):
    """Read the JSON format template"""
    with open(json_path, "r") as file:
        return json.load(file)


# Read the resume content and format template
# resume_content = read_resume_pdf("../Resume_Paul_Flanagan.pdf")
json_format = read_json_format("resume.json")

# Example request body
data = {
    "model": "openai/gpt-4",  # You can choose other models listed on OpenRouter
    "messages": [
        {
            "role": "system",
            "content": f"""You are Paul Flanagan, a fullstack software engineer, whose professional experience and skills center around fullstack software development, cloud computing, and AI integration.
            
            All professional information can be found here:
            {json_format}

            Respond to all user questions using only the information provided in this JSON structure, analyzing the data and providing the best answer in a conversational format in full, complete sentences. 
            Do not fabricate or assume any details beyond what is explicitly stated in the JSON. If you are asked any questions
            that are not related to software engineering, fullstack development, cloud computing, or AI integration, politely inform the user that you can only provide information related to your professional expertise as outlined in the JSON.
            
            Responses should be concise, conversational, and professional. Although you have access to detailed information, avoid overwhelming the user with excessive detail unless specifically requested.
            """,
        },
    ],
}

response = requests.post(url, headers=headers, json=data)

if response.status_code == 200:
    result = response.json()
    # Extract the assistant's reply
    print(result["choices"][0]["message"]["content"])
else:
    print("Error:", response.status_code, response.text)
