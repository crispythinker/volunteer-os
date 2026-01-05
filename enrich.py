import os
import json
import yaml
import hashlib
import google.generativeai as genai

# Configure Gemini from ENV
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY not set")

genai.configure(api_key=api_key)

PROMPT_VERSION = "v2.0"
MODEL_VERSION = "gemini-1.5-flash"

def compute_confidence(skills, bio):
    score = 0.4
    if len(skills) >= 3:
        score += 0.3
    if len(str(bio).split()) > 30:
        score += 0.2
    return round(min(score, 1.0), 2)

def hash_output(obj):
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True).encode()
    ).hexdigest()

def enrich_bio(bio):
    with open("prompts.yaml") as f:
        prompt_template = yaml.safe_load(f)["prompt"]

    prompt = prompt_template.replace("{{bio}}", str(bio))

    model = genai.GenerativeModel(MODEL_VERSION)
    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0,
            "response_mime_type": "application/json"
        }
    )

    parsed = json.loads(response.text)

    skills = parsed.get("skills", [])
    persona = parsed.get("persona", "Uncertain")

    confidence = compute_confidence(skills, bio)
    if confidence < 0.6:
        persona = "Uncertain"

    output = {
        "skills": skills,
        "persona": persona,
        "confidence": confidence
    }

    return (
        skills,
        persona,
        confidence,
        MODEL_VERSION,
        PROMPT_VERSION,
        hash_output(output)
    )
