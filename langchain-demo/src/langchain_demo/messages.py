# Messages and Conversation Context

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.messages import SystemMessage, HumanMessage, AIMessage

def run()->None:
    
    load_dotenv()
    
    llm = init_chat_model(
        model="gpt-4.1-mini",
        temperature=0.1,
    )

    # Create a conversation context
    conversation = [
        SystemMessage(content="You are a helpful assistant."),
        HumanMessage(content="Explain LangChain in three simple sentences."),
    ]

    # Get the response from the model
    response = llm.invoke(conversation)

    print("First answer:", response.content)

    # Include the assistant's answer in the conversation history.
    conversation.append(AIMessage(content=response.content))

    # Ask a follow-up question
    conversation.append(HumanMessage(content="Can you provide a simple example?"))
    followup = llm.invoke(conversation)
    print("Second answer:", followup.content)