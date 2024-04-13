import csv
import chromadb

from tqdm.auto import tqdm

from constants import CHROMA_HOST, CHROMA_PORT, CHROMA_COLLECTION_NAME
from util import clean_text

def get_formatted_course_details_list(course_data_csv_path):
    """
    Function to read a CSV file containing course data and format it into a list of dictionaries.

    Args:
        course_data_csv_path (str): Path to the CSV file containing the course data.

    Returns:
        list: A list of dictionaries, each representing a course and its details.
    """
    course_details_list = []
    with open(course_data_csv_path, 'r', encoding="cp1252") as course_data_file:
        course_data_reader = csv.DictReader(course_data_file)
        for row in course_data_reader:
            # Extracting course details from the row
            unformatted_subject = row.get("Subject", "").strip()
            unformatted_title = row.get("Course Title", "").strip()
            unformatted_catalog_number = row.get("Catalog Number", "").strip()
            unformatted_course_type = row.get("Course Type", "").strip()
            unformatted_description = row.get("Description", "").strip()
            unformatted_grading = row.get("Grading", "").strip()
            unformatted_prerequisites = row.get("Prerequisites", "").strip()
            if len(unformatted_prerequisites) == 0:
                unformatted_prerequisites = "None"
            display_text = f"Subject: {unformatted_subject}\nTitle: {unformatted_title}\nCatalog Number: {unformatted_catalog_number}\nCourse Type: {unformatted_course_type}\nDescription: {unformatted_description}\nGrading: {unformatted_grading}\nPrerequisites: {unformatted_prerequisites}"

            # Formatting the extracted course details
            subject = row.get("Subject", "").strip().lower()
            title = row.get("Course Title", "").strip().lower()
            catalog_number = row.get("Catalog Number", "").strip().lower()
            course_type = row.get("Course Type", "").strip().lower().replace("-", " ")
            description = row.get("Description", "").strip().lower()
            keywords = row.get("Keywords", "").strip().lower()
            grading = row.get("Grading", "").strip().lower()
            prerequisites = row.get("Prerequisites").strip().lower()

            # Cleaning the formatted course details
            subject = clean_text(subject)
            title = clean_text(title)
            catalog_number = clean_text(catalog_number)
            course_type = clean_text(course_type)
            description = clean_text(description)
            keywords = clean_text(keywords)
            grading = clean_text(grading)
            prerequisites = clean_text(prerequisites)
            if len(prerequisites) == 0:
                prerequisites = "None"

            # Creating a dictionary of the cleaned course details
            formatted_course_dict = {
                "subject": subject,
                "title": title,
                "catalog_number": catalog_number,
                "course_type": course_type,
                "description": description,
                "keywords": keywords,
                "grading": grading,
                "prerequisites": prerequisites,
                "display_text": display_text
            }
            course_details_list.append(formatted_course_dict)

    return course_details_list


def ingest_course_details_into_vector_db(course_details_list):
    """
    Function to ingest the course details into a vector database.

    Args:
        course_details_list (list): A list of dictionaries, each representing a course and its details.
    """
    # Creating a ChromaDB client
    chroma_client = chromadb.HttpClient(f"{CHROMA_HOST}:{CHROMA_PORT}")

    # Getting or creating a collection in the vector database
    course_collection = chroma_client.get_or_create_collection(
        CHROMA_COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}  # l2 is the default
    )

    # Ingesting the course details into the vector database
    for course in tqdm(course_details_list):
        # Extracting course details from the course dictionary
        subject = course["subject"]
        title = course["title"]
        catalog_number = course["catalog_number"]
        course_type = course["course_type"]
        description = course["description"]
        keywords = course["keywords"]
        grading = course["grading"]
        prerequisites = course["prerequisites"]

        # Creating a document from the course details
        doc = f"Subject: {subject}\nTitle: {title}\nCatalog Number: {catalog_number}\nCourse Type: {course_type}\nDescription: {description}\nKeywords: {keywords}\nGrading: {grading}\nPrerequisites: {prerequisites}"
        doc_id = str(hash(frozenset(course.items())))
        doc_metadata = course

        # Adding the document to the vector database
        try:
            course_collection.add(
                documents=[doc],
                ids=[doc_id],
                metadatas=[doc_metadata]
            )
        except Exception as ex:
            print(ex)

    print("[+] Ingestion into vector database completed.")


if __name__ == '__main__':
    # Getting the formatted course details list
    course_details_list = get_formatted_course_details_list(
        "data/raw/courses.csv"
    )

    # Ingesting the course details into the vector database
    ingest_course_details_into_vector_db(course_details_list)