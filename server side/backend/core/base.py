import abc

class BaseAIModel(abc.ABC):
    @abc.abstractmethod
    def preprocessing(self, image_path):
        """
        Load and preprocess the image from the given file path.
        Should return a preprocessed image array.
        """
        pass

    @abc.abstractmethod
    def predict(self, preprocessed_image):
        """
        Run inference on the preprocessed image.
        Should return predictions in a standard format (e.g., a dictionary).
        """
        pass
    
    @abc.abstractmethod
    def run(self, image_path):
        """
        Template method: preprocess the image and then predict.
        """
        preprocessed_image = self.preprocessing(image_path)
        return self.predict(preprocessed_image)