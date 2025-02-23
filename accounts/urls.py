from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('complete-profile/', views.complete_profile, name='complete_profile'),
] 