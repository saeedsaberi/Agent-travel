"""
Actions for the chatbot.
"""

import logging
import os
import re

from chatbot.config import SAVE_DIR

from . import (
    ask_user,
    calculate,
    generate_schematic_image,
    query_wikipedia,
    rank_flights_by_price,
    rank_snippets_with_llm,
    rank_travel_plans,
    retrieve_and_rank_travel_plans,
    search_flights,
    search_internet,
    search_tripadvisor,
    summarize_with_llm,
)

# Configure logging
logging.basicConfig(
    filename=os.path.join(SAVE_DIR, "agent_ai_logs.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

KNOWN_ACTIONS = {
    "search_tripadvisor": search_tripadvisor,
    "query_wikipedia": query_wikipedia,
    "calculate": calculate,
    "generate_schematic_image": generate_schematic_image,
    "search_internet": search_internet,
    "ask_user": ask_user,
    "search_flights": search_flights,
    "rank_flights_by_price": rank_flights_by_price,
    "retrieve_and_rank_travel_plans": retrieve_and_rank_travel_plans,
    "summarize_with_llm": summarize_with_llm,
    "rank_travel_plans": rank_travel_plans,
    "rank_snippets_with_llm": rank_snippets_with_llm,
}

ACTION_RE = re.compile(r"^Action: (\w+): (.*)$")
