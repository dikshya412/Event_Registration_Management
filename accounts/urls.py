from django.urls import path
from . import views

urlpatterns = [
    path('organizer-request/',views.organizer_request,name='organizer_request'),

]
