from django.contrib.auth import authenticate
from .seriallizers import UserSerialize
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError,AuthenticationFailed
from django.core.mail import EmailMultiAlternatives
from UserRegistration.utils import encode_token,decode_token,encode_token_userid
from .coordinator import Coordinator

class Index(APIView):
    """
    [This method will return welcome message]
    """
    def get(self,request):
        return Response('Welcome to Login and Registration App')

class RegisterAPI(APIView):

    def get(self,request,pk=None):
        """This method will read the data from the table."""
        try:
            id = pk
            if id is not None:
                user=Coordinator().get_data_by_id(id)
                serializer = UserSerialize(user[0])
                return Response({'Data':serializer.data})
            return Response({'message': 'Enter your id to get registered data'})
        except Exception as e:
            return Response({'message':str(e)})

    def post(self,request):
        """[This method will take the required input and register it]

        Returns:
            [returns the message if successfully registered]
        """
        try:
            data=request.data
            get_data=Coordinator().post_data(data)
            print(get_data)
            if get_data[0]==1:
                return Response({'message': 'Username is already registered with another user.'}, status=status.HTTP_400_BAD_REQUEST)
            get_inserted_data=Coordinator().post_insert_data(data)
            print(get_inserted_data[1]['id'])
            token = encode_token(get_inserted_data[1]['id'],get_data[1])
            subject, from_email, to='Register yourself by complete this verification','santospanda111@gmail.com',get_inserted_data[0]
            html_content= f'<a href="http://127.0.0.1:8000/verify/{token}">Click here</a>'
            text_content='Verify yourself'
            msg=EmailMultiAlternatives(subject,text_content,from_email,[to])
            msg.attach_alternative(html_content,"text/html")
            msg.send()
            return Response({"message":"CHECK EMAIL for verification"})
        except ValueError:
            return Response({"message": 'Invalid Input'}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError:
            return Response({'message': 'Invalid Input'}, status=status.HTTP_400_BAD_REQUEST)  
        except Exception as e:
            return Response({"message1": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class LogInAPI(APIView):

    def get(self,request):
        """This method will give the string response as given below."""
        return Response("This is LogInAPI")
        
    def post(self,request):
        """[This method will take the required input and do login]

        Returns:
            [returns the message if successfully loggedin]
        """
        try:
            data=request.data
            username=data.get('username')
            password=data.get('password')
            user = authenticate(username=username, password=password)
            user_id=Coordinator().post_login_data(username)
            print(user_id)
            token=encode_token_userid(user_id[0])
            if user is not None:
                return Response({"msg": "Loggedin Successfully", 'data' : {'username': data.get('username'), 'token': token}}, status=status.HTTP_200_OK)
            return Response({"msg": 'Wrong username or password'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({"message": 'Invalid Input'}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError:
            return Response({'message': "wrong credentials"}, status=status.HTTP_400_BAD_REQUEST) 
        except AuthenticationFailed:
            return Response({'message': 'Authentication Failed'}, status=status.HTTP_400_BAD_REQUEST) 
        except Exception:
            return Response({"msg1": "wrong credentials"}, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmail(APIView):

    def get(self,request,token=None):
        '''This method will get token from server then decode and verify the email'''
        try:
            user= decode_token(token)
            user_id=user.get("user_id")
            username=user.get("username")
            data=Coordinator().get_verify_email(user_id,username)
            if data is not None:
                return Response({"message":"Email Verified and Registered successfully"},status=status.HTTP_200_OK)
            return Response({"message":"Try Again......Wrong credentials"})
        except Exception as e:
            return Response({"message":str(e)})
