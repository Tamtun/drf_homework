from rest_framework.serializers import ValidationError

class YouTubeLinkValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        link = dict(value).get(self.field)
        if link and 'youtube.com' not in link:
            raise ValidationError({self.field: 'Разрешены только ссылки на youtube.com'})
