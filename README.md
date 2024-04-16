![Image](https://github.com/JaredBaileyDuke/student_class_recommender/blob/main/images/front_end_screenshot_1.png)
![Image](https://github.com/JaredBaileyDuke/student_class_recommender/blob/main/images/front_end_screenshot_2.png)


# AIPI-540 Module 3
This is the repository for the third class module of the AIPI-540 course of the MEng in Artificial Intelligence at Duke University. The module is focused on applying recommendation systems to solve a problem. This project consists of two main parts:
- PyTorch Modeling: Jupyter notebooks that contain the modeling work using PyTorch, including the creation, training, and validation of a the models.
- React Web UI: A Progressive Web App (PWA) built with React that uses TensorFlow.js to load and run the trained model directly in the browser, allowing for real-time course recommendations using students profile.

## Introduction
### Problem
Duke's Master's of Engineering students have a large number of classes to choose from each semester. In addition to reading course titles, they must investigate course descriptions and prerequisite requirements. This is a time consuming process that is open to missing out on interesting courses that the student may be interested in, but not know about.

### Past Work
A lot of previous work has been done to match potential students to colleges. We also found an example of matching students to study abroad opportunities at various universities which involves looking at courses. However, we found a lack of recommender systems to match students with potential classes. Universities depend on students to manually filter and keyword search for potential courses.

### Objective
Simplify the course selection process by implementing a
course recommendation system that is
- Smart
- Intuitive
- Tailored


## Directory Structure
```
.
├── DukeClassRecomm.pdf
├── README.md
├── constants.py
├── data
│   ├── processed
│   │   ├── courses_list.json
│   │   ├── labeled_data_student_to_courseRecomm.csv
│   │   └── user_features.json
│   └── raw
│       ├── Student_Personas_v2.csv
│       ├── courses.csv
│       └── student_personas_v1.csv
├── images
│   ├── front_end_screenshot_1.png
│   └── front_end_screenshot_2.png
├── models
│   └── ncf_model_full.pth
├── notebooks
│   ├── dl-approach-ncf.ipynb
│   ├── naive-bert.ipynb
│   └── non_dl_approach.ipynb
├── requirements.txt
├── scripts
│   ├── inference_DL.py
│   ├── ingest_course_data.py
│   ├── main_DL.py
│   ├── preprocessing_DL.py
│   ├── query_vector_db.py
│   ├── test_evaluate_DL.py
│   └── train_model_DL.py
├── server.py
├── util.py
└── web-ui
    ├── README.md
    ├── package-lock.json
    ├── package.json
    ├── postcss.config.js
    ├── public
    │   ├── favicon.ico
    │   ├── index.html
    │   ├── logo192.png
    │   ├── logo512.png
    │   ├── manifest.json
    │   └── robots.txt
    ├── src
    │   ├── App.js
    │   ├── assets
    │   │   └── countries.json
    │   ├── constants.js
    │   ├── index.css
    │   ├── index.js
    │   ├── ui
    │   │   ├── buttons.jsx
    │   │   ├── input.jsx
    │   │   ├── label.jsx
    │   │   └── multi-step-loader.jsx
    │   └── util
    │       └── cn.js
    └── tailwind.config.js

14 directories, 46 files

```
### Important Directories
- `models`: Store for the trained model
- `scripts`: Store for all the pipeline scripts; Hence, both RAG & NCF. 
- `web-ui/`: The source code for the React-based PWA.


## Training Details
### Data
- As this is a cold start for the recommendation system, we did not have data to work with.
- We created synthetic data of users using Chat-GPT and manual updates, as well as scraped data of Duke graduate level classes. The Chat-GPT data included many duplicates, so we spent time reducing the number of duplicates in the final data set. It can be found in `data\raw`
- We then used BERT (Naive approach) to assign 5 classes to each student. BERT performance was terrible, so we hand labeled the data after before using in a different model -> `data\processed`
- We expect that future improvements to the models could be made using collected student data, as well as collecting student ratings on current recommendations from the current system.

### Models
We implemented 4 models:
- BERT, pretrained (naive)
  - Course embeddings made with BERT pretrained model
  - Student embeddings made with BERT pretrained model
  - Cosine similarity
  - Top 5 courses predicted per student
- TF-IDF (Non-deep learning)
  - Extract course descriptions
  - Stop words removal and lemmatization
  - TF-IDF matix
  - Cosine similarity of student features with course descriptions
  - Top 5 courses predicted per student
- NCF - MLP variant(deep learning)
  - Embed student and course features
  - Train a neural network of 2 fully connected layers and a dense layers
  - Top 5 courses predicted per student
- RAG with Gemini (deep learning)
  - Remove stop words and lemmatization
  - Word embeddings performed in chromadb
  - Gemini pro used with prompt engineering to show top 5 courses, as well as suggested terms to take the courses
  - API exposure for inference
  - React app to showcase results to students

Despite being a simple method, we found powerful performance with the TF-IDF model. If you are resource constrained, this could be a good method for you to use.


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

Check the results with an example:
```bash
python scripts/query_vector_db.py
```

This will show both the RAG and NCF results. 
```bash
python scripts/main_DL.py --mode training
python scripts/main_DL.py --mode inference --Field_Of_Study "Environmental Engineering" --Primary_Hobby "Beekeeping" --Secondary_Hobby "Embroidery" --Desired_Career_Field "Environmental Engineer"
```
To train & get inference of NCF model

## API Endpoints
Recommend courses for a student based on their persona:

```bash
curl 'http://127.0.0.1:6942/recommend-courses/' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Accept-Language: en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7' \
  -H 'Content-Type: application/json' \
  --data-raw '{"field_of_study":"Biomedical Engineering","primary_hobby":"Cycling","secondary_hobby":"Swimming","desired_career_field":"Molecular engineering","gender":"male","country_of_origin":"India"}'
```


## Authors

- [Mrinoy Banerjee](https://www.linkedin.com/in/mrinoy)
- [Samyukta Palle](https://www.linkedin.com/in/sai-samyukta-palle)
- [Abhishek Murthy](https://www.linkedin.com/in/abhishekwl)
- [Jared Bailey](https://www.linkedin.com/in/jared-l-bailey-mba-cpcu-are/)
