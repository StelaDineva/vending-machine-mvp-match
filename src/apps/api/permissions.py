from rest_framework import permissions


class BuyerPermission(permissions.BasePermission):
    """
    Role Permission Class
    """

    def has_permission(self, request, view):
        return request.user.get_role() == "buyer"


class SellerPermission(permissions.BasePermission):
    """
    Role Permission Class
    """

    def has_permission(self, request, view):
        return request.user.get_role() == "seller"
