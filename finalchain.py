import warnings
warnings.filterwarnings(action='ignore')

from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document
from langchain_core.exceptions import OutputParserException


def format_context(context: list[Document]):
    a = []
    for items in context:
        a.append(items.page_content)
    text = "\n\n".join(a)
    return text


def final_chain(model, retriver, parser):
    prompt = PromptTemplate(
        template="""
You are a helpful assistant. Answer the {query} based only on the {context} provided.
If context is insufficient or irrelevant just say you dont know and dont assume stuff.

{format}
""",
        input_variables=["query", "context"],
        partial_variables={"format": parser.get_format_instructions()},
    )

    parallelchain = RunnableParallel(
        {
            "query": RunnablePassthrough(),
            "context": retriver | RunnableLambda(format_context),
        }
    )

    def clean_and_parse(output):
        text = getattr(output, "content", str(output))

        if "<think>" in text and "</think>" in text:
            text = text.split("</think>", 1)[1].strip()

        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1:
            raise OutputParserException(f"No JSON object found in model output:\n{text}")

        json_str = text[start : end + 1]
        return parser.parse(json_str)

    sequentialchain = prompt | model | RunnableLambda(clean_and_parse)
    finalchain = parallelchain | sequentialchain
    return finalchain
