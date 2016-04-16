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
                              default=settings.DEFAULT_INGREDIENT_IMG,
                              null=True, blank=True)

    # Liquid ingredients are measured in millilitres, non liquid - in grams,
    # something else can measured in units (ice cubes, for example)
    MEASURES = (
        ('g', 'Grams'),
        ('ml', 'Millilitres'),
        ('pcs', 'Pieces')
    )
    measure = models.CharField(max_length=3, choices=MEASURES)

    def __str__(self):
        return self.name


class CocktailComponent(models.Model):
    """ It contains ingredient, quantity and measure of that. """
    ingredient = models.ForeignKey(Ingredient, related_name='components')
    up_quantity = models.FloatField('up quantity of ingredient')
    to_quantity = models.FloatField('to quantity of ingredient',
                                    default=None, null=True, blank=True)

    def __str__(self):
        return '%s (%s - %s)' % (self.ingredient.name,
                                 self.up_quantity,
                                 self.to_quantity)


class RecipeStage(models.Model):
    """
    One stage of cocktail's recipe.
    (Usually a cocktail's recipe has a few stages for making)
    """
    stage_number = models.PositiveSmallIntegerField(default=1)
    content = models.TextField()

    def __str__(self):
        short_content = self.content.split('.')[0][:60]
        return '#%d %s' % (self.stage_number, short_content)


class CocktailTool(models.Model):
    """ Tool for making cocktails. """
    name = models.CharField('name', max_length=200, db_index=True)
    description = models.TextField(blank=True)
    image = models.ImageField(null=True, blank=True,
                              upload_to=settings.TOOL_IMAGE_PATH,
                              default=settings.DEFAULT_TOOL_IMG)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """ Cocktail's recipe. """
    title = models.CharField('name', max_length=250, db_index=True)
    author = models.ForeignKey(User, related_name='recipes',
                               null=True, blank=True, db_index=True)
    title_image = models.ImageField('title image', null=True, blank=True,
                                    upload_to=settings.RECIPE_IMAGE_PATH,
                                    default=settings.DEFAULT_RECIPE_IMG)
    description = models.TextField(blank=True)

    # Ingredient with quantity
    components = models.ManyToManyField(CocktailComponent,
                                        related_name='recipes')
    stages = models.ManyToManyField(RecipeStage, related_name='recipes')

    tools = models.ManyToManyField(CocktailTool, related_name='recipes')

    COCKTAIL_TYPE = (
        ('st', 'Shot'),
        ('lg', 'Long'),
    )
    type = models.CharField('type of cocktail', max_length=3,
                            choices=COCKTAIL_TYPE)

    def get_min_volume(self):
        """ Returns the sum of min volumes for each liquid components. """
        return sum(item.up_quantity for item in self.components.all()
                   if item.ingredient.liquid)

    def get_max_volume(self):
        """ Returns the sum of max volumes for each liquid components. """
        return sum(item.to_quantity if item.to_quantity else item.up_quantity
                   for item in self.components.all() if item.ingredient.liquid)

    def get_avg_volume(self):
        """ Returns the sum of averages volumes for each liquid components. """
        avg_volume = 0
        for item in self.components.all():
            if item.ingredient.liquid:
                if item.to_quantity:
                    avg_volume += (item.up_quantity + item.to_quantity) / 2.0
                else:
                    avg_volume += item.up_quantity
        return avg_volume

    def get_avg_abv(self):
        volume = self.get_min_volume()
        return sum(item.ingredient.abv * item.up_quantity / volume
                   for item in self.components.all() if item.ingredient.liquid)

    def is_alcoholic(self):
        is_alcoholic = False
        for item in self.components.all():
            if item.ingredient.liquid and item.ingredient.abv > 0.0:
                is_alcoholic = True
                break
        return is_alcoholic

    def is_strong(self):
        """ Returns true if cocktails has average abv more then 17%. """
        strong_abv = 17.0
        return self.get_avg_abv() > strong_abv

    def is_shot(self):
        return self.type == 'st'

    def is_long(self):
        return self.type == 'lg'

    def __str__(self):
        return self.title
