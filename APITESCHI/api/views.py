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
    
class Botones (APIView):
    template_name = "buttons.html"
    def get (self, request):
        return render(request, self.template_name)
    def post (self, request):
        return render(request, self.template_name)
    
class Tarjetas (APIView):
    template_name = "cards.html"
    def get (self, request):
        return render(request, self.template_name)
    def post (self, request):
        return render(request, self.template_name)
    
class Graficas (APIView):
    template_name = "charts.html"
    def get (self, request):
        return render(request, self.template_name)
    def post (self, request):
        return render(request, self.template_name)

class Tablas (APIView):
    template_name = "tables.html"
    def get (self, request):
        return render(request, self.template_name)
    def post (self, request):
        return render(request, self.template_name)
    
class Animacion (APIView):
    template_name = "utilities-animation.html"
    def get (self, request):
        return render(request, self.template_name)
    def post (self, request):
        return render(request, self.template_name)

class Border (APIView):
    template_name = "utilities-border.html"
    def get (self, request):
        return render(request, self.template_name)
    def post (self, request):
        return render(request, self.template_name)
    
class Color (APIView):
    template_name = "utilities-color.html"
    def get (self, request):
        return render(request, self.template_name)
    def post (self, request):
        return render(request, self.template_name)
    
class Otro (APIView):
    template_name = "utilities-other.html"
    def get (self, request):
        return render(request, self.template_name)
    def post (self, request):
        return render(request, self.template_name)
    
class Error404 (APIView):
    template_name = "404.html"
    def get (self, request):
        return render(request, self.template_name)
    def post (self, request):
        return render(request, self.template_name)

class Blank (APIView):
    template_name = "blank.html"
    def get (self, request):
        return render(request, self.template_name)
    def post (self, request):
        return render(request, self.template_name)