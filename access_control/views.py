from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import AccessLog
from .serializers import AccessLogSerializer

class AccessLogViewSet(viewsets.ModelViewSet):

    queryset = AccessLog.objects.all()
    serializer_class = AccessLogSerializer
    
    def get_queryset(self):
        """
        Override to add filtering capability
        """
        queryset = AccessLog.objects.all()
        
        card_id = self.request.query_params.get('card_id', None)
        if card_id:
            queryset = queryset.filter(card_id=card_id)
            
        door_name = self.request.query_params.get('door_name', None)
        if door_name:
            queryset = queryset.filter(door_name=door_name)
        
        access_granted = self.request.query_params.get('access_granted', None)
        if access_granted is not None:
            queryset = queryset.filter(access_granted=access_granted.lower() == 'true')
            
        return queryset
    
    def create(self, request, *args, **kwargs):
        """
        Create a new AccessLog entry
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def destroy(self, request, *args, **kwargs):
        """
        Delete an AccessLog entry - returns 204 No Content
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)