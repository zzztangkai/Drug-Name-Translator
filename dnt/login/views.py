from django.shortcuts import render,redirect
from . import models
from .forms import UserForm,RegisterForm,ForgetPwdForm,UpdateDetailForm,UpdatePwdForm
import hashlib
from django.conf import settings
import datetime
from django.utils import timezone
from argon2 import PasswordHasher
from django.contrib import messages
from django.db import IntegrityError


def login(request):
    if request.session.get('is_login',None):
        return redirect('search_view')

    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "Please check all fields"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(name=username)
                if not user.has_confirmed:   #Check if the email is verified or not.
                    message = "This account currently is disabled, please check your email."
                    return render(request, 'login/login.html', locals())

                ph = PasswordHasher()
                if ph.verify(user.password,password): 
                    #Check if the password is correct, thows exception if it is not
                    #Write user status and data into Session dict
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id  
                    request.session['user_name'] = user.name
                    request.session['user_email'] =user.email
                    request.session['user_password']=user.password
                    request.session['user_phone'] =user.phone
                    return redirect('search_view')
            except:
                message = "Username or password is incorrect"
        return render(request, 'login/login.html', locals())
 
    login_form = UserForm()
    return render(request, 'login/login.html', locals())


def register(request):
    if request.session.get('is_login',None):
        #When user already logged in then does not allow go to sign up page
        return redirect("search_view")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "Please check all fields"
        if register_form.is_valid():  # Get data
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            phone = register_form.cleaned_data['phone']
            
            if password1 != password2:  # Check if two password match
                message = "Passwords do not match, please try again"
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:  # 
                    message = 'Username already exists, please use a different username'
                    return render(request, 'login/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:  
                    message = 'This email address is already signed up, please use a different email address'
                    return render(request, 'login/register.html', locals())
 
                # When everything is ok, then save user information into database
 
                new_user = models.User.objects.create()
                new_user.name = username
                new_user.password = hash_password(password1)
                new_user.email = email  
                new_user.phone = phone
                new_user.save()

                code = make_confirm_string(new_user)
                send_email(email, code)  # send the link to that email address

                messages.success(request, "A verification has been send to your email account. If the email can't be found, please check your junk folder.")
                return redirect('login')  # Jump to Log in page
    register_form = RegisterForm()
    return render(request, 'login/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        # If its not loged in jump to home page
        return redirect("login")
    request.session.flush()
   
    return redirect("login")


def forget(request):
    if request.method == "POST":
        resetpwd_form =ForgetPwdForm(request.POST)
        message = "Please check all fields"
        if resetpwd_form.is_valid():
            email = resetpwd_form.cleaned_data['email']
            password1 = resetpwd_form.cleaned_data['password1']
            password2 = resetpwd_form.cleaned_data['password2']
            if password1 != password2:  # Check if two password match
                message = "Passwords do not match, please try again"
                return render(request, 'login/forget.html', locals())

            email_exist = models.User.objects.filter(email=email)  #select Email Query.  Note: Cannot use GET
            if email_exist:
                user = models.User.objects.get(email=email) # find the corresponding user
                code = make_password_string(user, password1)
                send_reset_email(email, code)  # send the link to that email address

                messages.success(request, "Please check your email to complete the password reset. If the email can't be found, please check your junk folder.")
                return redirect('login')  # Jump to Log in page
            else:
                message = "Email does not exist!"
                return render(request, 'login/forget.html', locals())

    resetpwd_form = ForgetPwdForm()
    return render(request, 'login/forget.html', locals())


def hash_code(s, salt):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  
    return h.hexdigest()


def hash_password(passwd):
    ph = PasswordHasher()
    pw_hash = ph.hash(passwd)
    return pw_hash


def account_deails(request):
    pass
    return render(request,'login/account_detail.html')


def update_details(request):

    username= request.session.get('user_name')
    user =models.User.objects.get(name=username) 

    if request.method == "POST":
        updateInfo_form =UpdateDetailForm(request.POST)
        message = "Please check all fields"
        if updateInfo_form.is_valid():
            newusername = updateInfo_form.cleaned_data['username'] or None
            newemail = updateInfo_form.cleaned_data['email'] or None
            phone = updateInfo_form.cleaned_data['phone'] or None
            
            if newusername is None : #if do not want to update username, ignore
                pass
            else:
                same_name_user = models.User.objects.filter(name=newusername)   # check if the new username if already exist in the database
                if same_name_user:  # 
                    message = 'Username already exists, please use a different username'
                    return render(request, 'login/update_details.html', locals())
                user.name=newusername
            if newemail is None :  
                pass
            else:
                same_email_user = models.User.objects.filter(email=newemail)
                if same_email_user:
                    message = 'This email address is already signed up, please use a different email address'
                    return render(request, 'login/update_details.html', locals())
                user.email=newemail
            if phone is None:
                pass
            else:
                user.phone=phone
        user.save()
        return redirect('/logout/') # after user update the information, user must re-login with new information
    updateInfo_form = UpdateDetailForm()
    return render(request, 'login/update_details.html', locals())


def update_pass(request):
    
    username= request.session.get('user_name')
    user =models.User.objects.get(name=username) 
   # print(user)
    if request.method == "POST":
        updatepass_form =UpdatePwdForm(request.POST)
        message = "Please check all fields"
        if updatepass_form.is_valid():
      #  updatepass_form = UpdatePwdForm()
            password1 = updatepass_form.cleaned_data['password1']
            password2 = updatepass_form.cleaned_data['password2']
            if password1 != password2:  # Check if two password match
                message = "Passwords do not match, please try again"
                return render(request, 'login/update_pass.html', locals())

        user.password=hash_password(password1)
        user.save()
        return redirect('/logout/') # after user update the password, user must re-login with new password
    updatepass_form = UpdatePwdForm()
    return render(request,'login/update_pass.html',locals())


def make_confirm_string(user):
    now = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name, now) #encrypt the user name.
    try:
        models.ConfirmString.objects.create(code=code, user=user,)  #generde the code for the user
    except IntegrityError:
        models.ConfirmString.objects.filter(user=user).delete()
        models.ConfirmString.objects.create(code=code, user=user,)  #generde the code for the user
    return code


def make_password_string(user,password):
    now = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name, now) #encrypt the user name.
    try:
        models.PasswordString.objects.create(code=code, user=user,password=password)  #generde the code for the user
    except IntegrityError:
        models.PasswordString.objects.filter(user=user).delete()
        models.PasswordString.objects.create(code=code, user=user,password=password)  #generde the code for the user
    return code


