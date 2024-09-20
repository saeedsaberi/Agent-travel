import os, re, logging
import httpx, openai, requests
from .config import  model_config, SAVE_DIR
import matplotlib.pyplot as plt
from .config import api_config, other_params # Importing config when needed
# import dalle, asyncio
# from dalle import text2im  

# Configure logging
logging.basicConfig(
    filename='agent_ai_logs.log',  # Log file name
    level=logging.INFO,  # Log level
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date format
)

# Example of logging a message
logging.info('Logging system initialized.')

def wikipedia(q):
    print('wikipedia')
    return httpx.get("https://en.wikipedia.org/w/api.php", params={
        "action": "query",
        "list": "search",
        "srsearch": q,
        "format": "json"
    }).json()["query"]["search"][0]["snippet"]

def calculate(what):
    return eval(what)



def generate_schematic_image(description,  size="1792x1024"):
    """
    Use DALL-E to generate a schematic image based on a detailed description.
    
    Parameters:
    - description: str, the detailed schematic description from GPT-4.
    
    Returns:
    - image, the generated image from DALL-E or a similar tool.
    """
    print('generate_schematic_image')

    client = openai.OpenAI(api_key=openai.api_key)

    response = client.images.generate(
        model   = "dall-e-3",
        prompt  = description,
        size    = size,
        quality = "standard",
        n       = 1,
    )
    image_url = response.data[0].url

    # Get the image content
    image_content = requests.get(image_url).content
    save_dir = "result_image"
    os.makedirs(SAVE_DIR, exist_ok=True)
    image_path = os.path.join(SAVE_DIR, "schematic_image.png")

    # Save the image
    with open(image_path, "wb") as image_file:
        image_file.write(image_content)

    # Return the path to the saved image
    return f" schematics plotted and saved to {image_path}"


def search_internet(context, query, max_pages=other_params['max_pages']):
    """
    Perform an internet search using the Bing Search API, retrieve up to max_pages,
    rank the results, and summarize them using GPT-4.

    Parameters:
    - query: str, the search query
    - max_pages: int, the maximum number of pages to retrieve

    Returns:
    - str, a summary of the top-ranked search results.
    """
    print('search_internet')
    bing_API_KEY = api_config['bing_API_KEY']
    bing_url = api_config['bing_url']
    headers = {"Ocp-Apim-Subscription-Key": bing_API_KEY}
    
    snippets = []
    
    for page in range(max_pages):
        start = page * 10 + 1  # Bing returns 10 results per page
        response = httpx.get(bing_url, params={"q": query, "offset": start}, headers=headers)
        
        if response.status_code == 200:
            search_results = response.json()
            
            if 'webPages' in search_results and 'value' in search_results['webPages']:
                page_snippets = [item.get('snippet', 'No snippet available') for item in search_results['webPages']['value']]
                snippets.extend(page_snippets)
            else:
                break  # No more pages or no results found
        else:
            logging.error(f"Error: Unable to retrieve search results. Status code {response.status_code}")
            return f"Error: Unable to retrieve search results. Status code {response.status_code} - {response.text}"
    
    if snippets:
        # Rank the snippets before summarizing
        ranked_snippets = rank_snippets_with_llm(context, snippets)
        full_text = "\n".join(ranked_snippets)
        
        # Summarize the content using GPT-4
        summary = summarize_with_llm(context,full_text)
        return summary
    else:
        logging.warning("No relevant search results found.")
        return "No relevant search results found."

def rank_snippets_with_llm(context,snippets):
    """
    Rank the snippets using GPT-4 based on their relevance.

    Parameters:
    - snippets: list of str, the snippets to be ranked

    Returns:
    - list of str, the ranked snippets
    """
    client = openai.OpenAI(api_key=openai.api_key)

    prompt = f"Rank the following snippets based on their relevance to the topic:\n\n{snippets} based on the follwing context querry: {context}"
    completion = client.chat.completions.create(
        model=model_config['default_model'],
        messages=[
            {"role": "system", "content": "You are an expert in ranking information."},
            {"role": "user", "content": prompt}
        ]
    )

    ranked_text = completion.choices[0].message.content
    ranked_snippets = ranked_text.split("\n")  # Assuming each ranked snippet is on a new line

    return ranked_snippets

def summarize_with_llm(context, text ):
    """
    Summarize the given text using GPT.

    Parameters:
    - text: str, the text to be summarized

    Returns:
    - str, the summary of the text.
    """
    client = openai.OpenAI(api_key=openai.api_key)

    completion = client.chat.completions.create(
        model=model_config['default_model'],
        messages=[
            {"role": "system", "content": "You are an expert in summarizing information and responding based on the context."},
            {"role": "user", "content": f"Please summarize the following content:\n\n{text} appropriately for the following context querry:{context}"}
        ]
    )
    summary = completion.choices[0].message.content
    return summary



