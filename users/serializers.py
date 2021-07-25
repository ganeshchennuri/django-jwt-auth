from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer Class for User Model"""
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password']
        
        extra_kwargs = {
            'password' : {'write_only': True} #Setting Password as only wtitable field
        }
        
    def create(self, validated_data):
        """ Overiding Create User Method to hash password """
        password = validated_data.pop('password', None)
        user = self.Meta.model(**validated_data)
        if password is not None:
            user.set_password(password)
        user.save()
        
        return user