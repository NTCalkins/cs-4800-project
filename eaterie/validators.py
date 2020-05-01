from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_ratings(value):
    if value < -1 or value > 6:
        raise ValidationError(
            _('Invalid score for timeliness or food quality'),
        )