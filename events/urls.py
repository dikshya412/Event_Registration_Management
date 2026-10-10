from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/',views.user_logout, name='logout'),
    path('create/', views.event_create, name='event_create'),
    path('<int:event_id>/edit/', views.event_update, name='event_update'),
    path('<int:event_id>/delete/', views.event_delete, name='event_delete'),
    path('event/<int:event_id>/register/',views.event_register,name='event_register'),
    path('<int:event_id>/', views.event_detail, name='event_detail'),
    path('my-registrations/', views.my_registrations, name='my_registrations'),
    path('registration/<int:registration_id>/cancel/',views.cancel_registration,name='cancel_registration'),
]
