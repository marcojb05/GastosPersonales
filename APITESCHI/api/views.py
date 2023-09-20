from django.shortcuts import render
from rest_framework.views import APIView
# Create your views here.

class Home (APIView):
    template_name = "index.html"
    #self es el equivalente del this en Java, hace referencia a sí mismo
    # request se consume
    def get (self, request):
        return render(request, self.template_name)
    def post (self, request):
        return render(request, self.template_name)

class Login (APIView):
    template_name = "login.html"
    def get (self, request):
        return render(request, self.template_name)
    def post (self, request):
        return render(request, self.template_name)

class Registro (APIView):
    template_name = "register.html"
    def get (self, request):
        return render(request, self.template_name)
    def post (self, request):
        return render(request, self.template_name)
    
class Reestablecer (APIView):
    template_name="forgot-password.html"
    def get (self, request):
        return render(request, self.template_name)
    def post (self, request):
        return render(request, self.template_name)