from django.urls import path

from . import views

urlpatterns = [
    path('imagelist', views.index, name='index'),
    path('imageviews/<int:image_id>/', views.imageviews, name='imageviews')
]
