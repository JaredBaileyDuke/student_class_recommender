![Image](https://github.com/JaredBaileyDuke/student_class_recommender/blob/main/images/front_end_screenshot_1.png)
![Image](https://github.com/JaredBaileyDuke/student_class_recommender/blob/main/images/front_end_screenshot_2.png)


# AIPI-540 Module 3

This is the repository for the third class module of the AIPI-540 course of the MEng in Artificial Intelligence at Duke University. The module is focused on applying recommendation systems to solve a problem.

## Description

A lot of previous work has been done to match potential students to colleges. We also found an example of matching students to study abroad opportunities at various universities. However, we found a lack of using recommender systems to match students with potential classes, outside of manually filtering and keyword search.
This project matches Duke Engineering students with potential classes they can consider taking.
Our project matches Duke Engineering students with potential classes they can consider taking in upcoming semesters.

## Problem
Duke's Master's of Engineering students have a large number of classes to choose from each semester. In addition to reading course titles, they must investigate course descriptions and prerequisite requirements. This is a time consuming process that is open to missing out on interesting courses that the student may be interested in, but not know about.

## Past Work
A lot of previous work has been done to match potential students to colleges. We also found an example of matching students to study abroad opportunities at various universities which involves looking at courses. However, we found a lack of recommender systems to match students with potential classes. Universities depend on students to manually filter and keyword search for potential courses.

## Directory Structure

```
.
├── README.md
├── chroma.log
├── constants.py
├── data
│   └── raw
│       ├── courses.csv
│       ├── student_personas_v1.csv
│       └── student_personas_v2.csv
│   └── processed
│       └──labeled_data_student_to_courseRecomm.csv
├── requirements.txt
├── scripts
│   ├── ingest_course_data.py
│   └── query_vector_db.py
├── server.py
└── util.py

4 directories, 11 files
```

## Data

As this is a cold start for the recommendation system, we did not have data to work with.
We created synthetic data of users using Chat-GPT and manual updates, as well as scraped data of Duke graduate level classes. The Chat-GPT data included many duplicates, so we spent time reducing the number of duplicates in the final data set.
We then used BERT (Naive approach) to assign 5 classes to each student. BERT performance was terrible, so we hand labeled the data after before using in a different model.
We expect that future improvements to the models could be made using collected student data, as well as collecting student ratings on current recommendations from the current system.

## Models
We implemented 4 models:
- BERT, pretrained (naive)
- TF-IDF (Non-deep learning)
- NCF (deep learning)
- RAG with Gemini (deep learning)

Despite being a simple method, we found powerful performance with the TF-IDF model. If you are resource constrained, this could be a good method for you to use.

## Pipelines
- BERT
  - Course embeddings made with BERT pretrained model
  - Student embeddings made with BERT pretrained model
  - Cosine similarity
  - Top 5 courses predicted per student
- TF-IDF
  - Extract course decrisptions
  - Stop words removal and lemitization
  - TF-IDF matix
  - Cosine similarity of student features with course descriptions
  - Top 5 courses predicted per student
- NCF
  - Embed student and course features into a matrix
  - Train a neural network of 2 fully connected layers on matrix
  - Top 5 courses predicted per student
- RAG with Gemini
  - Remove stop words and lemmitize
  - Word embeddings performed in chromadb
  - Gemini pro used with prompt engineering to show top 5 courses, as well as suggested terms to take the courses
  - API exposure for inference
  - React app to showcase results to students

## Implementation


First install the required packages using the following command:

```bash
pip install -r requirements.txt
```

To ingest the course data, run the following command:

```bash
python scripts/ingest_course_data.py
```

Run the FastAPI server using:

```bash
uvicorn server:app --host 0.0.0.0 --port 6942 --reload
```

## API Endpoints

Recommend courses for a student based on their persona:

```bash
curl 'http://127.0.0.1:6942/recommend-courses/' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Accept-Language: en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7' \
  -H 'Content-Type: application/json' \
  --data-raw '{"field_of_study":"Biomedical Engineering","primary_hobby":"Cycling","secondary_hobby":"Swimming","desired_career_field":"Molecular engineering","gender":"male","country_of_origin":"India"}'
```

## Implementation

- We've ingested the course data into `chromadb` using the `ingest_course_data.py` script.
- For the inference, we've exposed an API endpoint using FastAPI.
- The API endpoint takes in the student persona as input, performs a query on the vector database and gets the top 10 recommended courses for the student.
- These results are then injected into a smartly crafted prompt and sent to Gemini API (RAG)
- The response from the Gemini API is then returned to the frontend where in it is rendered as markdown

## Authors

- [Mrinoy Banerjee](https://www.linkedin.com/in/mrinoy)
- [Samyukta Palle](https://www.linkedin.com/in/sai-samyukta-palle)
- [Abhishek Murthy](https://www.linkedin.com/in/abhishekwl)
- [Jared Bailey](https://www.linkedin.com/in/jared-l-bailey-mba-cpcu-are/)
