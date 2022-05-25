from django.contrib import admin
from django.db.models import Func
from import_export.admin import ImportExportModelAdmin
from .resources import *
from .forms import *
from .models import scrollModel

admin.site.index_title = ""

# Register your models here.
admin.site.register(tufidco_info)

admin.site.register(scrollModel)
@admin.register(Officer)
class OfficerAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'Designation'
    ]

    ordering = [
        'id'
    ]


class PostImageAdmin(admin.StackedInline):
    model = postphotogallery_slider


class PostFormSlider(admin.StackedInline):
    model = postreformslider


class PostMainSlider(admin.StackedInline):
    model = postmainslider


class GalleryAdmin(admin.StackedInline):
    model = gallery_Images


@admin.register(body_images)
class BodyAdmin(admin.ModelAdmin):
    inlines = [
        PostImageAdmin,
        PostFormSlider,
        PostMainSlider
    ]

    class Meta:
        model = body_images


@admin.register(postphotogallery_slider)
class PostImageAdmin(admin.ModelAdmin):
    pass


@admin.register(postreformslider)
class PostFormSlider(admin.ModelAdmin):
    pass


@admin.register(postmainslider)
class PostMainSlider(admin.ModelAdmin):
    pass


@admin.register(gallery_Images)
class GalleryAdmin(admin.ModelAdmin):
    list_display = [
        'place',
        'Date'
    ]

    readonly_fields = (
        'image_preview',
    )

    ordering = [
        'id'
    ]

    def image_preview(self, obj):
        return obj.image_preview

    image_preview.short_description = 'Image Preview'
    image_preview.allow_tags = True


# Sanction Form


admin.site.register(About)


class SchemeAdmin(ImportExportModelAdmin, admin.AdminSite):
    model = Scheme

    list_display = [
        'Scheme'
    ]


admin.site.register(Scheme, SchemeAdmin)

admin.site.register(SchemeSanctionPdf)


@admin.register(Scheme_Faq_Questions)
class SchemeFAQQuestion(admin.ModelAdmin):
    list_display = [
        'question',
        'name'
    ]

    ordering = [
        'question'
    ]


@admin.register(Scheme_Page)
class SchemePageAdmin(admin.ModelAdmin):
    pass


class AgencyTypeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    model = AgencyType

    list_display = [
        'AgencyType'
    ]

    ordering = [
        'id'
    ]


admin.site.register(AgencyType, AgencyTypeAdmin)


class AgencyNameAdmin(ImportExportModelAdmin):
    resource_class = AgencyNameResource

    list_display = [
        'AgencyName',
        'AgencyType'
    ]
    list_filter = ['AgencyType']
    ordering = [
        'AgencyName'
    ]

    search_fields = [
        'AgencyName'
    ]


admin.site.register(AgencyName, AgencyNameAdmin)


class DistrictAdmin(ImportExportModelAdmin):
    resource_class = DistrictResource

    list_display = [
        'District'
    ]

    ordering = [
        'District'
    ]

    search_fields = [
        'District'
    ]


admin.site.register(District, DistrictAdmin)


class RegionAdmin(ImportExportModelAdmin):
    resource_class = RegionResource

    list_display = [
        'Region'
    ]

    ordering = [
        'Region'
    ]

    search_fields = [
        'Region'
    ]


admin.site.register(Region, RegionAdmin)





class MasterSanctionFormAdmin(ImportExportModelAdmin, admin.AdminSite):
    change_form_template = 'admin/masterform.html'
    resource_class = MasterSanctionResource

    exclude = ['total']

    list_display = [
        'SNo',
        'AgencyName',
        'Sector',
        'ProjectName',
        'Project_ID',
        'Scheme',
        'ApprovedProjectCost',
        'SchemeShare',
        'ULBShare'
    ]

    list_filter = (
        'AgencyType',
        'Sector',
        'Scheme',
        'GoMeeting',
    )

    ordering = (
        'SNo',
    )

    search_fields = (
        'Project_ID',
        'Scheme__Scheme',
        'Sector',
        'GoMeeting',
        'ProjectName',
        'AgencyName__AgencyName',
        'District__District'
    )




admin.site.register(MasterSanctionForm, MasterSanctionFormAdmin)





"""
    Agency admin
"""




@admin.register(LatestReports)
class LatestReportAdmin(admin.ModelAdmin):
    pass





class Round(Func):
    function = "ROUND"
    template = "%(function)s(%(expressions)s::numeric, 2)"


admin.site.register(ULBReleaseRequest)

admin.site.register(PageCounter)




class SRPMasterSanctionFormAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = SRPMasterSanctionResource

    list_display = [
        'SNo',
        'AgencyType',
        'AgencyName',
        'Project_ID',
        'ProjectCost',
        'SchemeShare'
    ]
    list_filter = [
        'AgencyType',
        'R1_Date',
        'R2_Date'
    ]
    ordering = [
        'SNo'
    ]
    search_fields = [
        'AgencyType__AgencyType',
        'AgencyName__AgencyName',
        'SchemeShare',
        'Project_ID',
    ]


admin.site.register(SRPMasterSanctionForm, SRPMasterSanctionFormAdmin)



