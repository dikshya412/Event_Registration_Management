from django.contrib import admin
from .models import UserProfile,OrganizerRequest
from django.utils import timezone
# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user','role','phone','created_at')
    list_filter = ('role',)
    search_fields = ('user__username','user__email')

@admin.register(OrganizerRequest)
class OrganizerRequestAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'status',
        'requested_at',
        'reviewed_at'
    )
    list_filter = ('status', 'requested_at')
    search_fields = ('user__username', 'reason')
    readonly_fields = ('requested_at', 'reviewed_at')
    actions = ['approve_requests', 'reject_requests']

    @admin.action(description='Approve selected requests')
    def approve_requests(self, request, queryset):
        for organizer_request in queryset:
            organizer_request.status = 'approved'
            organizer_request.reviewed_at = timezone.now()
            organizer_request.save()

            # Change the user's role
            profile = organizer_request.user.profile
            profile.role = 'organizer'
            profile.save()

    @admin.action(description='Reject selected requests')
    def reject_requests(self, request, queryset):
        for organizer_request in queryset:
            organizer_request.status = 'rejected'
            organizer_request.reviewed_at = timezone.now()
            organizer_request.save()

    
