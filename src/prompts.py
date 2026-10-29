# Safe imports for prompts across different LangChain versions
try:
    from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
except ImportError:
    from langchain.prompts import PromptTemplate, ChatPromptTemplate

try:
    from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
except ImportError:
    from langchain.schema import SystemMessage, HumanMessage, AIMessage

# 1. System safety guidelines and role definition
SYSTEM_SAFETY_PROMPT = """You are MediGuide AI, an educational AI prototype designed to provide preliminary medical symptom assessment and patient guidance.

CRITICAL SAFETY RULES:
1. You are NOT a licensed doctor, professional diagnosis tool, or emergency service.
2. Never present a confirmed diagnosis. Always frame conditions as educational possibilities.
3. Every assessment must clearly state safety disclaimers.
4. If symptoms indicate severe distress (e.g., severe chest pain, extreme shortness of breath, heavy bleeding), set the urgency_level to "EMERGENCY" and explicitly instruct the user to seek immediate emergency help.
5. Respond strictly in valid JSON format matching the requested schema without any markdown formatting or code blocks around it.
6. The entire response must be written in the specified target language: {language}.
"""

# 2. Human template containing patient inputs
PATIENT_INPUT_PROMPT = """Please analyze the following patient details and symptoms:
- Age: {age}
- Gender: {gender}
- Symptoms: {symptoms}
- Duration: {duration}
- Severity Level (1-10): {severity}
- Existing Medical Conditions: {existing_conditions}
- Current Medications: {current_medications}
- Additional Notes: {notes}
- Target Language: {language}

Provide your assessment as a strict JSON object with the following keys:
- "summary": A brief clinical summary of the patient's presentation.
- "possible_conditions": A list of objects, each containing "name" (educational condition name) and "reason" (why it matches).
- "urgency_level": Must be exactly one of: "LOW", "MEDIUM", "HIGH", "EMERGENCY".
- "recommended_next_steps": Clear steps the patient should take.
- "questions_for_doctor": A list of questions the patient should ask their healthcare professional.
- "warning_signs": A list of critical red-flag warning signs that require immediate escalation.
"""

# 3. Reusable ChatPromptTemplate for the LLM chain
ASSESSMENT_CHAT_TEMPLATE = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_SAFETY_PROMPT),
    ("human", PATIENT_INPUT_PROMPT)
])

# 4. Reusable single-string PromptTemplate (as required by assignment milestones)
ASSESSMENT_PROMPT_TEMPLATE = PromptTemplate(
    template=SYSTEM_SAFETY_PROMPT + "\n\n" + PATIENT_INPUT_PROMPT,
    input_variables=[
        "age", "gender", "symptoms", "duration", "severity",
        "existing_conditions", "current_medications", "notes", "language"
    ]
)

# 5. Demo function for raw System/Human/AI message interaction
def get_raw_chat_messages(inputs: dict) -> list:
    """Demonstrates raw SystemMessage, HumanMessage, and AIMessage usage."""
    sys_msg = SystemMessage(content=SYSTEM_SAFETY_PROMPT.format(language=inputs.get("language", "English")))
    human_msg = HumanMessage(content=PATIENT_INPUT_PROMPT.format(**inputs))
    ai_demo_msg = AIMessage(content="[Demo AI Message initialized for conversation flow check]")
    return [sys_msg, human_msg, ai_demo_msg]