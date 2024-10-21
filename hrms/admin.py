# hrms/admin.py
from django.contrib import admin
from .models import CustomUser, Employee, Attendance, LeaveRequest, PerformanceReview

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'position', 'department', 'date_hired')
    search_fields = ('user__username', 'position', 'department')

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'check_in_time', 'check_out_time')
    list_filter = ('employee', 'date')

class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('employee', 'leave_type', 'start_date', 'end_date', 'status')
    list_filter = ('employee', 'leave_type', 'status')

class PerformanceReviewAdmin(admin.ModelAdmin):
    list_display = ('employee', 'review_date', 'goals')
    list_filter = ('employee',)

# Register your models
admin.site.register(CustomUser)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(LeaveRequest, LeaveRequestAdmin)
admin.site.register(PerformanceReview, PerformanceReviewAdmin)