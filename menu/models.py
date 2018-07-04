from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse

from restaurant.models import RestaurantLocation

# Create your models here.

class Item(models.Model):
    # assocaition
    user            = models.ForeignKey(settings.AUTH_USER_MODEL)
    restaurant      = models.ForeignKey(RestaurantLocation)

    # item stuffs
    name            = models.CharField(max_length=120)
    contents        = models.TextField(help_text="seperate each items by comma")
    excludes        = models.TextField(blank=True, null=True, help_text="seperate each items by comma")
    public          = models.BooleanField(default=True)
    timestap        = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
        
    def get_absolute_url(self):
        # return f"/restaurant/{self.slug}"
        return reverse("menu:detail", kwargs={"pk":self.pk})

    class Meta:
        ordering = ['-updated', '-timestap']   #Item.objects.all()

    def get_contents(self):
        return self.contents.split(",")

    def get_excludes(self):
        return self.excludes.split(",")
