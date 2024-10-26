from rest_framework import serializers
from users.models import User
from script.models import Script

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'role', 'password', 'profile_picture']

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
            del validated_data['password']
        return super().update(instance, validated_data)

# Script Serializer
class ScriptSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Include the entire user data

    class Meta:
        model = Script
        fields = ['script_id', 'title', 'synopsis', 'user', 'genre', 'google_doc_link', 'pdf_file']
