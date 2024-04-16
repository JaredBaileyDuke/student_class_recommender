import chromadb

from constants import CHROMA_HOST, CHROMA_PORT, CHROMA_COLLECTION_NAME, COURSE_RECOMMENDATION_PROMPT
from util import clean_text, get_formatted_key_value_pairs, get_response_from_llm, get_unique_values_from_dict

def get_chroma_db_collection():
    """
    Function to get the ChromaDB collection.

    Returns:
        chromadb.Collection: The ChromaDB collection.
    """
    # Creating a ChromaDB client
    chroma_client = chromadb.HttpClient(f"{CHROMA_HOST}:{CHROMA_PORT}")

    # Getting the collection from the ChromaDB client
    course_collection = chroma_client.get_collection(CHROMA_COLLECTION_NAME)

    return course_collection


def perform_search(query: str, course_collection: chromadb.Collection = None, num_results: int = 10):
    """
    Function to perform a search in the ChromaDB collection.

    Args:
        query (str): The query to search for.
        course_collection (chromadb.Collection, optional): The ChromaDB collection to search in. Defaults to None.
        num_results (int, optional): The number of results to return. Defaults to 15.

    Returns:
        dict: The search results.
    """
    # Performing the search in the ChromaDB collection
    search_results = course_collection.query(
        query_texts=[query],
        n_results=num_results
    )

    return search_results


if __name__ == "__main__":
    # Defining the demo profile details
    demo_profile_details = {
        "Field_Of_Study": "Computer Science",
        "Primary_Hobby": "Glassblowing",
        "Secondary_Hobby": "Model Building",
        "Gender": "Female",
        "Desired_Career_Field": "Machine Learning Engineer",
        "Country_Of_Origin": "Norway",
    }

    # Formatting the demo profile details
    demo_profile_details_formatted = get_formatted_key_value_pairs(
        demo_profile_details
    )

    # Getting the unique values from the demo profile details
    search_phrase = get_unique_values_from_dict(demo_profile_details)

    # Cleaning the search phrase
    search_phrase = clean_text(str(search_phrase))

    # Getting the ChromaDB collection
    course_collection = get_chroma_db_collection()

    # Performing the search in the ChromaDB collection
    search_results = perform_search(search_phrase, course_collection)

    # Getting the metadata from the search results
    metadata_list = search_results.get("metadatas", [])
    if len(metadata_list) >= 1:
        metadata_list = metadata_list[0]

    # Formatting the course list
    courses_list_formatted = ""
    for metadata in metadata_list:
        courses_list_formatted += f"{metadata['display_text']}\n\n"
    courses_list_formatted = courses_list_formatted.strip()

    # Formatting the course recommendation prompt
    course_recommendation_prompt = COURSE_RECOMMENDATION_PROMPT.format(
        formatted_background_and_interests=demo_profile_details,
        formatted_course_list=courses_list_formatted
    )

    # Getting the response from the language model
    response = get_response_from_llm(course_recommendation_prompt)

    # Printing the response
    print("\n"+response)