from django import forms
from .models import Item
from restaurant.models import RestaurantLocation

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            'restaurant',
            'name',
            'contents',
            'excludes',
            'public',
        ]

# to handle the change made on ItemCreateView of kwargs
    def __init__(self, user=None, *args, **kwargs):
        # print(kwargs.pop('user'))
        print(user)
        # print(kwargs.pop('instance')) #Item object
        # print(kwargs)
        super(ItemForm, self).__init__(*args, **kwargs)
        # self.fields['restaurant'].queryset = RestaurantLocation.objects.none()
        # self.fields['restaurant'].queryset = RestaurantLocation.objects.filter(owner=user, item__isnull=True).exclude(item__isnull=False)
        self.fields['restaurant'].queryset = RestaurantLocation.objects.filter(owner=user)
