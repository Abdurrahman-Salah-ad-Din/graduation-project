from rest_framework.exceptions import APIException
from .errors import ErrorCodes
from .error_messages import ERROR_MESSAGES

class AppException(APIException):
    def __init__(self, error_code, field=None, status_code=400):
        self.status_code = status_code
        
        # Get the error message from our mapping
        message = ERROR_MESSAGES.get(error_code, "An error occurred")
        
        # Construct the error response
        error_data = {
            "code": error_code,
            "message": message
        }
        
        # Add field information if provided
        if field:
            error_data["field"] = field
            
        # DRF will use this to construct the response
        self.detail = [error_data]