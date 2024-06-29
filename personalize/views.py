from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from api.utils import try_except_wrapper
from personalize.models import Personalize
from personalize.serializer import PersonalizeSerializer

class PersonalizeApi(ViewSet):
    
    @try_except_wrapper
    def list(self, request):
        """List all Personalize entries."""
        personalizes = Personalize.objects.all()
        serializer = PersonalizeSerializer(personalizes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @try_except_wrapper
    def create(self, request):
        """Create a new Personalize entry."""
        serializer = PersonalizeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @try_except_wrapper
    def retrieve(self, request, pk=None):
        """Retrieve a specific Personalize entry."""
        try:
            personalize = Personalize.objects.get(pk=pk)
        except Personalize.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PersonalizeSerializer(personalize)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @try_except_wrapper
    def update(self, request, pk=None):
        """Update a specific Personalize entry."""
        try:
            personalize = Personalize.objects.get(pk=pk)
        except Personalize.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PersonalizeSerializer(personalize, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @try_except_wrapper
    def partial_update(self, request, pk=None):
        """Partially update a specific Personalize entry."""
        try:
            personalize = Personalize.objects.get(pk=pk)
        except Personalize.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PersonalizeSerializer(personalize, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @try_except_wrapper
    def destroy(self, request, pk=None):
        """Delete a specific Personalize entry."""
        try:
            personalize = Personalize.objects.get(pk=pk)
        except Personalize.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        personalize.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
