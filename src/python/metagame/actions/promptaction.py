from metagame.utils.llmutils import get_chatgpt_output


def run_prompt_action(action_parser, data, parent_args):
    llm_config_data = data[0]
    if isinstance(llm_config_data, dict):
        prompt = llm_config_data["prompt"]
    elif isinstance(llm_config_data, str):
        prompt = llm_config_data
    llm_output = get_chatgpt_output(user_input=prompt)
    return llm_output
