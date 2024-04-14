# AIPI-540 Module 3
This is the repository for the third class module of the AIPI-540 course of the MEng in Artificial Intelligence at Duke University. The module is focused on applying recommendation systems to solve a problem.

## Description
A lot of previous work has been done to match potential students to colleges. We also found an example of matching students to study abroad opportunities at various universities. However, we found a lack of using recommender systems to match students with potential classes, outside of manually filtering and keyword search.
This project matches Duke Engineering students with potential classes they can consider taking.

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
We created synthetic data of users using Chat-GPT and manual updates, as well as scraped data of Duke graduate level classes.
We then used BERT to assign 5 classes to each student. BERT performance was terrible, so we hand labeled the data after.
We expect that future improvements could be made using collected student data.

## Running the Code

## Authors
* [Mrinoy Banerjee](https://www.linkedin.com/in/mrinoy)
* [Samyukta Palle](https://www.linkedin.com/in/sai-samyukta-palle)
* [Abhishek Murthy](https://www.linkedin.com/in/abhishekwl)
* [Jared Bailey](https://www.linkedin.com/in/jared-l-bailey-mba-cpcu-are/)