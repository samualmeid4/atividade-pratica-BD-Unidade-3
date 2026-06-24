from rest_framework.permissions import BasePermission

class IsAtleta(BasePermission):
    message = 'Apenas atletas podem realizar esta ação.'

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_atleta())

class IsTreinador(BasePermission):
    message = 'Apenas treinadores podem realizar esta ação.'
   
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_treinador())

class IsOrganizador(BasePermission):
    message = 'Apenas organizadores podem realizar esta ação.'
    
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_organizador())