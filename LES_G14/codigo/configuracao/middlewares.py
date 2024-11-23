import logging
from django.db import DatabaseError
from django.shortcuts import redirect
from django.urls import reverse

class DatabaseErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, DatabaseError):
            logging.error(f'Database error occurred: {exception}')
            return redirect(reverse('utilizadores:mensagem', kwargs={'id': 19}))
        return None
