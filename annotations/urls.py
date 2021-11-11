from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = "annotations"
urlpatterns = [
    path('image_list/', views.ImageListView.as_view(), name='image-list'),
    path('image_views/<int:image_id>/', views.image_views, name='image-views'),
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('registration/success/', views.registration_success_views, name="registration-success"),
    path('image_upload/', views.image_upload_views, name='image-upload'),
    path('image_upload/success/', views.image_upload_success_views, name='image-upload-success'),
    path('login/', views.UserLoginView.as_view(), name = 'login'),
    path('login/success/', views.user_login_success_view, name = 'login-success'),
    path('logout/', views.UserLogoutView.as_view(), name = "logout"),
    path('logout/success/', views.user_logout_success_view, name = 'logout-success'),
    path('contact/', views.contact_view, name = 'contact'),
    path('profile/', views.user_profile_view_self, name = 'profile-self'),
    path('profile/<int:user_id>/', views.user_profile_view_others, name = 'profile-others'),
    path('organization', views.organization_profile_view_self, name = 'organization-view-self'),
    path('organization/<int:organization_id>/', views.organization_profile_view_others, name = 'organization-view-others'),
    path('image_group/<int:image_group_id>/', views.image_group_view, name = 'image-group-view'),
    path('people/', views.people_view, name = "people")
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
