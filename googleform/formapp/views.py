from django.shortcuts import redirect, render
from django.contrib.auth.models import User,auth
from django.contrib import messages
from formapp.models import googleformdata
from django.core.mail import send_mail,EmailMessage
from googleform import settings
from django.contrib.auth import authenticate,login,logout
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
# from django.utils.encoding import force_bytes, force_text
from django.utils.encoding import force_bytes, force_str
from . tokens import tokengenrator

def home(request):
    return render(request,'home.html')
def index(request):
    return render(request,'index.html')
def register(request):
    if request.method == 'POST':
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        email=request.POST.get('email')
        password=request.POST.get('password')
        confirm_password=request.POST.get('password2')
       
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('register')
        
        print(fname,lname,email,password)
        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = fname
        user.last_name = lname
      
        user.save()
        print(user.username)
        messages.success(request,'you have successfully register')
        user.is_active=False
        
        #EMAIL TO USER 
        subject = 'you have successfully registered with us '
        message = f"Hi {fname} {lname}!\n\nWelcome aboard! We're delighted to have you join us on this journey. Your presence enriches our community, and we can't wait to embark on exciting adventures together."  
        from_email= settings.EMAIL_HOST_USER   
        to_list=[user.username] 
        send_mail(subject,message,from_email,to_list,fail_silently=True) 
        
        # conformation email
        current_site=get_current_site(request)
        subject2="welcome you to my dunia please conform your account"
        message2=render_to_string("email_conformation.html",
                                  {
                                      'name':user.first_name,
                                      'domain':current_site.domain,
                                      'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                                      'token':tokengenrator.make_token(user)
                                      })
        email=EmailMessage(subject2,message2,settings.EMAIL_HOST_USER,
        [user.email])
        email.fail_silently=True
        email.send()
        
        
        
        return redirect('signin')    
    return render(request, 'register.html')


def activation(request,uidb64,token):
    try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        user=User.objects.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user=None
    if user is not None and tokengenrator.check_token(user,token):
        user.is_active=True
        user.save()
        login(request,user)
        messages.success(request, "Your Account has been activated!!")
        return redirect('signin')
    else:
         return render(request,'home.html')

def signin(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request, user)
            fname = user.first_name
            lname = user.last_name
            context={'fname':fname,'lname':lname}
            messages.success(request,'User successfully registered')
            return render(request,'home.html', context)
        else:
            messages.error(request,'User does not exist')
            return redirect('signin')
       
    return render(request, 'signin.html')

def signout(request):
    logout(request)
    messages.success(request,'logged out successfully')
    return redirect('index')