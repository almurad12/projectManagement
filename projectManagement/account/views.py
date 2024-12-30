from django.shortcuts import render
from account.serializers import UserRegistration
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from account.models import CustomUser
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from account.serializers import CustomUserSerializer

# Create your views here.
@api_view(['post'])
def Register(request):
    if request.method == 'POST':
        # data = request.data
        print(request.data)
        serializer = UserRegistration(data=request.data)
        if serializer.is_valid():
            print(serializer)
            user = serializer.save()
            return Response({
                "message": "Register Account Created Successfully"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        If the user is an admin, allow any authenticated user to access, otherwise
        only allow the user to update their own details.
        """
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            # Allow users to access only their data or admin users
            if self.request.user.is_staff:
                return [IsAuthenticated(), IsAdminUser()]
            else:
                return [IsAuthenticated()]
        return super().get_permissions()

    def update(self, request, *args, **kwargs):
        """Override update to allow user to update only their own data."""
        # if str(request.user.id) != kwargs['pk']:
        #     return Response({"detail": "You can only update your own data."}, status=status.HTTP_403_FORBIDDEN)

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Override destroy to allow user to delete only their own data."""
        # if str(request.user.id) != kwargs['pk']:
        #     return Response({"detail": "You can only delete your own data."}, status=status.HTTP_403_FORBIDDEN)

        return super().destroy(request, *args, **kwargs)
    


