import re
import nltk
import google.generativeai as genai

from google.generativeai.types import HarmCategory, HarmBlockThreshold

# Local
from constants import GEMINI_API_KEY

# Define safety settings for the generative model
safety_settings = {
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
}

# Initialize the generative model with the defined safety settings
__llm_model__ = genai.GenerativeModel(
    "gemini-pro",
    safety_settings=safety_settings,
)

# Download the stopwords from nltk
nltk.download('stopwords')

# Configure the generative model with the API key
genai.configure(api_key=GEMINI_API_KEY)


def remove_special_chars(text):
    """
    Function to remove special characters from a given text.

    Args:
        text (str): The text to remove special characters from.

    Returns:
        str: The text with special characters removed.
    """
    return re.sub(r'[^a-zA-Z0-9\s]', '', text)


def remove_stop_words_from_text(text):
    """
    Function to remove stop words from a given text.

    Args:
        text (str): The text to remove stop words from.

    Returns:
        str: The text with stop words removed.
    """
    stop_words = set(nltk.corpus.stopwords.words('english'))
    words = text.split(" ")
    words = [word for word in words if word not in stop_words]
    return " ".join(words)


def clean_text(text):
    """
    Function to clean a given text by removing special characters, stop words, and extra spaces.

    Args:
        text (str): The text to clean.

    Returns:
        str: The cleaned text.
    """
    text = text.strip().lower()
    text = remove_special_chars(text)
    text = remove_stop_words_from_text(text)
    text = text.strip()
    # Replace 1 or more spaces with single semicolon
    text = re.sub(r' +', ' ', text)
    text = text.strip()
    return text


def get_formatted_key_value_pairs(data: dict):
    """
    Function to format a dictionary into a string of key-value pairs.

    Args:
        data (dict): The dictionary to format.

    Returns:
        str: The formatted string of key-value pairs.
    """
    formatted_pairs = []
    for key, value in data.items():
        key = key.replace("_", " ")
        formatted_pairs.append(f"{key}: {value}")
    formatted_pairs = "\n".join(formatted_pairs)
    formatted_pairs = formatted_pairs.strip()
    return formatted_pairs


def get_unique_values_from_dict(data: dict):
    """
    Function to get the unique values from a dictionary.

    Args:
        data (dict): The dictionary to get the unique values from.

    Returns:
        set: The set of unique values.
    """
    unique_values = set()
    for _, value in data.items():
        unique_values.add(value)
    return unique_values


def get_response_from_llm(prompt: str):
    """
    Function to get a response from the language model.

    Args:
        prompt (str): The prompt to generate a response for.

    Returns:
        str: The generated response.
    """
    response = __llm_model__.generate_content(prompt)
    response = response.text.strip()
    return response
