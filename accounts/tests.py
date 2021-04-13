from django.test import TestCase
from .models import User,Appointment

# Create your tests here.
class Basictest(TestCase):
    def setUp(self):
        self.blog=User.objects.create(name='abcd',password1='1234',password2='1234',contact='1234567891',email_id='abc@gmail.com')
        # self.blog1 = Appointment.objects.create(visit_type='interview',description="python interview",date_from='2020-04-02',date_to='2020-04-14'
        #                                         ,confirm_date='2020-04-07',is_Active=True,otp_Number=4444)

    def test_model(self):
        test=self.blog

        self.assertTrue(isinstance(test,User))
        self.assertEqual(str(test),'abcd')

    # def Appoint_model(self):
    #     test1 = self.blog1
    #
    #     self.assertTrue(isinstance(test1, Appointment))
    #     self.assertEqual(str(test1), 'interview')

