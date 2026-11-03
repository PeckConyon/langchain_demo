from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from pydantic import BaseModel, Field

# Define the data structure we want the model to stick with when reply
class StudyCard(BaseModel):
    topic: str = Field(description="The Python topic being explained")
    explanation: str = Field(description="A short, beginner-friendly explanation")
    example: str = Field(description="A small Python code example")
    quiz: str = Field(description="One practice question, without its answer")
    time_to_answer: int = Field(ge=0, description="Suggested time to provide answer in minutes")

def run() -> None:
    load_dotenv()

    llm = init_chat_model(
        model="gpt-4.1-mini",
        temperature = 0.1
    )

    prompt_template = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template("You are a Python tutor creating study cards."),
        HumanMessagePromptTemplate.from_template("Create a study card about {topic}.")
    ])

    structured_llm = llm.with_structured_output(StudyCard)


    # The input key must match {topic} in the template above.
    # "text" belonged to the student-extraction example, not this study-card prompt.
    inputs = {"topic": "list comprehensions"}

    # Option 1: connect two processing steps from left to right.
    # Here | means pipeline composition, NOT a type union such as int | None.
    # Flow: inputs -> prompt_template -> structured_llm -> StudyCard.
    # Creating the chain does not make an API request.
    chain = prompt_template | structured_llm

    # Run both steps: format the messages, call the model, and validate its output.
    card = chain.invoke(inputs)

    # Option 2: the equivalent workflow written as two explicit steps.
    # To try it, comment out card = chain.invoke(inputs) above and uncomment
    # the next two lines. Running both options would make two API requests
    # and overwrite card with the second result (answers may differ).
    # formatted_prompt = prompt_template.invoke(inputs)  # Formatting only; no API call.
    # card = structured_llm.invoke(formatted_prompt)     # API call + validation.

    print("Topic:", card.topic)
    print("\nExplanation:", card.explanation)
    print("\nExample:", card.example)
    print("\nQuiz:", card.quiz)
    print("\nTime:", card.time_to_answer)

    # Convert the object to formatted JSON when needed.
    print("\nJSON:")
    print(card.model_dump_json(indent=2))

    # Convert the object to formatted Dictionary when needed.
    print("\nDictionary:")
    print(card.model_dump())
