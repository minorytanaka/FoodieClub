import base64

from django.shortcuts import get_object_or_404
from django.core.files.base import ContentFile
from rest_framework.response import Response
from rest_framework import serializers, status

from users.models import Follow


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


def create_object(user, recipe=None, author=None, model_class=None):
    if recipe:
        obj, created = model_class.objects.get_or_create(
            user=user,
            recipe=recipe
        )
        if created:
            return Response({'detail': 'Объект успешно создан.'},
                            status=status.HTTP_201_CREATED)
        return Response({'detail': 'Такой объект уже существует.'},
                        status=status.HTTP_400_BAD_REQUEST)
    elif author:
        if user == author:
            return Response({'detail': 'Нельзя подписаться на самого себя!'},
                            status=status.HTTP_400_BAD_REQUEST)
        subscription, created = Follow.objects.get_or_create(
            user=user,
            following=author
        )
        if created:
            return Response({'detail': 'Подписка успешно создана.'},
                            status=status.HTTP_201_CREATED)
        return Response({'detail': 'Вы уже подписаны.'},
                        status=status.HTTP_400_BAD_REQUEST)


def delete_object(user, recipe=None, author=None, model_class=None):
    if recipe:
        recipe_to_remove = get_object_or_404(
            model_class,
            user=user,
            recipe=recipe
        )
        recipe_to_remove.delete()
        return Response({'detail': 'Объект успешно удален!'},
                        status=status.HTTP_204_NO_CONTENT)
    elif author:
        subscription = get_object_or_404(Follow, user=user, following=author)
        subscription.delete()
        return Response({'detail': 'Подписка отменена.'},
                        status=status.HTTP_204_NO_CONTENT)
