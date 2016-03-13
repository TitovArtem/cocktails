from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Ingredient(models.Model):
    """ Cocktail's ingredient. """
    name = models.CharField('name', max_length=200, db_index=True)
    liquid = models.BooleanField('is liquid', default=True)
    abv = models.FloatField('alcohol by volume', default=0.0)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to=settings.INGREDIENT_IMAGE_PATH,
                              null=True, blank=True)

    def __str__(self):
        return '<name: %s, abv: %0.1f, is_liquid: %s>' % \
               (self.name, self.abv, self.liquid)


class CocktailComponent(models.Model):
    """ It contains ingredient, quantity and measure of that. """
    ingredient = models.ForeignKey(Ingredient, related_name='ingredients')
    quantity = models.FloatField('quantity of ingredient')

    # Liquid ingredients are measured in millilitres, non liquid - in grams,
    # something else can measured in units (ice cubes, for example)
    MEASURES = (
        ('g', 'Grams'),
        ('ml', 'Millilitres'),
        ('pcs', 'Pieces')
    )
    measure = models.CharField(max_length=3, choices=MEASURES)


class RecipeStage(models.Model):
    """
    One stage of cocktail's recipe.
    (Usually a cocktail's recipe has a few stages for making)
    """
    stage_number = models.PositiveSmallIntegerField(default=1)
    content = models.TextField()


class Recipe(models.Model):
    """ Cocktail's recipe. """
    title = models.CharField('name', max_length=250, db_index=True)
    author = models.ForeignKey(User, related_name='authors',
                               null=True, blank=True, db_index=True)
    title_image = models.ImageField('title image',
                                    upload_to=settings.RECIPE_IMAGE_PATH,
                                    null=True, blank=True)
    description = models.TextField(blank=True)
    ingredients = models.ManyToManyField(CocktailComponent,
                                         related_name='ingredients')
    stages = models.ManyToManyField(RecipeStage, related_name='stages')
