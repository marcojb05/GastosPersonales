from django.shortcuts import render
from rest_framework.views import APIView
# Create your views here.

class Home (APIView):
    template_name = "index.html"
    def get (self, request):
        return render(request, self.template_name)
    def post (self, request):
        return render(request, self.template_name)