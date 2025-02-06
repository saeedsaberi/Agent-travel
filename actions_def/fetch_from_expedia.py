import logging, httpx


logger = logging.getLogger(__name__)


def fetch_from_expedia(query, preferences):
    """
    Fetch travel options from Expedia based on the query and preferences.

    Parameters:
    - query (str): The travel query (e.g., "flights to Paris").
    - preferences (dict): User preferences for the trip.

    Returns:
    - list: A list of travel options from Expedia.
    """
    expedia_url = "https://api.expedia.com/flights"  # Example URL (replace with actual)
    params = {
        "query": query,
        "budget": preferences.get("budget", 1000),
        "departure_time": preferences.get("flight_time", "morning"),
    }
    logger.info(f"Fetching travel options from Expedia with params: {params}")

    try:
        print(f"Sending request to Expedia with URL: {expedia_url} and params: {params}")
        response = httpx.get(expedia_url, params=params)
        print(f"Received response from Expedia: {response.status_code} - {response.text}")
        response.raise_for_status()
    except httpx.RequestError as e:
        logger.error(f"Error fetching travel options from Expedia: {e}")
        return []

    travel_options = response.json().get("travel_options", [])
    logger.info(f"Received {len(travel_options)} travel options from Expedia")
    return travel_options
