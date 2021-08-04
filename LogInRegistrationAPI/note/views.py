from rest_framework.views import APIView
from .serializer import NoteSerializer
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from note.utils import verify_token
from .coordinator import Coordinator

class NotesAPI(APIView):
    
    @verify_token
    def get(self, request):
        """This method will read the data from the table."""
        try:
            data= request.data
            note_data=Coordinator().get_note(data)
            if note_data is not None:
                serializer=NoteSerializer(note_data[0], many=True)
                return Response({"data":{"note-list": serializer.data}}, status=status.HTTP_200_OK)
            return Response({"message":"Put user id to get notes"}, status=status.HTTP_400_BAD_REQUEST)    
        except AssertionError as e:
            return Response({"message":"Put user id to get notes"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message":str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @verify_token
    def post(self, request):
        """
            :param: title, description and user id as parameter.
            :return: It's return response that notes succcessfully created or not.
        """
        try:
            data=request.data
            inserted_data=Coordinator().post_note(data)
            serializer = NoteSerializer(inserted_data[0])
            return Response({'message': 'Notes created successfully'}, status=status.HTTP_200_OK)
        except KeyError:
            return Response({'message': 'Invalid Input'}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError:
            return Response({'message': 'Invalid Input'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({'message': 'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

    @verify_token  
    def put(self,request):
        """This method is used to update the data from the table by using id as a parameter"""
        try:
            data=request.data
            updated_data=Coordinator().put_note(data)
            if updated_data is True:
                return Response({'msg':'Complete Data Updated'}, status=status.HTTP_200_OK)
        except ValueError:
            return Response({"message": 'Invalid Input'}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError:
            return Response({"message": 'Invalid Input'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @verify_token
    def delete(self,request):
        """This method is used to delete the data from the table by using id as a parameter"""
        try:
            data=request.data
            deleted_data=Coordinator().delete_note(data)
            if deleted_data is True:
                return Response({'msg':'Data Deleted'}, status=status.HTTP_200_OK) 
        except ValueError:
            return Response({"message": 'Invalid Input'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
