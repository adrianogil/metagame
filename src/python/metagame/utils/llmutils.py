from .printme import printme

from openai import OpenAI
import base64
import os

client = OpenAI(
    api_key=os.environ["CHATGPT_SECRET_API_KEY"],
)


def get_chatgpt_output(user_input="Hello world!", messages=None, functions=None, model='gpt-4o-mini', attached_images=None, response_format=None):
    if not messages:
        messages = []
    if attached_images:
        content_data = [
        {
          "type": "text",
          "text": user_input
        },
        ]
        for image_path in attached_images:
            base64_image = None
            with open(image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            content_data.append(
                {
                  "type": "image_url",
                  "image_url": {
                       "url": f"data:image/jpeg;base64,{base64_image}"
                  }
                }
            )
        messages.append({"role": "user", "content": content_data})
    else:
        messages.append({"role": "user", "content": user_input})

    printme(f"Running LLM prompt with model: {model}", debug=True)

    args = {
        "model": model,
        "messages": messages
    }
    if functions:
        args["functions"] = functions
        args["function_call"] = "auto"

    if response_format:
        args["response_format"] = response_format

    completion = client.beta.chat.completions.parse(**args)

    if response_format:
        return completion.choices[0].message.parsed
    elif not functions:
        return completion.choices[0].message.content

    return completion
