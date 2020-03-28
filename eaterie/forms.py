from betterforms.multiform import MultiModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.db import transaction
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from eaterie.models import CustomUserModel, Restaurant, Customer, ZipCode


class CustomerSignUpForm(UserCreationForm):
    class Meta:
        model = CustomUserModel
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

    @transaction.atomic
    def save(self, commit=False):
        user = super(CustomerSignUpForm, self).save(commit)
        user.is_customer = True
        user.save()
        customer = Customer.objects.create(user=user)
        return customer.user


class RestaurantSignUpForm(UserCreationForm):
    phone_number = forms.CharField(max_length=10, )
    restaurant_name = forms.CharField(max_length=80)
    zip_code = forms.CharField(max_length=5)

    class Meta:
        model = CustomUserModel
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'restaurant_name', 'password1', 'password2',
                  'zip_code']

    def clean_zip_code(self):
        zip = self.cleaned_data['zip_code']
        if not ZipCode.objects.filter(zip_code=zip).exists():
            raise ValidationError(_('We are sorry, our service is not available at your location.'))
        return zip

    @transaction.atomic
    def save(self, commit=False):
        user = super(RestaurantSignUpForm, self).save(commit)
        user.is_restaurant = True
        user.save()
        restaurant = Restaurant.objects.create(user=user,
                                               restaurant_name=self.cleaned_data.get('restaurant_name'),
                                               phone_number=self.cleaned_data.get('phone_number'),
                                               zip_code=ZipCode.objects.get(zip_code=self.cleaned_data.get('zip_code'))
                                               )
        restaurant.save()
        return restaurant.user


class CustomerProfileForm(ModelForm):
    class Meta:
        model = Customer
        exclude = ['user']
        widgets = {'avatar': forms.FileInput}


class RestaurantProfileForm(ModelForm):
    class Meta:
        model = Restaurant
        exclude = ['zip_code', 'user']
        widgets = {'image_file': forms.FileInput}


class UserForm(ModelForm):
    class Meta:
        model = CustomUserModel
        fields = ('first_name', 'last_name')


class CustomerUpdateForm(MultiModelForm):
    form_classes = {
        'user_account': UserForm,
        'customer_profile': CustomerProfileForm
    }


class RestaurantUpdateForm(MultiModelForm):
    form_classes = {
        'user_account': UserForm,
        'restaurant_profile': RestaurantProfileForm,
    }


class RestaurantSearchForm(forms.Form):
    zip_code = forms.CharField(label='Zip Code', max_length=5, required=True)
