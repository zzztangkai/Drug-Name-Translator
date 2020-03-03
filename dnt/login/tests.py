from django.test import TestCase
from django.test import Client
from django.urls import reverse
from .forms import *
from . import views
from .models import User

class LoginURL(TestCase):
     def test_login_url(self):
        response = self.client.get(reverse('login'))
        self.assertEquals(response.status_code, 200)
    
     def test_register_url(self):
        response = self.client.get(reverse('register'))
        self.assertEquals(response.status_code, 200)   

class Setup_Class(TestCase):
   def setUp(self):
        self.user = User.objects.create_user(username="dnt",password="dnt")

class User_Form_Test(TestCase):
   def test_UserForm_valid(self):
      form = UserForm(data={'username': "dnt", 'password': "dnt"})
      self.assertTrue(form.is_valid())

   def test_UserForm_invalid(self):
      form = UserForm(data={'username': "", 'password': "dnt"})
      self.assertFalse(form.is_valid())

  

class User_Views_Test(TestCase):
   def test_home_view(self):   
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login/login.html')

   def test_login_use_empty_username_password(self):
    login_account_test_data = {'username':'', 'password':''}
    response = self.client.post(path='/login/login.html', data=login_account_test_data)
    self.assertEqual(response.status_code, 200)
  
    def test_login_success(self):
        login_account_test_data = {'username': 'dnt', 'password': 'dnt'}
        response = self.client.post(path='/login/login.html', data=login_account_test_data)
        