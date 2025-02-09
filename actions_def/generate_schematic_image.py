import logging
import os

import requests  # type: ignore
from openai import OpenAI

from chatbot.config import SAVE_DIR, api_config


def generate_schematic_image(description, size="1792x1024"):
    """
    Use DALL-E to generate a schematic image based on a detailed description.

    Parameters:
    - description: str, the detailed schematic description from GPT-4.

    Returns:
    - str, the path to the saved image.
    """
    logger = logging.getLogger(__name__)
    logger.info("generate_schematic_image")

    client = OpenAI(api_key=api_config["OPENAI_API_KEY"])

    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=description,
            size=size,
            quality="standard",
            n=1,
        )
        print("Response from OpenAI:", response)
        print("Response content:", response.content)
        image_url = response.data[0].url
        print(f"Image URL: {image_url}")

        # Get the image content
        logger.info(f"Fetching image from {image_url}")
        image_response = requests.get(image_url)
        image_response.raise_for_status()  # Raise an exception for bad status codes
        image_content = response.content
        print("Image content:", image_content)
        print("Image content length:", len(image_content))


        # Save the image
        image_path = os.path.join(SAVE_DIR, "schematic_image.png")
        logger.info(f"Saving image to {image_path}")
        with open(image_path, "wb") as image_file:
            image_file.write(image_content)

        # Return the path to the saved image
        return image_path
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching image: {e}")
        raise
    except Exception as e:
        logger.error(f"Error generating schematic image: {e}")
        raise

