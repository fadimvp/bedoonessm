from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import RegistertionForm
from .models import Account
# Create your views here.
from django.contrib import messages, auth
from django.contrib.auth import authenticate


def register(request):
    if request.method == 'POST':
        form1 = RegistertionForm(request.POST)

        if form1.is_valid():
            print(form1, "create")

            first_name = form1.cleaned_data['first_name']
            last_name = form1.cleaned_data['last_name']
            email = form1.cleaned_data['email']
            password = form1.cleaned_data['password']
            username = email.split('@')[0]
            phone_number = form1.cleaned_data['phone_number']

            user = Account.objects.create_user(first_name=first_name, last_name=last_name, username=username,
                                               email=email, password=password)
            user.phone_number = phone_number
            user.save()

            # user  activation
            current_site = get_current_site(request)
            mail_subject = "please  activate your mail "
            message = render_to_string('activate.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            messages.success(request, " thanks you for register with us . please check you email")
            return redirect('/account/login/?command=verification&email=' + email)
    else:

        form1 = RegistertionForm(request.POST)
    context = {

        'form1': form1,

    }

    return render(request, 'register.html', context)


def Login(request):
    if request.method == 'POST':
        print("name after ")

        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            print("name found")
            return redirect('/')
        else:
            messages.error(request, 'incorrect password try again ')
            return redirect('account:login')

    context = {

    }
    return render(request, 'register.html', context)


@login_required(login_url='login')
def Logout(request):
    auth.logout(request)
    messages.success(request, 'success logout ')
    return redirect('account:login')

    context = {

    }
    return render(request, 'register.html')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'your account is activated ')
        return redirect('account:register')
    else:

        messages.error(request, 'invalid activation link')
        return redirect('account:register')


def forgotpass(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            # register password email
            current_site = get_current_site(request)
            mail_subject = "rest your Password  "
            message = render_to_string('rest_password_valid.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            messages.success(request, 'Password rest email  has been sent to your email ')

            return redirect('account:login')

        else:
            messages.error(request, "Account does not exist ")
            return redirect('account:forgotpass')

    context = {

    }

    return render(request, 'lost-password.html', context)


def forgot_password_validate(request, uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):

        request.session['uid'] =uid
        messages.success(request,'please rest your password ')
        return redirect('account:resetpassword')
    else:
        messages.error(request,'this link  been expired ')
        return redirect('account:login')



    return HttpResponse("ok")


def resetpassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            uid = request.session.get('uid')
            user =Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'password request successful')
            return redirect('account:login')
        else:
            messages.success(request, 'password do not match ')
            return redirect('account:resetpassword')
    else:

         return render(request,'change-password.html',)