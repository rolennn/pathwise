from dotenv import load_dotenv, find_dotenv
import json
from openai import OpenAI
import streamlit as st

from config.constants import *
from lib.tools_and_functions import *

# Set page config
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# Get API Key from environment variable
load_dotenv(find_dotenv())

# Title
st.title("🤖 AI Chatbot")
st.write("Chat with an AI assistant powered by OpenAI")

# Sidebar for API key input
with st.sidebar:
    st.header("Configuration")
    
    model = st.selectbox(
        "Select Model:",
        ["gpt-5-mini", "gpt-5"],
        index=0
    )
    
    # Clear chat button in sidebar
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Initialize session state for messages and response_id
if "messages" not in st.session_state:
    st.session_state.messages = []
if "response_id" not in st.session_state:
    st.session_state.response_id = None

# Function to get AI response
def get_ai_response(messages,system_instructions, model):
    try:
        client = OpenAI()
        response = client.responses.create(
            model=model,
            input=messages,
            instructions=system_instructions,
            tools = TOOLS,
            previous_response_id=st.session_state.response_id
        )
        st.session_state.response_id = response.id

        tool_result = []
        for item in response.output:
            if item.type == "function_call":
                function_call = item
                function_call_arguments = json.loads(item.arguments)

                func = FUNCTION_MAP.get(function_call.name)
                if func:
                    result = func(**function_call_arguments)
                else:
                    result = f"Function {function_call.name} not found."
                
                tool_result.append({
                    "type": "function_call_output",
                    "call_id": function_call.call_id,
                    "output": json.dumps(result),
                })

        if not tool_result:
            return response.output_text
        
        follow_up_response = client.responses.create(
            model=model,
            input=tool_result,
            instructions= "Respond using ONLY the output of the tool calls and nothing else",
            tools = TOOLS,
            previous_response_id= st.session_state.response_id
        )
        st.session_state.response_id = follow_up_response.id

        return follow_up_response.output_text
    
    except Exception as e:
        return f"Error: {str(e)}"

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User input
user_input = st.chat_input("Type your message here...")

# Handle user input and generate response
if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    with st.chat_message("user"):
        st.write(user_input)
    
    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Prepare messages for OpenAI API
            response = get_ai_response(user_input,INSTRUCTIONS,model)

            st.write(response)
        
    # Add AI response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})