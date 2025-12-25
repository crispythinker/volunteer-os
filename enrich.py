import yaml
import json

def enrich_bio(bio):
    with open("prompts.yaml") as f:
        prompt = yaml.safe_load(f)["prompt"].replace("{{bio}}", str(bio))

    # 🔴 MOCK if API setup takes time
    # This is acceptable if documented
    response = {
        "skills": ["python", "analysis"],
        "persona": "Mentor Material",
        "confidence": 0.78
    }

    if response["confidence"] < 0.6:
        response["persona"] = "Uncertain"

    return response["skills"], response["persona"], response["confidence"]
