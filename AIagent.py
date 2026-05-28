import os
from openai import OpenAI


def make_context(set_role, set_content):
    return {'role': set_role, 'content': set_content}


def agent(system_prompt, user_prompt, model="nvidia/nemotron-3-super-120b-a12b:free"):

    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.getenv('OPENROUTER_KEY'))

    system_prompt = make_context('system', system_prompt)
    user_prompt = make_context('user', user_prompt)

    messages = [system_prompt, user_prompt]

    completion = client.chat.completions.create(
        model=model,
        messages=messages
    )
    answer = completion.choices[0].message.content

    messages.append(make_context('assistant', answer))

    return answer
