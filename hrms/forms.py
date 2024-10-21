# hrms/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Employee, LeaveRequest, PerformanceReview, Attendance

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']


class EmployeeForm(forms.ModelForm):
    username = forms.CharField(max_length=150, label="Username")
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    
    class Meta:
        model = Employee
        fields = ['username', 'email', 'password', 'position', 'department', 'date_of_birth', 'date_hired']

    def save(self, commit=True):
        # Create a new CustomUser first
        user = CustomUser(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            role='Employee'  # Set the role to Employee
        )
        user.set_password(self.cleaned_data['password'])  # Set the password securely
        if commit:
            user.save()
        
        # Now create the employee record
        employee = super().save(commit=False)
        employee.user = user
        if commit:
            employee.save()
        
        return employee




class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['leave_type', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class PerformanceReviewForm(forms.ModelForm):
    class Meta:
        model = PerformanceReview
        fields = ['employee', 'goals', 'feedback']
        widgets = {
            'feedback': forms.Textarea(attrs={'rows': 4}),
        }

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['check_in_time', 'check_out_time']  # Ensure both fields are included
        widgets = {
            'check_in_time': forms.TimeInput(attrs={'type': 'time'}),
            'check_out_time': forms.TimeInput(attrs={'type': 'time'}),
        }