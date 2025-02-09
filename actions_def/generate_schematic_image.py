import os
import requests
from openai import OpenAI
from chatbot.config import SAVE_DIR, api_config
from typing import Literal

# Define allowed image sizes
SizeType = Literal["256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"]


def generate_schematic_image(description: str, size: SizeType = "1792x1024") -> str:
    """
    Generates a schematic image using DALL-E based on a provided description.

    Parameters:
        description (str): The detailed schematic description.
        size (SizeType): The size of the generated image. Defaults to "1792x1024".

    Returns:
        str: The path to the saved image.

    Raises:
        Exception: If image generation or fetching fails.
    """
    try:
        # Initialize OpenAI client
        api_key = api_config.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("Missing OpenAI API key in configuration.")

        openai_client = OpenAI(api_key=api_key)

        # Generate the image
        image_response = openai_client.images.generate(
            model="dall-e-3",
            prompt=description,
            size=size,
            quality="standard",
            n=1,
        )

        # Extract image URL
        image_url = image_response.data[0].url
        if not image_url:
            raise Exception("OpenAI did not return a valid image URL.")

        # Fetch the generated image
        http_response = requests.get(image_url, timeout=10)
        http_response.raise_for_status()

        # Save the image to a file
        image_path = os.path.join(SAVE_DIR, "schematic_image.png")
        with open(image_path, "wb") as image_file:
            image_file.write(http_response.content)

        return image_path

    except requests.exceptions.RequestException as e:
        raise Exception(f"Network error while fetching image: {e}") from e
    except ValueError as e:
        raise Exception(f"Configuration error: {e}") from e
    except Exception as e:
        raise Exception(f"Unexpected error during image generation: {e}") from e
