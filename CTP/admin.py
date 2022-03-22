from django.contrib import admin
from CTP.models import *


# Register your models here.

@admin.register(TownPanchayatDetails)
class TownPanchayatDetailsAdmin(admin.ModelAdmin):
    exclude = ['user']

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            'show_save': True,
            'show_save_and_add_another': False,
        })
        return super().render_change_form(request, context, add, change, form_url, obj)

    def get_queryset(self, request):
        qs = super(TownPanchayatDetailsAdmin, self).get_queryset(request)
        if not request.user.groups.filter(name__in=["Admin",]).exists():
            return qs.filter(user=request.user)
        return qs

    def has_add_permission(self, request, *args, **kwargs):
        return not TownPanchayatDetails.objects.filter(user=request.user).exists() and not request.user.groups.filter(
            name__in=[
                "Admin", "CMD_DGM"]).exists()
