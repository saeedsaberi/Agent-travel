def search_internet(context, query, max_pages=other_params["max_pages"]):
    """
    Perform an internet search using the Bing Search API, retrieve up to max_pages,
    rank the results, and summarize them using GPT-4.

    Parameters:
    - query: str, the search query
    - max_pages: int, the maximum number of pages to retrieve

    Returns:
    - str, a summary of the top-ranked search results.
    """
    logging.info("search_internet")
    bing_API_KEY = api_config["bing_API_KEY"]
    bing_url = api_config["bing_url"]
    headers = {"Ocp-Apim-Subscription-Key": bing_API_KEY}

    snippets = []

    for page in range(max_pages):
        start = page * 10 + 1  # Bing returns 10 results per page
        response = httpx.get(
            bing_url, params={"q": query, "offset": start}, headers=headers
        )

        if response.status_code == 200:
            logging.debug(f"Received page {page} of search results")
            search_results = response.json()

            if "webPages" in search_results and "value" in search_results["webPages"]:
                page_snippets = [
                    item.get("snippet", "No snippet available")
                    for item in search_results["webPages"]["value"]
                ]
                snippets.extend(page_snippets)
            else:
                logging.warning(f"No search results found on page {page}")
                break  # No more pages or no results found
        else:
            logging.error(
                f"Error: Unable to retrieve search results. Status code {response.status_code}"
            )
            return f"Error: Unable to retrieve search results. Status code {response.status_code} - {response.text}"

    if snippets:
        # Rank the snippets before summarizing
        logging.info("Ranking snippets")
        ranked_snippets = rank_snippets_with_llm(context, snippets)
        full_text = "\n".join(ranked_snippets)

        # Summarize the content using GPT-4
        logging.info("Summarizing content")
        summary = summarize_with_llm(context, full_text)
        return summary
    else:
        logging.warning("No relevant search results found.")
        return "No relevant search results found."
