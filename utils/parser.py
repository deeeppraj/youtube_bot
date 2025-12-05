import pydantic
from langchain_core.output_parsers import PydanticOutputParser
from pydantic  import BaseModel,Field
from typing import List

class response(BaseModel):
    answer : str = Field(description="Response to the user's query")
    context :List[str] = Field(
        description="List of transcript chunks (page_content) used as context."
    )

myparser = PydanticOutputParser(pydantic_object=response)

def parser():
    return myparser
