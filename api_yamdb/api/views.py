from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .filters import TitleFilter
from .models import Category, Genre, Review, Title
from .permissions import IsAdmin, IsAdminOrReadOnly, IsAuthorOrStaffOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleReadOnlySerializer, TitleSerializer,
                          TokenObtainByEmailSerializer,
                          UserEmailConfirmationSerializer, UsersSerializer)

User = get_user_model()


class ListCreateDestroyModelViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class UserEmailConfirmationView(CreateAPIView):
    serializer_class = UserEmailConfirmationSerializer
    permission_classes = (permissions.AllowAny,)


class TokenObtainByEmailView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = TokenObtainByEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User,
            email=serializer.validated_data.get('email')
        )
        token = AccessToken().for_user(user)
        data = {'token': str(token)}
        return Response(data, status=status.HTTP_200_OK)


class UsersViewSet(viewsets.ModelViewSet):
    """
    Обработка запросов к /users/. Доступ разрёшен только если
    User.is_staff=True и User.role='admin'. Исключение - методы,
    декорированные @action с другим значением permission_classes
    """
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (IsAdmin,)
    filter_backends = [SearchFilter, ]
    search_fields = ['username', ]
    lookup_field = 'username'

    @action(detail=False,
            permission_classes=[IsAuthenticated],
            url_path='me', url_name='users-me')
    def get_self_user_data(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @get_self_user_data.mapping.patch
    def patch_self_user_data(self, request):
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CategoryViewSet(ListCreateDestroyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', ]
    ordering_fields = ['name', ]
    lookup_field = 'slug'


class GenreViewSet(ListCreateDestroyModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    # serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    filterset_class = TitleFilter
    search_fields = ('name',)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleReadOnlySerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrStaffOrReadOnly,)

    def get_queryset(self):
        return get_object_or_404(
            Title,
            pk=self.kwargs.get('title_id')
        ).reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        )

    def get_object(self):
        obj = get_object_or_404(Review, title_id=self.kwargs['title_id'],
                                id=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrStaffOrReadOnly,)

    def get_queryset(self):
        return get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id')
        ).comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=get_object_or_404(
                Review,
                title_id=self.kwargs.get('title_id'),
                pk=self.kwargs.get('review_id')
            )
        )
