import argparse

# Import custom modules for each stage of the deep learning process
from scripts.preprocessing_DL import preprocess_workflow
from scripts.train_model_DL import training_model_workflow
from scripts.test_evaluate_DL import evaluate
from scripts.inference_DL import predict

def train_test_model(filepath):
    """
    Trains and evaluates a deep learning model using the provided dataset filepath.
    
    Handles the complete workflow from data preprocessing, model training, to model evaluation.
    It retrieves training and testing data, trains the model, and then evaluates its performance on the test set.
    
    Args:
        filepath (str): The path to the dataset file to be used for training and testing.
    
    Returns:
        None: Outputs the test loss directly to the console.
    """
    # Preprocess the data and get data loaders for both training and testing
    X_train, X_test, Y_train, Y_test, train_loader, test_loader = preprocess_workflow(filepath=filepath)
    # Train the model using the preprocessed data and training data loader
    model = training_model_workflow(X_train, Y_train, train_loader)
    # Evaluate the trained model using the testing data loader
    test_loss = evaluate(model, test_loader)
    # Print out the test loss to console
    print(f"Test Loss: {test_loss}")

def predictions(new_student):
    """
    Generates predictions for course recommendations based on the attributes of a new student.
    
    This function filters the necessary attributes from the new student's data,
    loads the trained model, and predicts top courses that suit the student's profile.
    
    Args:
        new_student (dict): A dictionary containing new student's attributes such as field of study, hobbies, and desired career field.
    
    Returns:
        None: Outputs the recommended courses directly to the console.
    """
    # Keys to extract relevant information from new student data
    keys_to_extract = 'Field_Of_Study', 'Primary_Hobby', 'Secondary_Hobby', 'Desired_Career_Field'
    # Create a dictionary for the student's data, extracting only necessary fields
    new_student = {key: new_student.get(key, None) for key in keys_to_extract}
    # Print filtered student data
    print(new_student)
    # Path to the trained model
    model_path = 'models/ncf_model_full.pth'
    # Predict courses using the inference function and print them
    top_courses = predict(new_student, model_path)
    print("Recommended Courses:", top_courses)

def main():
    """
    Main function to handle command line arguments for either training the model or making predictions.
    
    Sets up command line arguments for operation mode, data file path, and new student attributes for inference.
    Depending on the operation mode selected, it either trains/tests the model or makes predictions based on new student data.
    
    Returns:
        None
    """
    # Define and parse command line arguments
    parser = argparse.ArgumentParser(description="Train and test the recommendation model or make predictions.")
    parser.add_argument("--mode", choices=["training", "inference"], required=True, help="Mode of operation: 'training' or 'inference'")
    parser.add_argument("--data", default="data/processed/labeled_data_student_to_courseRecomm.csv", help="Path to the training data file")
    parser.add_argument("--Field_Of_Study", type=str, help="New student's field of study")
    parser.add_argument("--Primary_Hobby", type=str, help="New student's primary hobby")
    parser.add_argument("--Secondary_Hobby", type=str, help="New student's secondary hobby")
    parser.add_argument("--Desired_Career_Field", type=str, help="New student's desired career field")
    args = parser.parse_args()

    # Execute the appropriate function based on the mode argument
    if args.mode == 'training':
        train_test_model(filepath=args.data)
    elif args.mode == 'inference':
        # Ensure all necessary fields are provided for inference
        if not (args.Field_Of_Study and args.Primary_Hobby and args.Secondary_Hobby and args.Desired_Career_Field):
            raise ValueError("All student fields must be provided for inference")
        # Create a dictionary for the new student data
        new_student = {
            'Field_Of_Study': args.Field_Of_Study,
            'Primary_Hobby': args.Primary_Hobby,
            'Secondary_Hobby': args.Secondary_Hobby,
            'Desired_Career_Field': args.Desired_Career_Field
        }
        predictions(new_student)

if __name__ == "__main__":
    main()
