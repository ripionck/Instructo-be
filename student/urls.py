from django.urls import path
from . import views

app_name = 'student'

urlpatterns = [
    path('register/', views.StudentRegistrationView.as_view(),
         name='student-register'),
    path('login/', views.StudentLoginApiView.as_view(), name='student-login'),
    path('logout/', views.StudentLogoutApiView.as_view(), name='student-logout'),
    path('profile/', views.StudentProfileApiView.as_view(), name='student-profile'),
    path('change-password/', views.ChangePasswordApiView.as_view(),
         name='change-password'),
    path('class-filter/', views.ClassFilter.as_view(), name='class-filter'),
]
