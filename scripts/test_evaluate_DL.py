import torch
import torch.nn as nn

def evaluate(model, loader):
    """
    Evaluate the trained model using a data loader.

    This function computes the average loss of the model across all batches in the provided data loader.

    Args:
    model (torch.nn.Module): The trained model to be evaluated.
    loader (torch.utils.data.DataLoader): DataLoader containing test/validation data.

    Returns:
    float: The average loss of the model on the provided data.
    """

    # Initialize the binary cross-entropy loss function
    criterion = nn.BCELoss()

    # Set the model to evaluation mode
    model.eval()

    # Initialize total loss accumulator
    total_loss = 0

    # Disable gradient calculations for efficiency
    with torch.no_grad():
        for features, labels in loader:
            # Generate predictions
            outputs = model(features)

            # Calculate loss between the predicted and actual values
            loss = criterion(outputs, labels)

            # Accumulate the batch loss
            total_loss += loss.item()

    # Calculate average loss over all batches
    average_loss = total_loss / len(loader)

    return average_loss