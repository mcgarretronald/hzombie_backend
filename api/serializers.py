from rest_framework import serializers
from users.models import User
from script.models import Script
from ratings.models import Rating

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

# Brief User Serializer
class UserBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']

# Script Serializer
class ScriptSerializer(serializers.ModelSerializer):
    user = UserBriefSerializer(read_only=True)  # Include brief user data

    class Meta:
        model = Script
        fields = ['script_id', 'title', 'synopsis', 'user', 'genre', 'total_likes', 'total_dislikes', 'google_doc_link', 'pdf_file']

# Rating Serializer

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'script', 'user', 'rating']  # Include 'user' in fields

    def validate_rating(self, value):
        if value not in [1, -1]:
            raise serializers.ValidationError("Rating must be either 1 (like) or -1 (dislike).")
        return value