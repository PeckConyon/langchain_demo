
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage


# With invoke(), your program waits for the complete answer. With stream(), you can print small pieces as the model produces them.

def run()-> None:
    load_dotenv()

    llm = init_chat_model(
        model="gpt-4.1-mini",
        temperature = 0.1
    )

    # Use HumanMessage for ready-to-send text; use a message template for placeholders you’ll fill later.

    # messages = [
    #     SystemMessage(content = "You are a Python tutor. Explain clearly with examples."),
    #     HumanMessage(content= "Explain {topic} in about 200 words")  # not replacing the value
    # ]

    # messages = [
    #     ("system", "You are a Python tutor. Explain clearly with examples."),
    #     # Tuple shorthand creates a template that substitutes {topic}.
    #     # HumanMessage(content="...") is already a final message: its text
    #     # is passed through unchanged, including any literal {topic}.
    #     ("human", "Explain {topic} in about 200 words")
    # ]

    system_message =  SystemMessage(content = "You are a Python tutor. Explain clearly with examples.")
        
    human_template = HumanMessagePromptTemplate.from_template(
        "Explain {topic} in about 200 words."
    )

    
    messages = [
       system_message,
       human_template
    ]


    prompt_template = ChatPromptTemplate.from_messages(messages)

    chain = prompt_template | llm

    

    complete_answer = ""

    input = { "topic" : "Langchain"}

    for chunk in chain.stream(input):
        text = chunk.content

        # end="" prevents a new line after every chunk.
        # flush=True displays the text immediately.
        print(text, end="", flush=True)

        complete_answer += text

    # Finish with a newline once streaming is complete.
    print()
    print("\nCharacters received:", len(complete_answer))


