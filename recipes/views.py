from django.shortcuts import get_object_or_404, render

from recipes.models import Category, Recipe


def home(request):

    recipes = Recipe.objects.filter(
        is_published=True
    ).order_by('-id')

    return render(request, 'recipes/pages/home.html', context={
        'recipes': recipes,
    })


def recipe(request, id):

    recipe = get_object_or_404(Recipe, pk=id, is_published=True)

    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': recipe,
        'is_detail_page': True,
    })


def category(request, category_id):

    recipes = Recipe.objects.filter(
        category__id=category_id,
        is_published=True
    ).order_by('-id')

    category = get_object_or_404(Category, id=category_id)    

    return render(request, 'recipes/pages/category.html', context={
        'recipes': recipes,
        'title': f'{category.name} - Category | '
    })
 
