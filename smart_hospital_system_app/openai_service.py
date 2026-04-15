import json
import requests
from django.conf import settings
print("openai_service loaded")

def ask_hospital_assistant(user_message, conversation_history=None):
    print("ask_hospital_assistant called")
    if conversation_history is None:
        conversation_history = []

    system_prompt = """
You are a hospital booking assistant.

Rules:
- Ask short and clear follow-up questions.
- Do not provide a medical diagnosis.
- If symptoms seem dangerous or urgent, tell the patient to seek urgent medical care.
- Your goal is to collect enough information to recommend the most suitable doctor specialty.
- Return ONLY valid JSON.
- Do not return markdown.
- Do not return explanation outside JSON.
- Your response must be a single JSON object.

The JSON must contain exactly these keys:
reply_for_patient
enough_information
recommended_specialty
keywords
urgency

Example:
{
  "reply_for_patient": "How long have you had these symptoms?",
  "enough_information": false,
  "recommended_specialty": "",
  "keywords": [],
  "urgency": "normal"
}
"""

    messages = [
        {"role": "system", "content": system_prompt}
    ]

    for msg in conversation_history:
        messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })

    messages.append({
        "role": "user",
        "content": user_message
    })

    headers = {
        "Authorization": "Bearer {}".format(settings.OPENAI_API_KEY),
        "Content-Type": "application/json",
    }

    payload = {
        "model": "gpt-4.1-mini",
        "messages": messages,
        "response_format": {"type": "json_object"},
        "temperature": 0.2,
        "max_tokens": 300
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=60
    )

    response.raise_for_status()
    data = response.json()

    content = data["choices"][0]["message"]["content"]
    print("RAW AI CONTENT:", content)

    try:
        parsed = json.loads(content)
    except Exception:
        parsed = {
            "reply_for_patient": "Sorry, I had trouble understanding that. Could you describe your symptoms again in a short sentence?",
            "enough_information": False,
            "recommended_specialty": "",
            "keywords": [],
            "urgency": "normal"
        }

    return parsed