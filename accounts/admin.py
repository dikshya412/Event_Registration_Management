from django.contrib import admin
from .models import UserProfile
# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user','role','phone','created_at')
    list_filter = ('role',)
    search_fields = ('user_username','user_email')

    
