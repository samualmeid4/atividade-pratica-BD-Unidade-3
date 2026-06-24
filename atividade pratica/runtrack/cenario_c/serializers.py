from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from usuarios.models import Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = [
            'id',
            'username',
            'email',
            'password',
            'tipo',
            'cidade',
            'data_nasc'
        ]

    def create(self, validated_data):
        senha = validated_data.pop('password')

        usuario = Usuario(**validated_data)
        usuario.set_password(senha)
        usuario.save()

        return usuario


class LoginSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['tipo'] = user.tipo
        token['username'] = user.username

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        data['tipo'] = self.user.tipo

        return data