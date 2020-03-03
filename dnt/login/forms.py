from django import forms


class UserForm(forms.Form):
    username = forms.CharField(label="Username", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username'}))
    password = forms.CharField(label="Password", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Enter Password','id':"id_password1"}))


class RegisterForm(forms.Form):
    gender = (
        ('male', "Male"),
        ('female', "Female"),
    )
    username = forms.CharField(label="Username", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username'}))
    password1 = forms.CharField(label="Password", min_length=8, max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Enter Password','id':"id_password1"}))
    password2 = forms.CharField(label="Confirm Password",min_length=8, max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Confirm Password','id':"id_password2"}))
    email = forms.EmailField(label="Email Address", widget=forms.EmailInput(attrs={'class': 'form-control','placeholder': 'Enter Email Address'}))
    phone = forms.CharField(label="Phone Number", widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter Phone Number'}))


class ForgetPwdForm(forms.Form):
    email = forms.EmailField(label="Email Address",widget=forms.EmailInput(attrs={'class': 'form-control','placeholder': 'Enter Email Address'}))
    password1 = forms.CharField(label="Password",min_length=8, max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Enter Password','id':"id_password1"}))
    password2 = forms.CharField(label="Confirm Password",min_length=8, max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Confirm Password','id':"id_password2"}))


class UpdateDetailForm(forms.Form):
    username = forms.CharField(label="Username",required=False, max_length=128, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'New Username'}))
    email = forms.EmailField(label="Email Address",required=False, widget=forms.EmailInput(attrs={'class': 'form-control','placeholder': 'New Email Address'}))
    phone = forms.CharField(label="Phone Number", required=False,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'New Phone Number'}))


class UpdatePwdForm(forms.Form):
    password1 = forms.CharField(label="Password", min_length=8,max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Enter New Password','id':"id_password1"}))
    password2 = forms.CharField(label="Confirm Password", min_length=8,max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Confirm Password','id':"id_password2"}))
