import streamlit as st
from src.config import (
    GENDER_OPTIONS, SYMPTOM_OPTIONS, DURATION_OPTIONS, LANGUAGE_OPTIONS
)
from src.cache_manager import configure_cache
from src.chains import create_assessment_chain, stream_narrative
from src.utils import parse_llm_json, get_urgency_color

# --- Page Configuration ---
st.set_page_config(
    page_title="MediGuide AI - Symptom Assessment",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Medical Disclaimer Banner ---
st.warning(
    "⚠️ **IMPORTANT MEDICAL & SAFETY NOTICE:** MediGuide AI is an educational AI prototype only. "
    "It is NOT a replacement for a licensed doctor, professional diagnosis, emergency service, or medical treatment. "
    "Never present a confirmed diagnosis. Always consult a qualified healthcare professional and seek emergency help in urgent situations.",
    icon="🚨"
)

# --- Sidebar Configuration ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/stethoscope.png", width=60)
    st.title("MediGuide AI")
    st.markdown("### AI-Powered Medical Symptom Assessment & Patient Guidance Assistant")
    
    st.markdown("---")
    st.markdown("### ⚙️ Settings & Configuration")
    
    # Caching Selection
    cache_choice = st.selectbox(
        "Select Caching Strategy",
        ["InMemory", "SQLite"],
        help="InMemory: Stored in RAM (fastest, clears on restart). SQLite: Stored in local file (persists across sessions)."
    )
    configure_cache(cache_choice)
    
    # Language Selection
    selected_language = st.selectbox(
        "Select Output Language",
        LANGUAGE_OPTIONS,
        index=0,
        help="Select the language for the AI-generated guidance."
    )
    
    st.markdown("---")
    st.markdown("### 🛡️ Safety Reminder")
    st.info(
        "This tool provides educational guidance only and does not diagnose medical conditions."
    )

# --- Main Form Input UI ---
st.title("🩺 Patient Symptom Assessment")
st.markdown("Please fill out the patient information below to receive structured preliminary guidance.")

with st.form("symptom_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.text_input("Patient Age", placeholder="e.g., 30")
        gender = st.selectbox("Gender", GENDER_OPTIONS)
        duration = st.selectbox("Duration of Symptoms", DURATION_OPTIONS)
        severity = st.slider("Severity Level (1 = Mild, 10 = Severe)", 1, 10, 3)
        
    with col2:
        selected_symptoms = st.multiselect("Select Primary Symptoms", SYMPTOM_OPTIONS)
        custom_symptoms = st.text_input("Additional Symptoms (Optional)", placeholder="e.g., mild dizziness")
        
    existing_conditions = st.text_area("Existing Medical Conditions", placeholder="e.g., Asthma, Diabetes, None")
    current_medicines = st.text_area("Current Medications", placeholder="e.g., Inhaler, Aspirin, None")
    additional_notes = st.text_area("Additional Notes / Context", placeholder="e.g., started after workout")
    
    submitted = st.form_submit_button("Analyze Symptoms & Generate Guidance 🚀", type="primary")

# --- Form Submission & Processing ---
if submitted:
    # Validate required inputs
    if not age.strip():
        st.error("Please enter the patient's age.")
    elif not selected_symptoms and not custom_symptoms.strip():
        st.error("Please select at least one symptom or enter custom symptoms.")
    else:
        # Combine symptoms
        all_symptoms_list = selected_symptoms.copy()
        if custom_symptoms.strip():
            all_symptoms_list.append(custom_symptoms.strip())
        symptoms_str = ", ".join(all_symptoms_list)
        
        # Prepare inputs dictionary
        inputs = {
            "age": age,
            "gender": gender,
            "symptoms": symptoms_str,
            "duration": duration,
            "severity": str(severity),
            "existing_conditions": existing_conditions if existing_conditions else "None",
            "current_medicines": current_medicines if current_medicines else "None",
            "notes": additional_notes if additional_notes else "None",
            "language": selected_language
        }
        
        st.markdown("---")
        st.subheader("📋 Assessment Results Dashboard")
        
        # 1. Display Patient Summary
        with st.expander("👤 View Patient Symptom Summary", expanded=True):
            col_a, col_b, col_c = st.columns(3)
            col_a.metric("Age / Gender", f"{age} / {gender}")
            col_b.metric("Severity Level", f"{severity}/10")
            col_c.metric("Duration", duration)
            st.write(f"**Symptoms Reported:** {symptoms_str}")
            st.write(f"**Existing Conditions:** {inputs['existing_conditions']}")
            st.write(f"**Current Medications:** {inputs['current_medicines']}")

        # 2. Run LLM Chain & Parse JSON
        with st.spinner("Analyzing symptoms and compiling guidance..."):
            try:
                chain = create_assessment_chain()
                raw_response = chain.run(inputs)
                parsed_data = parse_llm_json(raw_response)
            except Exception as e:
                parsed_data = {
                    "summary": "An error occurred during analysis.",
                    "possible_conditions": [{"name": "System Error", "reason": str(e)}],
                    "urgency_level": "LOW",
                    "recommended_next_steps": "Please try again.",
                    "questions_for_doctor": [],
                    "warning_signs": []
                }
        
        # 3. Urgency Level Display
        urgency = parsed_data.get("urgency_level", "LOW")
        urgency_badge = get_urgency_color(urgency)
        
        st.markdown(f"### Urgency Assessment: {urgency_badge}")
        
        if "EMERGENCY" in urgency.upper():
            st.error("🚨 **EMERGENCY WARNING:** Critical symptoms detected. Please seek immediate emergency medical help or go to the nearest emergency room!")
        elif "HIGH" in urgency.upper():
            st.warning("⚠️ **HIGH URGENCY:** It is strongly recommended to consult a healthcare professional promptly.")
            
        # 4. Results Tabs Layout
        tab1, tab2, tab3, tab4 = st.tabs(["Overview & Summary", "Possible Conditions", "Next Steps & Questions", "Live Narrative Stream"])
        
        with tab1:
            st.markdown("#### Clinical Summary")
            st.info(parsed_data.get("summary", "No summary provided."))
            
            warning_signs = parsed_data.get("warning_signs", [])
            if warning_signs:
                st.markdown("#### ⚠️ Critical Warning Signs to Watch For")
                for sign in warning_signs:
                    st.error(f"- {sign}")

        with tab2:
            st.markdown("#### Possible Educational Conditions")
            st.caption("For educational purposes only. Not a confirmed medical diagnosis.")
            conditions = parsed_data.get("possible_conditions", [])
            if conditions:
                for cond in conditions:
                    with st.expander(f"📌 {cond.get('name', 'Condition')}"):
                        st.write(f"**Reason / Match:** {cond.get('reason', 'N/A')}")
            else:
                st.write("No specific conditions listed.")

        with tab3:
            st.markdown("#### Recommended Next Steps")
            st.success(parsed_data.get("recommended_next_steps", "Consult a doctor."))
            
            questions = parsed_data.get("questions_for_doctor", [])
            if questions:
                st.markdown("#### 🩺 Questions to Ask Your Doctor")
                for q in questions:
                    st.write(f"- {q}")

        with tab4:
            st.markdown("#### 💬 Live AI Narrative Stream")
            st.caption("Streaming response generated live from ChatOpenAI:")
            try:
                st.write_stream(stream_narrative(inputs))
            except Exception as stream_err:
                st.error(f"Streaming error: {stream_err}")
                
        st.markdown("---")
        st.caption("🩺 Reminder: MediGuide AI is an educational assistant and is not a medical device.")