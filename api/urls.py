from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'muscles', views.MuscleViewSet, basename='muscle')
router.register(r'exercises', views.ExerciseViewSet, basename='exercise')
router.register(r'trainings', views.TrainingViewSet, basename='training')

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', views.register, name='register'),
    path('auth/login/', views.login, name='login'),
    path('auth/profile/', views.profile, name='profile'),
    
    # Router URLs
    path('', include(router.urls)),
]
