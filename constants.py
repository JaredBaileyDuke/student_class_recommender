import os

# Vector DB
CHROMA_HOST = os.environ.get('CHROMA_HOST', 'http://127.0.0.1')
CHROMA_PORT = os.environ.get('CHROMA_PORT', 8000)
CHROMA_COLLECTION_NAME = "courses"

# API keys
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', "")

# Prompt templates
COURSE_RECOMMENDATION_PROMPT = """
You are the program coordinator, student counsellor and course management expert for graduate courses.
You are an expert at recommending relevant courses to students based on their backgrounds and interests.

Output the results in the same format as the course list provided.
Include prerequisites for the course if available.
Group courses by program. For each program, list the courses in the order of their catalog number.
Let the title of the group be the program name.
Every list point under it should be of the form: "Course Name (Course Code) - Course Title\nCourse Description\n (Prerequisites if any)".

Do not remove any details from course details while generating the output.
Render the results in a list and not a table.
Fix any typos or grammatical errors in the course details as you parse them.

In the end, add another section to the output called recommended order indicating in which course they should take in which semester (spring/summer/fall).
It is currently Spring semester.

My background and interests are as follows:
{formatted_background_and_interests}

These are the courses that came up when I searched for the phrase: "security".
Out of these, give me the top 10 most relevant courses that align with my background and interests.

Courses:
{formatted_course_list}
"""