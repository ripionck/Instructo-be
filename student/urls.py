from django.urls import path
from . import views

app_name = 'student'

urlpatterns = [
    path('register/', views.StudentRegistrationView.as_view(),
         name='student-register'),
    path('login/', views.StudentLoginView.as_view(), name='student-login'),
    path('logout/', views.StudentLogoutView.as_view(), name='student-logout'),
    path('profile/', views.StudentProfileView.as_view(), name='student-profile'),
    path('change-password/', views.ChangePasswordView.as_view(),
         name='change-password'),
    path('class-filter/', views.ClassFilterView.as_view(), name='class-filter'),
]
