from django.contrib import admin
from .models import User, Image, Annotation, Organization, ImageGroup

admin.site.register(User)
admin.site.register(Image)
admin.site.register(Annotation)
admin.site.register(Organization)
admin.site.register(ImageGroup)
