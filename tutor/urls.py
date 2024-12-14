from django.urls import path
from . import views

app_name = 'tutor'

urlpatterns = [
    path('', views.TutorList.as_view(), name='tutor-list'),
    path('create/', views.TutorViewset.as_view(), name='tutor-create'),
    path('<int:pk>/', views.TutorDetail.as_view(), name='tutor-detail'),
    path('reviews/', views.ReviewViewset.as_view(), name='review-list-create'),
    path('search/', views.TutorSearchAPIView.as_view(), name='tutor-search'),
]
