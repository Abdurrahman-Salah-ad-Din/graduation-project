import tensorflow as tf
import numpy as np
from ..base import BaseAIModel
import cv2

class ChestCTTensorFlowClassification(BaseAIModel):
    def __init__(self, model_path, target_size, labels):
        self.model = tf.keras.models.load_model(model_path)
        self.target_size = target_size
        self.labels = labels

    def preprocessing(self, image_path):
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Cannot load {image_path}")
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, self.target_size)
        img = img.astype('float32')
        img = np.expand_dims(img, axis=0)
        return img

    def predict(self, preprocessed_image):
        predictions = self.model.predict(preprocessed_image)[0]
        if self.labels and len(self.labels) == len(predictions):
            return {self.labels[i]: float(predictions[i]) for i in range(len(predictions))}
        return predictions.tolist()