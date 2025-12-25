import yaml
import json
import hashlib

PROMPT_VERSION = "v1.1"

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
        prompt = yaml.safe_load(f)["prompt"]

    # Mocked LLM response
    skills = ["python", "analysis", "mentoring"]
    persona = "Mentor Material"

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
        PROMPT_VERSION,
        hash_output(output)
    )
