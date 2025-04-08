import streamlit as st
import os
import time
from google.generativeai import configure, GenerativeModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
sr_no_c=os.getenv("sr_no")
#sr_no=(int)sr_no_c
configure(api_key=API_KEY)

# Adding default values
sr_no=100
model_name=""
system_prompt = "You are a helpful assistant."
user_prompt = "Hello! How are you?"
top_p_value = 0.9
top_k_value = 40
temperature = 0.9
max_tokens = 1000

st.set_page_config(page_title="Home", layout="wide",page_icon="./images/logo.png")

# Streamlit UI

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

st.title("CREATE YOUR OWN AI MODEL")
st.markdown("---")  # Adds a horizontal line for separation

col1, col2 = st.columns([1, 2])  
    # User Inputs
with col1:
    model_name= st.text_input("Enter the name of your AI Model")
    system_prompt = st.text_area("Enter System Prompt","You are a helpful assistant.")
    user_prompt = st.text_area("Enter User Prompt", "Hello! How are you?")
    temperature = st.slider("Select Temperature", 0.0, 1.0, 0.7, 0.05)
    top_p_value = st.slider("Select Top P", 0.0, 1.0, 0.9)
    top_k_value = st.number_input("Select Top K", min_value=1, value=40, step=1)
    max_tokens = st.number_input("Max Tokens", min_value=1, value=1000, step=1)

with col2:
    st.markdown("---")
    # Generate Response Button
    if st.button("Generate Response"):

        model = GenerativeModel("gemini-1.5-pro")

        print("Generating response with the following parameters:")
        print(f"System Prompt: {system_prompt}")
        print(f"User Prompt: {user_prompt}")
        print(f"Temperature: {temperature}")
        print(f"Min Tokens: min_tokens, Max Tokens: {max_tokens}")

        try:
            time.sleep(2)  # Adding delay to avoid rate limit errors
            response = model.generate_content(contents=[system_prompt + user_prompt],
                                            generation_config={
                                                "temperature": temperature,
                                                "max_output_tokens": max_tokens,
                                                "top_p": top_p_value,
                                                "top_k": top_k_value
                                            })
            print("Response received successfully")
            st.subheader("Response:")
            st.write(response.text)
        except Exception as e:
            print(f"Error occurred: {e}")
            st.error(
                "Error: API Quota exceeded or service unavailable. Try again later."
            )

    # creating model 

    if st.button("submit model"):

        sr_no = sr_no -1
        model_identidy=f"pages/{sr_no}_{model_name}.py"

        with open(model_identidy, "w", encoding="utf-8") as f:
            f.write(f'''import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

# Configuration variables
sr_no = 100
model_name="{model_name}"
system_prompt ='"{system_prompt}"'
top_p_value = {top_p_value}
top_k_value = {top_k_value}
temperature = {temperature}
max_tokens = {max_tokens}

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
model = gen_ai.GenerativeModel('gemini-1.5-pro')

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
    st.session_state.chat_history.append(dict(role="assistant",avatar="./images/man.png",content= ai_response))''')
        f.close()
