from rest_framework.decorators import api_view, permission_classes
from .serializer import ResgistrationSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
def registration_view(request):
    if request.method=='POST':
        serializer=ResgistrationSerializer(data=request.data)
        data={}
        if serializer.is_valid():
            account=serializer.save()
            data["response"]="success"
            data["user"]=account.username
            data["email"]=account.email
            token, created=Token.objects.get_or_create(user=account)
            data['token']=token.key
            return Response(data)
        else:
            data['errors']=serializer.errors
            return Response(data)

@api_view(['POST',])
def logout_view(request):
    if request.method=='POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_202_ACCEPTED)