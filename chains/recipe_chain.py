from utils.groq_client import get_llm
from prompts.recipe_prompt import get_recipe_prompt
from langchain_core.output_parsers import StrOutputParser

def generate_recipe(
    dish_name="Not Specified", 
    ingredients="Not Specified", 
    cuisine_type="Any", 
    difficulty_level="Any", 
    dietary_preference="Any", 
    cooking_time_limit="Any"
):
    """
    Executes the recipe generation chain.
    """
    llm = get_llm()
    prompt = get_recipe_prompt()
    
    # LangChain Expression Language (LCEL) Pipeline
    chain = prompt | llm | StrOutputParser()
    
    return chain.invoke({
        "dish_name": dish_name,
        "ingredients": ingredients,
        "cuisine_type": cuisine_type,
        "difficulty_level": difficulty_level,
        "dietary_preference": dietary_preference,
        "cooking_time_limit": cooking_time_limit
    })
