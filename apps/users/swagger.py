from rest_framework import status

from apps.users.serializers import (
    LogSerializer,
    RegSerializer,
    ApplicationSerializer,
)

login_response = {status.HTTP_200_OK: LogSerializer}

reg_response = {status.HTTP_200_OK: RegSerializer}

applications_response = {status.HTTP_200_OK: ApplicationSerializer}
