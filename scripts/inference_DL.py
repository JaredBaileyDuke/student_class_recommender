import pandas as pd
import torch
import numpy as np
import json

def predict(new_student, model_path):
    """
    Predict the top 5 course recommendations for a new student.

    Args:
    new_student (dict): A dictionary containing the new student's features.
    model_path (str): The path to the trained neural collaborative filtering model.

    Returns:
    list: A list of the top 5 recommended courses for the new student.
    """
    print(new_student)
    # Load user features from JSON file as a list
    with open('D:/Duke/Sem2/DLA/CourseRecomm/CourseRecom_git/student_class_recommender/data/processed/user_features.json', 'r') as f:
        user_features_cols = json.load(f)

    # Load courses list from JSON file as a list
    with open('D:/Duke/Sem2/DLA/CourseRecomm/CourseRecom_git/student_class_recommender/data/processed/courses_list.json', 'r') as f:
        courses_list = json.load(f)

    # Create a DataFrame for the new student with all columns initialized to zero
    new_student_df = pd.DataFrame(0, index=[0], columns=user_features_cols)

    # Update the DataFrame with new student data by setting the appropriate fields
    for key in new_student:
        feature_name = key + "_" + new_student[key]
        if feature_name in new_student_df.columns:
            new_student_df.loc[0, feature_name] = 1

    # Convert the DataFrame to a PyTorch tensor
    new_student_tensor = torch.tensor(new_student_df.values.astype(np.float32))

    # Load the model and set it to evaluation mode
    model = torch.load(model_path)
    model.eval()

    # Perform prediction using the model
    with torch.no_grad():
        predictions = model(new_student_tensor)

    # Convert the model's predictions to probabilities
    course_probabilities = predictions.numpy().flatten()

    # Identify the indices of the top 5 courses
    top_course_indices = np.argsort(course_probabilities)[-5:][::-1]

    # Map indices to course names
    top_courses = [courses_list[idx] for idx in top_course_indices]

    return top_courses