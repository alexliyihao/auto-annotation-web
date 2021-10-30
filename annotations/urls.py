from django.urls import path

from . import views

app_name = "annotations"
urlpatterns = [
    path('image_list', views.ImageListView.as_view(), name='imagelist'),
    path('image_views/<int:image_id>/', views.image_views, name='imageviews')
    #path('image_views/<int:pk>/', views.ImageViewsView.as_view(), name='imageviews')
]
