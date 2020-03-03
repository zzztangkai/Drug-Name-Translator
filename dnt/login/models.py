from django.db import models


class User(models.Model):
    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    c_time = models.DateTimeField(auto_now_add=True)
    has_confirmed = models.BooleanField(default=False)   #Hasdcode, default = False account is not verify

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["c_time"]
        verbose_name = "user"
        verbose_name_plural = "user"


class ConfirmString(models.Model):
    code = models.CharField(max_length=256)
    user = models.OneToOneField('User', on_delete=models.CASCADE )
    c_time = models.DateTimeField(auto_now_add=True)  #register time

    def __str__(self):
        return self.user.name + ":   " + self.code

    class Meta:

        ordering = ["-c_time"]
        verbose_name = "Verify Code"
        verbose_name_plural = "Verify Code"


class PasswordString(models.Model):
    code = models.CharField(max_length=256)
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    password = models.CharField(max_length=256)
    c_time = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.user.name + ":   " + self.code

    class Meta:

        ordering = ["-c_time"]
        verbose_name = "Password Code"
        verbose_name_plural = "Password Code"
