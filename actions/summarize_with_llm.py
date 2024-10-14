import logging


def summarize_with_llm(context, text):
    """
    Summarize the given text using GPT.

    Parameters:
    - text: str, the text to be summarized

    Returns:
    - str, the summary of the text.
    """
    logging.info(f"Summarizing text: {text}")
    client = openai.OpenAI(api_key=openai.api_key)

    prompt = f"Please summarize the following content: {text} appropriately for the following context query: {context}"
    logging.info(f"Prompt: {prompt}")

    completion = client.chat.completions.create(
        model=model_config["default_model"],
        messages=[
            {
                "role": "system",
                "content": "You are an expert in summarizing information and responding based on the context.",
            },
            {"role": "user", "content": prompt},
        ],
    )
    summary = completion.choices[0].message.content
    logging.info(f"Summary: {summary}")

    return summary
