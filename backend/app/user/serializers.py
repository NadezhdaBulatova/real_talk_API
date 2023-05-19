from django.contrib.auth import get_user_model
from rest_framework.serializers import (ModelSerializer, as_serializer_error)
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class UserCreateSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'username']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}
    
    # def validate(self, kwargs):
    #     user = get_user_model(**kwargs)
    #     password = kwargs.get('password')
    # try:
    #     validate_password('password')
    # except ValidationError as e:
    #     """To return all errors as list"""
    #     serializer_errors = as_serializer_error(e)
    #     raise ValidationError({
    #         'password': serializer_errors['non_field_errors']
    #     })
    
    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)
    
class UserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['email', 'username']