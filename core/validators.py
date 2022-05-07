from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_regno(value):
    if value // 1000000 == 0:
        raise ValidationError(
            _('%(value)s is not a valid registration number'),
            params={'value': value},
        )


def validate_matricno(value):
    if len(value) != 10 or not value[0:2].isnumeric() or not value[2:4].isalpha():
        raise ValidationError(
            _('%(value)s is not a valid matriculation number'),
            params={'value': value},
        )