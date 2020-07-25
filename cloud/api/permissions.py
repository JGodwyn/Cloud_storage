from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    object level permissions to only allow owners of an object to edit it.
    Assumes the model instance has an owner attribute
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        #  so we will always allow GET, HEAD or SAFE requests
        if request.method in permissions.SAFE_METHODS:
            return True

        # instance must have an attribute named 'owner'
        return obj.owner == request.user
