# 🩺 MediGuide AI: AI-Powered Medical Symptom Assessment and Patient Guidance Assistant

An intelligent Streamlit application built with LangChain and OpenAI (`gpt-4o-mini`) that accepts basic patient information and symptoms to generate structured, safety-focused preliminary guidance[cite: 2].

> **⚠️ IMPORTANT MEDICAL & SAFETY NOTICE:** 
> MediGuide AI is an educational AI prototype only. It is **NOT** a replacement for a licensed doctor, professional diagnosis, emergency service, or medical treatment. It never presents a confirmed diagnosis. All screens direct users to consult a qualified healthcare professional and seek emergency help in urgent situations[cite: 1].

---

## 🚀 Features & Architecture
- **LangChain Integration:** Utilizes `ChatOpenAI`, `ChatPromptTemplate`, `PromptTemplate`, and custom message objects.
- **Structured JSON Output:** Forces the model to return valid JSON schemas parsed safely without crashing the app[cite: 3, 6].
- **Live Streaming Output:** Streams AI guidance responses in real-time using `.stream()` and `st.write_stream()`[cite: 3, 6].
- **Dual Caching System:** Supports both **`InMemoryCache`** (RAM-based, fastest) and **`SQLiteCache`** (disk-based, persists across sessions)[cite: 3, 5, 6].
- **Multi-Language Support:** Generate guidance in English, Urdu, Spanish, French, Arabic, and Hindi[cite: 6].

---

## 📁 Project Structure
```text
medical_ai_assistant/
│
├── .env                  # Environment variables (API Key)
├── .env.example          # Environment variables template
├── .gitignore            # Ignored files (venv, .env, cache db)
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
├── app.py                # Main Streamlit UI entry point
│
└── src/
    ├── __init__.py         # Package initialization
    ├── config.py           # Settings and form dropdown options
    ├── prompts.py          # Safety system prompts, templates & schema
    ├── chains.py           # ChatOpenAI, LLMChain & streaming logic
    ├── cache_manager.py    # InMemoryCache & SQLiteCache configuration
    └── utils.py            # Safe JSON parsing & UI helper functions