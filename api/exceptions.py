from rest_framework.exceptions import APIException


class InvalidFormatException(APIException):
    status_code = 400
    default_detail = 'Invalid input data format'
    default_code = 'invalid_format'


class AlreadyExistsException(APIException):
    status_code = 400
    default_detail = 'The same entity already exists'
    default_code = 'already_exist'
