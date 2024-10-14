import logging
import httpx


def query_wikipedia(q):
    """
    Queries Wikipedia for the given query and returns the first snippet.

    Parameters:
    - q (str): The query to search on Wikipedia.

    Returns:
    - str: The first snippet from the search results.
    """
    logging.info(f"Querying Wikipedia for: {q}")
    try:
        response = httpx.get(
            "https://en.wikipedia.org/w/api.php",
            params={
                "action": "query",
                "list": "search",
                "srsearch": q,
                "format": "json",
            },
        )
        response.raise_for_status()
        result = response.json()["query"]["search"][0]["snippet"]
        logging.info(f"Found snippet: {result}")
        return result
    except (httpx.RequestError, KeyError) as e:
        logging.error(f"Error querying Wikipedia: {e}")
        return None
