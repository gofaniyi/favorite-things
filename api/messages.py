ERROR_MESSAGES = {
    'SERVER' : 'Authorization failed. Please contact support',
    'JWT_EXPIRED_TOKEN' : 'Token expired. Please login to get a new token',
    'JWT_INVALID_TOKEN' : 'Authorization failed due to an Invalid token',
    'JWT_ISSUER' : 'Cannot verify the token provided as the expected issuer does not match',
    'JWT_ALGORITHM' : 'Cannot verify the token provided as it was signed with a different algorithm',
    'JWT_SIGNATURE' : 'Cannot verify the signature of the token provided as it was signed by a non matching private key',
    'USER_LOGIN' : 'User login attempt failed',
    'INVALID_LOGIN_CREDENTIALS' : 'Email or password is incorrect',
    'PASSWORDS_MISMATCH' : 'Passwords do not match',
    'INVALID_EMAIL' : 'This is an invalid email address',
    'DEFAULT' : 'An error occurred',
    'NOT_STRONG_PASSWORD' : 'Password should be at least 8 characters',
    'EMAIL_EXISTS' : 'Email already exist',
    'EMPTY_PAYLOAD' : 'No valid field(s) in request body',
    'REQUIRED_FIELD' : 'Missing data for required field.',
    'COMPANY_EXISTS' : 'Company already exist',
    'EXISTS' : '{} already exist',
    'PROVIDE_CUSTOM_ATTRIBUTES' : 'Please provide at least one attribute for this risk type',
    'NOT_FOUND' : '{} not found',
    'NOT_FOUND_IDENTIFIER' : 'The {} id provided was not found',
    'ATTRIBUTE_NOT_FOUND' : '{} attribute not found',
    'MISSING_FIELDS' : 'Some fields are missing',
    'ATTRIBUTE_NOT_RELATED':
        'attribute with the id of {attribute_id} is not related to the risk type of id {risk_type_id}',
    'ATTRIBUTE_NOT_RELATED_1' : 'attribute is not related to the risk type - {}',
    'INPUT_CONTROL': 'Incorrect input control type provided, please provide one of {input_controls}',
    'CHOICES_REQUIRED' : 'choices seperated by comma must be provided if multi choice inputs controls are selected',
    'BAD_DATA_ATTRIBUTE' : 'There is so problems with the data attributes, See errors',
    'DELETING_RELATED_OBJECTS' : "Can't remove a {} that has active {}",
    'STRING_LENGTH' : 'Field must be {0} characters or more'
}


SUCCESS_MESSAGES = {
    'USER_LOGOUT' : 'User logged out successfully',
    'USER_LOGIN' : 'User logged in successfully',
    'USER_SIGNUP' : 'User signup successfully',
    'RISK_TYPE_CREATED' : 'Risk Type created successfully',
    'CREATED' : '{} created successfully',
    'FETCHED' : '{} fetched successfully',
    'UPDATED': '{} successfully updated',
    'DELETED' : '{} deleted successfully'
}
