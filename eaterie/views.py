from allauth.account.views import SignupView
from django import forms
from django.forms import inlineformset_factory
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView, UpdateView, DetailView, ListView
from nested_formset import nestedformset_factory

from eaterie.forms import CustomerSignUpForm, RestaurantSignUpForm, CustomerUpdateForm, RestaurantUpdateForm, \
    RestaurantSearchForm
from eaterie.models import Restaurant, CustomUserModel, MenuCategory, MenuItem


def login_redirect(request):
    if request.user.is_authenticated:
        user = CustomUserModel.objects.get(id=request.user.id)
        if user.is_customer:
            return redirect('eaterie:customer_home')
        elif user.is_restaurant:
            return redirect('eaterie:restaurant_home')
    return redirect('eaterie:home')


class HomePageView(TemplateView):
    template_name = 'eaterie/home.html'


class CustomerHomeView(ListView):
    model = Restaurant
    form_class = RestaurantSearchForm
    template_name = 'eaterie/customer_home.html'
    context_object_name = 'restaurants'
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super(CustomerHomeView, self).get_context_data(**kwargs)
        context['form'] = RestaurantSearchForm
        return context

    def get_queryset(self):
        form = self.form_class(self.request.GET)
        if form.is_valid():
            return Restaurant.objects.filter(zip_code__zip_code=form.cleaned_data['zip_code'])
        return Restaurant.objects.none()


class RestaurantHomeView(TemplateView):
    model = Restaurant
    template_name = 'eaterie/restaurant_home.html'


class CustomerSignUpView(SignupView):
    model = CustomUserModel
    form_class = CustomerSignUpForm
    template_name = 'eaterie/customer_signup.html'


class RestaurantSignUpView(SignupView):
    model = CustomUserModel
    form_class = RestaurantSignUpForm
    template_name = 'eaterie/restaurant_signup.html'


class AccountUpdateView(UpdateView):
    model = CustomUserModel
    template_name = 'eaterie/account_update.html'

    def get_form_kwargs(self):
        kwargs = super(AccountUpdateView, self).get_form_kwargs()
        if self.request.user.is_customer:
            kwargs.update(instance={
                'user_account': self.object,
                'customer_profile': self.object.customer,
            })
        elif self.request.user.is_restaurant:
            kwargs.update(instance={
                'user_account': self.object,
                'restaurant_profile': self.object.restaurant,
            })
        return kwargs

    def get_form_class(self):
        if self.request.user.is_customer:
            return CustomerUpdateForm
        elif self.request.user.is_restaurant:
            return RestaurantUpdateForm

    def get_success_url(self):
        return reverse('eaterie:update_account', args=[str(self.request.user.id)])


class MenuView(DetailView):
    model = Restaurant
    template_name = 'eaterie/restaurant_menu.html'

    def get_success_url(self):
        restaurant = Restaurant.objects.get(user=self.request.user)
        return reverse('eaterie:menu', args=[str(restaurant.id)])


class MenuUpdateView(UpdateView):
    model = Restaurant
    exclude = ['user', 'zip_code']
    template_name = 'eaterie/menu_update.html'

    def get_form_class(self):
        return nestedformset_factory(
            Restaurant,
            MenuCategory,
            extra=1,
            nested_formset=inlineformset_factory(
                MenuCategory,
                MenuItem,
                fields='__all__',
                widgets={'image_file': forms.FileInput},
                extra=1
            )
        )

    def get_success_url(self):
        restaurant = Restaurant.objects.get(user=self.request.user)
        return reverse('eaterie:update_menu', args=[str(restaurant.id)])
