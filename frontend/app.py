import streamlit as st
import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# API configuration
API_BASE_URL = "http://localhost:8000/api"  # Update this if your API is hosted elsewhere

# Set page config
st.set_page_config(
    page_title="FAQ System",
    page_icon="❓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
        padding: 1rem;
    }
    .stButton>button {
        width: 100%;
    }
    .question-card {
        padding: 1.5rem;
        margin-bottom: 1rem;
        border-radius: 0.5rem;
        background-color: #f8f9fa;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .question-card h3 {
        margin-top: 0;
        color: #1e88e5;
    }
    .category-tag {
        display: inline-block;
        background-color: #e3f2fd;
        color: #1565c0;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.875rem;
        margin-bottom: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

def fetch_categories():
    """Fetch all FAQ categories from the API."""
    try:
        response = requests.get(f"{API_BASE_URL}/categories/")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching categories: {e}")
        return []

def fetch_questions(category_id=None, search_query=None):
    """Fetch FAQ questions, optionally filtered by category or search query."""
    try:
        params = {}
        if category_id:
            params['category_id'] = category_id
        
        response = requests.get(f"{API_BASE_URL}/questions/", params=params)
        response.raise_for_status()
        questions = response.json()['results']
        
        # Apply search filter if provided
        if search_query:
            search_query = search_query.lower()
            questions = [
                q for q in questions 
                if (search_query in q['question'].lower() or 
                     search_query in q['answer'].lower())
            ]
            
        return questions
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching questions: {e}")
        return []

def translate_text(text, target_lang):
    """Translate text to the target language using the API."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/translate/",
            json={
                'text': text,
                'target_lang': target_lang,
                'source_lang': 'en'
            }
        )
        response.raise_for_status()
        return response.json()['translated_text']
    except requests.exceptions.RequestException as e:
        st.error(f"Translation error: {e}")
        return text

def main():
    """Main Streamlit application."""
    st.title("FAQ System")
    st.write("Browse frequently asked questions and get answers in multiple languages.")
    
    # Sidebar for filters
    with st.sidebar:
        st.header("Filters")
        
        # Language selection
        languages = {
            'English': 'en',
            'Spanish': 'es',
            'French': 'fr',
            'German': 'de'
        }
        selected_lang_name = st.selectbox(
            "Select Language",
            options=list(languages.keys()),
            index=0
        )
        selected_lang = languages[selected_lang_name]
        
        # Category filter
        categories = fetch_categories()
        category_options = ["All Categories"] + [cat['name'] for cat in categories]
        selected_category = st.selectbox("Filter by Category", category_options)
        
        # Search
        search_query = st.text_input("Search questions")
        
        # Add a new question (admin feature)
        st.markdown("---")
        st.subheader("Add New Question")
        
        with st.form("new_question_form"):
            new_question = st.text_area("Question")
            new_answer = st.text_area("Answer")
            new_category = st.selectbox(
                "Category",
                [cat['name'] for cat in categories]
            )
            
            submitted = st.form_submit_button("Submit Question")
            if submitted:
                if new_question and new_answer and new_category:
                    category_id = next(
                        cat['id'] for cat in categories 
                        if cat['name'] == new_category
                    )
                    try:
                        response = requests.post(
                            f"{API_BASE_URL}/questions/",
                            json={
                                'question': new_question,
                                'answer': new_answer,
                                'category': category_id
                            }
                        )
                        response.raise_for_status()
                        st.success("Question added successfully!")
                    except requests.exceptions.RequestException as e:
                        st.error(f"Error adding question: {e}")
    
    # Main content area
    st.header("Frequently Asked Questions")
    
    # Get selected category ID
    category_id = None
    if selected_category != "All Categories":
        category_id = next(
            cat['id'] for cat in categories 
            if cat['name'] == selected_category
        )
    
    # Fetch and display questions
    questions = fetch_questions(category_id, search_query)
    
    if not questions:
        st.info("No questions found matching your criteria.")
    else:
        for question in questions:
            with st.container():
                st.markdown(f"""
                    <div class="question-card">
                        <span class="category-tag">{question['category_name']}</span>
                        <h3>{question['question']}</h3>
                        <p>{question['answer']}</p>
                        <p><small>👁️ {question['views']} views</small></p>
                    </div>
                """, unsafe_allow_html=True)
                
                # Translation button
                if selected_lang != 'en':
                    if st.button(f"Translate to {selected_lang_name}", 
                               key=f"translate_{question['id']}"):
                        with st.spinner(f"Translating to {selected_lang_name}..."):
                            translated_q = translate_text(question['question'], selected_lang)
                            translated_a = translate_text(question['answer'], selected_lang)
                            
                            st.markdown(f"""
                                <div class="question-card" style="background-color: #f0f7ff;">
                                    <h3>{translated_q}</h3>
                                    <p>{translated_a}</p>
                                </div>
                            """, unsafe_allow_html=True)
                
                st.markdown("---")

if __name__ == "__main__":
    main()
