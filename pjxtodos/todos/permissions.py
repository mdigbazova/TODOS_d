from rest_framework import permissions

"""
Create custom permissions at object level
"""

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so it is always allowed GET, HEAD or OPTIONS requests.
        #import pdb; pdb.set_trace ()
        if request.method in permissions.SAFE_METHODS or request.user.is_superuser:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user