def send_email(email, code):
    from django.core.mail import EmailMultiAlternatives
    subject, from_email, to = 'Verify your email', 'drugnametranslator@gmail.com', email  #Title
    text_content = 'Welcome to Drug Name Translator.' 
    html_content = '''
                    '<p>Welcome to Drug Name Translator <a href="http://{}/confirm/?code={}" target=blank>dnt.crabdance.com</a>, </p>
                    <p>Please click the link to complete the email verification </p>
                     <p>This link is valid for {} days! </p>'
                    '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def send_reset_email(email, code):
    from django.core.mail import EmailMultiAlternatives
    subject, from_email, to = 'Reset Password', 'curtincapstone@gmail.com', email  #Title
    text_content = 'Reset Password.' 
    html_content = '''
                    <p>Forgot Password?    </p>
                    <p>Are you trying to reset your password? If yes, please click  <a href="http://{}/reset/?code={}" target=blank>dnt.crabdance.com</a> to complete reset password </p>
                    <p>If you did't mean to reset your password, then you can ignore your this email. Your password will not change  </p>
                    <p>This link is valid for {} days! </p>
                    
                    '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def user_confirm(request):
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = models.ConfirmString.objects.get(code=code) 
    except:
        message = 'Invalid request'
        return render(request, 'login/confirm.html', locals())

    c_time = confirm.c_time
    now = timezone.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):  #Link Expired after # days
        confirm.user.delete()
        message = 'Link is expired, please try again'
        return render(request, 'login/confirm.html', locals())
    else:
        confirm.user.has_confirmed = True  # Email comfirmed
        confirm.user.save()  #Save user's information after email verifed
        confirm.delete()  #Delete the link
        message = 'Thanks for verifying, now you can go to log in page'
        return render(request, 'login/confirm.html', locals())


def pwd_reset(request):
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = models.PasswordString.objects.get(code=code) 
    except:
        message = 'Invalid request'
        return render(request, 'login/confirm.html', locals())

    c_time = confirm.c_time
    now = timezone.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):  #Link Expired after # days
        confirm.user.delete()
        message = 'Link is expired, please try again'
        return render(request, 'login/confirm.html', locals())
    else:
        
        pwd=confirm.password
        confirm.user.password=hash_password(pwd)
        confirm.user.save()  #Save user's information after email verifed
        confirm.delete()  #Delete the link
        
        message = 'Thanks for verifying, now you can go to log in page'
        return render(request, 'login/confirm.html', locals())

def contact_us(request):
    pass
    return render(request, 'login/contact_us.html')


def help(request):
    return render(request, 'login/help.html')
