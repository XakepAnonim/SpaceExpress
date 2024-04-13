from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import Response

from .permissions import IsAdmin
from .swagger import application_response
from ..main.serializers import ManufacturerSerializer
from ..users.models import Application
from ..users.serializers import CityApplicationSerializer


@extend_schema(
    request=CityApplicationSerializer,
    responses=application_response,
    tags=["Other"]
)
@api_view(["GET"])
@permission_classes([IsAdmin])
def application_display(request):
    application = Application.objects.all()
    serializer = CityApplicationSerializer(application, many=True)
    return Response({"data": serializer.data}, status=status.HTTP_200_OK)


@permission_classes([IsAdmin])
@api_view(["POST"])
def accept_application(request, pk):
    application = Application.objects.get(pk=pk)

    manufacturer_data = {
        "name": application.name,
        "user": application.user.pk,
        "cities": [city.pk for city in application.cities.all()],
    }
    manufacturer_serializer = ManufacturerSerializer(data=manufacturer_data)
    if manufacturer_serializer.is_valid():
        manufacturer = manufacturer_serializer.save()

        if manufacturer.user:
            user = manufacturer.user
            user.is_manufacturer = True
            user.company = manufacturer
            user.save()
        application.delete()

        return Response(
            {"message": "Заявка принята"}, status=status.HTTP_201_CREATED
        )
    return Response(
        manufacturer_serializer.errors, status=status.HTTP_400_BAD_REQUEST
    )
