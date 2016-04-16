from django.test import TestCase

from .models import Recipe, CocktailComponent, Ingredient


class RecipeMethodTests(TestCase):

    def setUp(self):
        self.ingred_a = Ingredient.objects.create(name='a', abv=40.0,
                                                  measure='ml')
        self.ingred_b = Ingredient.objects.create(name='b', abv=20.0,
                                                  measure='ml')
        self.ingred_c = Ingredient.objects.create(name='c', abv=0, measure='ml')
        self.ingred_d = Ingredient.objects.create(name='c', liquid=False)

        self.comp_1 = CocktailComponent.objects.create(ingredient=self.ingred_a,
                                                       up_quantity=20)
        self.comp_2 = CocktailComponent.objects.create(ingredient=self.ingred_c,
                                                       up_quantity=200,
                                                       to_quantity=250)
        self.comp_3 = CocktailComponent.objects.create(ingredient=self.ingred_b,
                                                       up_quantity=80)
        self.comp_4 = CocktailComponent.objects.create(ingredient=self.ingred_d,
                                                       up_quantity=1)

        self.recipe_a = Recipe.objects.create(title='Cocktail#1', type='st')
        self.recipe_a.components.add(self.comp_1, self.comp_3)

        self.recipe_b = Recipe.objects.create(title='Cocktail#2', type='lg')
        self.recipe_b.components.add(self.comp_1, self.comp_2, self.comp_3)

        self.recipe_c = Recipe.objects.create(title='Cocktail#3', type='lg')
        self.recipe_c.components.add(self.comp_1, self.comp_2, self.comp_4)

        self.non_alc_recipe = Recipe.objects.create(title='Cocktail#3',
                                                    type='lg')
        self.non_alc_recipe.components.add(self.comp_2)

        self.non_liquid_recipe = Recipe.objects.create(title='Cocktail#3',
                                                       type='lg')
        self.non_liquid_recipe.components.add(self.comp_4)

    def test_min_volume(self):
        self.assertEqual(self.recipe_a.get_min_volume(), 100)
        self.assertEqual(self.recipe_b.get_min_volume(), 300)
        self.assertEqual(self.recipe_c.get_min_volume(), 220)
        self.assertEqual(self.non_liquid_recipe.get_min_volume(), 0)

    def test_max_volume(self):
        self.assertEqual(self.recipe_a.get_max_volume(), 100)
        self.assertEqual(self.recipe_b.get_max_volume(), 350)
        self.assertEqual(self.recipe_c.get_max_volume(), 270)
        self.assertEqual(self.non_liquid_recipe.get_min_volume(), 0)

    def test_avg_volume(self):
        self.assertEqual(self.recipe_a.get_avg_volume(), 100)
        self.assertEqual(self.recipe_b.get_avg_volume(), 325)
        self.assertEqual(self.recipe_c.get_avg_volume(), 245)
        self.assertEqual(self.non_liquid_recipe.get_min_volume(), 0)

    def test_avg_abv(self):
        self.assertEqual(self.recipe_a.get_avg_abv(), 24)
        self.assertEqual(self.recipe_b.get_avg_abv(), 8)
        self.assertEqual(self.non_liquid_recipe.get_avg_abv(), 0)

    def test_is_alcoholic(self):
        self.assertTrue(self.recipe_a.is_alcoholic())
        self.assertFalse(self.non_alc_recipe.is_alcoholic())

    def test_is_strong(self):
        self.assertTrue(self.recipe_a.is_strong())
        self.assertFalse(self.recipe_b.is_strong())

    def test_is_shot(self):
        self.assertTrue(self.recipe_a.is_shot())
        self.assertFalse(self.recipe_b.is_shot())

    def test_is_long(self):
        self.assertFalse(self.recipe_a.is_long())
        self.assertTrue(self.recipe_b.is_long())
