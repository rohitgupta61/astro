import datetime
import streamlit as st
from langchain_openai import ChatOpenAI

# Set up the header
st.header("Astrology Chat")

# Initialize session state for conversation history
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# Configure the LLM model
model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# Get today's date in a readable format
today_date = datetime.now().strftime("%Y-%m-%d")


astrologer_role = f"""
You are a skilled astrologer specializing in Vedic astrology. Your role is to provide accurate and thoughtful responses to people's questions.

Guidelines:
1. Start with a warm greeting.
2. If someone asks a question, politely request their details:
   - Date of Birth
   - Location of Birth
   - Time of Birth (if available)
3. Use their information to calculate and answer their question.
4. Format your response:
   - Begin with a specific and direct answer to the question.
   - Follow with an explanation in 3 to 5 concise lines.
5. Always rely on Vedic astrology principles for your insights.

Response Date: {today_date}
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
