from rest_framework import serializers
from django.contrib.auth.models import User

class ResgistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["username","password","email",]
        extra_kwargs={
            'password': {'write_only':True}
        }
        
    def save(self):
        user = User.objects.create(
        username=self.validated_data['username'],
        email=self.validated_data.get('email')
        )
        user.set_password(self.validated_data['password'])
        user.save()
            
        return user
        
        
            
