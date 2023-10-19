from rest_framework import serializers

# import model from models.py
from .models import User


# Create a model serializer
class UserSerializer(serializers.ModelSerializer):
    # specify model and fields
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'phone_number', 'password', 'created_at',
                  'date_joined', 'is_superuser', 'last_login')

        # specify read only fields
        # https://www.geeksforgeeks.org/modelserializer-in-serializers-django-rest-framework/
        # read_only_fields = ['is_superuser']
