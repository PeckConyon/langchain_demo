from dotenv import load_dotenv
from langchain.tools import tool
from langchain.chat_models import init_chat_model


@tool(
    "multiply",
    description="Multiply two integers and return the result.",  #  With this no need docstring
    return_direct=False,
)
def multiply(a: int , b: int) -> int:
    """Multiply two integers and return the result."""   # docstring so LangChain can describe it to the model.
    print("\nMultiply function got called by the llm")
    return a * b


def run() -> None:
    load_dotenv()

    llm = init_chat_model(
        model = "gpt-4.1-mini",
        temperature = 0.1
    )

    # Register the tools Python is allowed to execute.
    tools = {multiply.name: multiply}

    # Tell the model which tools are available.
    # This does not execute the tools.
    llm_with_tools = llm.bind_tools(list(tools.values()))

    response = llm_with_tools.invoke("Multiply 2 by 10")

    #print("Text:", repr(response.content))
    print("Tool calls:", response.tool_calls)
     
    for tool_call in response.tool_calls:
        selected_tool = tools[tool_call["name"]]
        result = selected_tool.invoke(tool_call["args"])
        print("Result:", result)