from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied


def error404(request, exception):
    return redirect('utilizadores:mensagem', 404)
def error500(request):
    return redirect('utilizadores:mensagem', 500)
def error403(request, exception):
    return redirect('utilizadores:mensagem', 403)
def error400(request, exception):
    return redirect('utilizadores:mensagem', 400)            