from django.urls import path
from .views import ApplicationListCreateView, ApplicationDetailView

app_name = 'application'

urlpatterns = [
    path('', ApplicationListCreateView.as_view(),
         name='application-list-create'),
    path('<int:pk>/', ApplicationDetailView.as_view(),
         name='application-detail'),
]
