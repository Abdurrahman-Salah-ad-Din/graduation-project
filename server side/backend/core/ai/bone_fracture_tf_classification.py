import tensorflow as tf
import numpy as np
from ..base import BaseAIModel
from tensorflow.keras.utils import load_img, img_to_array

class BoneFractureTensorFlowClassification(BaseAIModel):
    def __init__(self, model_path, target_size, labels):
        self.model = tf.keras.models.load_model(model_path)
        self.target_size = target_size
        self.labels = labels

    def preprocessing(self, image_path):
        print(f"here {image_path}")
        img = load_img(image_path, target_size=self.target_size)
        arr = img_to_array(img).astype('float32') / 255.0
        arr = np.expand_dims(arr, axis=0)
        return arr

    def predict(self, preprocessed_image):
        predictions = self.model.predict(preprocessed_image)[0]
        if self.labels and len(self.labels) == len(predictions):
            return {self.labels[i]: float(predictions[i]) for i in range(len(predictions))}
        return predictions.tolist()