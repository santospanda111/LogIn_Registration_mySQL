from rest_framework import serializers

#This serializer will serialize the complex data.
class UserSerialize(serializers.Serializer):
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)



  
