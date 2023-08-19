from django.core.exceptions import ValidationError


def validator_username(value):
    if value.lower() == "me":
        raise ValidationError("me слово запрещенное, в любом регистре. ")
    return value
