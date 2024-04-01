#import re 
from django.contrib.auth import get_user_model 

User = get_user_model() 


def activate_account(self):
    if user.code_method == 'phone': 
        phone = self.validated_data.get('phone') 
        user = User.objects.get(phone=phone) 
    elif user.code_method == 'email': 
        email = self.validated_data.get('email') 
        user = User.objects.get(email=email) 
        user.is_active = True 
        user.activation_code = ''
        user.save()