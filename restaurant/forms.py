from django import forms
from .validators import validate_category

from .models import RestaurantLocation

class RestaurantCreateForm(forms.Form):
    name            = forms.CharField()
    location        = forms.CharField(required=False)
    catagory        = forms.CharField(required=False)
    # files           = forms.FileField(required=False)

    # def clean_name(self):
    #     name = self.cleaned_data.get('name')
    #     if name == "hello":
    #         raise forms.ValidationError("Not a valid name")
    #     return name


class RestaurantLocationCreateForm(forms.ModelForm):
    # email       = forms.EmailField()     # builtin method
    # category      = forms.CharField(required= False, validators=[validate_category])
    class Meta:
        model = RestaurantLocation
        fields = [
            'name',
            'location',
            'category',
            'slug'
        ]

#custome  method
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name == "hello":
            raise forms.ValidationError("Not a valid name")
        return name

    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     if '.eyu' in email:
    #         raise forms.ValidationError("We don't accept .eyu")
    #     return email
