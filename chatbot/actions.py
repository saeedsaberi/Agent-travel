import os, re, io, logging
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


def plot_line(data, save_path=SAVE_DIR +"/plot.png"):
    """
    Plot the given data, save the image to a file, and return the base64 encoded image.
    The data is expected to be a list of (x, y) tuples.
    
    Parameters:
    - data: str, a string representing a list of (x, y) tuples, e.g., "[(1, 2), (2, 3), (3, 4)]"
    - save_path: str, the file path where the plot image will be saved.
    
    Returns:
    - str, the base64 encoded image.
    """
    print('plot_line')
    # Parse the data assuming it's in the form of a string of tuples
    points = eval(data)  # Example input: "[(1, 2), (2, 3), (3, 4)]"

    # Separate the points into x and y coordinates
    x, y = zip(*points)

    # Ensure the directory exists
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    # Create the plot
    plt.figure()
    plt.plot(x, y, marker='o')
    plt.title("Generated Plot")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")

    # Save the plot to a file
    plt.savefig(save_path)
    
    # Save the plot to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)

    # Return the base64 string
    return f"data:image/png;base64, line plotted and saved to {save_path}"


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
    api_url = "YOUR_TRAVEL_API_ENDPOINT"
    api_key = api_config['travel_API_KEY']
    
    # Use preferences to form the query
    response = httpx.get(api_url, params={
        "destination": query,
        "budget": preferences['budget'],
        "airports": preferences['airports'],
        "time_of_day": preferences['time_pref'],
        "key": api_key
    })
    
    flights = response.json()
    
    # Rank flights based on the user’s preferences
    ranked_flights = rank_flights_by_preferences(flights, preferences)
    
    return ranked_flights


def rank_flights_by_preferences(flights, preferences):
    # Sort flights based on cost, timing, or other preferences
    ranked_flights = sorted(flights, key=lambda x: x['price'])  # Example based on price
    return ranked_flights

known_actions = {
    "wikipedia": wikipedia,
    "calculate": calculate,
    "plot_line": plot_line,
    "generate_schematic_image": generate_schematic_image,
    "search_internet": search_internet, 
    "ask_user": ask_user,
    "search_flights": search_flights,
    "rank_flights_by_preferences": rank_flights_by_preferences
}


action_re = re.compile('^Action: (\w+): (.*)$')
