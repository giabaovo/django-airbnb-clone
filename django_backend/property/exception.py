from rest_framework.exceptions import APIException


class InvalidPropertyIDException(APIException):
    status_code = 400
    default_detail = "Invalid property ID"
