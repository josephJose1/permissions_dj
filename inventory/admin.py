from django.contrib import admin
from inventory.models import Product
from guardian.admin import GuardedModelAdmin

@admin.register(Product)
class ProductAdmin(GuardedModelAdmin):
    list_display = ('name',) #username raise error is not callable
    
# admin.site.register(Product, ProductAdmin)

    def has_module_permission(self, request):
        #change slightly to avoid acces of all product
        if super().has_module_permission(request):
            #why we do that? we don't want to granted access to model, we want to granted access to object permission
            return True
    
    def get_queryset(self, request):
        return super().get_queryset(request)
    #create usrer to determine what user has permissions to?
    def has_permission(self, request, obj, action):
        opts = self.opts
        #action #view, change, delete
        #USING CODENAME IN THE TABLE
        code_name = f'{action}_{opts.model_name}' #for example add_logentry
        #check wether of user has permissions
        if obj:
            return request.user.has_perm(f'{opts.app_label}.{code_name}', obj)
    def has_view_permission(self, request, obj=None):
        return True
    def has_change_permission(self, request, obj=None):
        return True
    def has_delete_permission(self, request, obj=None):
        return True