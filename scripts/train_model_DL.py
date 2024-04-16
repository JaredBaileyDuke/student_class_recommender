import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.optim import Adam


class NCFModel(nn.Module):
    """
    Neural Collaborative Filtering (NCF) model for recommendation systems.

    This class implements a neural network for predicting user-item interactions.
    It uses two fully connected layers and outputs probabilities of interactions
    between users and items using a sigmoid activation function.

    Attributes:
        fc1 (torch.nn.Linear): First fully connected layer.
        fc2 (torch.nn.Linear): Second fully connected layer.
        output (torch.nn.Linear): Output layer that predicts interaction probabilities.
    """

    def __init__(self, num_users_features, num_courses):
        """
        Initializes the NCFModel with two hidden layers and an output layer.

        Args:
            num_users_features (int): Number of features in the input dataset.
            num_courses (int): Number of courses or items in the recommendation system.
        """
        super(NCFModel, self).__init__()
        self.fc1 = nn.Linear(num_users_features, 128)
        self.fc2 = nn.Linear(128, 64)
        self.output = nn.Linear(64, num_courses)

    def forward(self, x):
        """
        Forward pass through the network.

        Args:
            x (torch.Tensor): Input tensor containing features of users.

        Returns:
            torch.Tensor: Output tensor containing predicted probabilities of interactions.
        """
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        # Using sigmoid since this is a binary classification
        x = torch.sigmoid(self.output(x))
        return x


def training_model_workflow(X_train, Y_train, train_loader):
    """
    Trains the NCF model using the provided training data loader.

    Args:
        X_train (numpy.array): Training data features.
        Y_train (numpy.array): Training data labels.
        train_loader (torch.utils.data.DataLoader): DataLoader for training data.

    Returns:
        torch.nn.Module: Trained model.
    """

    # Initialize the model
    model = NCFModel(X_train.shape[1], Y_train.shape[1])
    optimizer = Adam(model.parameters(), lr=0.01)
    criterion = nn.BCELoss()
    print("Initialized the model parameters")

    def train(model, loader, optimizer, criterion):
        """
        Training process for a single epoch.

        Args:
            model (torch.nn.Module): The model being trained.
            loader (torch.utils.data.DataLoader): DataLoader for the data.
            optimizer (torch.optim.Optimizer): Optimizer for updating model weights.
            criterion (torch.nn.Module): Loss function used for training.

        Returns:
            float: Average loss for this training epoch.
        """
        model.train()
        total_loss = 0
        for features, labels in loader:
            optimizer.zero_grad()
            outputs = model(features)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        return total_loss / len(loader)

    # Training loop
    for epoch in range(50):
        train_loss = train(model, train_loader, optimizer, criterion)
        print(f"Epoch {epoch+1}, Loss: {train_loss}")

    # Save model
    torch.save(model, 'models/ncf_model_full.pth')
    print("Saved the model!")
    return model
