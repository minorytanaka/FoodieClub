import base64

from django.core.files.base import ContentFile
from recipes.models import Recipe
from rest_framework import serializers


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


def is_recipe_unique(name, ingredients):
    try:
        Recipe.objects.get(name=name,
                           recipe_ingredients__ingredient__in=ingredients)
        return False
    except Recipe.DoesNotExist:
        return True
