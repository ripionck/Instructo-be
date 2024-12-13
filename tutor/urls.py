from django.urls import path
from . import views

app_name = 'tutor'

urlpatterns = [
    path('', views.TutorListView.as_view(), name='tutor-list'),
    path('create/', views.TutorCreateView.as_view(), name='tutor-create'),
    path('<int:pk>/', views.TutorDetailView.as_view(), name='tutor-detail'),
    path('<int:pk>/update/', views.TutorUpdateView.as_view(), name='tutor-update'),
    path('<int:pk>/delete/', views.TutorDeleteView.as_view(), name='tutor-delete'),

    path('subjects/', views.SubjectChoiceListView.as_view(), name='subject-list'),

    path('<int:tutor_id>/reviews/', views.ReviewListCreateView.as_view(),
         name='review-list-create'),
    path('reviews/<int:pk>/', views.ReviewDetailView.as_view(), name='review-detail'),

    path('filter/class/', views.TutorClassFilterView.as_view(), name='class-filter'),
    path('filter/subject/', views.TutorSubjectFilterView.as_view(),
         name='subject-filter'),
]
