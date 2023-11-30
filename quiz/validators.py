from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class PhoneValidator(RegexValidator):
    regex = r'^\+998[0-9]{9}$'
    message = _("Enter a valid phone number.")


phone_validator = PhoneValidator()