def ask_user(question):
    """
    Ask a clarifying question to the user.

    Parameters:
    - question: str, the question to ask the user.

    Returns:
    - str, the user's response.
    """
    # Simulate asking the question to the user (In a real system, this would involve interacting with the user interface)
    print(f"ask_user: Clarification needed: {question}")
    user_response = input(f"Clarification needed: {question}\n Your response: ")
    return user_response

def search_flights(query, preferences):
    """
    Search for flights based on the given destination and user preferences using a travel API.

    Parameters:
    - query (str): The destination for the flight search, typically a city or airport code.
    - preferences (dict): A dictionary containing user preferences for the flight search.
        Expected keys include:
        - 'budget' (str or int): The maximum budget for the flight in USD or the relevant currency.
        - 'airports' (str): The preferred airport(s) for departure.
        - 'time_pref' (str): The preferred time of day for the flight (e.g., 'morning', 'afternoon', 'evening').

    Returns:
    - list: A list of flights ranked by user preferences. Each flight in the list is represented
      as a dictionary with details such as price, departure time, duration, etc.

    Example:
    >>> preferences = {
            'budget': 500,
            'airports': 'JFK, LAX',
            'time_pref': 'morning'
        }
    >>> search_flights('Toronto', preferences)
    """
    google_flight_api_url = "https://serpapi.com/search"
 
    
    # Use preferences to form the query
    response = httpx.get(google_flight_api_url, params={
        "destination": query,
        "budget": preferences['budget'],
        "airports": preferences['airports'],
        "time_of_day": preferences['time_pref'],
        "key": api_config['google_flights_api_key']
    })
    
    flights = response.json()
    
    # Rank flights based on the user’s preferences
    ranked_flights = rank_flights_by_preferences(flights, preferences)
    
    return ranked_flights


def rank_flights_by_preferences(flights, preferences):
    # Sort flights based on cost, timing, or other preferences
    ranked_flights = sorted(flights, key=lambda x: x['price'])  # Example based on price
    return ranked_flights


def fetch_tripadvisor_data(destination, preferences):
    """
    Fetch travel recommendations from the TripAdvisor API (or similar) based on user preferences.
    
    Parameters:
    - destination (str): The location the user wants to visit.
    - preferences (dict): User preferences, such as:
        - 'budget' (int): The maximum budget for the trip in USD.
        - 'rating' (float): The minimum rating of the hotel or activity.
        - 'accommodation_type' (str): Type of accommodation (e.g., 'hotel', 'resort').
        - 'amenities' (list): List of desired amenities (e.g., ['wifi', 'pool']).
    
    Returns:
    - list: A list of ranked travel options (hotels, activities) based on user preferences.
    """
    tripadvisor_api_url = "https://api.tripadvisor.com/api/v1/hotels"  # This is a placeholder URL
    api_key =  api_config['TRIPADVISOR_API_KEY']  
    
    # Construct the query parameters based on user preferences
    params = {
        "destination": destination,
        "budget": preferences.get('budget', 500),  # Default budget of $500 if not provided
        "min_rating": preferences.get('rating', 4.0),  # Default minimum rating of 4.0
        "accommodation_type": preferences.get('accommodation_type', 'hotel'),
        "amenities": ",".join(preferences.get('amenities', [])),
        "key": api_key
    }
    
    # Fetch data from the TripAdvisor API
    response = httpx.get(tripadvisor_api_url, params=params)
    
    if response.status_code != 200:
        return f"Error: Unable to fetch data from TripAdvisor. Status code: {response.status_code}"
    
    travel_data = response.json()
    
    # Filter and rank the results based on preferences (e.g., rating and budget)
    ranked_results = rank_results_by_preferences(travel_data, preferences)
    
    return ranked_results

def rank_results_by_preferences(data, preferences):
    """
    Rank the results based on user preferences such as budget and rating.
    
    Parameters:
    - data (list): List of travel options from the API.
    - preferences (dict): The user preferences used to filter the results.
    
    Returns:
    - list: A list of ranked travel options.
    """
    # Filter by budget and rating
    filtered_data = [
        item for item in data
        if item['price'] <= preferences['budget'] and item['rating'] >= preferences['rating']
    ]
    
    # Rank by rating (highest first)
    ranked_data = sorted(filtered_data, key=lambda x: x['rating'], reverse=True)
    
    return ranked_data

