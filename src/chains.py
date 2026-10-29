from langchain_openai import ChatOpenAI
from src.config import OPENAI_API_KEY, DEFAULT_MODEL, DEFAULT_TEMPERATURE
from src.prompts import ASSESSMENT_CHAT_TEMPLATE

# Safe import for LLMChain across LangChain versions
try:
    from langchain.chains import LLMChain
except ImportError:
    try:
        from langchain_community.chains import LLMChain
    except ImportError:
        # Fallback implementation if LLMChain is deprecated in newer versions
        class LLMChain:
            def __init__(self, llm, prompt):
                self.llm = llm
                self.prompt = prompt
            def run(self, inputs):
                messages = self.prompt.format_messages(**inputs)
                response = self.llm.invoke(messages)
                return response.content

def get_llm_model(temperature: float = DEFAULT_TEMPERATURE, streaming: bool = False):
    """Initializes and returns the ChatOpenAI model instance."""
    if not OPENAI_API_KEY:
        raise ValueError("OpenAI API key is missing. Please check your .env file.")
    
    return ChatOpenAI(
        model=DEFAULT_MODEL,
        temperature=temperature,
        openai_api_key=OPENAI_API_KEY,
        streaming=streaming
    )

def create_assessment_chain():
    """
    Creates and returns a reusable LLMChain using ChatOpenAI 
    and our ChatPromptTemplate.
    """
    llm = get_llm_model(streaming=True)
    
    chain = LLMChain(
        llm=llm,
        prompt=ASSESSMENT_CHAT_TEMPLATE
    )
    return chain

def stream_narrative(inputs: dict):
    """
    Streams the LLM response chunks live using .stream() 
    for natural typing effect in Streamlit.
    """
    llm = get_llm_model(streaming=True)
    messages = ASSESSMENT_CHAT_TEMPLATE.format_messages(**inputs)
    
    for chunk in llm.stream(messages):
        if chunk.content:
            yield chunk.content