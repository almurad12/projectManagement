from account.models import CustomUser
from rest_framework import serializers
from rest_framework.response import Response
class UserRegistration(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password2 = serializers.CharField(write_only=True)
    class Meta:
       model = CustomUser
       fields = ['username','first_name','last_name','email','password','password2']
    def validate(self,attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords must match"})
        return attrs
    def create(self, validated_data):
          user = CustomUser.objects.create_user(
            username =validated_data['username'],
            first_name =validated_data['first_name'],
            last_name = validated_data['last_name'],
            email= validated_data['email'],
            password= validated_data['password'],
            is_staff = True,
            is_active = True
          )
          return user
    

###Custom user edit update delete serializers

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'date_joined']