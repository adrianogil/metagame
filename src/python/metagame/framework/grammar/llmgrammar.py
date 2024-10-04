from metagame.utils.llmutils import get_chatgpt_output
from metagame.utils.printme import printme

from pydantic import BaseModel, Field


class GeneratedDataList(BaseModel):
    data: list[str] = Field(..., title="The generated list according to the prompt.")

def generate_list_from_prompt(prompt) -> list[str]:

    printme("generate_list_from_prompt: " + prompt, debug=True)
    user_prompt = "Generate a list of items from the following prompt: " + prompt

    llm_output = get_chatgpt_output(user_input=user_prompt, response_format=GeneratedDataList)
    return llm_output.data

