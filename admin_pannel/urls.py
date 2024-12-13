from django.urls import path
from .views import (
    AdminApiView,
    AdminLoginApiView,
    AdminLogoutApiView,
    AdminRegistrationView,
    activate_view
)

app_name = 'admin_pannel'

urlpatterns = [
    path('list/', AdminApiView.as_view(), name='admin-list'),
    path('register/', AdminRegistrationView.as_view(), name='register'),
    path('login/', AdminLoginApiView.as_view(), name='login'),
    path('logout/', AdminLogoutApiView.as_view(), name='logout'),
    path('active/<str:uid64>/<str:token>/', activate_view, name='activate'),
]
