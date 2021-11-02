from django.urls import path

from . import views

app_name = "annotations"
urlpatterns = [
    path('image_list/', views.ImageListView.as_view(), name='imagelist'),
    path('image_views/<int:image_id>/', views.image_views, name='imageviews'),
    #path('image_views/<int:pk>/', views.ImageViewsView.as_view(), name='imageviews')
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('registration/success/', views.registration_success_views, name="regi-success"),
    path('image_upload/', views.image_upload_views, name='image-upload'),
    path('image_upload/success', views.image_upload_success_views, name='image-upload-success')

    ]
