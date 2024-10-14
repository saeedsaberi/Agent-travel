import openai
from config import model_config


def rank_snippets(context, snippets):
    """
    Rank snippets based on their relevance to a given context using GPT-4.

    Parameters:
    - context (str): The context to rank snippets against
    - snippets (list[str]): The snippets to be ranked

    Returns:
    - list[str]: The ranked snippets
    """
    client = openai.OpenAI(api_key=openai.api_key)

    prompt = (
        f"Rank the following snippets based on their relevance to the topic:\n\n{snippets} "
        f"based on the following context query: {context}"
    )

    completion = client.chat.completions.create(
        model=model_config["default_model"],
        messages=[
            {"role": "system", "content": "You are an expert in ranking information."},
            {"role": "user", "content": prompt},
        ],
    )

    ranked_snippets = completion.choices[0].message.content.splitlines()

    return ranked_snippets
