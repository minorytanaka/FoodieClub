from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError


def username_validator(value):
    unicode_validator = UnicodeUsernameValidator()
    unicode_validator(value)

    if value.lower() == 'me':
        raise ValidationError(
            'Недопустимое имя пользователя!'
        )
