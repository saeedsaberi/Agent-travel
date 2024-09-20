from chatbot.bot import ChatBot
from chatbot.config import other_params, system_prompt
from chatbot.actions import known_actions, action_re, query_with_prepopulated_preferences





class UnknownActionError(Exception):
    """Exception raised when the bot encounters an unknown action."""
    def __init__(self, action, action_input):
        self.action = action
        self.action_input = action_input
        self.message = f"Unknown action: {action} with input: {action_input}"
        super().__init__(self.message)


def query(question, max_turns=other_params.max_turns):
    """
    Executes a chatbot query to answer a given question.
    
    Args:
        question (str): The question to be answered.
        max_turns (int, optional): The maximum number of turns allowed for the query. Defaults to 5.
    
    Returns:
        str: The answer to the question.
    
    Raises:
        Exception: If the bot encounters an unknown action.
    
    """
    bot = ChatBot(system=system_prompt)
    next_prompt = question
    i = 0
            

    while i < max_turns:
        i += 1
        result = bot(next_prompt)
        actions = [action_re.match(a) for a in result.split('\n') if action_re.match(a)]
        if actions:
            action, action_input = actions[0].groups()
            if action not in known_actions:
                raise UnknownActionError(action, action_input)
            elif action=='search_flights':
                preferences = query_with_prepopulated_preferences(question)
            elif action=='search_internet':
                observation = known_actions[action](question, action_input)
            else:                  
                observation = known_actions[action](action_input)

            next_prompt = f"""{action} performed, resulting in Observation: {observation}, 
                                next_prompt: {next_prompt}\n"""
 
        else:
            print(result)
            print()
            # print(next_prompt)

            return result

def prepopulate_preferences(question):
    """
    Pre-populate preferences in JSON format using a smaller OpenAI model.
    
    Parameters:
    - query (str): The user's input query, typically about vacation preferences or flights.
    
    Returns:
    - dict: A dictionary containing pre-populated preferences such as budget, preferred airports,
            and flight time preferences.
    """
    client = openai.OpenAI(api_key=openai.api_key)

    prompt = f"Based on the following query: '{question}', 
    pre-populate a JSON object containing travel preferences such as budget, preferred airports,
    and flight time preferences."

    # Use a lower-size model like 'gpt-3.5-turbo' to infer preferences
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", 
                "content": "You are an AI assistant that helps users plan their vacations."},
            {"role": "user", 
             "content": prompt}
        ]
    )

    preferences_json = completion.choices[0].message.content

    return preferences_json

def check_query_relevance(query):
    """
    Check if the query is relevant to vacation planning or flight searches using a lower-size OpenAI model.
    
    Parameters:
    - query (str): The user's input query.
    
    Returns:
    - bool: True if the query is relevant, False otherwise.
    """
    client = openai.OpenAI(api_key=openai.api_key)

    prompt = f"Is the following query relevant to vacation planning or flight searches? Reply only with 'yes' or 'no'. Query: '{query}'"

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an AI assistant that determines the relevance of queries."},
            {"role": "user", "content": prompt}
        ]
    )

    relevance = completion.choices[0].message.content.strip().lower()

    return relevance == 'yes'

def query_with_relevance_check(query):
    """
    Execute the vacation planning or flight search query if it is relevant.
    
    Parameters:
    - query (str): The user's input query.
    
    Returns:
    - str: The result of the query, or a message indicating that the query is not relevant.
    """
    # First, check if the query is relevant
    if check_query_relevance(query):
        # Pre-populate preferences using the lower-size model
        preferences = prepopulate_preferences(query)

        # Proceed with the flight search or vacation planning
        print(f"Query is relevant. Proceeding with the search...\nPreferences: {preferences}")
        return preferences  # You can then use this for the actual search logic
    else:
        return "The query is not relevant to vacation planning or flight searches."




if __name__ == "__main__":
    question = "I want to book a flight to Paris and stay in a hotel with a pool."
    if check_query_relevance(question):
        result = query(question)
    else:
        print('question is not relevant to vacation planning or flight searches')
