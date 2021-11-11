from django.contrib import admin
from .models import User, Image, Annotation, Organization, ImageGroup

class UserAdmin(admin.ModelAdmin):
    fieldsets = (
    ("login", {
        "fields": ["username", "password"]
    }),
    ("Personal Information",{
        'classes': ('collapse',),
        'fields': ["UNI" , "email", "first_name", "last_name",
         "organizations"],
    }),
    )
admin.site.register(User, UserAdmin)


class ImageAdmin(admin.ModelAdmin):
    fields = [
        "image_name","translated", "svs_path",
        "dzi_path","height","width","completely_annotated",
        "group", "submit_user", "image_description"
        ]
admin.site.register(Image, ImageAdmin)


class AnnotationAdmin(admin.ModelAdmin):
    fields = [
        'W3C_id','annotation_class','contour',
        "image","annotator", 'description'
        ]

admin.site.register(Annotation, AnnotationAdmin)


class OrganizationAdmin(admin.ModelAdmin):
    fields = [
        "organization_name", 'supervisor', 'description'
        ]

admin.site.register(Organization, OrganizationAdmin)


class ImageGroupAdmin(admin.ModelAdmin):
    fields = [
        "group_name", "group_description"
        ]

admin.site.register(ImageGroup, ImageGroupAdmin)
