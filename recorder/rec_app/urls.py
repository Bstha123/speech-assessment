from django.urls import path
from . import views

urlpatterns = [
    path('',views.record_audio, name="recorder")
]
