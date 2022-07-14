from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from api.permissions import BuyerPermission
from api.serializers.profiles import ProfileSerializer, DepositSerializer
from profiles.models import User


class ProfileViewSet(viewsets.ModelViewSet):
    """
    CRUD endpoint for User
    """
    queryset = User.objects.none()
    serializer_class = ProfileSerializer

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = []
        if self.action in ["deposit", "reset"]:
            self.permission_classes = [IsAuthenticated, BuyerPermission]
        return super().get_permissions()

    @action(methods=['post'], detail=False)
    def deposit(self, request: Request) -> Response:
        serializer = DepositSerializer(data=request.data)
        if serializer.is_valid():
            request.user.deposit += serializer.validated_data['amount']
            request.user.save()
        else:
            return Response(serializer.errors, status=400)
        return Response({'deposit': request.user.deposit})

    @action(methods=['get'], detail=False)
    def reset(self, request: Request) -> Response:
        request.user.deposit = 0
        request.user.save()
        return Response({"success": True})
