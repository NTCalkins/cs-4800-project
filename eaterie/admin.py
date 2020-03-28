from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from eaterie.models import CustomUserModel, Restaurant, Customer, MenuCategory, State, City, ZipCode, MenuItem


@admin.register(CustomUserModel)
class CustomUserAdmin(UserAdmin):
    model = CustomUserModel
    list_display = ('email', 'first_name', 'last_name', 'is_customer', 'is_restaurant', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_customer', 'is_restaurant', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'groups', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


# register model to admin
admin.site.register(Customer)


class MenuItemInline(TabularInline):
    model = MenuItem
    extra = 1


class MenuCategoryInline(TabularInline):
    model = MenuCategory
    extra = 1


# Register the Admin classes for Restaurant using the decorator
@admin.register(Restaurant)
class RestaurantAdmin(ModelAdmin):
    list_display = ('restaurant_name', 'restaurant_address', 'phone_number', 'zip_code')
    list_filter = ('zip_code', 'restaurant_name')
    inlines = [MenuCategoryInline]


# Register the Admin classes for MenuCategory using the decorator
@admin.register(MenuCategory)
class MenuCategoryAdmin(ModelAdmin):
    list_display = ('category_name', 'restaurant')
    list_filter = ('category_name', 'restaurant')
    inlines = [MenuItemInline]


# Register the Admin classes for MenuCategory using the decorator
@admin.register(MenuItem)
class MenuItemAdmin(ModelAdmin):
    list_display = ('item_name', 'category')
    list_filter = ('item_name', 'category')


class CityInline(TabularInline):
    model = City
    extra = 1


class ZipCodeInline(TabularInline):
    model = ZipCode
    extra = 1


# Register the Admin classes for States using the decorator
@admin.register(State)
class StateAdmin(ModelAdmin):
    list_display = ('state_code', 'state_name')
    list_filter = ('state_code', 'state_name')
    inlines = [CityInline]


# Register the Admin classes for MenuCategory using the decorator
@admin.register(City)
class CityAdmin(ModelAdmin):
    list_display = ('city_name', 'state_code')
    list_filter = ('city_name', 'state_code')
    inlines = [ZipCodeInline]


# Register the Admin classes for MenuCategory using the decorator
@admin.register(ZipCode)
class ZipCodeAdmin(ModelAdmin):
    list_display = ('zip_code', 'city')
    list_filter = ('zip_code', 'city')
