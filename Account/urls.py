from django.urls import path, re_path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup_form'),
    path('api_token_auth/', obtain_auth_token, name='api_token_auth'),
    path('files/', views.GetFileListView.as_view(), name='get_file_list'),
    path('profile/', views.ProfileView.as_view(), name='profile_view'),
    re_path('files/(?P<filename>.+)/', views.FileView.as_view(), name='file'),
]
