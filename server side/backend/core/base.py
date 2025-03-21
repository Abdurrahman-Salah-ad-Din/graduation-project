import abc
from rest_framework import renderers

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
    
    def run(self, image_path):
        """
        Template method: preprocess the image and then predict.
        """
        preprocessed_image = self.preprocessing(image_path)
        return self.predict(preprocessed_image)

class BaseResponseRenderer(renderers.JSONRenderer):
    """
    Custom JSON renderer that wraps response data in a standardized structure
    with 'is_success', 'data', and 'errors' keys.
    """
    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Override the render method to customize the response format.
        """
        response_data = self._build_response_data(data, renderer_context)
        return super().render(response_data, accepted_media_type, renderer_context)

    def _build_response_data(self, data, renderer_context):
        """
        Construct the response data structure based on the presence of exceptions.
        """
        if renderer_context:
            response = renderer_context.get('response')
            if (response and response.exception) or (not 200 <= response.status_code < 300):
                return {
                    'is_success': False,
                    'data': None,
                    'errors': self._format_errors(data)
                }
            return {
                'is_success': True,
                'data': data,
                'errors': None
            }

    def _flatten_errors(self, errors):
        """
        Recursively flatten nested errors into a flat list of strings.
        """
        flattened = []
        if isinstance(errors, list):
            for error in errors:
                flattened.extend(self._flatten_errors(error))
        elif isinstance(errors, dict):
            for value in errors.values():
                flattened.extend(self._flatten_errors(value))
        else:
            flattened.append(str(errors))
        return flattened

    def _format_errors(self, errors):
        """
        Format the errors to ensure they are returned as a list of strings.
        """
        return self._flatten_errors(errors)