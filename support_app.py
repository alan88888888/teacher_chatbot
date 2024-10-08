import streamlit as st
from streamlit_chat import message
import llm

def load_prompt(file_path, question, history):
    """Load the prompt from a file and replace the placeholder with the user's question and conversation history."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            user_prompt = f.read().replace("{question}", question)
        # Combine user prompt with the history
        if history:
            return f"{history}\n{user_prompt}"
        return user_prompt
    except FileNotFoundError:
        st.error("Prompt file not found. Please ensure the file path is correct.")
        return None

def generate_response(text_input, history):
    """Generate a response based on the user's input and conversation history."""
    # Check for author-related questions
    if "author" in text_input.lower():
        return "Author is Wong, Hiu Fai."
    else:
        # Load and prepare the user prompt
        user_prompt = load_prompt("prompt2.txt", text_input, history)
        if user_prompt is None:
            return "Error loading prompt."

        system_prompt = "你是一个作业辅导老师，正在帮助学生解决问题。"

        # Get the response from the LLM
        try:
            response = llm.answer(system_prompt, user_prompt)
            return response
        except Exception as e:
            st.error(f"Error generating response: {e}")
            return "Error generating response."

# Initialize conversation history in session state
if 'history' not in st.session_state:
    st.session_state.history = []

st.title("AI Conversation")

# Display the conversation history
for i, msg in enumerate(st.session_state.history):
    message(msg['user'], is_user=True, key=f"{i}_user")
    message(msg['ai'], key=f"{i}")

# Create a text input box for user question
text_input = st.text_input("Enter your question:")

# Create a submit button
if st.button("Generate Responses") and text_input:
    response = generate_response(text_input, "\n".join(
        [f"User: {msg['user']}\nAI: {msg['ai']}" for msg in st.session_state.history]))

    # Update the conversation history
    st.session_state.history.append({"user": text_input, "ai": response})
    st.experimental_rerun()  # Rerun the script to update the conversation history

# Update the conversation history text area
st.session_state.history = st.session_state.history