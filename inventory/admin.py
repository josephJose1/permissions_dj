from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

# Register your models here.
from inventory.models import Product

from django.contrib.auth.models import User, Group

admin.site.unregister(User)
admin.site.unregister(Group)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    def get_form(self, request, obj = None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        
        if not is_superuser:
            if 'username' in form.base_fields:
                form.base_fields['username'].disabled = True
            form.base_fields['is_superuser'].disabled = True
            form.base_fields['user_permissions'].disabled = True
            form.base_fields['groups'].disabled = True
            
        return form

# admin.site.register(Product)
# class ReadOnlyAdminMixin:
#     #access permissions directly
#     def has_add_permission(self, request):
#         return False
#     #https://docs.djangoproject.com/en/4.1/topics/auth/default/
#     def has_change_permission(self, request, obj=None):
#         if request.user.has_perm('inventory.change_product'):
#             #app_label.codename
#             return True
#         else:
#             return False

#     def has_delete_permission(self, request, obj=None):
#         return False

#     def has_view_permission(self, request, obj= None):
#         return True

#BE CAREFULL WITH NAME RESOLUTIONS , read onlyclas goes first

# @admin.register(Product)
# class ProductAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
#     list_display = ("name",)
#     #what user is able to do
#     def get_form(self, request, obj = None, **kwargs):
#         form = super().get_form(request, obj, **kwargs)
#         is_superuser = request.user.is_superuser
        
#         if not is_superuser:
#             if 'name' in form.base_fields:
#                 form.base_fields['name'].disabled = True
#         return form
    


