from allauth.account.views import SignupView
from django import forms
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, UpdateView, DetailView, ListView
from nested_formset import nestedformset_factory

from eaterie.decorators import (customer_required, restaurant_required, user_identity_check,
                                restaurant_owner_identity_check)
from eaterie.forms import (CustomerSignUpForm, RestaurantSignUpForm, CustomerUpdateForm, RestaurantUpdateForm,
                           RestaurantSearchForm)
from eaterie.models import Restaurant, CustomUserModel, MenuCategory, MenuItem, Customer, Cart, CartEntry, Order


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


@method_decorator(customer_required, name='dispatch')
class CustomerHomeView(ListView):
    model = Restaurant
    form_class = RestaurantSearchForm
    template_name = 'eaterie/customer_home.html'
    context_object_name = 'restaurants'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(CustomerHomeView, self).get_context_data(**kwargs)
        customer = Customer.objects.get(user=self.request.user)
        initial = {'zip_code': customer.zip_code}
        context['form'] = RestaurantSearchForm(initial=initial)
        return context

    def get_queryset(self):
        form = self.form_class(self.request.GET)
        customer = Customer.objects.get(user=self.request.user)
        if form.is_valid():
            return Restaurant.objects.filter(zip_code__zip_code=form.cleaned_data['zip_code'])
        elif customer.zip_code:
            return Restaurant.objects.filter(zip_code__zip_code=customer.zip_code)
        return Restaurant.objects.none()


@method_decorator(restaurant_required, name='dispatch')
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


@method_decorator(user_identity_check, name='dispatch')
@method_decorator(login_required, name='dispatch')
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





@method_decorator(login_required, name='dispatch')
class MenuView(DetailView):
    model = Restaurant
    template_name = 'eaterie/restaurant_menu.html'

    def get_success_url(self):
        restaurant = Restaurant.objects.get(user=self.request.user)
        return reverse('eaterie:menu', args=[str(restaurant.id)])

    def post(self, request, *args, **kwargs):
        if "Add to cart" == request.POST['add_to_cart_button']:
            menu_item_pk = request.POST['mipk']
            item_amount = int(request.POST['item_amount'])
            cart = Cart.objects.get(customer=self.request.user.customer)
            Cart.add_cart_item(cart, menu_item_pk, item_amount)
        return HttpResponseRedirect(request.path_info)


@method_decorator(restaurant_owner_identity_check, name='dispatch')
@method_decorator(restaurant_required, name='dispatch')
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


#@method_decorator(customer_required, name='dispatch')
#@method_decorator(user_identity_check, name='dispatch')
@method_decorator(login_required, name='dispatch')
class CartView(TemplateView):
    model = Cart
    template_name = 'eaterie/cart_view.html'

    def post(self, request, *args, **kwargs):
        customer = self.request.user.customer
        si = request.POST['special_instructions']
        print(si)
        cart = Cart.objects.get(customer=customer)
        print("Emptying cart of " + str(cart.customer))
        new_order = Cart.checkout(cart)
        # Check if a new order was generated
        if new_order:
            new_order.special_instruction = si
            new_order.save()
        return HttpResponseRedirect(request.path_info)

@method_decorator(login_required, name='dispatch')
@method_decorator(customer_required, name='dispatch')
class OrderListView(ListView):
    model = Order
    template_name = 'eaterie/order_list_view.html'


    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user.customer)

@method_decorator(user_identity_check, name='dispatch')
@method_decorator(customer_required, name='dispatch')
class OrderDetailView(DetailView):
    model = Order
    template_name = 'eaterie/order_detail_view.html'

