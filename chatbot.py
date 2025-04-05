#chatbot.py
import os
from groq import Groq
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq

# Get API key from environment variable
groq_api_key = os.getenv('GROQ_API_KEY')

if not groq_api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set.")

# Initialize chat model and memory
model_name = "gemma2-9b-it"
memory = ConversationBufferWindowMemory(k=5)
groq_chat = ChatGroq(groq_api_key=groq_api_key, model_name=model_name)
conversation = ConversationChain(llm=groq_chat, memory=memory)

def chatbot_response(user_input):
    response = conversation(user_input)
    return response['response']
