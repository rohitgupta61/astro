import streamlit as st
from langchain_openai import ChatOpenAI
from datetime import datetime

# Get today's date in a readable format
today_date = datetime.now().strftime("%Y-%m-%d")

# Set up the header
st.header("Astrology Chat")

# Initialize session state for conversation history
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# Configure the LLM model
model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

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
   - If someone asks WHEN, give a estimate month with astrological explannation. 
   - If someone asks WHETHER, give a answer in Yes or No with astrological explannation. 
5. Always rely on Vedic astrology principles for your insights.
6. If someone is asking about relationship, ask details about their partner. 
7. I want to make the results consistent on similar questions. Answer all astrology-related questions based on Brihat Parashara Hora Shastra. 
8. In the same session, don't ask the details again and again. 
9. Use transit and progression 
11. Response Date: {today_date}. Don't answer in past. 

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

# Custom CSS for styling chat bubbles
st.markdown("""
    <style>
        .chat-bubble {
            padding: 10px;
            margin: 5px;
            border-radius: 10px;
            max-width: 70%;
        }
        .user-bubble {
            background-color: #000000;
            align-self: flex-end;
            text-align: right;
        }
        .bot-bubble {
            background-color: #000000;
            align-self: flex-start;
            text-align: left;
        }
        .chat-container {
            display: flex;
            flex-direction: column;
        }
    </style>
""", unsafe_allow_html=True)

# Display the conversation history
if st.session_state.conversation:
    for chat in st.session_state.conversation:
        st.markdown(
            f'<div class="chat-container">'
            f'<div class="chat-bubble user-bubble"><b>You:</b> {chat["user"]}</div>'
            f'<div class="chat-bubble bot-bubble"><b>Astrologer:</b> {chat["bot"]}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
