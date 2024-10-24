# hrms/urls.py
from django.urls import path
from .views import (
    register, 
    employee_list, 
    add_employee, 
    update_employee, 
    delete_employee,
    leave_request_list,
    request_leave,
    approve_leave,
    reject_leave,
    payroll_list,
    add_payroll,
    performance_review_list,
    add_performance_review,
    attendance_list,
    mark_attendance,
    attendance_report,
    custom_login,
    custom_logout,
    admin_dashboard,
    employee_dashboard,
    employee_profile,
    conduct_review,
    view_performance_reviews,
    
)

urlpatterns = [
    path('', register, name='register'),
    path('employees/', employee_list, name='employee_list'),
    path('employees/add/', add_employee, name='add_employee'),
    path('employees/update/<int:pk>/', update_employee, name='update_employee'),
    path('employees/delete/<int:pk>/', delete_employee, name='delete_employee'),
    path('leaves/', leave_request_list, name='leave_request_list'),
    path('leaves/request/', request_leave, name='request_leave'),
    path('leaves/approve/<int:pk>/', approve_leave, name='approve_leave'),
    path('leaves/reject/<int:pk>/', reject_leave, name='reject_leave'),
    path('payrolls/', payroll_list, name='payroll_list'),
    path('payrolls/add/', add_payroll, name='add_payroll'),
    path('performance/', performance_review_list, name='performance_review_list'),
    path('performance/add/', add_performance_review, name='add_performance_review'),
    path('attendance/', attendance_list, name='attendance_list'),
    path('attendance/mark/', mark_attendance, name='mark_attendance'),
    path('attendance/report/', attendance_report, name='attendance_report'),
    path('login/', custom_login, name='custom_login'),
    path('admin/', admin_dashboard, name='admin_dashboard'),
    path('employee/', employee_dashboard, name='employee_dashboard'),
    path('employee/profile/', employee_profile, name='employee_profile'),
    path('logout/', custom_logout, name='logout'),
    path('performance/conduct/', conduct_review, name='conduct_review'),
    path('performance/reviews/', view_performance_reviews, name='view_performance_reviews'),
]