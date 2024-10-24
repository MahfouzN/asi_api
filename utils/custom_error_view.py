from django.http import JsonResponse

def custom_error_view(request, exception=None):
    return JsonResponse({
        "status": "0002",
        "message": "Une erreur inattendue s'est produite",
        "data": {}
    }, status=500)