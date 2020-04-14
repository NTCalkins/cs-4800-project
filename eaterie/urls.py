from django.urls import path

from eaterie import views

app_name = 'eaterie'
urlpatterns = [
    path('', views.login_redirect, name='login_redirect'),  # used for redirecting authenticated user
    path('home/', views.HomePageView.as_view(), name='home'),

    path('customer/signup/', views.CustomerSignUpView.as_view(), name='customer_signup'),
    path('lets-eat/', views.CustomerHomeView.as_view(), name='customer_home'),
    path('customer/<int:pk>/cart/', views.CartView.as_view(), name='cart_view'),

    path('restaurant/signup', views.RestaurantSignUpView.as_view(), name='restaurant_signup'),
    path('restaurant/dashboard/', views.RestaurantHomeView.as_view(), name='restaurant_home'),

    path('account/<int:pk>/update', views.AccountUpdateView.as_view(), name='update_account'),
    path('restaurant/<int:pk>/menu', views.MenuView.as_view(), name='restaurant_menu'),
    path('restaurant/<int:pk>/menu/update', views.MenuUpdateView.as_view(), name='update_menu'),
]
