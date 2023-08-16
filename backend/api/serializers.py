import base64
from urllib.parse import urljoin

from core.validators import ingredients_validator, tags_validator
from django.core.files.base import ContentFile
from django.db.models import F
from djoser.serializers import UserSerializer
from rest_framework import serializers

from recipes.models import (Favorite, Ingredient, IngredientinRecipe, Recipe,
                            Shopping, Tag)
from users.models import Follow, User


class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            file_format, img_code = data.split(';base64,')
            ext = file_format.split('/')[-1]
            data = ContentFile(base64.b64decode(img_code), name='temp.' + ext)
        return super().to_internal_value(data)


class RecipeMiniSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('__all__',)


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = ('__all__',)


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'
        read_only_fields = ('__all__',)


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return Follow.objects.filter(user=user, following=obj).exists()
        return False

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed')
        read_only_fields = ('__all__',)


class UserSubscription(CustomUserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes = obj.recipes.values(
            'id', 'name', 'image', 'cooking_time'
        )
        for recipe in recipes:
            image_url = urljoin(
                request.build_absolute_uri('/media/'), recipe['image'])
            recipe['image'] = image_url
        return recipes

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed', 'recipes', 'recipes_count')
        read_only_fields = ('__all__',)


class RecipeSerializer(serializers.ModelSerializer):
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    tags = TagSerializer(read_only=True, many=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    image = Base64ImageField()

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return Favorite.objects.filter(
                user=user, favorite_recipe=obj).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return Shopping.objects.filter(
                user=user, recipe=obj).exists()
        return False

    def get_ingredients(self, recipe):
        ingredients = recipe.ingredients.values(
            "id", "name", "measurement_unit",
            amount=F("recipe_with_ingredient__amount")
        )
        return ingredients

    def validate(self, data):
        method = self.context['request'].method
        tags = self.initial_data.get("tags")
        ingredients = self.initial_data.get("ingredients")

        if method == "POST":
            tags = tags_validator(tags, Tag)
            ingredients = ingredients_validator(ingredients, Ingredient)

        data.update(
            {
                "tags": tags,
                "ingredients": ingredients,
                "author": self.context.get("request").user,
            }
        )
        return data

    def create_ingredients(self, ingredients, recipe):
        for ing in ingredients:
            ingredient = Ingredient.objects.get(id=ing['id'])
            IngredientinRecipe.objects.get_or_create(
                ingredient=ingredient, recipe=recipe, amount=ing['amount']
            )

    def create(self, validated_data):
        tags = validated_data.pop("tags")
        ingredients = validated_data.pop("ingredients")
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time)
        instance.text = validated_data.get('text', instance.text)
        instance.image = validated_data.get('image', instance.image)
        if isinstance(validated_data['tags'], list):
            tags = validated_data.pop('tags')
            instance.tags.clear()
            instance.tags.set(tags)
        if isinstance(validated_data['ingredients'], list):
            ingredients = validated_data.pop('ingredients')
            instance.ingredients.clear()
            self.create_ingredients(ingredients, instance)
        instance.save()
        return instance

    class Meta:
        model = Recipe
        fields = '__all__'
        read_only_fields = (
            'author', 'pub_date', 'tags', 'is_favorited',
            'is_in_shopping_cart',)


class ShoppingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shopping
        fields = '__all__'
        read_only_fields = ('__all__',)


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = '__all__'
        read_only_fields = ('__all__',)
