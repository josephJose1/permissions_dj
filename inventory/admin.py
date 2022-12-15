from django.contrib import admin

# Register your models here.
from inventory.models import Product

# admin.site.register(Product)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name",)
    #what user is able to do
    def get_form(self, request, obj = None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        
        if not is_superuser:
            if 'name' in form.base_fields:
                form.base_fields['name'].disabled = True
        return form
    
    #access permissions directly
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj= None):
        return True

