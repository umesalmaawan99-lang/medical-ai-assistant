import json
import re

def parse_llm_json(raw_output: str) -> dict:
    """
    Safely parses JSON output from the LLM, stripping markdown fences 
    or extra text if present. Never lets bad JSON crash the app.
    """
    cleaned_output = raw_output.strip()
    
    # Remove markdown code blocks if the model wrapped the JSON in ```json ... ```
    if cleaned_output.startswith("```"):
        cleaned_output = re.sub(r"^```(?:json)?\s*", "", cleaned_output)
        cleaned_output = re.sub(r"\s*```$", "", cleaned_output)
        cleaned_output = cleaned_output.strip()
        
    try:
        parsed_data = json.loads(cleaned_output)
        return parsed_data
    except json.JSONDecodeError as e:
        # Fallback dictionary if JSON parsing fails
        return {
            "summary": "Error parsing JSON response from AI model.",
            "possible_conditions": [{"name": "Parsing Error", "reason": str(e)}],
            "urgency_level": "LOW",
            "recommended_next_steps": "Please try submitting the form again.",
            "questions_for_doctor": [],
            "warning_signs": ["Raw output for debugging:\n" + raw_output]
        }

def get_urgency_color(urgency: str) -> str:
    """Returns color-coded badges for streamlit display based on urgency level."""
    urgency_upper = urgency.upper().strip()
    if "EMERGENCY" in urgency_upper:
        return "🔴 EMERGENCY"
    elif "HIGH" in urgency_upper:
        return "🟠 HIGH"
    elif "MEDIUM" in urgency_upper:
        return "🟡 MEDIUM"
    else:
        return "🟢 LOW"