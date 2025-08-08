# from rest_framework import generics, permissions
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from .models import UserProfiles
# from .serializers import UserSerializer, UserProfileSerializer

# class RegisterView(generics.CreateAPIView):
#     serializer_class = UserSerializer
#     permission_classes = [permissions.AllowAny]

# class ProfileView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         serializer = UserProfileSerializer(request.user.profile)
#         return Response(serializer.data)

#     def put(self, request):
#         serializer = UserProfileSerializer(request.user.profile, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)


# with the cache redis for profile faster ..


from django.core.cache import cache
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import UserProfiles
from .serializers import UserSerializer, UserProfileSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        cache_key = f"user-profile:{user.id}"

        # Try to fetch profile data from Redis
        data = cache.get(cache_key)

        if not data:
            # Cache miss → fetch from DB and set in cache
            serializer = UserProfileSerializer(user.profile)
            data = serializer.data
            cache.set(cache_key, data, timeout=600)  # cache for 10 minutes

        return Response(data)

    def put(self, request):
        user = request.user
        serializer = UserProfileSerializer(user.profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Invalidate Redis cache
        cache_key = f"user-profile:{user.id}"
        cache.delete(cache_key)

        return Response(serializer.data)
