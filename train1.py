import os
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import models, transforms
from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder

# Define the transformations with data augmentation
transform_train = transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(degrees=30),
    transforms.RandomVerticalFlip(),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

transform_test = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Load your emotion dataset using ImageFolder
train_dataset = ImageFolder('C:\\Users\\MEGHNA\\Downloads\\spotify3\\song\\archive\\train', transform=transform_train)
test_dataset = ImageFolder('C:\\Users\\MEGHNA\\Downloads\\spotify3\\song\\archive\\test', transform=transform_test)


# Use DataLoader for batch processing
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

# Load a pre-trained ResNet model
resnet = models.resnet18(pretrained=True)

# Modify the output layer for your emotion classes
num_emotions = len(train_dataset.classes)
resnet.fc = nn.Linear(resnet.fc.in_features, num_emotions)

# Use GPU if available
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
resnet.to(device)

# Define loss function and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(resnet.parameters(), lr=0.0001, weight_decay=0.0005)

num_epochs = 40
best_accuracy = 0.0

for epoch in range(num_epochs):
    resnet.train()
    for inputs, labels in train_loader:
        inputs, labels = inputs.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = resnet(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

    # Save the model after each epoch
    model_save_path = f'third/emotion_resnet_model_epoch_{epoch + 1}.pth'
    torch.save(resnet.state_dict(), model_save_path)
    print(f'Model saved at: {model_save_path}')

    resnet.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for inputs, labels in test_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = resnet(inputs)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    accuracy = correct / total
    print(f'Epoch {epoch + 1}/{num_epochs}, Loss: {loss.item()}, Accuracy: {accuracy}')

    # Save the best model
    if accuracy > best_accuracy:
        best_accuracy = accuracy
        torch.save(resnet.state_dict(), 'third/best_model.pth')

print(f'Best Accuracy: {best_accuracy * 100:.2f}%')