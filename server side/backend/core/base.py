import abc
from rest_framework import renderers
from .errors import ErrorCodes
from .error_messages import ERROR_MESSAGES

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
        response = renderer_context.get('response') if renderer_context else None

        if response and response.status_code == 204:
            return b''

        response_data = self._build_response_data(data, renderer_context)
        return super().render(response_data, accepted_media_type, renderer_context)

    def _build_response_data(self, data, renderer_context):
        """
        Construct the response data structure based on the presence of exceptions.
        """
        if isinstance(data, dict) and {'is_success','data','errors'}.issubset(data.keys()):
            return data

        if renderer_context:
            response = renderer_context.get('response')
            if (response and response.exception) or (not 200 <= response.status_code < 300):
                return {
                    'is_success': False,
                    'data': None,
                    'errors': self._format_errors(data, response)
                }
            return {
                'is_success': True,
                'data': data,
                'errors': None
            }
        return data

    def _format_errors(self, errors, response=None):
        """
        Format errors with error codes based on the response.
        """
        # If errors is already in our format, return as is
        if isinstance(errors, list) and all(isinstance(e, dict) and 'code' in e for e in errors):
            return errors
            
        formatted_errors = []
        
        # Handle validation errors dict
        if isinstance(errors, dict):
            # Map common DRF fields to our error codes
            field_to_error_code = {
                'email': ErrorCodes.USER_001,
                'first_name': ErrorCodes.USER_002,
                'last_name': ErrorCodes.USER_003,
                'password': ErrorCodes.USER_004,
                'job': ErrorCodes.USER_005,
                'gender': ErrorCodes.USER_006,
                'phone_number': ErrorCodes.USER_007,
                'date_of_birth': ErrorCodes.USER_008,
                # Patient fields
                'patient_email': ErrorCodes.PAT_001,
                'patient_first_name': ErrorCodes.PAT_002,
                'patient_last_name': ErrorCodes.PAT_003,
                'patient_gender': ErrorCodes.PAT_004,
                'patient_date_of_birth': ErrorCodes.PAT_005,
                # Scan fields
                'patient': ErrorCodes.SCAN_001,
                'image_scan_url': ErrorCodes.SCAN_002,
                'organ': ErrorCodes.SCAN_003,
            }
            
            # Authentication errors
            if 'detail' in errors:
                detail = str(errors['detail']).lower()
                if ('authenticated' or 'Unauthorized') in detail:
                    formatted_errors.append({
                        'code': ErrorCodes.PERM_001,
                        'message': ERROR_MESSAGES[ErrorCodes.PERM_001]
                    })
                elif 'No Patient matches the given query.'.lower() in detail:
                    formatted_errors.append({
                        'code': ErrorCodes.PAT_009,
                        'message': ERROR_MESSAGES[ErrorCodes.PAT_009]
                    })
                elif 'permission' in detail:
                    formatted_errors.append({
                        'code': ErrorCodes.PERM_002,
                        'message': ERROR_MESSAGES[ErrorCodes.PERM_002]
                    })
                elif 'credentials' in detail or 'inactive' in detail:
                    formatted_errors.append({
                        'code': ErrorCodes.AUTH_001,
                        'message': ERROR_MESSAGES[ErrorCodes.AUTH_001]
                    })
                else:
                    formatted_errors.append({
                        'code': ErrorCodes.GEN_001,
                        'message': str(errors['detail'])
                    })
            else:
                # Process field errors
                for field, error_msgs in errors.items():
                    if field not in ('detail', 'non_field_errors'):
                        if not isinstance(error_msgs, list):
                            error_msgs = [error_msgs]
                            
                        for msg in error_msgs:
                            msg_str = str(msg).lower()
                            error_code = field_to_error_code.get(field, ErrorCodes.GEN_001)
                            
                            # Further refine error code based on error message
                            if 'already exists' in msg_str and field == 'email':
                                if 'patient' in msg_str:
                                    error_code = ErrorCodes.PAT_006
                                else:
                                    error_code = ErrorCodes.USER_009
                            elif 'valid email address' in msg_str:
                                error_code = ErrorCodes.USER_016
                            elif 'field has no more' in msg_str and field == 'first_name':
                                error_code = ErrorCodes.GEN_002
                            elif 'field has no more' in msg_str and field == 'last_name':
                                error_code = ErrorCodes.GEN_003
                            elif 'field has no more' in msg_str:
                                error_code = ErrorCodes.PAT_010
                            elif 'format' in msg_str and field == 'phone_number':
                                error_code = ErrorCodes.USER_010
                            
                            elif 'valid date' in msg_str or 'date format' in msg_str:
                                error_code = ErrorCodes.USER_011
                            elif 'valid choice' in msg_str and field == 'job':
                                error_code = ErrorCodes.USER_012
                            elif 'valid choice' in msg_str and field == 'gender':
                                error_code = ErrorCodes.USER_013
                            elif ('short' in msg_str or 'characters' in msg_str) and field == 'password':
                                error_code = ErrorCodes.USER_015
                                
                            formatted_errors.append({
                                'code': error_code,
                                'message': ERROR_MESSAGES.get(error_code, str(msg)),
                                'field': field
                            })
                
                # Process non-field errors
                if 'non_field_errors' in errors:
                    non_field_errors = errors['non_field_errors']
                    if not isinstance(non_field_errors, list):
                        non_field_errors = [non_field_errors]
                        
                    for error in non_field_errors:
                        formatted_errors.append({
                            'code': ErrorCodes.GEN_001,
                            'message': str(error)
                        })
        
        # Handle string or other error types
        elif errors:
            formatted_errors.append({
                'code': ErrorCodes.GEN_001,
                'message': str(errors)
            })
            
        # Fallback for empty errors
        if not formatted_errors:
            formatted_errors.append({
                'code': ErrorCodes.GEN_001,
                'message': "An unknown error occurred"
            })
            
        return formatted_errors