import logging

import httpx

from chatbot.config import api_config, other_params
from actions_def.rank_snippets_with_llm import rank_snippets_with_llm
from actions_def.summarize_with_llm import summarize_with_llm
from typing import List

def search_internet(context: str, query: str, max_pages: int = other_params["max_pages"]) -> str:
    """
    Perform an internet search using the Bing Search API, retrieve up to max_pages,
    rank the results, and summarize them using GPT-4.

    Args:
        context (str): The context of the search query
        query (str): The search query
        max_pages (int): The maximum number of pages to retrieve (default: 5)

    Returns:
        str: A summary of the top-ranked search results
    """
    bing_api_key = api_config["bing_API_KEY"]
    bing_url = api_config["bing_url"]
    headers = {"Ocp-Apim-Subscription-Key": bing_api_key}

    search_results:List[str] = []

    for page in range(max_pages):
        start = page * 10 + 1  # Bing returns 10 results per page
        response = httpx.get(bing_url, params={"q": query, "offset": start}, headers=headers)

        if response.status_code == 200:
            search_results.extend(
                item.get("snippet", "No snippet available")
                for item in response.json()["webPages"]["value"]
            )
        else:
            logging.error(
                f"Error: Unable to retrieve search results. Status code {response.status_code} - {response.text}"
            )
            return f"Error: Unable to retrieve search results. Status code {response.status_code} - {response.text}"

    if search_results:
        ranked_snippets = rank_snippets_with_llm(context, search_results)
        full_text = "\n".join(ranked_snippets)
        summary = summarize_with_llm(context, full_text)
        return summary
    else:
        logging.warning("No relevant search results found.")
        return "No relevant search results found."

