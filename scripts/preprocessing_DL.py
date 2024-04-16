import pandas as pd
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
import json

class DataProcessor:
    """
    Class to handle data preprocessing tasks for a recommendation system dataset.
    This class handles the generation of user and course features and splits the dataset into training and testing sets.
    """

    def __init__(self, filepath):
        """
        Initializes the DataProcessor class by loading the data from a specified CSV file path.
        
        Args:
            filepath (str): The path to the CSV file containing the dataset.
        """
        self.df = pd.read_csv(filepath)
        print("Data loaded successfully.")

    def preprocess_courses(self):
        """
        Processes course recommendations from the dataset to create binary columns for each unique course.
        
        Returns:
            pd.DataFrame: A DataFrame with added binary columns for each course, indicating course recommendations.
        """
        courses_list = set()
        for recommendations in self.df['Recommendations']:
            courses = [course.strip().replace("'", "") for course in recommendations.strip("[]").split(",")]
            courses_list.update(courses)
        
        self.courses_list = list(courses_list)
        with open('D:/Duke/Sem2/DLA/CourseRecomm/CourseRecom_git/student_class_recommender/data/processed/courses_list.json', 'w') as file:
            json.dump(self.courses_list, file, indent=4)

        # Create binary features for each course
        for course in self.courses_list:
            self.df[course] = self.df['Recommendations'].apply(lambda x: int(course in x))

        print("Course features created.")
        return self.df

    def preprocess_user_features(self):
        """
        Converts categorical user features into a format suitable for modeling (one-hot encoding).
        
        Returns:
            pd.DataFrame: A DataFrame with one-hot encoded user features.
        """
        feature_columns = ['Field_Of_Study', 'Primary_Hobby', 'Secondary_Hobby', 'Desired_Career_Field']
        user_features_df = pd.get_dummies(self.df[feature_columns])
        user_features = user_features_df.columns.tolist()

        with open('D:/Duke/Sem2/DLA/CourseRecomm/CourseRecom_git/student_class_recommender/data/processed/user_features.json', 'w') as file:
            json.dump(user_features, file, indent=4)

        print("User features processed.")
        return user_features_df

    def split_data(self, features, labels):
        """
        Splits the data into training and testing sets.
        
        Args:
            features (pd.DataFrame): The feature DataFrame.
            labels (pd.DataFrame): The labels DataFrame.
        
        Returns:
            tuple: A tuple containing training and testing datasets for both features and labels.
        """
        X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)
        print("Data split into train and test sets.")
        return X_train, X_test, y_train, y_test
    

class CustomDataset(Dataset):
    """
    A class to create PyTorch datasets from provided features and labels for model training and evaluation.
    """
    def __init__(self, features, labels):
        """
        Initialize the dataset with features and labels.

        Args:
            features (pd.DataFrame): The DataFrame containing input features.
            labels (pd.DataFrame): The DataFrame containing labels for the input features.
        """
        self.features = torch.tensor(features.values, dtype=torch.float32)
        self.labels = torch.tensor(labels.values, dtype=torch.float32)

    def __len__(self):
        """Return the total number of samples in the dataset."""
        return len(self.features)

    def __getitem__(self, idx):
        """
        Retrieve a single item from the dataset.

        Args:
            idx (int): The index of the item to retrieve.

        Returns:
            tuple: A tuple containing the feature and label tensors for the specified index.
        """
        return self.features[idx], self.labels[idx]

def preprocess_workflow(filepath):
    """
    Handles the complete preprocessing workflow including data loading, processing,
    dataset creation, and dataloader preparation.

    Args:
        filepath (str): Path to the CSV file containing the dataset.

    Returns:
        tuple: Contains train and test splits for features and labels, and DataLoaders for both.
    """
    # Initialize the data processor and preprocess data
    processor = DataProcessor(filepath)
    df_with_courses = processor.preprocess_courses()
    user_features_df = processor.preprocess_user_features()
    labels = df_with_courses[processor.courses_list]

    # Split the data
    X_train, X_test, Y_train, Y_test = processor.split_data(user_features_df, labels)

    # Create PyTorch datasets
    train_dataset = CustomDataset(X_train, Y_train)
    test_dataset = CustomDataset(X_test, Y_test)
    print("Datasets for training and testing have been created.")

    # Prepare DataLoaders
    train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=16, shuffle=False)
    print("DataLoaders for training and testing have been prepared.")

    return X_train, X_test, Y_train, Y_test, train_loader, test_loader


