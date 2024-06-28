from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from db_handler import DatabaseHandler  # Ensure db_handler.py is in the same directory as manage.py

class SubmitData(APIView):
    def post(self, request):
        data = request.data
        db = DatabaseHandler()
        try:
            db.add_pass(data)
            return Response({"message": "Data submitted successfully."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)