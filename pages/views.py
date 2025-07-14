from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm

# Create your views here.


def about_us(request):
    """Render the about us page"""
    return render(request, 'pages/about.html')


def contact_us(request):
    """Handle contact form display and submission"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Try to send the email
            email_sent = form.send_email()

            if email_sent:
                # Redirect to prevent form resubmission
                return redirect('pages:contact_success')
            else:
                messages.error(
                    request,
                    "Sorry, there was an issue sending your message. Please try again or contact us directly at rroslan@gmail.com."
                )
    else:
        form = ContactForm()

    context = {
        'form': form,
        'page_title': 'Contact Us',
    }
    return render(request, 'pages/contact.html', context)


def contact_success(request):
    """Display contact form success page"""
    return render(request, 'pages/contact_success.html')
