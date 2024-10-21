# hrms/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from .forms import PerformanceReviewForm, LeaveRequestForm, AttendanceForm, UserRegistrationForm, EmployeeForm
from .models import Employee, LeaveRequest, PerformanceReview, Attendance, CustomUser
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.contrib.auth.decorators import user_passes_test  # Import the decorator


# Decorator to check if the user is an admin
def is_admin(user):
    return user.is_superuser  # or user.groups.filter(name='Admin').exists() for group-based checks



def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to a home page or dashboard
    else:
        form = UserRegistrationForm()
    return render(request, 'hrms/registration/register.html', {'form': form})


def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'hrms/employee_list.html', {'employees': employees})


def request_leave(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave_request = form.save(commit=False)
            leave_request.employee = request.user
            leave_request.save()
            messages.success(request, "Leave request submitted!")
            return redirect('view_leave_requests')
    else:
        form = LeaveRequestForm()
    return render(request, 'hrms/request_leave.html', {'form': form})
@login_required
def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Employee added successfully!")
            return redirect('employee_list')  # Redirect to the employee list view
    else:
        form = EmployeeForm()
    
    return render(request, 'hrms/add_employee.html', {'form': form})


def update_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'hrms/update_employee.html', {'form': form})

def delete_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        return redirect('employee_list')

def request_leave(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave_request = form.save(commit=False)
            leave_request.employee = request.user
            leave_request.save()
            messages.success(request, "Leave request submitted!")
            return redirect('view_leave_requests')
    else:
        form = LeaveRequestForm()
    return render(request, 'hrms/request_leave.html', {'form': form})
    return render(request, 'hrms/delete_employee.html', {'employee': employee})



def leave_request_list(request):
    leave_requests = LeaveRequest.objects.all()
    return render(request, 'hrms/leave_request_list.html', {'leave_requests': leave_requests})

def request_leave(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave_request = form.save(commit=False)
            leave_request.employee = request.user
            leave_request.save()
            messages.success(request, "Leave request submitted!")
            return redirect('view_leave_requests')
    else:
        form = LeaveRequestForm()
    return render(request, 'hrms/request_leave.html', {'form': form})

@login_required
def approve_leave(request, pk):
    if request.user.role != 'Admin':
        return HttpResponseForbidden("You do not have permission to approve leaves.")

    # Create attendance records for the leave period
    for single_date in pd.date_range(leave_request.start_date, leave_request.end_date):
        Attendance.objects.create(
            employee=leave_request.employee,
            date=single_date.date(),
            status='Absent',
            leave_request=leave_request
        )

    # Send notification email
    subject = 'Leave Approved'
    message = render_to_string('email/leave_approved.html', {
        'employee_name': leave_request.employee.user.username,
        'leave_type': leave_request.leave_type,
        'start_date': leave_request.start_date,
        'end_date': leave_request.end_date,
    })
    send_mail(subject, message, 'from@example.com', [leave_request.employee.user.email])

    return redirect('leave_request_list')

def reject_leave(request, pk):
    leave_request = get_object_or_404(LeaveRequest, pk=pk)
    leave_request.status = 'Rejected'
    leave_request.save()
    return redirect('leave_request_list')


def payroll_list(request):
    payrolls = Payroll.objects.all()
    return render(request, 'hrms/payroll_list.html', {'payrolls': payrolls})

def add_payroll(request):
    if request.method == 'POST':
        form = PayrollForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('payroll_list')
    else:
        form = PayrollForm()
    return render(request, 'hrms/add_payroll.html', {'form': form})


def conduct_review(request):
    if request.method == 'POST':
        review = PerformanceReview(
            employee=request.POST['employee'],
            goals=request.POST['goals'],
            feedback=request.POST['feedback']
        )
        review.save()
        messages.success(request, "Performance review saved!")
        return redirect('view_performance_reviews')
    return render(request, 'hrms/conduct_review.html')

def view_performance_reviews(request):
    reviews = PerformanceReview.objects.filter(employee=request.user)
    return render(request, 'hrms/view_performance_reviews.html', {'reviews': reviews})

def performance_review_list(request):
    reviews = PerformanceReview.objects.all()
    return render(request, 'hrms/performance_review_list.html', {'reviews': reviews})

def add_performance_review(request):
    if request.method == 'POST':
        form = PerformanceReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('performance_review_list')
    else:
        form = PerformanceReviewForm()
    return render(request, 'hrms/add_performance_review.html', {'form': form})


def attendance_list(request):
    attendance_records = Attendance.objects.all()
    return render(request, 'hrms/attendance_list.html', {'attendance_records': attendance_records})


@login_required
def mark_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save(commit=False)  # Don't save to the database yet
            attendance.employee = request.user  # Set the employee to the logged-in user
            attendance.date = timezone.now().date()  # Set the date to today
            attendance.save()  # Now save the instance
            messages.success(request, "Attendance marked successfully!")
            return redirect('attendance_list')  # Adjust the redirect as necessary
        else:
            messages.error(request, "Failed to mark attendance. Please check the form.")
            print(form.errors)  # Debugging line to check form errors
    else:
        form = AttendanceForm()
    
    return render(request, 'hrms/mark_attendance.html', {'form': form})
    
@user_passes_test(is_admin)
def attendance_report(request):
    attendance_records = Attendance.objects.all()  # Query all attendance records
    return render(request, 'hrms/attendance_report.html', {'attendance_records': attendance_records})


def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            if user.is_staff:  # Admin user
                return redirect('admin_dashboard')  # Redirect to admin dashboard
            else:  # Employee user
                return redirect('employee_dashboard')  # Redirect to employee dashboard
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'hrms/login.html')


def custom_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('custom_login')


def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('custom_login')  # Redirect non-admin users
    return render(request, 'hrms/admin_dashboard.html')


def employee_dashboard(request):
    if request.user.is_staff:
        return redirect('custom_login')  # Redirect admin users
    return render(request, 'hrms/employee_dashboard.html')


def employee_profile(request):
    employee = get_object_or_404(Employee, user=request.user)  # Get the logged-in employee
    return render(request, 'hrms/employee_profile.html', {'employee': employee})



