from django.core.mail import send_mail
from django.shortcuts import render
from .forms import EmailForm

def send_email_view(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            recipient = form.cleaned_data['recipient']
            send_mail(subject, message, 'joerironaldl@gmail.com', [recipient])
            return render(request, 'emailapp/email_sent.html')
    else:
        form = EmailForm()
    
    return render(request, 'emailapp/send_email.html', {'form': form})