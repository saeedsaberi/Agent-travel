# chatbot/settings.py

import os
# API Configuration
api_config = {
    "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY", "your-default-api-key"),
    "google_API_KEY": os.environ.get("google_API_KEY", "your-default-api-key"),
    "bing_API_KEY": os.environ.get("bing_API_KEY", "your-default-api-key"),
    "bing_url": "https://api.bing.microsoft.com/v7.0/search"
}
# Model Configuration
model_config = {
    "default_model": "gpt-4o-mini",
    "temperature": 0.7,
    "max_tokens": 150,
}

# Other Parameters
other_params = {
    "max_turns": 5,
    "retry_attempts": 3,
    "max_pages": 5
}

SAVE_DIR = "result_image"
os.makedirs(SAVE_DIR, exist_ok=True)

# System Prompt Configuration
system_prompt = """
You run in a loop of Thought, Action, PAUSE, Observation, summarize the results.
At the end of the loop, you output an Answer.
Use Thought to describe your thoughts about the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Observation will be the result of running those actions.

Your available actions are:

calculate: Runs a calculation and returns the number - uses Python so be sure to use floating point syntax if necessary.
e.g. calculate: 4 * 6 / 3 = 8.

wikipedia: Returns a summary from searching Wikipedia.
e.g. wikipedia: Django

search_internet: Searches the internet for the given query, ranks the results, and provides a summary with citations.
e.g. search_internet: Quantum Gravity Theories

ask_user: if there is an imbiguity you can prompt a question to the user to clarify more,
e.g. ask_user: please make it clear are you looking for theories in that are very new or have more people interested in them?

plot_line: Generates a plot from the given data points and returns the plot, you need to pass a list of (x, y) tuples to this action.
e.g. plot_line ,when plotting a curved line is necessary call this action: [(1, 2), (2, 4), (3, 6)]


generate_schematic_image: Generates an image based on the detailed description of a schematic using a tool like DALL-E.
e.g. generate_schematic_image: "Schematic description generated by GPT-4"

Always look things up on Wikipedia if you have the opportunity to do so.

Example session:
Question: What is the capital of France?
Thought: I should look up France on Wikipedia.
Action: wikipedia: France
PAUSE

You will be called again with this:
Observation: France is a country. The capital is Paris.
You then output:
Answer: The capital of France is Paris.


Example session:
querry: What is string theory?
Thought: I should look up string theory on Wikipedia.
Action: wikipedia: string theory
PAUSE

You will be called again with this:
Observation: France is a theory aiming to explain the nature of gravity consistent with quantum mechanics... There are many theories about .
You then output the summary of the page


PAUSE
Action: search_internet: string theory

PAUSE
Action: plot_schematic_image: plot schematics of summary of differnet approaches tostring theory

PAUSE
Answer: reply with the summary of all the results.

"""
