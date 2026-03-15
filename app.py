import streamlit as st
from chains.recipe_chain import generate_recipe
from utils.pdf_generator import create_recipe_pdf
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Page Configuration
st.set_page_config(
    page_title="SmartChef AI – Intelligent Recipe Generator",
    page_icon="👨‍🍳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Premium Modern UI
def load_css():
    st.markdown("""
    <style>
    /* Background & Global Font */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: #f8fafc;
        font-family: 'Outfit', sans-serif;
    }
    
    /* Hide top header bar & footer */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Typography Overrides */
    h1, h2, h3, h4, h5, h6, .st-markdown {
        color: #ffffff !important;
        font-family: 'Outfit', sans-serif !important;
    }
    
    .hero-title {
        text-align: center; 
        font-weight: 700;
        font-size: 3.5rem !important;
        background: -webkit-linear-gradient(45deg, #FF6B6B, #FF8E53);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
        letter-spacing: -1px;
    }
    
    .hero-subtitle {
        text-align: center;
        color: #94a3b8 !important;
        font-size: 1.2rem;
        font-weight: 300;
        margin-bottom: 2rem;
    }
    
    /* Glassmorphic Container styling */
    .glass-container {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 24px;
        padding: 2rem;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    }
    
    /* Inputs */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div, .stNumberInput>div>div>input {
        background: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(148, 163, 184, 0.2) !important;
        color: #f8fafc !important;
        border-radius: 12px !important;
        padding: 0.75rem 1rem !important;
        transition: all 0.3s ease;
        font-size: 1rem;
    }
    
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #FF6B6B !important;
        box-shadow: 0 0 0 2px rgba(255, 107, 107, 0.2) !important;
        background: rgba(15, 23, 42, 0.8) !important;
    }
    
    /* Primary Gradient Button */
    .stButton>button {
        background: linear-gradient(135deg, #FF416C, #FF4B2B) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        letter-spacing: 0.5px;
        padding: 0.75rem 2rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        width: 100%;
        margin-top: 1rem;
        box-shadow: 0 4px 15px rgba(255, 75, 43, 0.3) !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(255, 75, 43, 0.5) !important;
        background: linear-gradient(135deg, #FF4B2B, #FF416C) !important;
    }
    
    /* Download Button override */
    .stDownloadButton>button {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px);
        box-shadow: none !important;
    }
    
    .stDownloadButton>button:hover {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: rgba(0,0,0,0.2);
        padding: 0.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        border: none;
        color: #94a3b8;
        font-weight: 600;
        transition: all 0.3s;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #f8fafc;
        background: rgba(255,255,255,0.05);
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: rgba(255, 255, 255, 0.1);
        color: #ffffff;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.03) !important;
        border-radius: 16px !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        padding: 1rem !important;
    }
    .streamlit-expanderHeader p {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        color: #FF8E53 !important;
    }
    .streamlit-expanderContent {
        background: rgba(15, 23, 42, 0.4) !important;
        border-radius: 0 0 16px 16px !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-top: none !important;
        padding: 1.5rem !important;
    }
    
    /* Recipe Display Area */
    .recipe-content {
        line-height: 1.8;
        font-size: 1.05rem;
        color: #e2e8f0;
    }
    .recipe-content h1, .recipe-content h2, .recipe-content h3 {
        color: #FF8E53 !important;
        margin-top: 1.5rem;
    }
    .recipe-content ul, .recipe-content ol {
        margin-left: 1.5rem;
    }
    .recipe-content li {
        margin-bottom: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

load_css()

# Hero Section
st.markdown("<h1 class='hero-title'>👨‍🍳 SmartChef AI</h1>", unsafe_allow_html=True)
st.markdown("<p class='hero-subtitle'>Your intelligent culinary assistant for personalized, chef-crafted recipes</p>", unsafe_allow_html=True)

# Layout Container
main_col1, main_col2, main_col3 = st.columns([1, 8, 1])

with main_col2:
    st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["🍽️ Dish Name", "🥦 Ingredients"])

    with tab1:
        st.markdown("### 🍳 What are you craving?")
        dish_name = st.text_input("", placeholder="e.g., Authentic Spicy Rigatoni...")
        
        col1, col2 = st.columns(2)
        with col1:
            cuisine_type = st.selectbox("Cuisine Origin", ["Any", "Italian", "Indian", "Mexican", "Japanese", "French", "Thai", "American"], key="cuisine_dish")
        with col2:
            difficulty_level = st.selectbox("Complexity", ["Any", "Beginner", "Intermediate", "Master Chef"], key="diff_dish")
        
        if st.button("✨ Generate Culinary Masterpiece", key="btn_dish"):
            if dish_name.strip() == "":
                st.warning("Please enter a dish name to begin.")
            else:
                progress_text = "Chef is heating up the pans..."
                my_bar = st.progress(0, text=progress_text)
                
                try:
                    for percent_complete in range(50):
                        time.sleep(0.02)
                        my_bar.progress(percent_complete + 1, text=progress_text)
                        
                    recipe = generate_recipe(
                        dish_name=dish_name,
                        cuisine_type=cuisine_type,
                        difficulty_level=difficulty_level
                    )
                    
                    for percent_complete in range(50, 100):
                        time.sleep(0.01)
                        my_bar.progress(percent_complete + 1, text="Plating the dish...")
                        
                    time.sleep(0.5)
                    my_bar.empty()
                    st.toast('Recipe ready! Bon Appétit!', icon='🎉')
                    
                    st.markdown(f"### Here is your {dish_name} recipe:")
                    with st.expander("📖 View Full Recipe & Instructions", expanded=True):
                        st.markdown(f"<div class='recipe-content'>{recipe}</div>", unsafe_allow_html=True)
                    
                    # Download Action Buttons
                    dl_col1, dl_col2 = st.columns(2)
                    with dl_col1:
                        st.download_button(
                            label="📄 Download as Text",
                            data=recipe,
                            file_name=f"{dish_name.replace(' ', '_')}_recipe.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
                    with dl_col2:
                        try:
                            pdf_bytes = create_recipe_pdf(recipe, dish_name)
                            st.download_button(
                                label="📥 Download as PDF",
                                data=pdf_bytes.getvalue(),
                                file_name=f"{dish_name.replace(' ', '_')}_recipe.pdf",
                                mime="application/pdf",
                                use_container_width=True
                            )
                        except Exception as pdf_err:
                            st.error(f"Failed to generate PDF: {pdf_err}")
                            
                except ValueError as ve:
                    my_bar.empty()
                    st.error(str(ve))
                except Exception as e:
                    my_bar.empty()
                    st.error(f"Error generating recipe.\nDetails: {e}")

    with tab2:
        st.markdown("### 🛒 What's in your fridge?")
        ingredients = st.text_area("", placeholder="Enter your ingredients separated by commas (e.g., chicken breast, garlic, heavy cream, parmesan)...", height=120)
        
        col1, col2 = st.columns(2)
        with col1:
            dietary_preference = st.selectbox("Dietary Needs", ["Any", "Vegetarian", "Vegan", "Gluten-Free", "Keto", "Paleo"], key="diet_ing")
        with col2:
            cooking_time_limit = st.select_slider(
                "Max Cooking Time",
                options=[15, 30, 45, 60, 90, 120, 180],
                value=45,
                format_func=lambda x: f"{x} mins" if x < 120 else f"{x//60} hrs"
            )
        
        if st.button("💡 Inspire Me", key="btn_ingredients"):
            if ingredients.strip() == "":
                st.warning("Please tell me what ingredients you have.")
            else:
                progress_text = "Chef is analyzing your ingredients..."
                my_bar = st.progress(0, text=progress_text)
                
                try:
                    for percent_complete in range(50):
                        time.sleep(0.02)
                        my_bar.progress(percent_complete + 1, text=progress_text)
                    
                    recipe = generate_recipe(
                        ingredients=ingredients,
                        dietary_preference=dietary_preference,
                        cooking_time_limit=str(cooking_time_limit)
                    )
                    
                    for percent_complete in range(50, 100):
                        time.sleep(0.01)
                        my_bar.progress(percent_complete + 1, text="Crafting the perfect recipe...")
                        
                    time.sleep(0.5)
                    my_bar.empty()
                    st.toast('Recipe ready! Bon Appétit!', icon='🎉')
                    
                    st.markdown("### Your Custom Ingredient Recipe:")
                    with st.expander("📖 View Full Recipe & Instructions", expanded=True):
                        st.markdown(f"<div class='recipe-content'>{recipe}</div>", unsafe_allow_html=True)
                    
                    # Download Action Buttons
                    dl_col1, dl_col2 = st.columns(2)
                    with dl_col1:
                        st.download_button(
                            label="📄 Download as Text",
                            data=recipe,
                            file_name="suggested_recipe.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
                    with dl_col2:
                        try:
                            pdf_bytes = create_recipe_pdf(recipe, "Suggested Recipe")
                            st.download_button(
                                label="📥 Download as PDF",
                                data=pdf_bytes.getvalue(),
                                file_name="suggested_recipe.pdf",
                                mime="application/pdf",
                                use_container_width=True
                            )
                        except Exception as pdf_err:
                            st.error(f"Failed to generate PDF: {pdf_err}")
                            
                except ValueError as ve:
                    my_bar.empty()
                    st.error(str(ve))
                except Exception as e:
                    my_bar.empty()
                    st.error(f"Error generating recipe.\nDetails: {e}")
                    
    st.markdown("</div>", unsafe_allow_html=True)

