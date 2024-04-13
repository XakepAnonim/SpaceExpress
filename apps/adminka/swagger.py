from rest_framework import status

from apps.users.serializers import CityApplicationSerializer

application_response = {status.HTTP_200_OK: CityApplicationSerializer}