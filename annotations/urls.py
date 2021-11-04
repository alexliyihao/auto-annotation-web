from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = "annotations"
urlpatterns = [
    path('image_list/', views.ImageListView.as_view(), name='image-list'),
    path('image_views/<int:image_id>/', views.image_views, name='image-views'),
    #path('image_views/<int:pk>/', views.ImageViewsView.as_view(), name='imageviews')
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('registration/success/', views.registration_success_views, name="regi-success"),
    path('image_upload/', views.image_upload_views, name='image-upload'),
    path('image_upload/success', views.image_upload_success_views, name='image-upload-success'),
    path('login/', views.UserLoginView.as_view(), name = 'login'),
    path('login/success', views.user_login_success_view, name = 'login-success'),
    path('logout', views.UserLogoutView.as_view(), name = "logout"),
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
