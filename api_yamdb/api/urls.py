from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, TokenObtainByEmailView,
                    UserEmailConfirmationView, UsersViewSet)

token_urls = [
    path(
        '',
        TokenObtainByEmailView.as_view(),
        name='token_obtain_pair'
    ),
]

router_v1 = DefaultRouter()
router_v1.register(
    r'categories',
    CategoryViewSet,
    basename='categories'
)
router_v1.register(
    r'genres',
    GenreViewSet,
    basename='genres'
)
router_v1.register(
    r'titles',
    TitleViewSet,
    basename='titles'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)
router_v1.register(
    r'users',
    UsersViewSet,
    basename='users'
)

urlpatterns = [
    path('v1/auth/email/', UserEmailConfirmationView.as_view()),
    path('v1/auth/token/', include(token_urls)),
    path('v1/', include(router_v1.urls)),
]
