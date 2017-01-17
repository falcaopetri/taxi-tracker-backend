from django.shortcuts import render
from django.conf import settings
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import NotAcceptable

from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_202_ACCEPTED


from oauth2client import client, crypt

from api.models import *
from api.serializers import *
from api import util

class MotoristaViewSet(viewsets.ModelViewSet):
    queryset = Motorista.objects.all()
    serializer_class = MotoristaSerializer
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (TokenAuthentication,)


class PassageiroViewSet(viewsets.ModelViewSet):
    queryset = Passageiro.objects.all()
    serializer_class = PassageiroSerializer
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (TokenAuthentication,)


class CorridaViewSet(viewsets.ModelViewSet):
    queryset = Corrida.objects.all()
    serializer_class = CorridaSerializer
    permission_classes = (permissions.IsAuthenticated, )
    #authentication_classes = (TokenAuthentication,)

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

	def post(self, request, format=None):
		isIdTokenValid, googleResponse = self.verifyGoogleToken(request.data.get('id_token'))
		if isIdTokenValid:
			try:
				user = User.objects.get(email=googleResponse.get('email'))
				token = Token.objects.get(user=user)
				statusCode = HTTP_202_ACCEPTED
			except User.DoesNotExist:
				user = User.objects.create(username=googleResponse.get('name'), email=googleResponse.get('email'))
				passageiro = Passageiro.objects.create(user=user)
				token = Token.objects.create(user=user)
				statusCode = HTTP_201_CREATED
			#except Token.DoesNotExist:
			#	token = Token.objects.create(user=user)
			#	statusCode = HTTP_201_CREATED

			additionalContent = {
				'token' : token.key,
				}
			googleResponse.update(additionalContent)
			return Response(googleResponse, statusCode)
		else:
			return Response(googleResponse, status=HTTP_400_BAD_REQUEST)

