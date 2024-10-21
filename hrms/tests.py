# hrms/tests.py
from django.test import TestCase
from django.core import mail
from .models import Employee, LeaveRequest, CustomUser
from django.urls import reverse
from datetime import date

class LeaveRequestEmailTest(TestCase):

    def setUp(self):
        # Create a test user
        self.user = CustomUser.objects.create(username='testuser', email='joerironald@gmail.com')
        
        # Create a test employee with all required fields
        self.employee = Employee.objects.create(
            user=self.user,
            position='Developer',
            department='IT',
            date_of_birth=date(1990, 1, 1),  # Example date
            date_hired=date(2020, 1, 1)      # Example date
        )
        
        # Create a test leave request
        self.leave_request = LeaveRequest.objects.create(
            employee=self.employee,
            leave_type='Sick Leave',
            start_date='2024-01-01',
            end_date='2024-01-05',
            status='Pending'
        )

    def test_leave_approval_email(self):
        # Approve the leave request
        self.leave_request.status = 'Approved'
        self.leave_request.save()

        # Trigger the email sending
        response = self.client.post(reverse('approve_leave', args=[self.leave_request.id]))

        # Check that one message has been sent
        self.assertEqual(len(mail.outbox), 1)

        # Verify the subject and body of the email
        self.assertEqual(mail.outbox[0].subject, 'Leave Approved')
        self.assertIn('Your leave request for Sick Leave from 2024-01-01 to 2024-01-05 has been approved.', mail.outbox[0].body)