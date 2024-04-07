from rest_framework.serializers import ValidationError


def url_validator(url):
    if url and 'youtube.com' not in url:
        raise ValidationError('Недопустимая ссылка')