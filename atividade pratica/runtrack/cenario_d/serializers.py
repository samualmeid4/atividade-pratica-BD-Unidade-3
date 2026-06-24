from django.db import transaction
from usuarios.models import Usuario
from .models import Atleta, Treinador, Organizador
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers


class AtletaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atleta
        fields = ['cpf','categoria','melhor_tempo']
        
class TreinadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Treinador
        fields = ['cref','especialidade','qtd_atletas_max']
        
class OrganizadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizador
        fields = ['cnpj','nome_organizacao','uf']
class RegistroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    perfil_atleta = AtletaSerializer(required=False)
    perfil_treinador = TreinadorSerializer(required=False)
    perfil_organizador= OrganizadorSerializer(required=False)
    
    class Meta:
        model = Usuario
        fields = ['id','username','email','password','tipo','cidade', 'perfil_atleta','perfil_treinador','perfil_organizador']
    
    def validate(self, data):
        tipo = data.get('tipo')
        if tipo == Usuario.Tipo.ATLETA and 'perfil_atleta' not in data:
            raise serializers.ValidationError('Atleta precisa enviar perfil_atleta.')
        if tipo == Usuario.Tipo.TREINADOR and 'perfil_treinador' not in data:
            raise serializers.ValidationError('Treinador precisa enviar perfil_treinador.')
        if tipo == Usuario.Tipo.ORGANIZADOR and 'perfil_organizador' not in data:
            raise serializers.ValidationError('Organizador precisa enviar perfil_organizador.')
        return data
    
    @transaction.atomic
    def create(self, validated_data):
        d_atleta = validated_data.pop('perfil_atleta', None)
        d_treino = validated_data.pop('perfil_treinador', None)
        d_org = validated_data.pop('perfil_organizador', None)
        senha = validated_data.pop('password')
        usuario = Usuario(**validated_data)
        usuario.set_password(senha)
        usuario.save()
        
        if d_atleta: Atleta.objects.create(usuario=usuario, **d_atleta)
        if d_treino: Treinador.objects.create(usuario=usuario, **d_treino)
        if d_org: Organizador.objects.create(usuario=usuario, **d_org)
        
        return usuario
        
class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['tipo'] = user.tipo
        return token
   
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        data['tipo'] = user.tipo
    # Dado específico do perfil na resposta do login
        if user.is_atleta() and hasattr(user, 'perfil_atleta'):
            data['categoria'] = user.perfil_atleta.categoria
        elif user.is_treinador() and hasattr(user, 'perfil_treinador'):
            data['cref'] = user.perfil_treinador.cref
        
        elif user.is_organizador() and hasattr(user, 'perfil_organizador'):
            data['organizacao'] = user.perfil_organizador.nome_organizacao
        return data