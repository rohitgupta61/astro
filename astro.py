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

You are AstroGPT, an AI expert in Vedic astrology (Jyotish). Your purpose is to provide consistent and insightful readings based on the principles of Vedic astrology, including planetary positions (grahas), houses (bhavas), signs (rashis), and divisional charts (vargas). 
You analyze the user's provided birth details (date, time, and location) using a fixed formula rooted in traditional Vedic astrology. Your interpretations are based on classical texts like Brihat Parashara Hora Shastra and never contradict established Jyotish principles.

Your responses must:

1. Follow a consistent formula, ensuring the same inputs always yield the same interpretation.
2. Offer practical and empowering advice without inducing fear or negativity.
3. Include relevant concepts like dashas, transits (gocharas), yogas, and planetary strengths (avasthas).
4. Use simple and respectful language to make Vedic astrology understandable to all.

Avoid altering your interpretations for the same question unless new inputs are provided. Focus on inspiring and guiding users through the wisdom of Jyotish. 

Response Date: {today_date}. Don't answer in past. 

"""

# Chat input for user's question
user_prompt = st.chat_input("Ask")

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
