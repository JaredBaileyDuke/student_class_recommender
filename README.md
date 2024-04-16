# AIPI-540 Module 3
This is the repository for the third class module of the AIPI-540 course of the MEng in Artificial Intelligence at Duke University. The module is focused on applying recommendation systems to solve a problem.

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
- BERT, not finetuned (naive)
- TF-IDF (Non-deep learning)
- NCF (deep learning)
- RAG with Gemini (deep learning)

Despite being a simple method, we found powerful performance with the TF-IDF model. If you are resource constrained, this could be a good method for you to use.

## Running the Code

## Authors
* [Mrinoy Banerjee](https://www.linkedin.com/in/mrinoy)
* [Samyukta Palle](https://www.linkedin.com/in/sai-samyukta-palle)
* [Abhishek Murthy](https://www.linkedin.com/in/abhishekwl)
* [Jared Bailey](https://www.linkedin.com/in/jared-l-bailey-mba-cpcu-are/)