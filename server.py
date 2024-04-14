from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from constants import COURSE_RECOMMENDATION_PROMPT
from scripts.query_vector_db import get_chroma_db_collection, perform_search
from util import clean_text, get_formatted_key_value_pairs, get_response_from_llm, get_unique_values_from_dict

# Get the chroma database collection
__chroma_collection__ = get_chroma_db_collection()

# Create a FastAPI instance
app = FastAPI()

# Add CORS middleware to the FastAPI instance
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)


# Health Check endpoint
@app.get("/")
async def health_check():
    """
    Health check endpoint. Returns a simple JSON response to indicate that the server is running.
    """
    return {"ping": "pong"}


@app.post("/recommend-courses/")
async def recommend_courses(req: Request):
    """
    Endpoint to recommend courses based on the user's profile. The profile is sent as a JSON payload in the request.

    Args:
        req (Request): The request object containing the user's profile.

    Returns:
        dict: The response from the language model.
    """
    # Get the user's profile from the request
    profile_dict = await req.json()

    # Format the profile details
    profile_details_formatted = get_formatted_key_value_pairs(profile_dict)

    # Get the unique values from the profile dict and clean the text
    search_phrase = get_unique_values_from_dict(profile_dict)
    search_phrase = clean_text(str(search_phrase))

    # Perform a search in the chroma collection using the search phrase
    search_results = perform_search(search_phrase, __chroma_collection__)

    # Get the metadata from the search results
    metadata_list = search_results.get("metadatas", [])
    if len(metadata_list) >= 1:
        metadata_list = metadata_list[0]

    # Format the courses list
    courses_list_formatted = ""
    for metadata in metadata_list:
        courses_list_formatted += f"{metadata['display_text']}\n\n"
    courses_list_formatted = courses_list_formatted.strip()

    # Format the course recommendation prompt
    course_recommendation_prompt = COURSE_RECOMMENDATION_PROMPT.format(
        formatted_background_and_interests=profile_details_formatted,
        formatted_course_list=courses_list_formatted
    )

    # Get the response from the language model
    response = get_response_from_llm(course_recommendation_prompt)

    return response