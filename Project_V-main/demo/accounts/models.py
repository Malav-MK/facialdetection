from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=300, unique=True)
    password1 = models.CharField(max_length=200)
    password2 = models.CharField(max_length=200,null=True)
    contact = models.IntegerField()
    email_id = models.CharField(max_length=200)
    # password = models.CharField(max_length=200)
    # contact = models.IntegerField(max_length=100)
    # email_id = models.CharField(max_length=200)


    def __str__(self):
        return self.name

class Appointment(models.Model):
    visit_type=models.CharField(max_length=200)
    description=models.CharField(max_length=100)
    date_from= models.DateField()
    date_to= models.DateField()
    confirm_date = models.DateField(null=True)
    user_id=models.ForeignKey(User,related_name='user',on_delete=models.CASCADE)
    is_Active=models.BooleanField(default=False)
    otp_Number=models.IntegerField(null=True)

    def __str__(self):
        return self.visit_type


