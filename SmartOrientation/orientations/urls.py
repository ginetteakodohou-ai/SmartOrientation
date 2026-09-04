from django.urls import path
from . import views

urlpatterns = [
    path('analyse/', views.orientation_view, name='orientation_analyse'),
]