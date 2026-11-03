from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.chat_models import init_chat_model

def run() -> None:
    load_dotenv()       
    
    # llm = ChatOpenAI(
    #     model="gpt-4o-mini",
    #     temperature=0.1,
    # )


    llm = init_chat_model(
        model="gpt-4.1-mini",
        #model_provider="openai",   # can infer
        temperature=0.1,
    )

    response = llm.invoke("Explain LangChain in three simple sentences.")

    print(response.content)