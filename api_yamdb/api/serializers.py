import uuid

from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.validators import UniqueValidator

from .models import Category, Comment, Genre, Review, Title, User


class TokenObtainByEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100)
    confirmation_code = serializers.CharField(max_length=50)

    def validate(self, attrs):
        user = get_object_or_404(User, email=attrs.get('email'))
        if user.confirmation_code != attrs.get('confirmation_code'):
            raise serializers.ValidationError(
                {'confirmation_code': 'Неверный код подтверждения'}
            )
        return attrs


class UserEmailConfirmationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)
        extra_kwargs = {'confirmation_code': {'write_only': True},
                        'username': {'write_only': True}}

    @staticmethod
    def generate_code(validated_data):
        return uuid.uuid3(
            uuid.NAMESPACE_OID,
            validated_data['email']
        )

    @staticmethod
    def generate_username(validated_data):
        return uuid.uuid3(uuid.NAMESPACE_DNS, validated_data['email'])

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            confirmation_code=self.generate_code(validated_data),
            username=self.generate_username(validated_data)
        )
        user.save()
        return user


class UsersSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=50,
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        max_length=50,
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        fields = (
            'first_name',
            'last_name',
            'username',
            'bio',
            'email',
            'role'
        )
        model = User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ['id']
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ['id']
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.FloatField(min_value=0, max_value=10, required=False)
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all(),
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        model = Title


class TitleReadOnlySerializer(serializers.ModelSerializer):
    rating = serializers.FloatField(min_value=0, max_value=10)
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title')
        read_only_fields = ('title',)
        model = Review

    def validate(self, attrs):
        attrs['title'] = get_object_or_404(
            Title, id=self.context['view'].kwargs['title_id'])
        if not self.partial and Review.objects.filter(
                title=attrs['title'],
                author=self.context['request'].user
        ).exists():
            raise serializers.ValidationError(
                {'author': 'Вы уже оставляли отзыв на это произведение'})
        return attrs


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
