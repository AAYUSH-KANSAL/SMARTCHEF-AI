# 👨‍🍳 SmartChef AI

**SmartChef AI** is an intelligent culinary assistant designed to craft personalized, professional-level recipes using LangChain, Groq API, and Streamlit.

## Features

- 🍽️ **Recipe by Dish Name**: Craving something specific? Enter a dish name, select the cuisine, and choose the difficulty level. The AI will provide a highly accurate, step-by-step recipe.
- 🥦 **Recipe from Ingredients**: Not sure what to make? Enter the ingredients you have on hand, specify your dietary needs and available cooking time, and the AI will suggest a creative dish.
- 🎨 **Modern Premium UI**: Experience a sleek, dark-themed glassmorphism interface with smooth animations and layout.
- 📄 **Export Options**: Download your generated recipes as a raw Text file or a clean, highly formatted PDF document!

## Architecture & Tech Stack

- **Streamlit**: Provides the rapid-prototype interactive UI.
- **LangChain**: Orchestrates the LLM prompts and extraction logic using LangChain Expression Language (LCEL).
- **Groq API / OpenAI Compatible**: Utilizes blazingly fast inference to generate results instantly using models like `gpt-oss-20b` or `Llama3` variations.
- **Python-dotenv**: Securely handles environment configurations.
- **ReportLab**: Renders model markdown outputs into reliable PDF exports.

## Installation and Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/AAYUSH-KANSAL/SMARTCHEF-AI.git
   cd SMARTCHEF-AI
   ```

2. **Install dependencies:**
   Make sure you have Python installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Setup:**
   Create a `.env` file in the root directory and add your API Key:
   ```env
   GROQ_API_KEY=your_api_key_here
   ```

4. **Run the Application:**
   ```bash
   streamlit run app.py
   ```

## Folder Structure

```
SMARTCHEF-AI/
│
├── app.py                     # Main Streamlit Application interface
├── requirements.txt           # Python package dependencies
├── .env                       # Environment variables (Ignored by Git)
├── .gitignore                 # Files to ignore in version control
│
├── chains/
│   └── recipe_chain.py        # LangChain LCEL Logic pipeline
│
├── prompts/
│   └── recipe_prompt.py       # Chef persona LangChain PromptTemplate
│
└── utils/
    ├── groq_client.py         # Initialization of LLM connection
    └── pdf_generator.py       # ReportLab engine for rendering PDF exports
```

Enjoy your culinary journey with **SmartChef AI**!
