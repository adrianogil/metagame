from metagame.utils.llmutils import get_chatgpt_output


def run_prompt_action(action_parser, data, parent_args):
    prompt = data[0]
    llm_output = get_chatgpt_output(user_input=prompt)
    return llm_output
