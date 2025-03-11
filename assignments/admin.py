from django.contrib import admin
from .models import Assignment, PremiumAssignment, NonPremiumAssignment

class AssignmentAdmin(admin.ModelAdmin):
    list_display = (
        'title', 
        'student', 
        'degree', 
        'module', 
        'deadline', 
        'payment_status', 
        'status',
        'created_at',
        'brief', 
        'instructions',
        'completed_file'
    )
    readonly_fields = ('created_at',)
    fieldsets = (
        (None, {
            'fields': ('student', 'title', 'degree', 'module', 'deadline', 'payment_status', 'status')
        }),
        ('Assignment Details', {
            'fields': ('instructions', 'brief', 'completed_file'),
        }),
        ('Metadata', {
            'fields': ('created_at',),
        }),
    )

admin.site.register(Assignment, AssignmentAdmin)

class PremiumAssignmentAdmin(AssignmentAdmin):
    pass

admin.site.register(PremiumAssignment, PremiumAssignmentAdmin)

class NonPremiumAssignmentAdmin(AssignmentAdmin):
    pass

admin.site.register(NonPremiumAssignment, NonPremiumAssignmentAdmin)
