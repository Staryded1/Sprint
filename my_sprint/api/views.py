from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from db_handler import DatabaseHandler

# Создание объекта db_handler
db_handler = DatabaseHandler()

class SubmitDataView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        print("Received data:", data)  # Отладочный принт
        result = db_handler.add_pass(data)
        if result:
            return Response({"message": "Pass successfully created"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Failed to create pass"}, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, pk=None):
        if pk:
            db_handler = DatabaseHandler()
            result = db_handler.get_pass(pk)
            if result:
                return Response(result, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            user_email = request.GET.get('user__email', None)
            if user_email:
                db_handler = DatabaseHandler()
                result = db_handler.get_passes_by_email(user_email)
                return Response(result, status=status.HTTP_200_OK)
            return Response({"message": "Email not provided"}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        data = request.data
        db_handler = DatabaseHandler()
        result = db_handler.update_pass(pk, data)
        if result['success']:
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)