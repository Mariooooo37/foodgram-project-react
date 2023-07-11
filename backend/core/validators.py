from django.core.exceptions import ValidationError


def tags_validator(tags, Tag):
    if tags is None or len(tags) == 0:
        raise ValidationError('Не указаны тэги')
    if len(tags) != len(set(tags)):
        raise ValidationError('В запросе повторяющиеся тэги')
    tags_obj = Tag.objects.filter(id__in=tags)
    if len(set(tags)) != len(tags_obj):
        raise ValidationError('В запросе несуществующий тэг')
    return tags


def ingredients_validator(ingredients, Ingredient):
    if ingredients is None or len(ingredients) == 0:
        raise ValidationError('Не указаны ингредиенты')
    ingredient_ids = [ingredient['id'] for ingredient in ingredients]
    ingredients_obj = Ingredient.objects.filter(id__in=ingredient_ids)
    if len(ingredient_ids) != len(set(ingredient_ids)):
        raise ValidationError('В запросе повторяющиеся ингредиенты')
    if len(set(ingredient_ids)) != len(ingredients_obj):
        raise ValidationError('В запросе несуществующие ингредиенты')
    return ingredients
