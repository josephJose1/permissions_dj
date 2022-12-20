from django.contrib import admin
from inventory.models import Product
from guardian.admin import GuardedModelAdmin
from guardian.shortcuts import get_objects_for_user

@admin.register(Product)
class ProductAdmin(GuardedModelAdmin):
    list_display = ('name',) #username raise error is not callable
    
# admin.site.register(Product, ProductAdmin)

    def has_module_permission(self, request):
        #change slightly to avoid acces of all product
        if super().has_module_permission(request):
            #why we do that? we don't want to granted access to model, we want to granted access to object permission
            return True
        return self.get_model_objects(request).exists()
    
    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        
        data = self.get_model_objects(request)
        return data    
        
    
    #create usrer to determine what user has permissions to?
    def has_permission(self, request, obj, action):
        opts = self.opts
        #action #view, change, delete
        #USING CODENAME IN THE TABLE
        code_name = f'{action}_{opts.model_name}' #for example add_logentry
        #check wether of user has permissions
        if obj:
            return request.user.has_perm(f'{opts.app_label}.{code_name}', obj)
        else:
            return True #if it's False #everything is forbidden
    def get_model_objects(self, request, action=None, klass=None):
        opts = self.opts
        actions = [action] if action else ['view', 'edit', 'delete', 'add']
        klass = klass if klass else opts.model
        model_name = klass._meta.model_name
        return get_objects_for_user(user=request.user, perms=[f'{perm}_{model_name}' for perm in actions], klass=klass, any_perm=True)
        #klass cannot be None
    
    
    def has_view_permission(self, request, obj=None):
        return self.has_permission(request, obj, 'view')
    
    def has_change_permission(self, request, obj=None):
        return self.has_permission(request, obj, 'change')
    
    def has_delete_permission(self, request, obj=None):
        return self.has_permission(request, obj, 'delete')
