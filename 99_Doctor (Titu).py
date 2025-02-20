import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

# Configuration variables
sr_no = 100
model_name="Doctor (Titu)"
system_prompt ='"You are Dr. Titu, a highly skilled and compassionate doctor. You diagnose illnesses, provide medical advice, and recommend treatments with professionalism and clarity. Stay in character as a doctor at all times, using precise medical terminology and a caring bedside manner. Keep responses concise, accurate, and focused on patient well-being."'
top_p_value = 0.9
top_k_value = 40
temperature = 0.7
max_tokens = 1000

# Streamlit UI

# Configure Streamlit page
st.set_page_config(page_title=model_name, page_icon=":brain:", layout="centered")

# Sidebar - GitHub, LinkedIn, and Internship Notice
st.sidebar.markdown("### 📂 GitHub Repository")
st.sidebar.markdown("[🔗 View on GitHub](https://github.com/Amanlnctu/your-AI)")

st.sidebar.markdown("### 💼 Linkedin")
st.sidebar.markdown("[🔗connect on  LinkedIn](https://www.linkedin.com/in/amankahar/)")

st.sidebar.markdown("---")  # Divider for spacing

st.sidebar.markdown("## 👨‍💻 Looking for an Internship!")
st.sidebar.write("I'm actively seeking an internship in software development, or related fields. Open to learning and contributing to exciting projects!")

st.sidebar.markdown("---")


st.sidebar.markdown("💡 *Let's collaborate and build something amazing!*")



# Get API Key
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

# Check if API Key exists
if not GOOGLE_API_KEY:
    st.error("⚠️ Google API Key is missing. Please set GEMINI_API_KEY in .env")
    st.stop()

# Initialize Gemini API
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

# Function to initialize chat history (without displaying system prompt)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # Keep system prompt hidden

# Display chatbot title
st.title(model_name)

# Display chat history (excluding system prompt)
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

    # User input
    # User input
user_prompt = st.chat_input("Enter your query here")

if user_prompt:
        # Display user message
    st.chat_message("user",avatar="./images/man.png").markdown(user_prompt)

        # Append user message to history
    st.session_state.chat_history.append(dict(role="user",avatar="./images/man.png",content=user_prompt))

        # Combine system prompt with user query (but don't store system prompt in history)
    full_prompt = system_prompt + user_prompt

        # Define generation config
    generation_config = dict(
        temperature=temperature,
        max_output_tokens=max_tokens,
        top_p=top_p_value,
        top_k=top_k_value,
    )

        # Send message to Gemini AI
    gemini_response = model.generate_content(full_prompt, generation_config=generation_config)

        # Extract response text safely
    ai_response = gemini_response.text if hasattr(gemini_response, "text") else "⚠️ Error generating response."

        # Display AI response
    with st.chat_message("assistant",avatar="./images/AI.png"):
        st.markdown(ai_response)

        # Append AI response to chat history (without system prompt)
    st.session_state.chat_history.append(dict(role="assistant",avatar="./images/man.png",content= ai_response))