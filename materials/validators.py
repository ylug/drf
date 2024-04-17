from rest_framework import serializers

GOOD_URL = "https://www.youtube.com/"

class ProhibitedUrlValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        data_url = dict(value).get(self.field)

        if GOOD_URL not in data_url:
            raise serializers.ValidationError("Нельзя использовать ссылки на сторонние сайты")
