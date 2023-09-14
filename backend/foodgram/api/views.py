from django.db.models import Sum
from django.shortcuts import HttpResponse, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, views, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated

from api.filters import IngredientFilter
from api.permissions import IsAdminAuthorOrReadOnly, IsAdminReadOnly
from api.serializers import (IngredientSerializer, RecipeCreateSerializer,
                             RecipeSerializer, SubscribedUserSerializer,
                             TagSerializer)
from recipes.models import (Ingredient, Recipe, RecipeIngredient, Tag,
                            Favorite)
from users.models import User
from api.utils import handle_request


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminReadOnly,)
    pagination_class = None


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminReadOnly,)
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAdminAuthorOrReadOnly,)

    def get_queryset(self):
        recipes = Recipe.objects.prefetch_related(
            'recipe_ingredients__ingredient', 'tags'
        ).distinct().all()

        tags = self.request.query_params.getlist('tags')
        if tags:
            recipes = recipes.filter(
                tags__slug__in=tags)

        is_in_shopping_cart = self.request.query_params.get(
            'is_in_shopping_cart'
        )
        is_favorited = self.request.query_params.get('is_favorited')
        author_id = self.request.query_params.get('author')

        if author_id:
            recipes = recipes.filter(author_id=author_id)
        if self.request.user.is_authenticated:
            if is_in_shopping_cart:
                recipes = recipes.filter(
                    added_to_carts__user=self.request.user)
            if is_favorited:
                recipes = recipes.filter(
                    favorited_by_users__user=self.request.user)
        return recipes.order_by('-id')

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=False,
        url_path='download_shopping_cart',
        methods=['get']
    )
    def download_shopping_cart(self, request):
        ingredients = RecipeIngredient.objects.filter(
            recipe__added_to_carts__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(
            total_amount=Sum('amount')
        ).order_by('ingredient__name')

        shopping_list = ['Список покупок:\n']

        for ingredient in ingredients:
            name = ingredient['ingredient__name']
            unit = ingredient['ingredient__measurement_unit']
            amount = ingredient['total_amount']
            shopping_list.append(f'\n {name} - {amount} {unit}')
        shopping_list.append('\n\nFoodgram - Вкус момента, разделяемый миром!')
        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = (
            'attachment; filename="shopping_cart.txt"'
        )
        return response


class SubscriptionsListAPIView(mixins.ListModelMixin,
                               viewsets.GenericViewSet):
    serializer_class = SubscribedUserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return User.objects.filter(following__user=self.request.user)


class UserSubscriptionsAPIView(views.APIView):

    def post(self, request, author_id):
        user = request.user
        author = get_object_or_404(User, id=author_id)
        return handle_request(
            user=user,
            author=author,
            action='create_subscription'
        )

    def delete(self, request, author_id):
        user = request.user
        author = get_object_or_404(User, id=author_id)
        return handle_request(
            user=user,
            author=author,
            action='delete_subscription'
        )


class FavoriteAPIView(views.APIView):

    def post(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)
        return handle_request(
            user=user,
            recipe=recipe,
            model_class=Favorite,
            action='add_recipe_favorite'
        )

    def delete(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)
        return handle_request(
            user=user,
            recipe=recipe,
            model_class=Favorite,
            action='remove_recipe_favorite'
        )


class ShoppingCartAPIView(views.APIView):

    def post(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)
        return handle_request(
            user=user,
            recipe=recipe,
            model_instance=user.shopping_carts,
            action='add_recipe'
        )

    def delete(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)
        return handle_request(
            user=user,
            recipe=recipe,
            model_instance=user.shopping_carts,
            action='remove_recipe'
        )
