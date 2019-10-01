"""View module for handling requests about park areas"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from kennywoodapi.models import Attraction, ParkArea, Itinerary, Customer


class ItineraryItemSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for park areas

    Arguments:
        serializers
    """
    class Meta:
        model = Itinerary
        url = serializers.HyperlinkedIdentityField(
            view_name='itineraryitem',
            lookup_field='id'
        )
        fields = ('id', 'url', 'starttime', 'attraction')
        depth = 2


class ItineraryItems(ViewSet):
    """Park Areas for Kennywood Amusement Park"""

    # def create(self, request):
    #     """Handle POST operations

    #     Returns:
    #         Response -- JSON serialized Attraction instance
    #     """
    #     new_itinerary = Itinerary()
    #     new_itinerary.starttime = request.data["starttime"]
    #     new_itinerary.customer = Customer.objects.get(user=request.auth.user)
    #     new_itinerary.attraction = Attraction.objects.get(
    #         pk=request.data["ride_id"])

    #     new_itinerary.save()

    #     serializer = ItemSerializer(
    #         new_itinerary, context={'request': request})

    #     return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Itinerary instance
        """
        newitem = Itinerary()
        newitem.starttime = request.data["starttime"]
        newitem.customer = Customer.objects.get(user=request.auth.user)
        newitem.attraction = Attraction.objects.get(pk=request.data["ride_id"])
        newitem.save()

        serializer = ItineraryItemSerializer(
            newitem, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single park area

        Returns:
            Response -- JSON serialized park area instance
        """
        try:
            area = Attraction.objects.get(pk=pk)
            serializer = AttractionSerializer(
                area, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a park area attraction

        Returns:
            Response -- Empty body with 204 status code
        """
        attraction = Attraction.objects.get(pk=pk)
        area = ParkArea.objects.get(pk=request.data["area_id"])
        attraction.name = request.data["name"]
        attraction.area = area
        attraction.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single park are

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            area = Attraction.objects.get(pk=pk)
            area.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Attraction.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to park attractions resource

        Returns:
            Response -- JSON serialized list of park attractions
        """
        customer = Customer.objects.get(user=request.auth.user)
        items = Itinerary.objects.filter(customer=customer)

        serializer = ItineraryItemSerializer(
            items, many=True, context={'request': request})
        return Response(serializer.data)
