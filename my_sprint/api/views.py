from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PerevalAdded
from .serializers import PerevalAddedSerializer

class SubmitDataView(APIView):

    def get(self, request, id=None):
        if id:
            try:
                pereval = PerevalAdded.objects.get(id=id)
                serializer = PerevalAddedSerializer(pereval)
                return Response(serializer.data)
            except PerevalAdded.DoesNotExist:
                return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            email = request.query_params.get('user__email')
            if email:
                perevals = PerevalAdded.objects.filter(user__email=email)
                serializer = PerevalAddedSerializer(perevals, many=True)
                return Response(serializer.data)
            return Response({'error': 'Email not provided'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer = PerevalAddedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id=None):
        if not id:
            return Response({'error': 'ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            pereval = PerevalAdded.objects.get(id=id)
        except PerevalAdded.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        if pereval.status != 'new':
            return Response({'state': 0, 'message': 'Cannot update record that is not in new status'}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data
        restricted_fields = ['user', 'user__email', 'user__fam', 'user__name', 'user__otc', 'user__phone']
        for field in restricted_fields:
            if field in data:
                data.pop(field)

        serializer = PerevalAddedSerializer(pereval, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'state': 1, 'message': 'Record updated successfully'})
        return Response({'state': 0, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
