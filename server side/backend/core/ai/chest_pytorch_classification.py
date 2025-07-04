from ..base import BaseAIModel
from torchvision.models import densenet121
import torch
import numpy as np
import random
from torchvision import transforms
from PIL import Image

seed = 42
torch.manual_seed(seed)
np.random.seed(seed)
random.seed(seed)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False

class CheXNet(torch.nn.Module):
    def __init__(self, num_classes=14):
        super().__init__()
        self.densenet121 = densenet121(pretrained=False)
        num_features = self.densenet121.classifier.in_features
        # ONE Sequential layer (matches "classifier.0" keys)
        self.densenet121.classifier = torch.nn.Sequential(
            torch.nn.Linear(num_features, num_classes)
        )
        
    def forward(self, x):
        return self.densenet121(x)

class ChestPytorchClassification(BaseAIModel):
    def __init__(self, model_path, target_size, labels):
        self.model_path = model_path
        self.target_size = target_size
        self.labels = labels
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def preprocessing(self, image_path):
        image = Image.open(image_path).convert('RGB')
        preprocess = transforms.Compose([
            transforms.Resize(self.target_size[0]),
            transforms.CenterCrop(self.target_size[0]),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
        return preprocess(image).unsqueeze(0).to(self.device)

    def predict(self, preprocessed_image):
        model = CheXNet(num_classes=14).to(self.device)
        state_dict = torch.load(self.model_path, map_location=self.device)

        new_state_dict = {}
        for k, v in state_dict.items():
            new_k = k.replace("densenet.", "densenet121.").replace("classifier.0", "classifier.0")
            new_state_dict[new_k] = v
            
        model.load_state_dict(new_state_dict, strict=True)  
        model.eval()

        with torch.no_grad():
            outputs = torch.sigmoid(model(preprocessed_image))
        predictions = outputs.cpu().numpy()[0]
        if self.labels and len(self.labels) == len(predictions):
            return {self.labels[i]: float(predictions[i]) for i in range(len(predictions))}
        return predictions.tolist()