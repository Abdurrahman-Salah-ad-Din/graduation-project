class ErrorCodes:
    # Authentication errors (AUTH_XXX)
    AUTH_001 = "AUTH_001"  # Invalid credentials
    AUTH_002 = "AUTH_002"  # Account locked/inactive
    AUTH_003 = "AUTH_003"  # Token expired/invalid
    AUTH_004 = "AUTH_004"  # Password reset OTP expired
    AUTH_005 = "AUTH_005"  # Password reset OTP already used
    AUTH_006 = "AUTH_006"  # Password reset OTP invalid
    AUTH_007 = "AUTH_007"  # Password reset OTP not verified
    AUTH_008 = "AUTH_008"  # Tokein is missing. 
      
    # User/Radiologist errors (USER_XXX)
    USER_001 = "USER_001"  # Email required
    USER_002 = "USER_002"  # First name required
    USER_003 = "USER_003"  # Last name required
    USER_004 = "USER_004"  # Password required
    USER_005 = "USER_005"  # Job required
    USER_006 = "USER_006"  # Gender required
    USER_007 = "USER_007"  # Phone number required
    USER_008 = "USER_008"  # Date of birth required
    USER_009 = "USER_009"  # Email already exists
    USER_010 = "USER_010"  # Invalid phone number format
    USER_011 = "USER_011"  # Invalid date format
    USER_012 = "USER_012"  # Invalid job choice
    USER_013 = "USER_013"  # Invalid gender choice
    USER_014 = "USER_014"  # Email not found
    USER_015 = "USER_015"  # Password too short
    USER_016 = "USER_016"  # Invalid Email
    
    # Patient errors (PAT_XXX)
    PAT_001 = "PAT_001"  # Patient email required
    PAT_002 = "PAT_002"  # Patient first name required
    PAT_003 = "PAT_003"  # Patient last name required
    PAT_004 = "PAT_004"  # Patient gender required
    PAT_005 = "PAT_005"  # Patient date of birth required
    PAT_006 = "PAT_006"  # Patient email already exists
    PAT_007 = "PAT_007"  # Invalid patient code
    PAT_008 = "PAT_008"  # Already have access to patient
    PAT_009 = "PAT_009"  # Patient not found
    PAT_010 = "PAT_010"  # Max length exceeded
    PAT_011 = "PAT_010"  # Blank patient code
    
    # Scan errors (SCAN_XXX)
    SCAN_001 = "SCAN_001"  # Patient ID required
    SCAN_002 = "SCAN_002"  # Image required
    SCAN_003 = "SCAN_003"  # Organ type required
    SCAN_004 = "SCAN_004"  # Invalid organ choice
    SCAN_005 = "SCAN_005"  # Image upload failed
    SCAN_006 = "SCAN_006"  # Patient not accessible
    SCAN_007 = "SCAN_007"  # AI prediction failed
    SCAN_008 = "SCAN_008"  # Scan not found
    
    # Permission errors (PERM_XXX)
    PERM_001 = "PERM_001"  # Not authenticated
    PERM_002 = "PERM_002"  # Permission denied
    
    # General errors (GEN_XXX)
    GEN_001 = "GEN_001"  # General server error
    GEN_002 = "GEN_002"  # Patient first name exceed the max length
    GEN_003 = "GEN_003"  # Patient last name exceed the max length