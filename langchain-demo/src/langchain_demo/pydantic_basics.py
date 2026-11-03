from pydantic import BaseModel, Field, ValidationError

class Student(BaseModel):
    name:str
    age:int = Field(ge=0, le =120)  # Age should be greater than or equal to zero and less than or equal to 120
    course: str = "Langchain"  # Default

def run()-> None:

    # valid object
    student = Student(name="Supun", age=25)
    print("Name", student.name)
    print("Name", student.age)
    print("Name", student.course)

     #  Pydantic can convert compatible values by default
    converted = Student(name="Supun", age="27" )
    print("Name", converted.name)
    print("Name", converted.age)
    print("Name", converted.course)

    # 3. Convert the validated object into common data formats.
    print("JSON :", student.model_dump_json(indent=2))
    print("Dictionary :", student.model_dump())

    try:
        Student(name = "Supz", age = -5)
    except ValidationError as error:
        print("\nValidation failed:")
        print(error)

