from django.core.exceptions import ValidationError
from urllib.parse import urlparse


class YouTubeLinkValidator:
    """
    Валидатор для поля урл
    """

    def __init__(self, field=None):
        self.field = field

    def __call__(self, value):
        parsed_url = urlparse(value)
        if not parsed_url.netloc.endswith("youtube.com"):
            raise ValidationError("Допускаются только ссылки на youtube.com")
