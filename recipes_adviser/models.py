from django.db import models


class Ingredient(models.Model):
    name = models.CharField('name', max_length=100)
    liquid = models.BooleanField('is liquid', default=True)
    abv = models.FloatField('alcohol by volume')
    #image = models.ImageField()

    def __str__(self):
        return '<%s %s %0.2f>' % (self.name, self.liquid, self.abv)
