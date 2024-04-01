from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.conf import settings

from .tasks import send_activation_code #, send_activation_sms, 
# from .utils import normalize_phone


User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):

    password_confirm = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'password', 'password_confirm', 'code_method')

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                'The username is taken. choose another one.'
                )
        if not username.replace('_', '').replace('.', '').isalnum(): 
            raise serializers.ValidationError('Username can only contain letters, numbers, an \'_\' and \'.\'')
        if '_.' in username or '._' in username:
            raise serializers.ValidationError('\'_\' and \'.\' cannot stand next to each other')
        if not username[0].isalpha():
            raise serializers.ValidationError('Username must start with a letter')
        return username

    def validate_phone(self, phone):
        if len(phone) != 13:
            raise serializers.ValidationError('Incorrect phone format.')
        return phone

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Passwords do not match.')
        return attrs

    def create(self, validated_data): 
        user = User.objects.create_user(**validated_data)
        user.create_activation_code()
        if validated_data['code_method'] == 'email':
            send_activation_code(user.email, user.activation_code)
            # send_activation_code.delay(user.email, user.activation_code)
        # if validated_data['code_method'] == 'phone':
        #     send_activation_sms(user.phone, user.activation_code) 
            # send_activation_sms.delay(user.phone, user.activation_code) 
        return user