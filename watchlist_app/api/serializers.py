from rest_framework import serializers
from watchlist_app.models import StreamPlatform, WatchList, Review

class ReviewSerializer(serializers.ModelSerializer):
    review_user=serializers.StringRelatedField()
    class Meta:
        model=Review
        
        exclude=["watchlist",]


class WatchListSerializers(serializers.ModelSerializer):
    # reviews=ReviewSerializer(many=True,read_only=True)
    platform=serializers.CharField(source='platform.name')
    class Meta:
        model=WatchList
        fields='__all__'

class StreamPlatformSerializers(serializers.ModelSerializer):
    watch_list=WatchListSerializers(many=True,read_only=True)
   
    class Meta:
        model=StreamPlatform
        fields='__all__'
        

        
        


# class MovieSerializers(serializers.Serializer):
    
#     id=serializers.IntegerField(read_only=True)
#     name=serializers.CharField()
#     description=serializers.CharField()
#     active=serializers.BooleanField()
#     summary=serializers.SerializerMethodField()
    
#     def get_summary(self,obj):
#         return f"{obj.name} john"
    
   
    
#     def validate_name(self,value):
#         if len(value)<2:
#             raise serializers.ValidationError("name should me more than two characters")
#         return value
#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         instance.name=validated_data.get("name", instance.name)
#         instance.description=validated_data.get("description", instance.description)
#         instance.active=validated_data.get("active", instance.active)
#         instance.save()    
        
#         return instance