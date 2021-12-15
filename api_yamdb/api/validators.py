from django.core.exceptions import ValidationError
from django.utils import timezone


def year_validator(value):
    if value < 1700 or value > timezone.datetime.today().year:
        raise ValidationError(
            '%(value) - это недопустимое значение года.',
            params={'value': value},
        )
