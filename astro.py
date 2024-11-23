import streamlit as st
from langchain_openai import ChatOpenAI

# Set up the header
st.header("Astrology Chat")

# Initialize session state for conversation history
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# Configure the LLM model
model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# Define the astrologer role
astrologer_role = """
You are an astrologer who uses astrology calculations to answer people's questions. 
- Start with gretting. 
- If someone asks a question, first ask for their basic details: date of birth, location of birth, and time of birth (if available).
- Use this information to calculate and answer their question.
- Format: Specific Answer of the question, explanation in minumum 3 and maximum 5 lines. 
- Use vedic astrology
"""

# Chat input for user's question
user_prompt = st.chat_input("Ask your question")

if user_prompt:
    # Build the prompt with the astrologer role and conversation history
    history = f"{astrologer_role}\n"
    for chat in st.session_state.conversation:
        history += f"User: {chat['user']}\nAstrologer: {chat['bot']}\n"
    
    # Add the new user query
    history += f"User: {user_prompt}\nAstrologer:"
    
    # Invoke the model with the updated prompt
    response = model.invoke(history)
    
    # Save the question and response to session state
    st.session_state.conversation.append({"user": user_prompt, "bot": response.content})

# Display the conversation history
if st.session_state.conversation:
    st.write("### Conversation History:")
    for chat in st.session_state.conversation:
        st.markdown(f"**You:** {chat['user']}")
        st.markdown(f"**Astrologer:** {chat['bot']}")
