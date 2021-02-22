from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class AuthUserSerializer(serializers.ModelSerializer): 
    id = serializers.ReadOnlyField()
    username = serializers.ReadOnlyField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    last_login = serializers.DateTimeField()

    class Meta: 
        model = User 
        fields = ('id', 'last_login', 'username', 'first_name', 'last_name', 'email') 
