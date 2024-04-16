import argparse
from preprocessing_DL import preprocess_workflow
from train_model_DL import training_model_workflow
from test_evaluate_DL import evaluate
from inference_DL import predict

def train_test_model(filepath):
    X_train, X_test, Y_train, Y_test, train_loader, test_loader = preprocess_workflow(filepath=filepath)
    model = training_model_workflow(X_train, Y_train, train_loader)
    test_loss = evaluate(model, test_loader)
    print(f"Test Loss: {test_loss}")

def predictions(new_student):
    keys_to_extract = 'Field_Of_Study', 'Primary_Hobby', 'Secondary_Hobby', 'Desired_Career_Field'
    new_student = {key: new_student.get(key, None) for key in keys_to_extract}
    print(new_student)
    model_path = 'D:/Duke/Sem2/DLA/CourseRecomm/CourseRecom_git/student_class_recommender/models/ncf_model_full.pth'
    top_courses = predict(new_student, model_path)
    print("Recommended Courses:", top_courses)

def main():
    parser = argparse.ArgumentParser(description="Train and test the recommendation model or make predictions.")
    parser.add_argument("--mode", choices=["training", "inference"], required=True, help="Mode of operation: 'training' or 'inference'")
    parser.add_argument("--data", default="D:/Duke/Sem2/DLA/CourseRecomm/CourseRecom_git/student_class_recommender/data/processed/labeled_data_student_to_courseRecomm.csv", help="Path to the training data file")
    parser.add_argument("--Field_Of_Study", type=str, help="New student's field of study")
    parser.add_argument("--Primary_Hobby", type=str, help="New student's primary hobby")
    parser.add_argument("--Secondary_Hobby", type=str, help="New student's secondary hobby")
    parser.add_argument("--Desired_Career_Field", type=str, help="New student's desired career field")
    args = parser.parse_args()

    if args.mode == 'training':
        train_test_model(filepath=args.data)

    elif args.mode == 'inference':
        if not (args.Field_Of_Study and args.Primary_Hobby and args.Secondary_Hobby and args.Desired_Career_Field):
            raise ValueError("All student fields must be provided for inference")
        new_student = {
            'Field_Of_Study': args.Field_Of_Study,
            'Primary_Hobby': args.Primary_Hobby,
            'Secondary_Hobby': args.Secondary_Hobby,
            'Desired_Career_Field': args.Desired_Career_Field
        }
        predictions(new_student)

if __name__ == "__main__":
    main()
