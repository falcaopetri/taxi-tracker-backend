from django.shortcuts import render
from django.conf import settings
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import NotAcceptable

from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_202_ACCEPTED


# from oauth2client import client, crypt
import google.oauth2.id_token 
import google.auth.transport.requests

from api.models import *
from api.serializers import *
from api import util

class MotoristaViewSet(viewsets.ModelViewSet):
    queryset = Motorista.objects.all()
    serializer_class = MotoristaSerializer
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (TokenAuthentication,)

    @list_route(methods=['post'])
    def refresh(self, request):
        user = request.user
        driver = Motorista.objects.get(user=user)
        if request.data.get('curr_pos'):
            driver.lastKnownLocation = request.data.get('curr_pos')
            driver.save()

        try:
            corrida = driver.corrida_set.filter(status=Corrida.ESPERA)

            if len(corrida) == 0:
                raise Corrida.DoesNotExist()
            else:
                corrida = corrida[0]

        except Corrida.DoesNotExist:
            return Response({'message': 'nenhuma corrida'})

        serializer = CorridaSerializer(corrida)
        return Response(serializer.data)

class PassageiroViewSet(viewsets.ModelViewSet):
    queryset = Passageiro.objects.all()
    serializer_class = PassageiroSerializer
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (TokenAuthentication,)

    @list_route(methods=['post'])
    def refresh(self, request):
        user = request.user
        passageiro = Passageiro.objects.get(user=user)

        try:
            corrida = passageiro.corrida_set.filter(status=Corrida.ESPERA)

            if len(corrida) == 0:
                raise Corrida.DoesNotExist()
            else:
                corrida = corrida[0]

        except Corrida.DoesNotExist:
            return Response({'message': 'nenhuma corrida'})

        serializer = CorridaSerializer(corrida)
        return Response(serializer.data)

class CorridaViewSet(viewsets.ModelViewSet):
    queryset = Corrida.objects.all()
    serializer_class = CorridaSerializer
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (TokenAuthentication,)

    def create(self,request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            self.perform_create(serializer)
        except DjangoValidationError as e:
            raise e
        except NotAcceptable as e:
            raise e

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)


    def perform_create(self, serializer):
        user = get_object_or_404(Passageiro, user=self.request.user)
        driver = util.get_available_driver()

        if user.has_active_race():
            raise NotAcceptable({"message": "Usuário já está em uma corrida."})

        if driver:
            serializer.save(passageiro=user, motorista=driver)
        else:
            raise NotAcceptable({"message": "Nenhum motorista disponível."})

    def create(self,request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            self.perform_create(serializer)
        except DjangoValidationError as e:
            raise e
        except NotAcceptable as e:
            raise e

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)


    def perform_create(self, serializer):
        user = get_object_or_404(Passageiro, user=self.request.user)
        driver = util.get_available_driver()

        if driver:
            serializer.save(passageiro=user, motorista=driver)
        else:
            raise NotAcceptable({"message": "Nenhum motorista disponível"})


class Login(APIView):
    # Source: http://jyotman94.pythonanywhere.com/entry/token-based-authentication-using-django-rest-framework
    def verifyGoogleToken(self, idToken):
        isIdTokenValid = True
        try:
            idinfo = client.verify_id_token(idToken, settings.CLIENT_ID)
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise crypt.AppIdentityError("Wrong issuer.")
        except crypt.AppIdentityError:
            # Invalid token
            isIdTokenValid = False
            idinfo = {
                'Response' : 'Invalid Google Token!',
            }
        return (isIdTokenValid, idinfo)

    # Source: https://cloud.google.com/appengine/docs/python/authenticating-users-firebase-appengine#verifying_tokens_on_the_server
    def verifyFirebaseToken(self, idToken):
        # Source: https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/appengine/standard/firebase/firenotes/backend/main.py#L28
        HTTP_REQUEST = google.auth.transport.requests.Request()

        claims = google.oauth2.id_token.verify_firebase_token(
                    idToken, HTTP_REQUEST)
        if claims:
            return (True, claims)
        else:
            return (False, { 'Response': 'Invalid Google Token' } )


    def post(self, request, format=None):
        #isIdTokenValid, googleResponse = self.verifyGoogleToken(request.data.get('id_token'))
        isIdTokenValid, googleResponse = self.verifyFirebaseToken(request.data.get('id_token'))
        if isIdTokenValid:
            try:
                user = User.objects.get(email=googleResponse.get('email'))

                token = Token.objects.get(user=user)
                statusCode = HTTP_202_ACCEPTED
            except User.DoesNotExist:
                user = User.objects.create(username=googleResponse.get('name'), email=googleResponse.get('email'))

                if request.data.get('tipo') == 'PASSAGEIRO':
                    passageiro = Passageiro.objects.create(user=user)
                elif request.data.get('tipo') == 'MOTORISTA':
                    motorista = Motorista.objects.create(user=user,)

                token = Token.objects.create(user=user)
                statusCode = HTTP_201_CREATED

            additionalContent = {
                'token' : token.key,
            }

            googleResponse.update(additionalContent)
            return Response(googleResponse, statusCode)
        else:
            return Response(googleResponse, status=HTTP_400_BAD_REQUEST)

