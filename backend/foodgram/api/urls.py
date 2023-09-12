from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.views import (FavoriteAPIView, IngredientViewSet, RecipeViewSet,
                       ShoppingCartAPIView, SubscriptionsListAPIView,
                       TagViewSet, UserSubscriptionsAPIView)

router = DefaultRouter()

router.register(r'tags', TagViewSet,
                basename='tags')
router.register(r'ingredients', IngredientViewSet,
                basename='ingredients')
router.register(r'recipes', RecipeViewSet,
                basename='recipes')

urlpatterns = [
    path('recipes/<int:recipe_id>/favorite/',
         FavoriteAPIView.as_view()),
    path('recipes/<int:recipe_id>/shopping_cart/',
         ShoppingCartAPIView.as_view()),
    path('users/<int:author_id>/subscribe/',
         UserSubscriptionsAPIView.as_view()),
    path('users/subscriptions/',
         SubscriptionsListAPIView.as_view({'get': 'list'})),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
    path('', include(router.urls)),
]
