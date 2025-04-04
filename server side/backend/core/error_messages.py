from .errors import ErrorCodes

ERROR_MESSAGES = {
    # Authentication errors
    ErrorCodes.AUTH_001: "Invalid credentials. Please check your email and password.",
    ErrorCodes.AUTH_002: "Your account is inactive or has been locked.",
    ErrorCodes.AUTH_003: "Your session has expired. Please log in again.",
    ErrorCodes.AUTH_004: "The OTP has expired. Please request a new one.",
    ErrorCodes.AUTH_005: "This OTP has already been used.",
    ErrorCodes.AUTH_006: "Invalid OTP. Please check and try again.",
    ErrorCodes.AUTH_007: "OTP not verified. Please verify your OTP first.",
    
    # User/Radiologist errors
    ErrorCodes.USER_001: "Email address is required.",
    ErrorCodes.USER_002: "First name is required.",
    ErrorCodes.USER_003: "Last name is required.",
    ErrorCodes.USER_004: "Password is required.",
    ErrorCodes.USER_005: "Job title is required.",
    ErrorCodes.USER_006: "Gender is required.",
    ErrorCodes.USER_007: "Phone number is required.",
    ErrorCodes.USER_008: "Date of birth is required.",
    ErrorCodes.USER_009: "A user with this email already exists.",
    ErrorCodes.USER_010: "Invalid phone number format.",
    ErrorCodes.USER_011: "Invalid date format.",
    ErrorCodes.USER_012: "Invalid job choice. Must be Doctor or Nurse.",
    ErrorCodes.USER_013: "Invalid gender choice. Must be Male or Female.",
    ErrorCodes.USER_014: "No user found with this email address.",
    ErrorCodes.USER_015: "Password must be at least 8 characters.",
    
    # Patient errors
    ErrorCodes.PAT_001: "Patient email is required.",
    ErrorCodes.PAT_002: "Patient first name is required.",
    ErrorCodes.PAT_003: "Patient last name is required.",
    ErrorCodes.PAT_004: "Patient gender is required.",
    ErrorCodes.PAT_005: "Patient date of birth is required.",
    ErrorCodes.PAT_006: "A patient with this email already exists.",
    ErrorCodes.PAT_007: "Invalid patient code.",
    ErrorCodes.PAT_008: "You already have access to this patient.",
    ErrorCodes.PAT_009: "Patient not found.",
    
    # Scan errors
    ErrorCodes.SCAN_001: "Patient ID is required.",
    ErrorCodes.SCAN_002: "Scan image is required.",
    ErrorCodes.SCAN_003: "Organ type is required.",
    ErrorCodes.SCAN_004: "Invalid organ choice. Must be Heart, Brain, or Chest.",
    ErrorCodes.SCAN_005: "Failed to upload image. Please check format and size.",
    ErrorCodes.SCAN_006: "You don't have access to this patient.",
    ErrorCodes.SCAN_007: "Failed to process scan for prediction.",
    ErrorCodes.SCAN_008: "Scan not found.",
    
    # Permission errors
    ErrorCodes.PERM_001: "Authentication required.",
    ErrorCodes.PERM_002: "You don't have permission to perform this action.",
    
    # General errors
    ErrorCodes.GEN_001: "An unexpected error occurred. Please try again later."
}