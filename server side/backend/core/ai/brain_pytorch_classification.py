import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
from core.base import BaseAIModel

class BrainPyTorchClassification(BaseAIModel):
    def __init__(self, model_path, target_size, labels):
        self.model_path = model_path
        self.target_size = target_size
        self.labels = labels
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def preprocessing(self, image_path):
        image = Image.open(image_path).convert('RGB')
        preprocess =  transforms.Compose([
            transforms.Resize(self.target_size),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                std=[0.229, 0.224, 0.225])
        ])
        return preprocess(image).unsqueeze(0).to(self.device)

    def predict(self, preprocessed_image):
        model = models.resnet18(pretrained=False)
        num_features = model.fc.in_features
        model.fc = nn.Sequential(
            nn.Linear(num_features, 512),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(512, len(self.labels))
        )
        model.load_state_dict(torch.load(self.model_path, map_location=self.device))
        model.to(self.device).eval()
        with torch.no_grad():
            logits = model(preprocessed_image)
            predictions = torch.softmax(logits, dim=1).cpu().numpy().flatten().tolist()
        if self.labels and len(self.labels) == len(predictions):
            return {self.labels[i]: float(predictions[i]) for i in range(len(predictions))}
        return predictions.tolist()