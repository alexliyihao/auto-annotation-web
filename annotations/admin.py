from django.contrib import admin
from .models import User, Image, Annotation, Organization, ImageGroup

class UserAdmin(admin.ModelAdmin):
    fields = [
        "username", "password","UNI" , "email", "first_name", "last_name",
        "register_date", "organizations"
        ]
admin.site.register(User, UserAdmin)

class ImageAdmin(admin.ModelAdmin):
    fields = [
        "image_name","submission_date","translated", "svs_path",
        "dzi_path","height","width","completely_annotated",
        "group", "submit_user", "image_description",
        ]
admin.site.register(Image, ImageAdmin)

class AnnotationAdmin(admin.ModelAdmin):
    fields = [
        'W3C_id','contour','update_date' ,"image","annotator"
        ]

admin.site.register(Annotation, AnnotationAdmin)

class OrganizationAdmin(admin.ModelAdmin):
    fields = [
        "organization_name", 'supervisor'
        ]

admin.site.register(Organization, OrganizationAdmin)

class ImageGroupAdmin(admin.ModelAdmin):
    fields = [
        "group_name", "group_size", "group_description"
        ]

admin.site.register(ImageGroup, ImageGroupAdmin)
