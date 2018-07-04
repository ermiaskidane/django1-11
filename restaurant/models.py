from django.conf import settings
from django.db import models
from django.db.models.signals  import pre_save, post_save
from .validators import validate_category
from django.core.urlresolvers import reverse
from django.db.models import Q

from .utils import unique_slug_generator

User  = settings.AUTH_USER_MODEL
# Create your models here.

# custome queryset
class RestaurantLocationQuerySet(models.query.QuerySet):

    def search(self, query):            # RestaurantLocation.objects.all().search(query)   or #RestaurantLocation.objects.filter(something).search()
        if query:
            query = query.strip()
            return self.filter(
                Q(name__icontains=query)|
                Q(location__icontains=query)|
                Q(location__iexact=query)|
                Q(category__icontains=query)|
                Q(category__iexact=query)|
                Q(item__name__icontains=query) |
                Q(item__contents__icontains=query)
                ).distinct()
        return self


class RestaurantLocationManager(models.Manager):
    def get_queryset(self):      # this override the standar queryset
        return RestaurantLocationQuerySet(self.model, using=self._db)

    def search(self, query):            #RestaurantLocation.objects.search()
        # return self.get_queryset().filter(name__icontains=query)
        return self.get_queryset().search(query)


class RestaurantLocation(models.Model):
    owner           = models.ForeignKey(User) #class_instance.models_set.all()  #django models unleash joincfe.com
    name            = models.CharField(max_length=120)
    location        = models.CharField(max_length=120, null=True, blank=True)
    category        = models.CharField(max_length=120, null=True, blank=True, validators=[validate_category])
    timestap        = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)
    files           = models.FileField(upload_to='profile_pic', max_length=120, null=True, blank=True)
    slug            = models.SlugField( null=True, blank=True)
    # email           = models.EmailField()

    objects         = RestaurantLocationManager()  # add models.objects.all()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # return f"/restaurant/{self.slug}"
        return reverse("restaurant:detail", kwargs={"slug":self.slug})

    @property
    def title(self):
        return self.name   #able to do obj.title in restaurant-detail instead of obj.name

def rl_pre_save_reciever(sender, instance, *args, **kwargs):
    instance.category = instance.category.capitalize()
    # print('saving...')
    # print(instance.timestap)
    if not instance.slug:
        # instance.name = " Another new Title"
        instance.slug = unique_slug_generator(instance)


# def rl_post_save_reciever(sender, instance, created, *args, **kwargs):
#     print('saved')
#     print(instance.timestap)
#     if not instance.slug:
#         instance.slug = unique_slug_generator(instance)
#         instance.save()


pre_save.connect(rl_pre_save_reciever, sender=RestaurantLocation)
# post_save.connect(rl_post_save_reciever, sender=RestaurantLocation)
