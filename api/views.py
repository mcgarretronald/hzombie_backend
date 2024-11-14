from rest_framework import generics, viewsets, permissions, status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.response import Response
from ratings.models import Rating
from .serializers import UserSerializer, ScriptSerializer, RatingSerializer
from users.models import User
from script.models import Script

# User Login View
class UserLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # Check if email and password are provided
        if not email or not password:
            return Response({'error': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user exists based on the provided email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'The email address does not exist'}, status=status.HTTP_404_NOT_FOUND)

        # Authenticate the user with the email and password
        user = authenticate(request, email=email, password=password)

        if user is not None:
            # If authentication is successful, return the user's details
            return Response({
                'message': 'Login successful',
                'email': user.email,
                'profile_picture': request.build_absolute_uri(user.profile_picture.url) if user.profile_picture else None
            }, status=status.HTTP_200_OK)

        # If email exists but password is incorrect
        return Response({'error': 'Incorrect password'}, status=status.HTTP_401_UNAUTHORIZED)


# User Registration View
class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# User Listing View
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# User Update View
class UserUpdateView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Script ViewSet for CRUD operations
class ScriptViewSet(viewsets.ModelViewSet):
    queryset = Script.objects.all()
    serializer_class = ScriptSerializer

    def perform_create(self, serializer):
        # Simply save the script without requiring a user
        serializer.save()


# Rating ViewSet
class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user')
        script_id = request.data.get('script')
        rating_value = request.data.get('rating')

        # Validate rating value
        if rating_value not in [1, -1]:
            return Response({"error": "Rating must be 1 (like) or -1 (dislike)."}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure user and script IDs are provided
        if not user_id or not script_id:
            return Response({"error": "User and script are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
            script = Script.objects.get(id=script_id)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Script.DoesNotExist:
            return Response({"error": "Script not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user already has a rating on this script
        rating, created = Rating.objects.get_or_create(user=user, script=script)

        # Adjust likes/dislikes based on rating action
        if created:
            # If new rating, just update counts
            if rating_value == 1:
                script.total_likes += 1
            else:
                script.total_dislikes += 1
            rating.rating = rating_value
            rating.save()
        else:
            # If already rated, toggle the rating
            if rating.rating == rating_value:
                # Remove the rating
                if rating_value == 1:
                    script.total_likes -= 1
                else:
                    script.total_dislikes -= 1
                rating.delete()
            else:
                # Update rating and counts
                if rating_value == 1:
                    script.total_likes += 1
                    script.total_dislikes -= 1
                else:
                    script.total_dislikes += 1
                    script.total_likes -= 1
                rating.rating = rating_value
                rating.save()

        # Save the script with updated counts
        script.save(update_fields=['total_likes', 'total_dislikes'])

        # Return the updated rating data
        serializer = RatingSerializer(rating)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
