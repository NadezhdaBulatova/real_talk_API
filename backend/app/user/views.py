from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from user.serializers import UserCreateSerializer, UserSerializer
from django.contrib.auth import get_user_model

class RegisterUserView(CreateAPIView):
    # def post(self, request):
    #     data = request.data
    #     serializer = UserCreateSerializer(data=data)

    #     if not serializer.is_valid():
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    #     user = serializer.create(serializer.validated_data)
    #     user = UserSerializer(user)

    #     return Response(user.data, status=status.HTTP_201_CREATED)
    serializer_class = UserCreateSerializer

# class RetrieveCurrentUserView(RetrieveAPIView):
#     # permission_classes = [permissions.IsAuthenticated]
#     queryset = get_user_model().objects.all()
#     serializer_class = UserSerializer
#     lookup_field = 'id'

class RetrieveUserView(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'


