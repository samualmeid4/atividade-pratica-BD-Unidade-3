from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import UsuarioSerializer, LoginSerializer
from .permissions import IsAtleta, IsOrganizador


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = UsuarioSerializer(data=request.data)

    if serializer.is_valid():
        usuario = serializer.save()

        return Response({
            "mensagem": "Usuário cadastrado com sucesso!",
            "usuario": UsuarioSerializer(usuario).data
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def perfil(request):
    usuario = request.user

    return Response({
        "id": usuario.id,
        "username": usuario.username,
        "email": usuario.email,
        "tipo": usuario.tipo,
        "cidade": usuario.cidade
    })


@api_view(['POST'])
@permission_classes([IsAtleta])
def treino(request):
    return Response({
        "mensagem": "Treino registrado com sucesso!",
        "dados": request.data
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsOrganizador])
def evento(request):
    return Response({
        "mensagem": "Evento criado com sucesso!",
        "dados": request.data
    }, status=status.HTTP_200_OK)
