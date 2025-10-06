from django.contrib import admin
from .models import Location, WeddingPartyMember, RSVP


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('location_name', 'city', 'state_country', 'order', 'is_active', 'date_visited')
    list_filter = ('is_active', 'state_country')
    search_fields = ('location_name', 'city', 'state_country', 'description')
    list_editable = ('order', 'is_active')
    ordering = ('order', 'date_visited')

    fieldsets = (
        ('Location Information', {
            'fields': ('location_name', 'city', 'state_country', 'latitude', 'longitude')
        }),
        ('Details', {
            'fields': ('description', 'significance', 'date_visited', 'photo')
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active')
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return ('created_at', 'updated_at')
        return ()


@admin.register(WeddingPartyMember)
class WeddingPartyMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'side', 'order', 'is_active')
    list_filter = ('side', 'role', 'is_active')
    search_fields = ('name', 'bio')
    list_editable = ('order', 'is_active')
    ordering = ('side', 'order')

    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'role', 'side', 'photo')
        }),
        ('Details', {
            'fields': ('bio',)
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active')
        }),
    )


@admin.register(RSVP)
class RSVPAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'attendance', 'number_of_guests', 'submitted_at')
    list_filter = ('attendance', 'submitted_at')
    search_fields = ('first_name', 'last_name', 'email')
    readonly_fields = ('submitted_at', 'updated_at')
    date_hierarchy = 'submitted_at'

    fieldsets = (
        ('Guest Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('RSVP Details', {
            'fields': ('attendance', 'number_of_guests', 'guest_names', 'dietary_restrictions')
        }),
        ('Special Requests', {
            'fields': ('song_request', 'message')
        }),
        ('Timestamps', {
            'fields': ('submitted_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Name'

    def has_add_permission(self, request):
        # Typically RSVPs should only be added through the form, not admin
        # But we'll allow it for flexibility
        return True
