from rest_framework.response import Response
from rest_framework import status as drf_status

def api_response(status_code, message, data=None, status=None):
    response_data = {
        "status": status_code,
        "message": message,
        "data": data if data is not None else {}
    }
    return Response(response_data, status=200)