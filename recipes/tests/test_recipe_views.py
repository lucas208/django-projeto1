from django.urls import resolve, reverse

from recipes import views
from recipes.models import Recipe

from .test_recipe_base import RecipeTestBase


class RecipeViewsTest(RecipeTestBase):
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            'No recipes found',
            response.content.decode('utf-8')
        )

    def test_recipe_home_template_loads_recipes(self):
        self.make_recipe()

        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        quantity = Recipe.objects.all().count()
        recipe = Recipe.objects.all().first()

        self.assertIn(recipe.title, content)
        self.assertIn(
            f"{recipe.preparation_time} {recipe.preparation_time_unit}",
            content
        )
        self.assertIn(f"{recipe.servings} {recipe.servings_unit}", content)
        self.assertEqual(len(response.context['recipes']), quantity)

    def test_recipe_home_template_dont_load_recipes_not_published(self):
        self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')

        self.assertIn(
            'No recipes found',
            content
        )

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(
            reverse(
                'recipes:category',
                kwargs={
                    'category_id': 1000
                }
            )
        )
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_returns_404_if_category_not_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_loads_recipes(self):
        title = 'This is a category test'
        self.make_recipe(title=title)

        response = self.client.get(reverse('recipes:category', args=(1,)))
        content = response.content.decode('utf-8')
        recipe = Recipe.objects.all().first()

        self.assertIn(recipe.title, content)
        self.assertIn(
            f"{recipe.preparation_time} {recipe.preparation_time_unit}",
            content
        )
        self.assertIn(f"{recipe.servings} {recipe.servings_unit}", content)

    def test_recipe_category_template_dont_load_recipes_not_published(self):
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(
            reverse(
                'recipes:category',
                kwargs={'category_id': recipe.category.id}
            )
        )
        content = response.content.decode('utf-8')

        self.assertIn(
            'No recipes found',
            content
        )

    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1000}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_returns_404_if_category_not_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_loads_the_correct_recipe(self):
        title = 'This is a detail page - It loads one recipe'
        self.make_recipe(title=title)

        response = self.client.get(
            reverse(
                'recipes:recipe',
                kwargs={
                    'id': 1
                }
            )
        )

        content = response.content.decode('utf-8')
        recipe = Recipe.objects.all().first()

        self.assertIn(recipe.title, content)
        self.assertIn(
            f"{recipe.preparation_time} {recipe.preparation_time_unit}",
            content
        )
        self.assertIn(f"{recipe.servings} {recipe.servings_unit}", content)

    def test_recipe_detail_template_dont_load_recipe_not_published(self):
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(
            reverse(
                'recipes:recipe',
                kwargs={
                    'id': recipe.id
                }
            )
        )

        self.assertEqual(response.status_code, 404)
