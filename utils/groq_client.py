import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

def get_llm():
    """
    Initializes and returns the Groq LLM instance using Langchain.
    Must have GROQ_API_KEY set in the environment variables.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "your_groq_api_key":
        raise ValueError("Valid GROQ_API_KEY not found in environment variables. Please update the .env file.")
    
    # Initialize the Groq model
    return ChatGroq(
        api_key=api_key,
        model_name="openai/gpt-oss-20b", 
        temperature=0.7,
        max_tokens=2048
    )