def search_tripadvisor(destination, preferences):
    """
    Action to search TripAdvisor for hotels and activities based on user preferences.
    
    Parameters:
    - destination (str): The destination where the user is looking to travel.
    - preferences (dict): User preferences (budget, rating, etc.).
    
    Returns:
    - str: A summary of the best-matching travel options based on the preferences.
    """
    # Fetch and rank the data
    ranked_results = fetch_tripadvisor_data(destination, preferences)
    
    if isinstance(ranked_results, str):
        return ranked_results  # Error message
    
    # Generate a summary of the top matches
    if not ranked_results:
        return "No results found that match your preferences."
    
    # Example summary output
    summary = "Here are the best-matching travel options based on your preferences:\n\n"
    
    for i, result in enumerate(ranked_results[:5], start=1):  # Top 5 results
        summary += (
            f"{i}. {result['name']} - Rating: {result['rating']}/5\n"
            f"   Price: ${result['price']} per night\n"
            f"   Location: {result['location']}\n"
            f"   Amenities: {', '.join(result['amenities'])}\n\n"
        )
    
    return summary


def prepopulate_preferences_with_fallback(query):
    """
    Pre-populate preferences in JSON format using a lightweight OpenAI model and ask the user for missing info.

    Parameters:
    - query (str): The user's input query, typically about vacation preferences or flights.

    Returns:
    - dict: A dictionary containing pre-populated preferences, asking the user to fill in any missing values.
    """
    client = openai.OpenAI(api_key=openai.api_key)

    prompt = f"Based on the following query: '{query}', pre-populate a JSON object containing travel preferences such as budget, preferred airports, and flight time preferences."

    # Use a lower-size model like 'gpt-3.5-turbo' to infer preferences
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an AI assistant that helps users plan their vacations."},
            {"role": "user", "content": prompt}
        ]
    )

    # Convert the model output to a dictionary (assuming it returns a valid JSON structure)
    preferences_json = completion.choices[0].message.content
    preferences = eval(preferences_json)  # Ensure it gets converted to a Python dictionary

    # Prepopulate missing fields with null values
    required_fields = ['budget', 'preferred_airports', 'flight_time', 'rating', 'accommodation_type', 'amenities']

    for field in required_fields:
        if field not in preferences or preferences[field] is None:
            preferences[field] = None

    # Ask user for missing information
    preferences = ask_for_missing_info(preferences)

    return preferences
def ask_for_missing_info(preferences):
    """
    Loop through the preferences and ask the user for missing information.
    
    Parameters:
    - preferences (dict): The partially prepopulated preferences.
    
    Returns:
    - dict: The updated preferences dictionary with user-provided values for missing keys.
    """
    questions = {
        "budget": "What's your budget for the trip?",
        "preferred_airports": "Which airport would you prefer to depart from?",
        "flight_time": "What time of the day should the flight be (morning, afternoon, evening)?",
        "rating": "What's the minimum acceptable rating (out of 5)?",
        "accommodation_type": "What type of accommodation are you looking for (e.g., hotel, resort)?",
        "amenities": "Any specific amenities you'd like (e.g., wifi, pool)?"
    }

    # Loop through preferences and ask the user for missing information
    for key, question in questions.items():
        if preferences.get(key) is None:  # Check if the field is missing (None)
            user_input = ask_user(question)
            if key == "amenities":
                # Split amenities into a list if the field is amenities
                preferences[key] = user_input.split(", ")
            else:
                preferences[key] = user_input

    return preferences



def query_with_prepopulated_preferences(query, preferences):
    """
    Action to query and prepopulate user preferences using a lightweight model, filling in missing info with ask_user.

    Parameters:
    - query (str): The user's input query.

    Returns:
    - dict: The final preferences dictionary after prepopulation and user input.
    """
    # Check if the query is relevant
    if check_query_relevance(query):
        # Prepopulate preferences, ask user for any missing values
        preferences = prepopulate_preferences_with_fallback(query)
        
        # Proceed with the vacation planning or flight search using the preferences
        print(f"Proceeding with the following preferences: {preferences}")
        
        # Example: Call the search action (e.g., flights or hotels)
        result = known_actions['search_tripadvisor'](query, preferences)  # Replace with appropriate action
        return result
    
    else:
        return "The query is not relevant to vacation planning or flight searches."


known_actions = {
    "search_tripadvisor": search_tripadvisor,
    "wikipedia": wikipedia,
    "calculate": calculate,
    "generate_schematic_image": generate_schematic_image,
    "search_internet": search_internet, 
    "ask_user": ask_user,
    "search_flights": search_flights,
    "rank_flights_by_preferences": rank_flights_by_preferences
}


action_re = re.compile('^Action: (\w+): (.*)$')
