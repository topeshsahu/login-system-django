from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect

from atg import settings
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .tokens import generate_token


def home(request):

	return render(request,"atgapp/home.html")

def signin(request):
	if request.method == 'POST':
		uname = request.POST['username']
		password = request.POST['password1']

		user = authenticate(request, username=uname, password=password)

		if user is not None:
			login(request, user)
			fname = user.first_name
			return render(request,'atgapp/home.html',{'fname' : fname })

		else:
			messages.error(request,'Invalid username/password! Please Register Yourself')
			return redirect('Home')

	return render(request,"atgapp/signin.html")

def signup(request):
	if request.method == "POST":
		uname = request.POST['username']
		email = request.POST['useremail']
		fname = request.POST['fname']
		lname = request.POST['lname']
		password1 = request.POST['password1']
		password2 = request.POST['password2']

		if(User.objects.filter(username = uname)):
			messages.error(request,'user already exists! please use another')
			return redirect('Home')

		if (User.objects.filter(email=email)):
			messages.error(request, 'email already exists! please use another')
			return redirect('Home')

		if (password1 != password2):
			messages.error(request, 'Password does not match! please check password')
			return redirect('Home')

		if (len(uname) > 10):
			messages.error(request, 'username must be 10 characters long')
			return redirect('Home')

		if (not uname.isalnum()):
			messages.error(request, 'Username should be alpha-numeric')
			return redirect('Home')

		myuser = User.objects.create_user(username=uname,email=email,password=password1)
		myuser.first_name = fname
		myuser.last_name = lname
		myuser.is_active = False
		myuser.save()
		messages.success(request,"You have been registered successfully! We have send you a email in order to avtivate your account please verify your email")

		#welcome email
		subject1 = 'welcome to ATG - Django login'
		message1 = "hello " + myuser.first_name + "\nThank you for registering into our organization\nWe have also sent you a confirmation email.\n\n Thank you \n Regards ATG Team"
		from_email1 = settings.EMAIL_HOST_USER
		to_email1 = [myuser.email]
		send_mail(subject1,message1,from_email1,to_email1,fail_silently=True)

		# sending confirmation email
		current_site = get_current_site(request)
		subject2 = "Confirmation email! at ATG"
		message2 = render_to_string('email_confirmation.html',
									{
										'name' : myuser.first_name,
										'domain' : current_site.domain,
										'uid' : urlsafe_base64_encode(force_bytes(myuser.pk)),
										'token' : generate_token.make_token(myuser),
									})
		emailobj = EmailMessage(subject2,message2,settings.EMAIL_HOST_USER,[myuser.email])
		emailobj.send(fail_silently = True)

		return render(request,'atgapp/signin.html')

	return render(request,"atgapp/signup.html")

def signout(request):
	logout(request)
	messages.success(request,'you logged out successfully')
	return redirect('Home')

def activate(request,uidb64,token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		myuser = User.objects.get(pk=uid)

	except (TypeError,ValueError,OverflowError):
		myuser = None

	if myuser is not None and generate_token.check_token(myuser,token):
		myuser.is_active = True
		myuser.save()
		login(request,myuser)
		return redirect('Home')

	else:
		return render(request,'activation_failed.html')

