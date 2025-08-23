from rest_framework import permissions


class IsVerified(permissions.BasePermission):
    """
    Permission to check if user is verified.
    """
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Check if user has verification and it's verified
        try:
            verification = request.user.verification
            return verification.status == 'verified'
        except:
            return False


class IsMinorWithConsent(permissions.BasePermission):
    """
    Permission to check if minor user has guardian consent.
    """
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # If user is not a minor, allow access
        if not request.user.is_minor:
            return True
        
        # If user is a minor, check for guardian consent
        try:
            verification = request.user.verification
            return verification.guardian_consented
        except:
            return False


class IsJobOwner(permissions.BasePermission):
    """
    Permission to check if user is the owner of the job.
    """
    
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsJobWorker(permissions.BasePermission):
    """
    Permission to check if user is the assigned worker for the job.
    """
    
    def has_object_permission(self, request, view, obj):
        return obj.assigned_to == request.user


class IsJobOwnerOrWorker(permissions.BasePermission):
    """
    Permission to check if user is either the owner or assigned worker of the job.
    """
    
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user or obj.assigned_to == request.user
