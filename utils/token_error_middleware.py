from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from utils.api_response import api_response



class TokenErrorMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        if isinstance(exception, (InvalidToken, TokenError)):
            return api_response("0001", "Token invalide ou expiré")