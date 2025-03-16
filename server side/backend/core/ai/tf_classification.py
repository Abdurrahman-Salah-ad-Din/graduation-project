import tensorflow as tf
import numpy as np
from PIL import Image
from ..base import BaseAIModel

class TFClassificationModel(BaseAIModel):
    def __init__(self, model_path, target_size, labels):
        self.model = tf.keras.models.load_model(model_path)
        self.target_size = target_size
        self.labels = labels

    def preprocessing(self, image_path):
        image = Image.open(image_path).convert('RGB')
        image = image.resize(self.target_size)
        image_array = np.array(image) / 255.0
        image_array = np.expand_dims(image_array, axis=0)
        return image_array

    def predict(self, preprocessed_image):
        predictions = self.model.predict(preprocessed_image)[0]
        if self.labels and len(self.labels) == len(predictions):
            return {self.labels[i]: float(predictions[i]) for i in range(len(predictions))}
        return predictions.tolist()